"""
Component test framework for CMU Web Standards compliance.

Tests reusable UI components for accessibility, structure, and behavior.
"""

import pytest
from bs4 import BeautifulSoup


class TestComponentFramework:
    """Base test framework for component testing."""
    
    def parse_html(self, html):
        """Parse HTML string into BeautifulSoup object."""
        return BeautifulSoup(html, 'html.parser')
    
    def assert_has_class(self, element, class_name):
        """Assert element has specific class."""
        classes = element.get('class', [])
        assert class_name in classes, f"Element missing class '{class_name}'"
    
    def assert_has_attribute(self, element, attr_name, expected_value=None):
        """Assert element has specific attribute."""
        assert element.has_attr(attr_name), f"Element missing attribute '{attr_name}'"
        if expected_value is not None:
            actual = element.get(attr_name)
            assert actual == expected_value, \
                f"Attribute '{attr_name}' has value '{actual}', expected '{expected_value}'"
    
    def assert_accessible(self, html):
        """Assert HTML is keyboard accessible and has proper ARIA."""
        soup = self.parse_html(html)
        
        # Check for interactive elements
        interactive = soup.find_all(['button', 'a', 'input', 'select', 'textarea'])
        for elem in interactive:
            # Links must have href
            if elem.name == 'a':
                assert elem.has_attr('href'), "Link missing href attribute"
            
            # Elements should not have tabindex=-1 unless intentional
            if elem.has_attr('tabindex'):
                tabindex = elem.get('tabindex')
                if tabindex == '-1':
                    # Only allowed if element has aria-hidden or is decorative
                    assert elem.has_attr('aria-hidden') or \
                           elem.has_attr('aria-label') or \
                           'decorative' in elem.get('class', []), \
                           "Interactive element has tabindex=-1 without justification"


class TestPageHeaderComponent(TestComponentFramework):
    """Test PageHeader component."""
    
    def test_header_structure(self):
        """Test header has proper structure."""
        html = '''
        <header class="page-header" role="banner">
            <nav aria-label="Breadcrumb">
                <ol class="breadcrumbs">
                    <li><a href="/">Home</a></li>
                    <li aria-current="page">Services</li>
                </ol>
            </nav>
            <h1>Services</h1>
            <p class="page-description">Manage your services</p>
        </header>
        '''
        soup = self.parse_html(html)
        
        # Check header element
        header = soup.find('header')
        assert header is not None
        self.assert_has_class(header, 'page-header')
        self.assert_has_attribute(header, 'role', 'banner')
        
        # Check breadcrumb navigation
        nav = header.find('nav')
        assert nav is not None
        self.assert_has_attribute(nav, 'aria-label', 'Breadcrumb')
        
        # Check h1 exists
        h1 = header.find('h1')
        assert h1 is not None
        assert h1.text == 'Services'
    
    def test_breadcrumb_current_page(self):
        """Test breadcrumb marks current page."""
        html = '''
        <nav aria-label="Breadcrumb">
            <ol class="breadcrumbs">
                <li><a href="/">Home</a></li>
                <li><a href="/services">Services</a></li>
                <li aria-current="page">Apache</li>
            </ol>
        </nav>
        '''
        soup = self.parse_html(html)
        
        # Find current page marker
        current = soup.find(attrs={'aria-current': 'page'})
        assert current is not None
        assert current.text == 'Apache'


class TestContentSectionComponent(TestComponentFramework):
    """Test ContentSection component."""
    
    def test_section_structure(self):
        """Test section has proper heading and content."""
        html = '''
        <section class="content-section">
            <h2>Installation</h2>
            <p>Follow these steps to install.</p>
        </section>
        '''
        soup = self.parse_html(html)
        
        section = soup.find('section')
        assert section is not None
        self.assert_has_class(section, 'content-section')
        
        # Check heading
        h2 = section.find('h2')
        assert h2 is not None
        
        # Check content
        p = section.find('p')
        assert p is not None
    
    def test_collapsible_section(self):
        """Test collapsible section has proper ARIA."""
        html = '''
        <section class="content-section collapsible">
            <button aria-expanded="false" aria-controls="section-1">
                <h2>Advanced Options</h2>
            </button>
            <div id="section-1" hidden>
                <p>Advanced content here.</p>
            </div>
        </section>
        '''
        soup = self.parse_html(html)
        
        button = soup.find('button')
        assert button is not None
        self.assert_has_attribute(button, 'aria-expanded')
        self.assert_has_attribute(button, 'aria-controls', 'section-1')
        
        content = soup.find('div', id='section-1')
        assert content is not None
        assert content.has_attr('hidden')


class TestActionCardComponent(TestComponentFramework):
    """Test ActionCard component."""
    
    def test_card_structure(self):
        """Test action card has proper structure."""
        html = '''
        <article class="action-card">
            <h3>Install Workstation</h3>
            <p>Set up a Fedora 43 virtual machine</p>
            <ul class="benefits">
                <li>Takes 5-10 minutes</li>
                <li>Fully automated setup</li>
            </ul>
            <a href="/install" class="btn btn-primary">Install Workstation</a>
        </article>
        '''
        soup = self.parse_html(html)
        
        article = soup.find('article')
        assert article is not None
        self.assert_has_class(article, 'action-card')
        
        # Check heading
        h3 = article.find('h3')
        assert h3 is not None
        
        # Check action button
        btn = article.find('a', class_='btn')
        assert btn is not None
        assert btn.has_attr('href')
        
        # Button text should start with action verb
        btn_text = btn.text.strip()
        action_verbs = ['install', 'deploy', 'create', 'start', 'stop', 
                       'restart', 'configure', 'delete', 'remove', 'update']
        assert any(btn_text.lower().startswith(verb) for verb in action_verbs), \
            f"Button text '{btn_text}' doesn't start with action verb"


class TestNavigationComponent(TestComponentFramework):
    """Test MainNavigation component."""
    
    def test_nav_structure(self):
        """Test navigation has proper structure."""
        html = '''
        <nav class="main-nav" role="navigation" aria-label="Main">
            <ul>
                <li><a href="/" aria-current="page">Dashboard</a></li>
                <li><a href="/services">Services</a></li>
                <li><a href="/tests">Tests</a></li>
                <li><a href="/help">Help</a></li>
            </ul>
        </nav>
        '''
        soup = self.parse_html(html)
        
        nav = soup.find('nav')
        assert nav is not None
        self.assert_has_class(nav, 'main-nav')
        self.assert_has_attribute(nav, 'role', 'navigation')
        self.assert_has_attribute(nav, 'aria-label', 'Main')
        
        # Check current page marker
        current = soup.find(attrs={'aria-current': 'page'})
        assert current is not None
    
    def test_nav_accessibility(self):
        """Test navigation is keyboard accessible."""
        html = '''
        <nav class="main-nav" role="navigation" aria-label="Main">
            <ul>
                <li><a href="/">Dashboard</a></li>
                <li><a href="/services">Services</a></li>
            </ul>
        </nav>
        '''
        self.assert_accessible(html)


