"""
Unit tests for formatters module.

Tests formatting functions for dates, numbers, and text.
"""

import pytest
from datetime import datetime, timedelta
from lib.formatters import (
    format_timestamp,
    format_duration,
    format_file_size,
    format_relative_time,
    format_number,
    truncate_text,
    format_list
)


class TestFormatTimestamp:
    """Test timestamp formatting."""
    
    def test_format_with_time(self):
        """Test formatting with time component."""
        dt = datetime(2025, 12, 9, 14, 30, 0)
        result = format_timestamp(dt, include_time=True)
        assert "December" in result
        assert "9" in result
        assert "2025" in result
        assert ":" in result  # Time separator
    
    def test_format_without_time(self):
        """Test formatting without time component."""
        dt = datetime(2025, 12, 9, 14, 30, 0)
        result = format_timestamp(dt, include_time=False)
        assert "December" in result
        assert "9" in result
        assert "2025" in result
        assert ":" not in result  # No time
    
    def test_none_datetime(self):
        """Test None datetime returns empty string."""
        assert format_timestamp(None) == ""


class TestFormatDuration:
    """Test duration formatting."""
    
    def test_seconds_only(self):
        """Test formatting seconds only."""
        assert format_duration(30) == "30s"
        assert format_duration(59) == "59s"
    
    def test_minutes_and_seconds(self):
        """Test formatting minutes and seconds."""
        assert format_duration(90) == "1m 30s"
        assert format_duration(150) == "2m 30s"
    
    def test_minutes_only(self):
        """Test formatting whole minutes."""
        assert format_duration(120) == "2m"
        assert format_duration(180) == "3m"
    
    def test_hours_and_minutes(self):
        """Test formatting hours and minutes."""
        assert format_duration(3690) == "1h 1m"
        assert format_duration(7200) == "2h"
    
    def test_negative_duration(self):
        """Test negative duration returns 0s."""
        assert format_duration(-10) == "0s"
    
    def test_zero_duration(self):
        """Test zero duration."""
        assert format_duration(0) == "0s"


class TestFormatFileSize:
    """Test file size formatting."""
    
    def test_bytes(self):
        """Test formatting bytes."""
        assert format_file_size(500) == "500 B"
        assert format_file_size(1023) == "1023 B"
    
    def test_kilobytes(self):
        """Test formatting kilobytes."""
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(2048) == "2.0 KB"
    
    def test_megabytes(self):
        """Test formatting megabytes."""
        assert format_file_size(1048576) == "1.0 MB"
        assert format_file_size(1572864) == "1.5 MB"
    
    def test_gigabytes(self):
        """Test formatting gigabytes."""
        assert format_file_size(1073741824) == "1.0 GB"
    
    def test_negative_size(self):
        """Test negative size returns 0 B."""
        assert format_file_size(-100) == "0 B"
    
    def test_zero_size(self):
        """Test zero size."""
        assert format_file_size(0) == "0 B"


class TestFormatRelativeTime:
    """Test relative time formatting."""
    
    def test_just_now(self):
        """Test recent times show as 'just now'."""
        now = datetime.now()
        assert format_relative_time(now) == "just now"
        
        thirty_seconds_ago = now - timedelta(seconds=30)
        assert format_relative_time(thirty_seconds_ago) == "just now"
    
    def test_minutes_ago(self):
        """Test minutes ago."""
        now = datetime.now()
        five_minutes_ago = now - timedelta(minutes=5)
        result = format_relative_time(five_minutes_ago)
        assert "minute" in result
        assert "ago" in result
    
    def test_hours_ago(self):
        """Test hours ago."""
        now = datetime.now()
        two_hours_ago = now - timedelta(hours=2)
        result = format_relative_time(two_hours_ago)
        assert "hour" in result
        assert "ago" in result
    
    def test_days_ago(self):
        """Test days ago."""
        now = datetime.now()
        three_days_ago = now - timedelta(days=3)
        result = format_relative_time(three_days_ago)
        assert "day" in result
        assert "ago" in result
    
    def test_weeks_ago(self):
        """Test weeks ago."""
        now = datetime.now()
        two_weeks_ago = now - timedelta(weeks=2)
        result = format_relative_time(two_weeks_ago)
        assert "week" in result
        assert "ago" in result
    
    def test_none_datetime(self):
        """Test None datetime returns 'unknown'."""
        assert format_relative_time(None) == "unknown"
    
    def test_future_time(self):
        """Test future time shows as 'just now'."""
        future = datetime.now() + timedelta(hours=1)
        assert format_relative_time(future) == "just now"


class TestFormatNumber:
    """Test number formatting."""
    
    def test_integer(self):
        """Test formatting integers."""
        result = format_number(1000)
        # Should have thousands separator
        assert "1" in result
        assert "000" in result or "0" in result
    
    def test_float_with_decimals(self):
        """Test formatting floats."""
        result = format_number(1234.56, decimals=2)
        assert "1" in result
        assert "234" in result or "2" in result
    
    def test_auto_decimals(self):
        """Test auto decimal detection."""
        # Integer should have no decimals
        result = format_number(100)
        assert "." not in result or result.endswith(".0")
        
        # Float should have decimals
        result = format_number(100.5)
        assert "." in result


class TestTruncateText:
    """Test text truncation."""
    
    def test_short_text_unchanged(self):
        """Test short text is not truncated."""
        text = "Short text"
        assert truncate_text(text, 50) == text
    
    def test_truncate_at_word_boundary(self):
        """Test truncation at word boundary."""
        text = "This is a long text that needs to be truncated"
        result = truncate_text(text, 20)
        assert len(result) <= 20
        assert result.endswith("...")
        assert not result[:-3].endswith(" ")  # No trailing space before ...
    
    def test_truncate_exact_length(self):
        """Test text at exact max length."""
        text = "Exactly twenty chars"
        result = truncate_text(text, 20)
        assert result == text
    
    def test_empty_text(self):
        """Test empty text."""
        assert truncate_text("", 10) == ""
        assert truncate_text(None, 10) is None
    
    def test_custom_suffix(self):
        """Test custom suffix."""
        text = "This is a long text"
        result = truncate_text(text, 10, suffix="…")
        assert result.endswith("…")


class TestFormatList:
    """Test list formatting."""
    
    def test_bullet_list(self):
        """Test bullet list formatting."""
        items = ["Item 1", "Item 2", "Item 3"]
        result = format_list(items, style='bullet')
        assert "<ul>" in result
        assert "</ul>" in result
        assert "<li>Item 1</li>" in result
        assert "<li>Item 2</li>" in result
        assert "<li>Item 3</li>" in result
    
    def test_numbered_list(self):
        """Test numbered list formatting."""
        items = ["First", "Second", "Third"]
        result = format_list(items, style='numbered')
        assert "<ol>" in result
        assert "</ol>" in result
        assert "<li>First</li>" in result
    
    def test_empty_list(self):
        """Test empty list returns empty string."""
        assert format_list([]) == ""
    
    def test_single_item(self):
        """Test single item list."""
        result = format_list(["Only item"])
        assert "<li>Only item</li>" in result
