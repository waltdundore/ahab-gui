"""Tests for command executor."""

import pytest
from pathlib import Path
from commands.executor import CommandExecutor, ExecutionResult, get_system_status


def test_executor_initialization():
    """Test that executor initializes with valid path."""
    # This will fail if ahab directory doesn't exist, which is expected
    ahab_path = Path('..') / 'ahab'
    if ahab_path.exists():
        executor = CommandExecutor(str(ahab_path))
        assert executor.ahab_path == ahab_path
        assert executor.timeout == 3600


def test_executor_invalid_path():
    """Test that executor raises error with invalid path."""
    with pytest.raises(ValueError, match="does not exist"):
        CommandExecutor('/nonexistent/path')


def test_executor_no_makefile():
    """Test that executor raises error if Makefile missing."""
    # Create a temporary directory without Makefile
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError, match="Makefile not found"):
            CommandExecutor(tmpdir)


def test_is_running():
    """Test checking if command is running."""
    ahab_path = Path('..') / 'ahab'
    if ahab_path.exists():
        executor = CommandExecutor(str(ahab_path))
        # No commands should be running initially
        assert not executor.is_running('install')
        assert not executor.is_running('test')


def test_get_running_commands():
    """Test getting list of running commands."""
    ahab_path = Path('..') / 'ahab'
    if ahab_path.exists():
        executor = CommandExecutor(str(ahab_path))
        # No commands should be running initially
        assert executor.get_running_commands() == []


def test_strip_ansi_codes():
    """Test stripping ANSI color codes."""
    text_with_ansi = '\x1b[32mGreen text\x1b[0m'
    clean_text = CommandExecutor.strip_ansi_codes(text_with_ansi)
    assert clean_text == 'Green text'
    assert '\x1b' not in clean_text


def test_preserve_ansi_codes():
    """Test preserving ANSI color codes."""
    text_with_ansi = '\x1b[32mGreen text\x1b[0m'
    preserved = CommandExecutor.preserve_ansi_codes(text_with_ansi)
    assert preserved == text_with_ansi


def test_get_system_status():
    """Test getting system status."""
    ahab_path = Path('..') / 'ahab'
    if ahab_path.exists():
        status = get_system_status(str(ahab_path))
        assert isinstance(status, dict)
        assert 'workstation_installed' in status
        assert 'workstation_running' in status
        assert 'services' in status
        assert 'last_updated' in status
        assert isinstance(status['workstation_installed'], bool)
        assert isinstance(status['workstation_running'], bool)
        assert isinstance(status['services'], list)


def test_execution_result_dataclass():
    """Test ExecutionResult dataclass."""
    from datetime import datetime
    result = ExecutionResult(
        command='test',
        exit_code=0,
        output='Test output',
        duration=1.5,
        timestamp=datetime.now(),
        success=True
    )
    assert result.command == 'test'
    assert result.exit_code == 0
    assert result.success is True
    assert result.duration == 1.5