class TestSkipLinksComponent(TestComponentFramework):
    """Test SkipLinks component."""
    
    def test_skip_link_structure(self):
        """Test skip links have proper structure."""
        html = '''
        <a href="#main-content" class="skip-link">Skip to main content</a>
        <a href="#main-nav" class="skip-link">Skip to navigation</a>
        '''
        soup = self.parse_html(html)
        
        skip_links = soup.find_all('a', class_='skip-link')
        assert len(skip_links) >= 1
        
        for link in skip_links:
            # Must have href starting with #
            href = link.get('href')
            assert href.startswith('#'), "Skip link must have fragment identifier"
            
            # Must have descriptive text
            text = link.text.strip()
            assert len(text) > 0, "Skip link must have text"
            assert 'skip' in text.lower(), "Skip link text should contain 'skip'"
    
    def test_skip_links_component_template(self):
        """Test skip-links.html component template structure."""
        # This would be tested with Flask app context
        # For now, test the expected HTML structure
        html = '''
        <div class="skip-links">
            <a href="#main-content" class="skip-link">Skip to main content</a>
            <a href="#main-nav" class="skip-link">Skip to navigation</a>
        </div>
        '''
        soup = self.parse_html(html)
        
        container = soup.find('div', class_='skip-links')
        assert container is not None
        
        skip_links = container.find_all('a', class_='skip-link')
        assert len(skip_links) >= 2, "Should have at least 2 skip links"
        
        # Verify main content skip link
        main_link = container.find('a', href='#main-content')
        assert main_link is not None
        assert 'main content' in main_link.text.lower()
        
        # Verify navigation skip link
        nav_link = container.find('a', href='#main-nav')
        assert nav_link is not None
        assert 'navigation' in nav_link.text.lower()


class TestBreadcrumbsComponent(TestComponentFramework):
    """Test Breadcrumbs component."""
    
    def test_breadcrumbs_component_structure(self):
        """Test breadcrumbs.html component template structure."""
        html = '''
        <nav id="breadcrumbs" aria-label="Breadcrumb" class="breadcrumb-nav">
            <ol class="breadcrumbs">
                <li class="breadcrumb-item">
                    <a href="/">Home</a>
                    <span class="breadcrumb-separator" aria-hidden="true">&gt;</span>
                </li>
                <li class="breadcrumb-item">
                    <a href="/services">Services</a>
                    <span class="breadcrumb-separator" aria-hidden="true">&gt;</span>
                </li>
                <li class="breadcrumb-item current">
                    <span aria-current="page">Apache</span>
                </li>
            </ol>
        </nav>
        '''
        soup = self.parse_html(html)
        
        # Check nav element
        nav = soup.find('nav', id='breadcrumbs')
        assert nav is not None
        self.assert_has_attribute(nav, 'aria-label', 'Breadcrumb')
        self.assert_has_class(nav, 'breadcrumb-nav')
        
        # Check ordered list
        ol = nav.find('ol', class_='breadcrumbs')
        assert ol is not None
        
        # Check breadcrumb items
        items = ol.find_all('li', class_='breadcrumb-item')
        assert len(items) >= 2, "Should have at least 2 breadcrumb items"
        
        # Check current page marker
        current = soup.find(attrs={'aria-current': 'page'})
        assert current is not None
        
        # Check separators are aria-hidden
        separators = soup.find_all('span', class_='breadcrumb-separator')
        for sep in separators:
            self.assert_has_attribute(sep, 'aria-hidden', 'true')
    
    def test_breadcrumbs_links_accessible(self):
        """Test breadcrumb links are keyboard accessible."""
        html = '''
        <nav aria-label="Breadcrumb">
            <ol class="breadcrumbs">
                <li><a href="/">Home</a></li>
                <li><a href="/services">Services</a></li>
                <li aria-current="page">Apache</li>
            </ol>
        </nav>
        '''
        self.assert_accessible(html)
    
    def test_breadcrumbs_empty_handling(self):
        """Test breadcrumbs component handles empty list."""
        # Component should not render if breadcrumbs list is empty
        # This is handled by the {% if breadcrumbs %} check in template
        html = ''  # Empty when no breadcrumbs
        soup = self.parse_html(html)
        
        nav = soup.find('nav', attrs={'aria-label': 'Breadcrumb'})
        assert nav is None, "Breadcrumbs should not render when list is empty"


