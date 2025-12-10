"""Pytest configuration and fixtures for ahab-gui tests."""

import os
from pathlib import Path

# Set environment variables BEFORE any imports
# This must happen at module level, before pytest even starts
os.environ['SECRET_KEY'] = 'test-secret-key-minimum-32-characters-long-for-testing'

# Calculate ahab path relative to this test file
# ahab-gui/tests/conftest.py -> ../../ahab
test_file_path = Path(__file__).resolve()
ahab_path = test_file_path.parent.parent.parent / 'ahab'
os.environ['AHAB_PATH'] = str(ahab_path.resolve())

os.environ['WUI_HOST'] = '127.0.0.1'
os.environ['WUI_PORT'] = '5000'
os.environ['DEBUG'] = 'true'
import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_ahab_dir():
    """Create a temporary ahab directory for testing."""
    temp_dir = tempfile.mkdtemp()
    ahab_dir = Path(temp_dir) / 'ahab'
    ahab_dir.mkdir(parents=True, exist_ok=True)
    
    # Create minimal required structure
    (ahab_dir / 'Makefile').write_text("""
.PHONY: help test install clean
help:
	@echo "Test Makefile"
test:
	@echo "Running tests"
install:
	@echo "Installing"
clean:
	@echo "Cleaning"
""")
    
    # Create required directories
    (ahab_dir / 'scripts').mkdir(exist_ok=True)
    (ahab_dir / 'scripts' / 'lib').mkdir(exist_ok=True)
    (ahab_dir / 'tests').mkdir(exist_ok=True)
    (ahab_dir / 'playbooks').mkdir(exist_ok=True)
    (ahab_dir / 'roles').mkdir(exist_ok=True)
    (ahab_dir / 'docs').mkdir(exist_ok=True)
    (ahab_dir / 'config').mkdir(exist_ok=True)
    (ahab_dir / 'inventory').mkdir(exist_ok=True)
    
    # Create essential files that tests expect
    (ahab_dir / 'README.md').write_text("# Test Ahab\nTest README")
    (ahab_dir / 'scripts' / 'lib' / 'common.sh').write_text("""#!/bin/bash
# Common shell functions for testing
function log_info() { echo "INFO: $1"; }
function log_error() { echo "ERROR: $1"; }
function print_success() { echo "✓ $1"; }
function print_error() { echo "✗ $1"; }
function print_info() { echo "ℹ $1"; }
function print_warning() { echo "⚠ $1"; }
function validate_input() { [[ -n "$1" ]]; }
function check_command() { command -v "$1" >/dev/null 2>&1; }
""")
    (ahab_dir / 'playbooks' / 'provision-workstation.yml').write_text("""---
- name: Test playbook
  hosts: all
  tasks:
    - name: Test task
      debug:
        msg: "Test"
""")
    (ahab_dir / 'docs' / 'SECURITY_MODEL.md').write_text("# Security Model\nTest security documentation")
    (ahab_dir / 'docs' / 'PRODUCTION_SETUP.md').write_text("# Production Setup\nTest production documentation")
    
    # Create ahab.conf in parent directory (config manager expects it there)
    (Path(temp_dir) / 'ahab.conf').write_text("""# Test configuration
DEFAULT_OS=fedora
FEDORA_VERSION=43
GITHUB_USER=test-user
WORKSTATION_MEMORY=4096
WORKSTATION_CPUS=2
""")
    
    yield ahab_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)

@pytest.fixture(autouse=True)
def setup_test_environment(temp_ahab_dir):
    """Automatically set up test environment for all tests."""
    # Override AHAB_PATH for tests
    original_path = os.environ.get('AHAB_PATH')
    os.environ['AHAB_PATH'] = str(temp_ahab_dir)
    
    yield
    
    # Restore original path
    if original_path:
        os.environ['AHAB_PATH'] = original_path
    else:
        os.environ.pop('AHAB_PATH', None)

@pytest.fixture
def app():
    """Create Flask app for testing."""
    # Import here to avoid circular imports
    from app import create_app
    
    app, socketio = create_app()  # Unpack the tuple
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()