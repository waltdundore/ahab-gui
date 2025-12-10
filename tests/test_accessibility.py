"""
Unit tests for accessibility module.

Tests ARIA helpers and accessibility utilities.
"""

import pytest
from lib.accessibility import (
    generate_aria_label,
    generate_aria_describedby,
    get_focus_order,
    create_skip_link,
    create_aria_live_region,
    announce_to_screen_reader,
    validate_keyboard_accessible,
    generate_breadcrumb_aria,
    generate_progress_indicator,
    ensure_color_contrast
)


class TestGenerateAriaLabel:
    """Test ARIA label generation."""
    
    def test_simple_label(self):
        """Test simple ARIA label."""
        result = generate_aria_label("workstation", "install")
        assert "Install" in result
        assert "workstation" in result
    
    def test_label_with_target(self):
        """Test ARIA label with target."""
        result = generate_aria_label("service", "restart", "Apache")
        assert "Restart" in result
        assert "Apache" in result
        assert "service" in result


class TestGenerateAriaDescribedby:
    """Test aria-describedby generation."""
    
    def test_describedby_attributes(self):
        """Test aria-describedby attributes."""
        result = generate_aria_describedby("port-input", "Port number between 1-65535")
        
        assert 'aria_describedby' in result
        assert 'description_html' in result
        assert 'port-input-description' in result['aria_describedby']
        assert 'Port number between 1-65535' in result['description_html']
        assert 'sr-only' in result['description_html']


class TestGetFocusOrder:
    """Test focus order retrieval."""
    
    def test_home_page_focus_order(self):
        """Test focus order for home page."""
        order = get_focus_order('home')
        assert 'skip-to-content' in order
        assert 'main-nav' in order
        assert order[0] == 'skip-to-content'  # Skip link should be first
    
    def test_workstation_page_focus_order(self):
        """Test focus order for workstation page."""
        order = get_focus_order('workstation')
        assert 'breadcrumbs' in order
        assert 'workstation-status' in order
    
    def test_unknown_page_default(self):
        """Test unknown page returns default focus order."""
        order = get_focus_order('unknown-page')
        assert 'skip-to-content' in order
        assert 'main-nav' in order


class TestCreateSkipLink:
    """Test skip link creation."""
    
    def test_skip_link_html(self):
        """Test skip link HTML generation."""
        result = create_skip_link('main-content', 'Skip to main content')
        assert 'href="#main-content"' in result
        assert 'Skip to main content' in result
        assert 'skip-link' in result


class TestCreateAriaLiveRegion:
    """Test ARIA live region creation."""
    
    def test_polite_live_region(self):
        """Test polite live region."""
        result = create_aria_live_region('polite', atomic=True)
        assert 'aria-live="polite"' in result
        assert 'aria-atomic="true"' in result
        assert 'role="status"' in result
        assert 'sr-only' in result
    
    def test_assertive_live_region(self):
        """Test assertive live region."""
        result = create_aria_live_region('assertive', atomic=False)
        assert 'aria-live="assertive"' in result
        assert 'aria-atomic="false"' in result


class TestAnnounceToScreenReader:
    """Test screen reader announcements."""
    
    def test_announcement_structure(self):
        """Test announcement data structure."""
        result = announce_to_screen_reader("Operation complete", "polite")
        assert result['message'] == "Operation complete"
        assert result['priority'] == "polite"
        assert 'timestamp' in result


class TestValidateKeyboardAccessible:
    """Test keyboard accessibility validation."""
    
    def test_accessible_button(self):
        """Test accessible button."""
        html = '<button>Click me</button>'
        assert validate_keyboard_accessible(html) is True
    
    def test_accessible_link(self):
        """Test accessible link with href."""
        html = '<a href="/page">Link</a>'
        assert validate_keyboard_accessible(html) is True
    
    def test_inaccessible_link(self):
        """Test link without href is not accessible."""
        html = '<a>Not a link</a>'
        assert validate_keyboard_accessible(html) is False
    
    def test_tabindex_negative(self):
        """Test element with tabindex=-1 is not accessible."""
        html = '<button tabindex="-1">Hidden</button>'
        assert validate_keyboard_accessible(html) is False


class TestGenerateBreadcrumbAria:
    """Test breadcrumb generation with ARIA."""
    
    def test_breadcrumb_html(self):
        """Test breadcrumb HTML generation."""
        breadcrumbs = [
            {'label': 'Home', 'url': '/'},
            {'label': 'Services', 'url': '/services'},
            {'label': 'Apache', 'url': '/services/apache'}
        ]
        result = generate_breadcrumb_aria(breadcrumbs)
        
        assert 'aria-label="Breadcrumb"' in result
        assert 'Home' in result
        assert 'Services' in result
        assert 'Apache' in result
        assert 'aria-current="page"' in result  # Last item is current
    
    def test_empty_breadcrumbs(self):
        """Test empty breadcrumbs returns empty string."""
        assert generate_breadcrumb_aria([]) == ""


class TestGenerateProgressIndicator:
    """Test progress indicator generation."""
    
    def test_progress_indicator_html(self):
        """Test progress indicator HTML."""
        result = generate_progress_indicator(2, 4)
        
        assert 'role="progressbar"' in result
        assert 'aria-valuenow="2"' in result
        assert 'aria-valuemin="1"' in result
        assert 'aria-valuemax="4"' in result
        assert 'Step 2 of 4' in result
    
    def test_progress_with_labels(self):
        """Test progress indicator with step labels."""
        labels = ['Setup', 'Configure', 'Deploy', 'Verify']
        result = generate_progress_indicator(2, 4, labels)
        
        assert 'Setup' in result
        assert 'Configure' in result
        assert 'Deploy' in result
        assert 'Verify' in result
        assert 'aria-current="step"' in result
    
    def test_progress_percentage(self):
        """Test progress percentage calculation."""
        result = generate_progress_indicator(1, 4)
        assert 'width: 25%' in result
        
        result = generate_progress_indicator(2, 4)
        assert 'width: 50%' in result


class TestEnsureColorContrast:
    """Test color contrast validation."""
    
    def test_sufficient_contrast(self):
        """Test sufficient color contrast."""
        # Black on white
        assert ensure_color_contrast('#000000', '#FFFFFF', 4.5) is True
        
        # Ahab blue on white
        assert ensure_color_contrast('#0066cc', '#FFFFFF', 4.5) is True
    
    def test_insufficient_contrast(self):
        """Test insufficient color contrast."""
        # Light gray on white
        assert ensure_color_contrast('#CCCCCC', '#FFFFFF', 4.5) is False
    
    def test_wcag_aaa_level(self):
        """Test WCAG AAA level (7.0 ratio)."""
        # Black on white passes AAA
        assert ensure_color_contrast('#000000', '#FFFFFF', 7.0) is True
        
        # Some colors that pass AA but not AAA
        # This depends on specific color combinations
    
    def test_invalid_color_format(self):
        """Test invalid color format returns False."""
        assert ensure_color_contrast('invalid', '#FFFFFF', 4.5) is False
        assert ensure_color_contrast('#000000', 'invalid', 4.5) is False
    
    def test_colors_without_hash(self):
        """Test colors without # prefix."""
        assert ensure_color_contrast('000000', 'FFFFFF', 4.5) is True