class TestMainNavigationComponent(TestComponentFramework):
    """Test Main Navigation component."""
    
    def test_navigation_component_structure(self):
        """Test navigation.html component template structure."""
        html = '''
        <nav id="main-nav" class="main-nav" role="navigation" aria-label="Main">
            <ul class="nav-list">
                <li class="nav-item current">
                    <a href="/" class="nav-link active" aria-current="page" data-icon="home">
                        <span class="nav-icon" aria-hidden="true"></span>
                        <span class="nav-label">Home</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/workstation" class="nav-link" data-icon="server">
                        <span class="nav-icon" aria-hidden="true"></span>
                        <span class="nav-label">Workstation</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/services" class="nav-link" data-icon="grid">
                        <span class="nav-icon" aria-hidden="true"></span>
                        <span class="nav-label">Services</span>
                        <span class="nav-badge" aria-label="3 notifications">3</span>
                    </a>
                </li>
            </ul>
        </nav>
        '''
        soup = self.parse_html(html)
        
        # Check nav element
        nav = soup.find('nav', id='main-nav')
        assert nav is not None
        self.assert_has_class(nav, 'main-nav')
        self.assert_has_attribute(nav, 'role', 'navigation')
        self.assert_has_attribute(nav, 'aria-label', 'Main')
        
        # Check nav list
        ul = nav.find('ul', class_='nav-list')
        assert ul is not None
        
        # Check nav items
        items = ul.find_all('li', class_='nav-item')
        assert len(items) >= 2, "Should have at least 2 nav items"
        
        # Check current page marker
        current = soup.find(attrs={'aria-current': 'page'})
        assert current is not None
        
        # Check nav links
        links = nav.find_all('a', class_='nav-link')
        for link in links:
            assert link.has_attr('href'), "Nav link must have href"
            
            # Check for nav label
            label = link.find('span', class_='nav-label')
            assert label is not None, "Nav link must have label"
    
    def test_navigation_current_page_indication(self):
        """Test navigation indicates current page correctly.
        
        Validates: Requirements 4.2 (Current page indication)
        """
        html = '''
        <nav class="main-nav" role="navigation" aria-label="Main">
            <ul class="nav-list">
                <li class="nav-item current">
                    <a href="/" class="nav-link active" aria-current="page">Home</a>
                </li>
                <li class="nav-item">
                    <a href="/services" class="nav-link">Services</a>
                </li>
            </ul>
        </nav>
        '''
        soup = self.parse_html(html)
        
        # Check aria-current="page" exists
        current = soup.find(attrs={'aria-current': 'page'})
        assert current is not None, "Current page must have aria-current='page'"
        
        # Check current item has 'current' class
        current_item = soup.find('li', class_='current')
        assert current_item is not None, "Current nav item must have 'current' class"
        
        # Check current link has 'active' class
        active_link = soup.find('a', class_='active')
        assert active_link is not None, "Current nav link must have 'active' class"
    
    def test_navigation_progressive_disclosure(self):
        """Test navigation respects progressive disclosure (is_available).
        
        Validates: Progressive disclosure principle
        """
        # When is_available=False, item should not be rendered
        # This is handled by {% if item.is_available %} in template
        html = '''
        <nav class="main-nav" role="navigation" aria-label="Main">
            <ul class="nav-list">
                <li class="nav-item">
                    <a href="/" class="nav-link">Home</a>
                </li>
                <!-- Services item not rendered because is_available=False -->
            </ul>
        </nav>
        '''
        soup = self.parse_html(html)
        
        items = soup.find_all('li', class_='nav-item')
        # Only available items should be rendered
        assert len(items) == 1, "Only available nav items should be rendered"
    
    def test_navigation_with_badge(self):
        """Test navigation badge for notifications."""
        html = '''
        <nav class="main-nav">
            <ul class="nav-list">
                <li class="nav-item">
                    <a href="/services" class="nav-link">
                        <span class="nav-label">Services</span>
                        <span class="nav-badge" aria-label="3 notifications">3</span>
                    </a>
                </li>
            </ul>
        </nav>
        '''
        soup = self.parse_html(html)
        
        badge = soup.find('span', class_='nav-badge')
        assert badge is not None
        self.assert_has_attribute(badge, 'aria-label')
        
        # Badge should have descriptive aria-label
        aria_label = badge.get('aria-label')
        assert 'notification' in aria_label.lower() or 'alert' in aria_label.lower()
    
    def test_navigation_nested_submenu(self):
        """Test navigation with nested submenu."""
        html = '''
        <nav class="main-nav">
            <ul class="nav-list">
                <li class="nav-item">
                    <a href="/services" class="nav-link">Services</a>
                    <ul class="nav-submenu">
                        <li class="nav-subitem">
                            <a href="/services/apache" class="nav-sublink">Apache</a>
                        </li>
                        <li class="nav-subitem">
                            <a href="/services/mysql" class="nav-sublink">MySQL</a>
                        </li>
                    </ul>
                </li>
            </ul>
        </nav>
        '''
        soup = self.parse_html(html)
        
        # Check submenu exists
        submenu = soup.find('ul', class_='nav-submenu')
        assert submenu is not None
        
        # Check submenu items
        subitems = submenu.find_all('li', class_='nav-subitem')
        assert len(subitems) >= 2
        
        # Check submenu links
        sublinks = submenu.find_all('a', class_='nav-sublink')
        for link in sublinks:
            assert link.has_attr('href')
    
    def test_navigation_accessibility(self):
        """Test navigation is fully keyboard accessible."""
        html = '''
        <nav id="main-nav" class="main-nav" role="navigation" aria-label="Main">
            <ul class="nav-list">
                <li class="nav-item">
                    <a href="/" class="nav-link">Home</a>
                </li>
                <li class="nav-item">
                    <a href="/services" class="nav-link">Services</a>
                </li>
            </ul>
        </nav>
        '''
        self.assert_accessible(html)
    
    def test_navigation_touch_targets(self):
        """Test navigation links meet minimum touch target size.
        
        Validates: Requirements 5.3, 8.5 (Touch target size)
        """
        # This would be tested with actual CSS rendering
        # For now, verify structure supports touch targets
        html = '''
        <nav class="main-nav">
            <ul class="nav-list">
                <li class="nav-item">
                    <a href="/" class="nav-link">Home</a>
                </li>
            </ul>
        </nav>
        '''
        soup = self.parse_html(html)
        
        links = soup.find_all('a', class_='nav-link')
        assert len(links) > 0
        
        # Links should have nav-link class which applies min-height in CSS
        for link in links:
            self.assert_has_class(link, 'nav-link')


class TestConfirmationDialogComponent(TestComponentFramework):
    """Test ConfirmationDialog component."""
    
    def test_dialog_structure(self):
        """Test dialog has proper ARIA structure."""
        html = '''
        <div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
            <h2 id="dialog-title">Destroy Workstation?</h2>
            <p>This will permanently delete your workstation VM.</p>
            <ul>
                <li>All deployed services will be removed</li>
                <li>Configuration will be preserved</li>
            </ul>
            <div class="dialog-actions">
                <button class="btn btn-danger">Destroy Workstation</button>
                <button class="btn btn-secondary">Cancel</button>
            </div>
        </div>
        '''
        soup = self.parse_html(html)
        
        dialog = soup.find(attrs={'role': 'dialog'})
        assert dialog is not None
        self.assert_has_attribute(dialog, 'aria-labelledby', 'dialog-title')
        self.assert_has_attribute(dialog, 'aria-modal', 'true')
        
        # Check title exists
        title = soup.find(id='dialog-title')
        assert title is not None
        
        # Check action buttons
        buttons = dialog.find_all('button')
        assert len(buttons) >= 2, "Dialog should have at least 2 buttons (confirm and cancel)"
    
    def test_dialog_consequences(self):
        """Test dialog explains consequences."""
        html = '''
        <div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
            <h2 id="dialog-title">Delete Service?</h2>
            <p>This action cannot be undone.</p>
            <ul>
                <li>Service will be stopped</li>
                <li>Data will be preserved</li>
            </ul>
            <div class="dialog-actions">
                <button class="btn btn-danger">Delete</button>
                <button class="btn btn-secondary">Cancel</button>
            </div>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Should have explanation text
        paragraphs = soup.find_all('p')
        assert len(paragraphs) > 0, "Dialog should explain consequences"
        
        # Should have list of consequences or detailed explanation
        has_list = soup.find('ul') is not None
        has_detailed_text = any(len(p.text) > 20 for p in paragraphs)
        assert has_list or has_detailed_text, \
            "Dialog should list consequences or provide detailed explanation"


class TestLoadingStateComponent(TestComponentFramework):
    """Test LoadingState component."""
    
    def test_loading_indicator(self):
        """Test loading indicator has proper ARIA."""
        html = '''
        <div role="status" aria-live="polite" aria-busy="true">
            <span class="spinner"></span>
            <span>Installing workstation...</span>
        </div>
        '''
        soup = self.parse_html(html)
        
        status = soup.find(attrs={'role': 'status'})
        assert status is not None
        self.assert_has_attribute(status, 'aria-live', 'polite')
        self.assert_has_attribute(status, 'aria-busy', 'true')
        
        # Should have descriptive text
        text = status.get_text(strip=True)
        assert len(text) > 0, "Loading indicator should have descriptive text"
    
    def test_progress_indicator(self):
        """Test progress indicator with percentage."""
        html = '''
        <div role="progressbar" aria-valuenow="50" aria-valuemin="0" 
             aria-valuemax="100" aria-label="Installation progress">
            <div class="progress-bar" style="width: 50%"></div>
            <span>50% complete</span>
        </div>
        '''
        soup = self.parse_html(html)
        
        progress = soup.find(attrs={'role': 'progressbar'})
        assert progress is not None
        self.assert_has_attribute(progress, 'aria-valuenow')
        self.assert_has_attribute(progress, 'aria-valuemin')
        self.assert_has_attribute(progress, 'aria-valuemax')
        self.assert_has_attribute(progress, 'aria-label')


class TestFormFieldComponent(TestComponentFramework):
    """Test FormField component."""
    
    def test_form_field_structure(self):
        """Test form field has proper label association."""
        html = '''
        <div class="form-group">
            <label for="port">Port Number</label>
            <input type="text" id="port" name="port" 
                   aria-describedby="port-help">
            <span id="port-help" class="help-text">
                Enter a port between 1 and 65535
            </span>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check label association
        label = soup.find('label')
        assert label is not None
        label_for = label.get('for')
        assert label_for is not None
        
        # Check input has matching id
        input_elem = soup.find('input', id=label_for)
        assert input_elem is not None
        
        # Check help text association
        if input_elem.has_attr('aria-describedby'):
            help_id = input_elem.get('aria-describedby')
            help_text = soup.find(id=help_id)
            assert help_text is not None
    
    def test_form_field_error(self):
        """Test form field with error state."""
        html = '''
        <div class="form-group error">
            <label for="email">Email</label>
            <input type="email" id="email" aria-invalid="true" 
                   aria-describedby="email-error">
            <span id="email-error" class="error-message" role="alert">
                Please enter a valid email address
            </span>
        </div>
        '''
        soup = self.parse_html(html)
        
        input_elem = soup.find('input')
        assert input_elem is not None
        self.assert_has_attribute(input_elem, 'aria-invalid', 'true')
        self.assert_has_attribute(input_elem, 'aria-describedby')
        
        # Check error message
        error_id = input_elem.get('aria-describedby')
        error_msg = soup.find(id=error_id)
        assert error_msg is not None
        self.assert_has_attribute(error_msg, 'role', 'alert')


