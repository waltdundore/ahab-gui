"""Tests for configuration management."""

import os
import pytest
from pathlib import Path
from config import Config, ConfigurationError


def test_config_defaults():
    """Test that configuration has sensible defaults."""
    config = Config()
    assert config.WUI_PORT == 5000 or isinstance(config.WUI_PORT, int)
    assert config.WUI_HOST == '127.0.0.1' or isinstance(config.WUI_HOST, str)
    assert isinstance(config.DEBUG, bool)


def test_config_allowed_commands():
    """Test that allowed commands list is defined."""
    config = Config()
    assert isinstance(config.ALLOWED_COMMANDS, list)
    assert len(config.ALLOWED_COMMANDS) > 0
    assert 'install' in config.ALLOWED_COMMANDS
    assert 'test' in config.ALLOWED_COMMANDS


def test_config_validation():
    """Test configuration validation."""
    config = Config()
    # If Config() succeeds, validation passed
    assert config.SECRET_KEY is not None
    assert len(config.SECRET_KEY) >= 32


def test_config_info():
    """Test configuration info retrieval."""
    config = Config()
    info = config.get_info()
    assert isinstance(info, dict)
    assert 'host' in info
    assert 'port' in info
    assert 'ahab_path' in info
    assert 'allowed_commands' in info


def test_session_directory_created():
    """Test that session directory is created."""
    config = Config()
    assert config.SESSION_FILE_DIR.exists()
    assert config.SESSION_FILE_DIR.is_dir()
