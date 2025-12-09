"""Tests for configuration management."""

import os
import pytest
from pathlib import Path
from config import Config


def test_config_defaults():
    """Test that configuration has sensible defaults."""
    assert Config.PORT == 5000 or isinstance(Config.PORT, int)
    assert Config.HOST == '127.0.0.1' or isinstance(Config.HOST, str)
    assert isinstance(Config.DEBUG, bool)
    assert isinstance(Config.COMMAND_TIMEOUT, int)
    assert Config.COMMAND_TIMEOUT > 0


def test_config_allowed_commands():
    """Test that allowed commands list is defined."""
    assert isinstance(Config.ALLOWED_COMMANDS, list)
    assert len(Config.ALLOWED_COMMANDS) > 0
    assert 'install' in Config.ALLOWED_COMMANDS
    assert 'test' in Config.ALLOWED_COMMANDS


def test_config_validation():
    """Test configuration validation."""
    is_valid, error = Config.validate()
    # Should be valid or have a clear error message
    if not is_valid:
        assert isinstance(error, str)
        assert len(error) > 0


def test_config_info():
    """Test configuration info retrieval."""
    info = Config.get_info()
    assert isinstance(info, dict)
    assert 'host' in info
    assert 'port' in info
    assert 'ahab_path' in info
    assert 'allowed_commands' in info


def test_session_directory_created():
    """Test that session directory is created."""
    assert Config.SESSION_FILE_DIR.exists()
    assert Config.SESSION_FILE_DIR.is_dir()