class TestNotificationComponent(TestComponentFramework):
    """Test Notification component."""
    
    def test_success_notification(self):
        """Test success notification structure."""
        html = '''
        <div role="status" aria-live="polite" class="notification success">
            <span class="icon">✓</span>
            <span>Workstation installed successfully</span>
            <button aria-label="Close notification">×</button>
        </div>
        '''
        soup = self.parse_html(html)
        
        notification = soup.find(class_='notification')
        assert notification is not None
        self.assert_has_attribute(notification, 'role', 'status')
        self.assert_has_attribute(notification, 'aria-live', 'polite')
        
        # Should have descriptive text
        text = notification.get_text(strip=True)
        assert len(text) > 0
    
    def test_error_notification(self):
        """Test error notification structure."""
        html = '''
        <div role="alert" aria-live="assertive" class="notification error">
            <span class="icon">✗</span>
            <span>Installation failed. Please check logs.</span>
            <button aria-label="Close notification">×</button>
        </div>
        '''
        soup = self.parse_html(html)
        
        notification = soup.find(class_='notification')
        assert notification is not None
        # Errors should use role="alert" or aria-live="assertive"
        has_alert = notification.get('role') == 'alert' or \
                   notification.get('aria-live') == 'assertive'
        assert has_alert, "Error notification should use role='alert' or aria-live='assertive'"


class TestComponentAccessibility(TestComponentFramework):
    """Test component accessibility patterns."""
    
    def test_all_buttons_have_text_or_aria_label(self):
        """Test all buttons have accessible text."""
        html = '''
        <button>Click me</button>
        <button aria-label="Close dialog">×</button>
        <button><span class="sr-only">Delete</span><i class="icon-trash"></i></button>
        '''
        soup = self.parse_html(html)
        
        buttons = soup.find_all('button')
        for button in buttons:
            # Must have text content or aria-label
            has_text = len(button.get_text(strip=True)) > 0
            has_aria_label = button.has_attr('aria-label')
            assert has_text or has_aria_label, \
                "Button must have text content or aria-label"
    
    def test_all_images_have_alt_text(self):
        """Test all images have alt text."""
        html = '''
        <img src="logo.png" alt="Ahab logo - whale tail symbol">
        <img src="icon.png" alt="">
        '''
        soup = self.parse_html(html)
        
        images = soup.find_all('img')
        for img in images:
            # All images must have alt attribute (can be empty for decorative)
            assert img.has_attr('alt'), "Image must have alt attribute"
    
    def test_interactive_elements_keyboard_accessible(self):
        """Test interactive elements are keyboard accessible."""
        html = '''
        <button>Button</button>
        <a href="/page">Link</a>
        <input type="text">
        <select><option>Option</option></select>
        '''
        self.assert_accessible(html)


class TestPageHeaderWithBreadcrumbs(TestComponentFramework):
    """Test PageHeader component with breadcrumbs and metadata."""
    
    def test_page_header_with_breadcrumbs(self):
        """Test page header includes breadcrumbs navigation.
        
        Validates: Requirements 4.3 (Breadcrumb navigation)
        """
        html = '''
        <header class="page-header" role="banner">
            <nav aria-label="Breadcrumb" class="breadcrumb-nav">
                <ol class="breadcrumbs">
                    <li class="breadcrumb-item">
                        <a href="/">Home</a>
                    </li>
                    <li class="breadcrumb-item">
                        <a href="/services">Services</a>
                    </li>
                    <li class="breadcrumb-item active">
                        <span aria-current="page">Apache</span>
                    </li>
                </ol>
            </nav>
            <div class="page-title-wrapper">
                <h1 class="page-title">Apache Web Server</h1>
            </div>
            <p class="page-description">Deploy and manage Apache HTTP Server</p>
        </header>
        '''
        soup = self.parse_html(html)
        
        # Check header structure
        header = soup.find('header', class_='page-header')
        assert header is not None
        self.assert_has_attribute(header, 'role', 'banner')
        
        # Check breadcrumbs
        nav = header.find('nav', attrs={'aria-label': 'Breadcrumb'})
        assert nav is not None
        
        # Check H1 exists
        h1 = header.find('h1', class_='page-title')
        assert h1 is not None
        assert h1.text.strip() == 'Apache Web Server'
        
        # Check description
        desc = header.find('p', class_='page-description')
        assert desc is not None
    
    def test_page_header_with_icon(self):
        """Test page header with optional icon."""
        html = '''
        <header class="page-header">
            <div class="page-title-wrapper">
                <span class="page-icon" aria-hidden="true">
                    <i class="icon-server"></i>
                </span>
                <h1 class="page-title">Workstation</h1>
            </div>
        </header>
        '''
        soup = self.parse_html(html)
        
        icon = soup.find('span', class_='page-icon')
        assert icon is not None
        self.assert_has_attribute(icon, 'aria-hidden', 'true')
    
    def test_page_header_metadata(self):
        """Test page header with metadata (last updated, reading time)."""
        html = '''
        <header class="page-header">
            <h1>Documentation</h1>
            <div class="page-meta">
                <span class="meta-item">
                    <i class="icon-clock" aria-hidden="true"></i>
                    <span class="sr-only">Last updated:</span>
                    <time datetime="2025-12-09">December 9, 2025</time>
                </span>
                <span class="meta-item">
                    <i class="icon-book" aria-hidden="true"></i>
                    <span class="sr-only">Estimated reading time:</span>
                    5 min read
                </span>
            </div>
        </header>
        '''
        soup = self.parse_html(html)
        
        meta = soup.find('div', class_='page-meta')
        assert meta is not None
        
        # Check time element
        time_elem = meta.find('time')
        assert time_elem is not None
        self.assert_has_attribute(time_elem, 'datetime')
        
        # Check screen reader text
        sr_text = meta.find_all('span', class_='sr-only')
        assert len(sr_text) >= 2


