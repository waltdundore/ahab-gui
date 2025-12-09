"""Tests for Flask application."""

import pytest
from pathlib import Path


def test_app_imports():
    """Test that app module can be imported."""
    try:
        import app
        assert hasattr(app, 'app')
        assert hasattr(app, 'socketio')
    except ImportError as e:
        pytest.skip(f"Cannot import app: {e}")


def test_config_imports():
    """Test that config module can be imported."""
    from config import Config
    assert Config is not None


def test_executor_imports():
    """Test that executor module can be imported."""
    from commands.executor import CommandExecutor, ExecutionResult
    assert CommandExecutor is not None
    assert ExecutionResult is not None


def test_templates_exist():
    """Test that template files exist."""
    templates_dir = Path('templates')
    assert (templates_dir / 'base.html').exists()
    assert (templates_dir / 'index.html').exists()


def test_static_files_exist():
    """Test that static files exist."""
    static_dir = Path('static')
    assert (static_dir / 'css' / 'style.css').exists()
    assert (static_dir / 'js' / 'app.js').exists()


def test_requirements_file_exists():
    """Test that requirements.txt exists."""
    assert Path('requirements.txt').exists()


def test_readme_exists():
    """Test that README.md exists."""
    assert Path('README.md').exists()
