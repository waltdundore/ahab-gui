"""
Unit tests for content module.

Tests content models and data structures.
"""

import pytest
from datetime import datetime
from lib.content import (
    Breadcrumb,
    ContentSection,
    Action,
    HelpContent,
    PageContent,
    NavItem,
    UserContext,
    StatusIndicator
)


class TestBreadcrumb:
    """Test Breadcrumb model."""
    
    def test_create_breadcrumb(self):
        """Test creating a breadcrumb."""
        crumb = Breadcrumb(label="Home", url="/", is_current=False)
        assert crumb.label == "Home"
        assert crumb.url == "/"
        assert crumb.is_current is False
    
    def test_to_dict(self):
        """Test converting breadcrumb to dict."""
        crumb = Breadcrumb(label="Services", url="/services", is_current=True)
        data = crumb.to_dict()
        assert data['label'] == "Services"
        assert data['url'] == "/services"
        assert data['is_current'] is True


class TestContentSection:
    """Test ContentSection model."""
    
    def test_create_section(self):
        """Test creating a content section."""
        section = ContentSection(
            heading="Overview",
            level=2,
            content="This is the overview section."
        )
        assert section.heading == "Overview"
        assert section.level == 2
        assert section.content == "This is the overview section."
    
    def test_invalid_heading_level(self):
        """Test invalid heading level raises error."""
        with pytest.raises(ValueError):
            ContentSection(heading="Bad", level=1, content="Content")
        
        with pytest.raises(ValueError):
            ContentSection(heading="Bad", level=7, content="Content")
    
    def test_to_html(self):
        """Test converting section to HTML."""
        section = ContentSection(
            heading="Test Section",
            level=2,
            content="<p>Test content</p>"
        )
        html = section.to_html()
        assert "<h2>Test Section</h2>" in html
        assert "<p>Test content</p>" in html
        assert "<section" in html
    
    def test_validate_hierarchy_valid(self):
        """Test valid heading hierarchy."""
        section = ContentSection(heading="Main", level=2, content="Content")
        subsection = ContentSection(heading="Sub", level=3, content="Content")
        section.subsections.append(subsection)
        
        assert section.validate_hierarchy(parent_level=1) is True
    
    def test_validate_hierarchy_invalid(self):
        """Test invalid heading hierarchy (skipped level)."""
        section = ContentSection(heading="Main", level=2, content="Content")
        subsection = ContentSection(heading="Sub", level=4, content="Content")  # Skips H3
        section.subsections.append(subsection)
        
        assert section.validate_hierarchy(parent_level=1) is False


class TestAction:
    """Test Action model."""
    
    def test_create_action(self):
        """Test creating an action."""
        action = Action(
            label="Install Apache",
            url="/install/apache",
            style="primary",
            icon="download"
        )
        assert action.label == "Install Apache"
        assert action.url == "/install/apache"
        assert action.style == "primary"
        assert action.icon == "download"
    
    def test_to_dict(self):
        """Test converting action to dict."""
        action = Action(label="Deploy", url="/deploy", style="primary")
        data = action.to_dict()
        assert data['label'] == "Deploy"
        assert data['url'] == "/deploy"
        assert data['style'] == "primary"
        assert data['aria_label'] == "Deploy"  # Default to label


class TestHelpContent:
    """Test HelpContent model."""
    
    def test_create_help_content(self):
        """Test creating help content."""
        help_content = HelpContent(
            title="Need Help?",
            content="This feature allows you to...",
            link="/docs/feature",
            link_text="Read more"
        )
        assert help_content.title == "Need Help?"
        assert help_content.content == "This feature allows you to..."
    
    def test_to_dict_default_link_text(self):
        """Test default link text."""
        help_content = HelpContent(
            title="Help",
            content="Content",
            link="/docs"
        )
        data = help_content.to_dict()
        assert data['link_text'] == "Learn more"