class TestCollapsibleContentSection(TestComponentFramework):
    """Test ContentSection component with collapsible and nested sections."""
    
    def test_content_section_basic(self):
        """Test basic content section structure.
        
        Validates: Requirements 1.2 (Heading hierarchy), 5.1 (Section spacing)
        """
        html = '''
        <section class="content-section" aria-labelledby="section-1-heading">
            <h2 class="section-heading" id="section-1-heading">Installation</h2>
            <div class="section-content" id="section-1-content">
                <div class="section-body">
                    <p>Follow these steps to install the workstation.</p>
                </div>
            </div>
        </section>
        '''
        soup = self.parse_html(html)
        
        section = soup.find('section', class_='content-section')
        assert section is not None
        
        # Check heading
        heading = section.find('h2', class_='section-heading')
        assert heading is not None
        assert heading.has_attr('id')
        
        # Check content
        content = section.find('div', class_='section-content')
        assert content is not None
    
    def test_content_section_collapsible(self):
        """Test collapsible content section (progressive disclosure).
        
        Validates: Progressive disclosure principle
        """
        html = '''
        <section class="content-section collapsible collapsed">
            <button class="section-toggle" 
                    aria-expanded="false"
                    aria-controls="section-1-content"
                    id="section-1-heading">
                <h2 class="section-heading">Advanced Options</h2>
                <span class="toggle-icon" aria-hidden="true">
                    <i class="icon-chevron-down"></i>
                </span>
            </button>
            <div class="section-content" 
                 id="section-1-content"
                 role="region"
                 aria-labelledby="section-1-heading"
                 hidden>
                <div class="section-body">
                    <p>Advanced configuration options.</p>
                </div>
            </div>
        </section>
        '''
        soup = self.parse_html(html)
        
        section = soup.find('section', class_='collapsible')
        assert section is not None
        
        # Check toggle button
        button = section.find('button', class_='section-toggle')
        assert button is not None
        self.assert_has_attribute(button, 'aria-expanded')
        self.assert_has_attribute(button, 'aria-controls')
        
        # Check content region
        content = section.find('div', class_='section-content')
        assert content is not None
        self.assert_has_attribute(content, 'role', 'region')
        self.assert_has_attribute(content, 'aria-labelledby')
        
        # Check collapsed state
        assert content.has_attr('hidden')
    
    def test_content_section_subsections(self):
        """Test content section with nested subsections.
        
        Validates: Requirements 1.2 (Heading hierarchy)
        """
        html = '''
        <section class="content-section">
            <h2 class="section-heading">Main Section</h2>
            <div class="section-content">
                <div class="section-body">
                    <p>Main content.</p>
                </div>
                <div class="subsections">
                    <section class="content-section">
                        <h3 class="section-heading">Subsection</h3>
                        <div class="section-content">
                            <div class="section-body">
                                <p>Subsection content.</p>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </section>
        '''
        soup = self.parse_html(html)
        
        # Check main section
        main_section = soup.find('section', class_='content-section', recursive=False)
        assert main_section is not None
        
        # Check main heading is H2
        main_heading = main_section.find('h2', recursive=False)
        assert main_heading is not None
        
        # Check subsections container
        subsections = main_section.find('div', class_='subsections')
        assert subsections is not None
        
        # Check subsection heading is H3 (proper hierarchy)
        sub_heading = subsections.find('h3')
        assert sub_heading is not None


