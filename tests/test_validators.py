"""
Unit tests for validators module.

Tests validation functions for CMU Web Standards compliance.
"""

import pytest
from lib.validators import (
    validate_heading_hierarchy,
    validate_paragraph_length,
    validate_button_label,
    validate_alt_text,
    validate_error_message,
    validate_form_label_association,
    validate_color_independent_status
)


class TestHeadingHierarchy:
    """Test heading hierarchy validation."""
    
    def test_valid_hierarchy(self):
        """Test valid heading hierarchy."""
        html = "<h1>Title</h1><h2>Section</h2><h3>Subsection</h3>"
        assert validate_heading_hierarchy(html) is True
    
    def test_skipped_level(self):
        """Test skipped heading level is invalid."""
        html = "<h1>Title</h1><h3>Skipped H2</h3>"
        assert validate_heading_hierarchy(html) is False
    
    def test_same_level_allowed(self):
        """Test same level headings are allowed."""
        html = "<h1>Title</h1><h2>Section 1</h2><h2>Section 2</h2>"
        assert validate_heading_hierarchy(html) is True
    
    def test_going_down_allowed(self):
        """Test going down levels is allowed."""
        html = "<h1>Title</h1><h2>Section</h2><h3>Sub</h3><h2>Another Section</h2>"
        assert validate_heading_hierarchy(html) is True
    
    def test_no_headings(self):
        """Test no headings is valid."""
        html = "<p>Just a paragraph</p>"
        assert validate_heading_hierarchy(html) is True
    
    def test_empty_html(self):
        """Test empty HTML is valid."""
        assert validate_heading_hierarchy("") is True


class TestParagraphLength:
    """Test paragraph length validation."""
    
    def test_short_paragraph(self):
        """Test short paragraph is valid."""
        text = "This is a short paragraph. It has two sentences."
        assert validate_paragraph_length(text) is True
    
    def test_exactly_four_sentences(self):
        """Test exactly four sentences is valid."""
        text = "One. Two. Three. Four."
        assert validate_paragraph_length(text) is True
    
    def test_five_sentences_invalid(self):
        """Test five sentences is invalid."""
        text = "One. Two. Three. Four. Five."
        assert validate_paragraph_length(text) is False
    
    def test_empty_paragraph(self):
        """Test empty paragraph is valid."""
        assert validate_paragraph_length("") is True
        assert validate_paragraph_length("   ") is True
    
    def test_multiple_punctuation(self):
        """Test multiple punctuation marks."""
        text = "Really?! Yes! Maybe... Okay."
        assert validate_paragraph_length(text) is True


class TestButtonLabel:
    """Test button label validation."""
    
    def test_valid_action_verbs(self):
        """Test valid action verbs."""
        assert validate_button_label("Install Apache") is True
        assert validate_button_label("Deploy Service") is True
        assert validate_button_label("Delete Workstation") is True
        assert validate_button_label("Create VM") is True
    
    def test_invalid_non_action(self):
        """Test invalid non-action labels."""
        assert validate_button_label("Apache") is False
        assert validate_button_label("Workstation") is False
        assert validate_button_label("The Service") is False
    
    def test_empty_label(self):
        """Test empty label is invalid."""
        assert validate_button_label("") is False
        assert validate_button_label("   ") is False
    
    def test_case_insensitive(self):
        """Test validation is case insensitive."""
        assert validate_button_label("INSTALL") is True
        assert validate_button_label("Install") is True
        assert validate_button_label("install") is True


class TestAltText:
    """Test alt text validation."""
    
    def test_valid_alt_text(self):
        """Test valid descriptive alt text."""
        assert validate_alt_text("Ahab logo - whale tail symbol") is True
        assert validate_alt_text("Screenshot of Apache configuration") is True
    
    def test_empty_alt_text(self):
        """Test empty alt text is invalid."""
        assert validate_alt_text("") is False
        assert validate_alt_text("   ") is False
    
    def test_generic_alt_text(self):
        """Test generic alt text is invalid."""
        assert validate_alt_text("image") is False
        assert validate_alt_text("picture") is False
        assert validate_alt_text("icon") is False
    
    def test_filename_as_alt_text(self):
        """Test filename as alt text is invalid."""
        assert validate_alt_text("logo.png", "logo.png") is False
        assert validate_alt_text("image123.jpg", "image123.jpg") is False
    
    def test_too_short(self):
        """Test very short alt text is invalid."""
        assert validate_alt_text("ab") is False
        assert validate_alt_text("a") is False


class TestErrorMessage:
    """Test error message validation."""
    
    def test_valid_error_with_solution(self):
        """Test valid error message with solution."""
        msg = "Connection failed. Please check your network and try again."
        assert validate_error_message(msg) is True
    
    def test_error_without_solution(self):
        """Test error without solution is invalid."""
        msg = "An error occurred."
        assert validate_error_message(msg) is False
    
    def test_empty_message(self):
        """Test empty message is invalid."""
        assert validate_error_message("") is False
    
    def test_various_solution_indicators(self):
        """Test various solution indicator words."""
        assert validate_error_message("Failed. Try restarting the service.") is True
        assert validate_error_message("Error. Please verify your input.") is True
        assert validate_error_message("Issue detected. You should check the logs.") is True


class TestFormLabelAssociation:
    """Test form label association validation."""
    
    def test_label_with_for_attribute(self):
        """Test label with for attribute."""
        html = '<label for="name">Name:</label><input type="text" id="name">'
        assert validate_form_label_association(html) is True
    
    def test_wrapped_label(self):
        """Test input wrapped in label."""
        html = '<label>Name: <input type="text"></label>'
        assert validate_form_label_association(html) is True
    
    def test_missing_label(self):
        """Test input without label is invalid."""
        html = '<input type="text" id="name">'
        assert validate_form_label_association(html) is False
    
    def test_hidden_input_ignored(self):
        """Test hidden inputs are ignored."""
        html = '<input type="hidden" name="csrf">'
        assert validate_form_label_association(html) is True
    
    def test_button_input_ignored(self):
        """Test button inputs are ignored."""
        html = '<input type="submit" value="Submit">'
        assert validate_form_label_association(html) is True
    
    def test_multiple_inputs(self):
        """Test multiple inputs all need labels."""
        html = '''
        <label for="name">Name:</label><input type="text" id="name">
        <input type="email" id="email">
        '''
        assert validate_form_label_association(html) is False


class TestColorIndependentStatus:
    """Test color-independent status indicators."""
    
    def test_status_with_text(self):
        """Test status indicator with text."""
        html = '<span class="status">Running</span>'
        assert validate_color_independent_status(html) is True
    
    def test_status_with_icon(self):
        """Test status indicator with icon."""
        html = '<span class="status"><i class="icon-check"></i></span>'
        assert validate_color_independent_status(html) is True
    
    def test_status_color_only(self):
        """Test status with color only is invalid."""
        html = '<span class="status"></span>'
        assert validate_color_independent_status(html) is False
    
    def test_no_status_elements(self):
        """Test no status elements is valid."""
        html = '<p>Just text</p>'
        assert validate_color_independent_status(html) is True
    
    def test_multiple_status_indicators(self):
        """Test multiple status indicators."""
        html = '''
        <span class="status">Running</span>
        <span class="badge">Active</span>
        <span class="indicator"><svg>...</svg></span>
        '''
        assert validate_color_independent_status(html) is True