class TestPageContent:
    """Test PageContent model."""
    
    def test_create_page_content(self):
        """Test creating page content."""
        breadcrumbs = [Breadcrumb("Home", "/")]
        sections = [ContentSection("Overview", 2, "Content")]
        
        page = PageContent(
            title="Test Page",
            meta_description="A test page",
            breadcrumbs=breadcrumbs,
            sections=sections
        )
        
        assert page.title == "Test Page"
        assert len(page.breadcrumbs) == 1
        assert len(page.sections) == 1
    
    def test_validate_hierarchy(self):
        """Test page hierarchy validation."""
        sections = [
            ContentSection("Section 1", 2, "Content"),
            ContentSection("Section 2", 2, "Content")
        ]
        
        page = PageContent(
            title="Page",
            meta_description="Desc",
            breadcrumbs=[],
            sections=sections
        )
        
        assert page.validate_hierarchy() is True
    
    def test_calculate_reading_time(self):
        """Test reading time calculation."""
        # Create content with known word count
        content = " ".join(["word"] * 200)  # 200 words = 1 minute
        sections = [ContentSection("Section", 2, content)]
        
        page = PageContent(
            title="Page",
            meta_description="Desc",
            breadcrumbs=[],
            sections=sections
        )
        
        reading_time = page.calculate_reading_time()
        assert reading_time >= 1  # At least 1 minute
    
    def test_to_dict(self):
        """Test converting page to dict."""
        page = PageContent(
            title="Test",
            meta_description="Desc",
            breadcrumbs=[Breadcrumb("Home", "/")],
            sections=[ContentSection("Section", 2, "Content")]
        )
        
        data = page.to_dict()
        assert data['title'] == "Test"
        assert 'breadcrumbs' in data
        assert 'sections' in data
        assert 'reading_time' in data


class TestNavItem:
    """Test NavItem model."""
    
    def test_create_nav_item(self):
        """Test creating a navigation item."""
        nav = NavItem(
            label="Home",
            url="/",
            icon="home",
            is_current=True
        )
        assert nav.label == "Home"
        assert nav.url == "/"
        assert nav.is_current is True
    
    def test_nav_with_children(self):
        """Test navigation item with children."""
        child1 = NavItem("Apache", "/services/apache")
        child2 = NavItem("MySQL", "/services/mysql")
        
        parent = NavItem("Services", "/services", children=[child1, child2])
        
        assert len(parent.children) == 2
        assert parent.children[0].label == "Apache"
    
    def test_to_dict(self):
        """Test converting nav item to dict."""
        nav = NavItem("Test", "/test", badge="3")
        data = nav.to_dict()
        assert data['label'] == "Test"
        assert data['badge'] == "3"


class TestUserContext:
    """Test UserContext model."""
    
    def test_create_user_context(self):
        """Test creating user context."""
        context = UserContext(
            workstation_installed=True,
            workstation_running=True,
            services_deployed=["apache", "mysql"]
        )
        assert context.workstation_installed is True
        assert context.workstation_running is True
        assert len(context.services_deployed) == 2
    
    def test_get_available_actions_home_no_workstation(self):
        """Test available actions on home with no workstation."""
        context = UserContext(workstation_installed=False)
        actions = context.get_available_actions('home')
        
        assert len(actions) > 0
        assert any('Create' in action.label for action in actions)
    
    def test_get_available_actions_home_workstation_running(self):
        """Test available actions on home with running workstation."""
        context = UserContext(
            workstation_installed=True,
            workstation_running=True
        )
        actions = context.get_available_actions('home')
        
        assert len(actions) > 0
        assert any('Services' in action.label for action in actions)
    
    def test_get_available_actions_workstation_running(self):
        """Test available actions on workstation page when running."""
        context = UserContext(
            workstation_installed=True,
            workstation_running=True
        )
        actions = context.get_available_actions('workstation')
        
        # Should have Stop, Restart, SSH, Destroy
        assert len(actions) >= 4
        labels = [action.label for action in actions]
        assert 'Stop' in labels
        assert 'SSH' in labels
    
    def test_get_available_actions_workstation_stopped(self):
        """Test available actions on workstation page when stopped."""
        context = UserContext(
            workstation_installed=True,
            workstation_running=False
        )
        actions = context.get_available_actions('workstation')
        
        # Should have Start, Destroy
        labels = [action.label for action in actions]
        assert 'Start' in labels
        assert 'Destroy' in labels
    
    def test_to_dict(self):
        """Test converting context to dict."""
        context = UserContext(workstation_installed=True)
        data = context.to_dict()
        assert data['workstation_installed'] is True


class TestStatusIndicator:
    """Test StatusIndicator model."""
    
    def test_create_status_indicator(self):
        """Test creating a status indicator."""
        status = StatusIndicator(
            status="success",
            label="Running",
            icon="check-circle"
        )
        assert status.status == "success"
        assert status.label == "Running"
        assert status.icon == "check-circle"
    
    def test_get_default_icon(self):
        """Test getting default icon for status."""
        status = StatusIndicator(status="success", label="OK")
        assert status.get_icon() == "check-circle"
        
        status = StatusIndicator(status="error", label="Failed")
        assert status.get_icon() == "x-circle"
    
    def test_to_dict(self):
        """Test converting status to dict."""
        status = StatusIndicator(status="running", label="Active")
        data = status.to_dict()
        assert data['status'] == "running"
        assert data['label'] == "Active"
        assert 'icon' in data