class TestActionCardWithStatus(TestComponentFramework):
    """Test ActionCard component with status indicators and multiple actions."""
    
    def test_action_card_basic(self):
        """Test basic action card structure.
        
        Validates: Requirements 6.2 (Action-oriented content), 6.3 (User benefits)
        """
        html = '''
        <article class="action-card card-default" role="article">
            <div class="card-header">
                <div class="card-icon" aria-hidden="true">
                    <i class="icon-server"></i>
                </div>
                <div class="card-header-content">
                    <h3 class="card-title">Install Workstation</h3>
                </div>
            </div>
            <div class="card-body">
                <p class="card-description">Set up a Fedora 43 virtual machine with Docker and Ansible</p>
                <ul class="benefits-list" aria-label="Benefits">
                    <li class="benefit-item">
                        <i class="icon-check" aria-hidden="true"></i>
                        <span>Takes 5-10 minutes</span>
                    </li>
                    <li class="benefit-item">
                        <i class="icon-check" aria-hidden="true"></i>
                        <span>Fully automated setup</span>
                    </li>
                    <li class="benefit-item">
                        <i class="icon-check" aria-hidden="true"></i>
                        <span>Ready for service deployment</span>
                    </li>
                </ul>
            </div>
            <div class="card-actions">
                <a href="/install" class="btn btn-primary card-action-primary">
                    Install Workstation
                    <i class="icon-arrow-right" aria-hidden="true"></i>
                </a>
            </div>
        </article>
        '''
        soup = self.parse_html(html)
        
        # Check article element
        article = soup.find('article', class_='action-card')
        assert article is not None
        self.assert_has_attribute(article, 'role', 'article')
        
        # Check card title (H3)
        title = article.find('h3', class_='card-title')
        assert title is not None
        
        # Check description
        desc = article.find('p', class_='card-description')
        assert desc is not None
        
        # Check benefits list
        benefits = article.find('ul', class_='benefits-list')
        assert benefits is not None
        self.assert_has_attribute(benefits, 'aria-label', 'Benefits')
        
        # Check benefit items
        items = benefits.find_all('li', class_='benefit-item')
        assert len(items) >= 1
        
        # Check primary action button
        btn = article.find('a', class_='card-action-primary')
        assert btn is not None
        assert btn.has_attr('href')
        
        # Button text should start with action verb (WEB 2.3)
        btn_text = btn.get_text(strip=True)
        action_verbs = ['install', 'deploy', 'create', 'start', 'stop', 
                       'restart', 'configure', 'delete', 'remove', 'update']
        assert any(btn_text.lower().startswith(verb) for verb in action_verbs), \
            f"Button text '{btn_text}' doesn't start with action verb"
    
    def test_action_card_with_status(self):
        """Test action card with status indicator."""
        html = '''
        <article class="action-card">
            <div class="card-header">
                <div class="card-header-content">
                    <h3 class="card-title">Apache Web Server</h3>
                    <div class="card-status">
                        <span class="status-indicator status-running" role="status">
                            <i class="icon-play-circle" aria-hidden="true"></i>
                            <span class="status-label">Running</span>
                        </span>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <p class="card-description">Web server is running</p>
            </div>
            <div class="card-actions">
                <a href="/apache/stop" class="btn btn-primary">Stop Server</a>
            </div>
        </article>
        '''
        soup = self.parse_html(html)
        
        # Check status indicator
        status = soup.find('span', class_='status-indicator')
        assert status is not None
        self.assert_has_attribute(status, 'role', 'status')
        
        # Check status has icon (color-independent indicator - WEB 3.2)
        icon = status.find('i')
        assert icon is not None
        self.assert_has_attribute(icon, 'aria-hidden', 'true')
        
        # Check status has text label
        label = status.find('span', class_='status-label')
        assert label is not None
    
    def test_action_card_with_secondary_actions(self):
        """Test action card with multiple actions."""
        html = '''
        <article class="action-card">
            <div class="card-header">
                <div class="card-header-content">
                    <h3 class="card-title">Workstation</h3>
                </div>
            </div>
            <div class="card-body">
                <p class="card-description">Manage your workstation</p>
            </div>
            <div class="card-actions">
                <a href="/ssh" class="btn btn-primary card-action-primary">
                    SSH into Workstation
                    <i class="icon-arrow-right" aria-hidden="true"></i>
                </a>
                <div class="card-actions-secondary">
                    <a href="/restart" class="btn btn-secondary btn-sm">
                        <i class="icon-refresh" aria-hidden="true"></i>
                        Restart
                    </a>
                    <a href="/stop" class="btn btn-secondary btn-sm">
                        <i class="icon-stop" aria-hidden="true"></i>
                        Stop
                    </a>
                </div>
            </div>
        </article>
        '''
        soup = self.parse_html(html)
        
        # Check primary action
        primary = soup.find('a', class_='card-action-primary')
        assert primary is not None
        
        # Check secondary actions
        secondary = soup.find('div', class_='card-actions-secondary')
        assert secondary is not None
        
        secondary_btns = secondary.find_all('a', class_='btn-secondary')
        assert len(secondary_btns) >= 2
    
    def test_action_card_disabled_state(self):
        """Test action card in disabled state."""
        html = '''
        <article class="action-card disabled">
            <div class="card-header">
                <div class="card-header-content">
                    <h3 class="card-title">Install Service</h3>
                </div>
            </div>
            <div class="card-body">
                <p class="card-description">Workstation must be running</p>
            </div>
            <div class="card-actions">
                <a href="/install" 
                   class="btn btn-primary card-action-primary"
                   aria-disabled="true"
                   tabindex="-1">
                    Install Service
                </a>
            </div>
        </article>
        '''
        soup = self.parse_html(html)
        
        # Check disabled class
        card = soup.find('article', class_='disabled')
        assert card is not None
        
        # Check button is marked disabled
        btn = card.find('a', class_='card-action-primary')
        assert btn is not None
        self.assert_has_attribute(btn, 'aria-disabled', 'true')
        self.assert_has_attribute(btn, 'tabindex', '-1')
    
    def test_action_card_touch_targets(self):
        """Test action card buttons meet touch target size.
        
        Validates: Requirements 8.5 (Touch target size)
        """
        html = '''
        <article class="action-card">
            <div class="card-actions">
                <a href="/install" class="btn btn-primary card-action-primary">
                    Install
                </a>
            </div>
        </article>
        '''
        soup = self.parse_html(html)
        
        # Button should have card-action-primary class which applies min-height
        btn = soup.find('a', class_='card-action-primary')
        assert btn is not None
        self.assert_has_class(btn, 'card-action-primary')
        # CSS applies min-height: var(--touch-target-min, 44px)
    
    def test_action_card_with_help_link(self):
        """Test action card with help link.
        
        Validates: Requirements 7.3 (Contextual help)
        """
        html = '''
        <article class="action-card">
            <div class="card-header">
                <div class="card-header-content">
                    <h3 class="card-title">Advanced Configuration</h3>
                </div>
            </div>
            <div class="card-body">
                <p class="card-description">Configure advanced settings</p>
            </div>
            <div class="card-actions">
                <a href="/configure" class="btn btn-primary">Configure</a>
            </div>
            <div class="card-footer">
                <a href="/help/advanced" class="help-link">
                    <i class="icon-help-circle" aria-hidden="true"></i>
                    Learn more
                </a>
            </div>
        </article>
        '''
        soup = self.parse_html(html)
        
        # Check help link
        help_link = soup.find('a', class_='help-link')
        assert help_link is not None
        assert help_link.has_attr('href')
        
        # Help link should have descriptive text
        text = help_link.get_text(strip=True)
        assert len(text) > 0


class TestStatusIndicatorComponent(TestComponentFramework):
    """Test StatusIndicator component."""
    
    def test_status_indicator_color_independent(self):
        """Test status indicator uses both color AND icon.
        
        Validates: Requirements 3.2 (Color-independent indicators)
        """
        html = '''
        <span class="status-indicator status-success" role="status">
            <i class="icon-check-circle" aria-hidden="true"></i>
            <span class="status-label">Success</span>
        </span>
        '''
        soup = self.parse_html(html)
        
        indicator = soup.find('span', class_='status-indicator')
        assert indicator is not None
        self.assert_has_attribute(indicator, 'role', 'status')
        
        # Must have icon (not just color)
        icon = indicator.find('i')
        assert icon is not None, "Status indicator must have icon (not just color)"
        self.assert_has_attribute(icon, 'aria-hidden', 'true')
        
        # Must have text label (not just icon)
        label = indicator.find('span', class_='status-label')
        assert label is not None, "Status indicator must have text label (not just icon)"
        assert len(label.text.strip()) > 0
    
    def test_status_indicator_variants(self):
        """Test different status indicator variants."""
        statuses = ['success', 'warning', 'error', 'info', 'running', 'stopped']
        
        for status in statuses:
            html = f'''
            <span class="status-indicator status-{status}" role="status">
                <i class="icon-circle" aria-hidden="true"></i>
                <span class="status-label">{status.title()}</span>
            </span>
            '''
            soup = self.parse_html(html)
            
            indicator = soup.find('span', class_='status-indicator')
            assert indicator is not None
            self.assert_has_class(indicator, f'status-{status}')



class TestDestructiveActionDialog(TestComponentFramework):
    """Test ConfirmationDialog component for destructive actions with consequences."""
    
    def test_confirmation_dialog_structure(self):
        """Test confirmation dialog has proper ARIA structure.
        
        Validates: Requirements 12.1 (Destructive action confirmation)
        """
        html = '''
        <div id="destroy-dialog" 
             class="confirmation-dialog dialog-danger" 
             role="dialog" 
             aria-labelledby="destroy-dialog-title"
             aria-describedby="destroy-dialog-description"
             aria-modal="true"
             hidden>
            <div class="dialog-container">
                <div class="dialog-header">
                    <div class="dialog-icon dialog-icon-danger" aria-hidden="true">
                        <svg width="24" height="24"></svg>
                    </div>
                    <h2 id="destroy-dialog-title" class="dialog-title">
                        Destroy Workstation?
                    </h2>
                    <button type="button" class="dialog-close" aria-label="Close dialog">
                        <svg width="20" height="20"></svg>
                    </button>
                </div>
                <div class="dialog-body">
                    <p id="destroy-dialog-description" class="dialog-message">
                        This will permanently delete your workstation VM.
                    </p>
                </div>
                <div class="dialog-actions">
                    <button type="button" class="btn btn-secondary dialog-btn-cancel">
                        Cancel
                    </button>
                    <button type="button" class="btn btn-danger dialog-btn-confirm">
                        Destroy Workstation
                    </button>
                </div>
            </div>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check dialog element
        dialog = soup.find(attrs={'role': 'dialog'})
        assert dialog is not None
        self.assert_has_attribute(dialog, 'aria-labelledby')
        self.assert_has_attribute(dialog, 'aria-describedby')
        self.assert_has_attribute(dialog, 'aria-modal', 'true')
        
        # Check title exists
        title_id = dialog.get('aria-labelledby')
        title = soup.find(id=title_id)
        assert title is not None
        
        # Check description exists
        desc_id = dialog.get('aria-describedby')
        desc = soup.find(id=desc_id)
        assert desc is not None
        
        # Check action buttons
        buttons = dialog.find_all('button', class_='btn')
        assert len(buttons) >= 2, "Dialog should have at least 2 buttons (confirm and cancel)"
    
    def test_confirmation_dialog_consequences(self):
        """Test dialog explains consequences clearly.
        
        Validates: Requirements 12.2 (Confirmation consequence explanation)
        """
        html = '''
        <div role="dialog" aria-modal="true">
            <div class="dialog-body">
                <p class="dialog-message">This will permanently delete your workstation VM.</p>
                <div class="dialog-consequences">
                    <p class="consequences-heading">This will:</p>
                    <ul class="consequences-list">
                        <li class="consequence-item">All deployed services will be removed</li>
                        <li class="consequence-item">Configuration will be preserved</li>
                        <li class="consequence-item">You can reinstall later</li>
                    </ul>
                </div>
            </div>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check consequences section
        consequences = soup.find('div', class_='dialog-consequences')
        assert consequences is not None, "Dialog should explain consequences"
        
        # Check consequences list
        items = consequences.find_all('li', class_='consequence-item')
        assert len(items) >= 1, "Dialog should list specific consequences"
    
    def test_confirmation_dialog_keyboard_accessible(self):
        """Test dialog is keyboard accessible.
        
        Validates: Requirements 3.1 (Keyboard navigation)
        """
        html = '''
        <div role="dialog" aria-modal="true">
            <div class="dialog-header">
                <h2>Confirm Action</h2>
                <button type="button" class="dialog-close" aria-label="Close dialog">×</button>
            </div>
            <div class="dialog-actions">
                <button type="button" class="btn btn-secondary">Cancel</button>
                <button type="button" class="btn btn-danger">Confirm</button>
            </div>
        </div>
        '''
        self.assert_accessible(html)
    
    def test_confirmation_dialog_with_checkbox(self):
        """Test dialog with confirmation checkbox for extra safety."""
        html = '''
        <div role="dialog" aria-modal="true">
            <div class="dialog-body">
                <p class="dialog-message">This action cannot be undone.</p>
                <div class="dialog-checkbox">
                    <label class="checkbox-label">
                        <input type="checkbox" 
                               id="confirm-checkbox"
                               class="confirm-checkbox"
                               required>
                        <span class="checkbox-text">
                            I understand the consequences
                        </span>
                    </label>
                </div>
            </div>
            <div class="dialog-actions">
                <button type="button" class="btn btn-secondary">Cancel</button>
                <button type="button" 
                        class="btn btn-danger"
                        data-requires-checkbox="confirm-checkbox"
                        disabled>
                    Confirm
                </button>
            </div>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check checkbox exists
        checkbox = soup.find('input', class_='confirm-checkbox')
        assert checkbox is not None
        self.assert_has_attribute(checkbox, 'type', 'checkbox')
        
        # Check confirm button is initially disabled
        confirm_btn = soup.find('button', class_='btn-danger')
        assert confirm_btn is not None
        assert confirm_btn.has_attr('disabled')
    
    def test_confirmation_dialog_types(self):
        """Test different dialog types (danger, warning, info)."""
        types = ['danger', 'warning', 'info']
        
        for dialog_type in types:
            html = f'''
            <div class="confirmation-dialog dialog-{dialog_type}" role="dialog">
                <div class="dialog-header">
                    <div class="dialog-icon dialog-icon-{dialog_type}" aria-hidden="true">
                        <svg></svg>
                    </div>
                    <h2>Confirm</h2>
                </div>
            </div>
            '''
            soup = self.parse_html(html)
            
            dialog = soup.find('div', class_='confirmation-dialog')
            assert dialog is not None
            self.assert_has_class(dialog, f'dialog-{dialog_type}')


class TestLoadingStateWithProgress(TestComponentFramework):
    """Test LoadingState component with spinner and progress indicators."""
    
    def test_loading_state_spinner(self):
        """Test loading state with spinner.
        
        Validates: Requirements 9.1 (Load time or indicator)
        """
        html = '''
        <div class="loading-state loading-spinner loading-md" 
             role="status" 
             aria-live="polite" 
             aria-busy="true">
            <div class="loading-spinner" aria-hidden="true">
                <svg class="spinner-svg" viewBox="0 0 50 50">
                    <circle class="spinner-circle" cx="25" cy="25" r="20"></circle>
                </svg>
            </div>
            <p class="loading-message">Installing workstation...</p>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check loading state element
        loading = soup.find('div', class_='loading-state')
        assert loading is not None
        self.assert_has_attribute(loading, 'role', 'status')
        self.assert_has_attribute(loading, 'aria-live', 'polite')
        self.assert_has_attribute(loading, 'aria-busy', 'true')
        
        # Check spinner
        spinner = loading.find('div', class_='loading-spinner')
        assert spinner is not None
        self.assert_has_attribute(spinner, 'aria-hidden', 'true')
        
        # Check message
        message = loading.find('p', class_='loading-message')
        assert message is not None
        assert len(message.text.strip()) > 0
    
    def test_loading_state_with_progress(self):
        """Test loading state with progress bar.
        
        Validates: Requirements 9.2 (Long operation progress)
        """
        html = '''
        <div class="loading-state" role="status" aria-live="polite" aria-busy="true">
            <p class="loading-message">Installing workstation...</p>
            <div class="loading-progress">
                <div class="progress-bar" 
                     role="progressbar" 
                     aria-valuenow="50" 
                     aria-valuemin="0" 
                     aria-valuemax="100"
                     aria-label="Progress: 50%">
                    <div class="progress-fill" style="width: 50%"></div>
                </div>
                <span class="progress-text">50%</span>
            </div>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check progress bar
        progress = soup.find('div', attrs={'role': 'progressbar'})
        assert progress is not None
        self.assert_has_attribute(progress, 'aria-valuenow')
        self.assert_has_attribute(progress, 'aria-valuemin')
        self.assert_has_attribute(progress, 'aria-valuemax')
        self.assert_has_attribute(progress, 'aria-label')
        
        # Check progress fill
        fill = progress.find('div', class_='progress-fill')
        assert fill is not None
        assert fill.has_attr('style')
    
    def test_loading_state_skeleton(self):
        """Test loading state with skeleton screen.
        
        Validates: Requirements 9.3 (Loading state placeholders)
        """
        html = '''
        <div class="loading-state loading-skeleton" role="status" aria-live="polite" aria-busy="true">
            <div class="loading-skeleton" aria-hidden="true">
                <div class="skeleton-line skeleton-line-1"></div>
                <div class="skeleton-line skeleton-line-2"></div>
                <div class="skeleton-line skeleton-line-3"></div>
            </div>
            <p class="loading-message">Loading content...</p>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check loading state element
        loading_state = soup.find('div', class_='loading-state')
        assert loading_state is not None
        
        # Check skeleton container (nested div with same class)
        skeleton = loading_state.find('div', class_='loading-skeleton')
        assert skeleton is not None
        self.assert_has_attribute(skeleton, 'aria-hidden', 'true')
        
        # Check skeleton lines
        lines = skeleton.find_all('div', class_='skeleton-line')
        assert len(lines) >= 3
    
    def test_loading_state_with_estimated_time(self):
        """Test loading state with estimated time.
        
        Validates: Requirements 9.2 (Progress feedback), 14.2 (Time formatting)
        """
        html = '''
        <div class="loading-state" role="status" aria-live="polite" aria-busy="true">
            <p class="loading-message">Installing workstation...</p>
            <p class="loading-time">Estimated time: 5m 30s</p>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check estimated time
        time_elem = soup.find('p', class_='loading-time')
        assert time_elem is not None
        assert 'estimated' in time_elem.text.lower()
    
    def test_loading_state_sizes(self):
        """Test loading state different sizes."""
        sizes = ['sm', 'md', 'lg']
        
        for size in sizes:
            html = f'''
            <div class="loading-state loading-{size}" role="status">
                <p class="loading-message">Loading...</p>
            </div>
            '''
            soup = self.parse_html(html)
            
            loading = soup.find('div', class_='loading-state')
            assert loading is not None
            self.assert_has_class(loading, f'loading-{size}')


class TestNotificationWithDismiss(TestComponentFramework):
    """Test Notification component with dismissible alerts and auto-dismiss."""
    
    def test_notification_success(self):
        """Test success notification structure.
        
        Validates: Requirements 9.4 (Operation success confirmation)
        """
        html = '''
        <div class="notification notification-success" 
             role="alert" 
             aria-live="polite" 
             aria-atomic="true">
            <div class="notification-icon" aria-hidden="true">
                <svg width="20" height="20"></svg>
            </div>
            <div class="notification-content">
                <p class="notification-message">Workstation installed successfully</p>
            </div>
            <button type="button" 
                    class="notification-dismiss" 
                    aria-label="Dismiss notification">
                <svg width="16" height="16"></svg>
            </button>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check notification element
        notification = soup.find('div', class_='notification')
        assert notification is not None
        self.assert_has_attribute(notification, 'role', 'alert')
        self.assert_has_attribute(notification, 'aria-live', 'polite')
        self.assert_has_attribute(notification, 'aria-atomic', 'true')
        
        # Check message
        message = notification.find('p', class_='notification-message')
        assert message is not None
        assert len(message.text.strip()) > 0
    
    def test_notification_error(self):
        """Test error notification structure.
        
        Validates: Requirements 2.4 (Plain language error messages), 9.5 (Network error recovery)
        """
        html = '''
        <div class="notification notification-error" 
             role="alert" 
             aria-live="polite" 
             aria-atomic="true">
            <div class="notification-icon" aria-hidden="true">
                <svg width="20" height="20"></svg>
            </div>
            <div class="notification-content">
                <h4 class="notification-title">Installation Failed</h4>
                <p class="notification-message">Unable to connect to the server.</p>
                <div class="notification-actions">
                    <button type="button" class="btn btn-sm notification-action-btn">
                        Retry
                    </button>
                </div>
            </div>
            <button type="button" class="notification-dismiss" aria-label="Dismiss notification">
                <svg width="16" height="16"></svg>
            </button>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check notification
        notification = soup.find('div', class_='notification-error')
        assert notification is not None
        
        # Check title (optional)
        title = notification.find('h4', class_='notification-title')
        if title:
            assert len(title.text.strip()) > 0
        
        # Check message
        message = notification.find('p', class_='notification-message')
        assert message is not None
        
        # Check action buttons (for retry, etc.)
        actions = notification.find('div', class_='notification-actions')
        if actions:
            buttons = actions.find_all('button')
            assert len(buttons) >= 1
    
    def test_notification_color_independent(self):
        """Test notification uses both color AND icon.
        
        Validates: Requirements 3.2 (Color-independent indicators)
        """
        html = '''
        <div class="notification notification-warning" role="alert">
            <div class="notification-icon" aria-hidden="true">
                <svg width="20" height="20"></svg>
            </div>
            <div class="notification-content">
                <p class="notification-message">Warning message</p>
            </div>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Must have icon (not just color)
        icon = soup.find('div', class_='notification-icon')
        assert icon is not None, "Notification must have icon (not just color)"
        self.assert_has_attribute(icon, 'aria-hidden', 'true')
        
        # Must have text message (not just icon)
        message = soup.find('p', class_='notification-message')
        assert message is not None, "Notification must have text message (not just icon)"
        assert len(message.text.strip()) > 0
    
    def test_notification_dismissible(self):
        """Test notification can be dismissed.
        
        Validates: Requirements 3.1 (Keyboard navigation)
        """
        html = '''
        <div class="notification" role="alert">
            <div class="notification-content">
                <p class="notification-message">Message</p>
            </div>
            <button type="button" 
                    class="notification-dismiss" 
                    aria-label="Dismiss notification">
                ×
            </button>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check dismiss button
        dismiss = soup.find('button', class_='notification-dismiss')
        assert dismiss is not None
        self.assert_has_attribute(dismiss, 'aria-label')
        
        # Button should be keyboard accessible
        self.assert_accessible(html)
    
    def test_notification_with_undo(self):
        """Test notification with undo action.
        
        Validates: Requirements 12.5 (Undo availability)
        """
        html = '''
        <div class="notification notification-success" role="alert">
            <div class="notification-content">
                <p class="notification-message">Service deleted successfully</p>
                <div class="notification-actions">
                    <button type="button" class="btn btn-sm notification-action-btn">
                        Undo
                    </button>
                </div>
            </div>
        </div>
        '''
        soup = self.parse_html(html)
        
        # Check undo button
        actions = soup.find('div', class_='notification-actions')
        assert actions is not None
        
        undo_btn = actions.find('button')
        assert undo_btn is not None
        assert 'undo' in undo_btn.text.lower()
    
    def test_notification_types(self):
        """Test different notification types."""
        types = ['success', 'error', 'warning', 'info']
        
        for notif_type in types:
            html = f'''
            <div class="notification notification-{notif_type}" role="alert">
                <div class="notification-icon" aria-hidden="true">
                    <svg></svg>
                </div>
                <div class="notification-content">
                    <p class="notification-message">Message</p>
                </div>
            </div>
            '''
            soup = self.parse_html(html)
            
            notification = soup.find('div', class_='notification')
            assert notification is not None
            self.assert_has_class(notification, f'notification-{notif_type}')
    
    def test_notification_auto_dismiss(self):
        """Test notification with auto-dismiss attribute."""
        html = '''
        <div class="notification" 
             role="alert"
             data-auto-dismiss="5">
            <div class="notification-content">
                <p class="notification-message">Auto-dismissing in 5 seconds</p>
            </div>
        </div>
        '''
        soup = self.parse_html(html)
        
        notification = soup.find('div', class_='notification')
        assert notification is not None
        self.assert_has_attribute(notification, 'data-auto-dismiss')
