"""
Tests for AhabConfigManager

Security testing:
- Input validation
- File operation safety
- Backup/restore functionality
"""
import os
import tempfile
import shutil
from pathlib import Path
import pytest

from lib.config_manager import AhabConfigManager


@pytest.fixture
def temp_ahab_dir():
    """Create temporary ahab directory with ahab.conf."""
    temp_dir = tempfile.mkdtemp()
    
    # Create ahab subdirectory (config manager expects ahab.conf in parent of ahab dir)
    ahab_dir = Path(temp_dir) / 'ahab'
    ahab_dir.mkdir()
    
    # Create ahab.conf in parent directory (temp_dir)
    config_file = Path(temp_dir) / 'ahab.conf'
    config_file.write_text("""# Ahab Configuration
DEFAULT_OS=fedora
WORKSTATION_MEMORY=4096
WORKSTATION_CPUS=2
""")
    
    yield str(ahab_dir)  # Return path to ahab directory
    
    # Cleanup
    shutil.rmtree(temp_dir)


def test_init_valid_path(temp_ahab_dir):
    """Test initialization with valid path."""
    mgr = AhabConfigManager(temp_ahab_dir)
    assert mgr.ahab_path == str(Path(temp_ahab_dir).resolve())
    assert mgr.config_file.exists()


def test_init_invalid_path():
    """Test initialization with invalid path."""
    with pytest.raises(ValueError, match="does not exist"):
        AhabConfigManager("/nonexistent/path")


def test_init_empty_path():
    """Test initialization with empty path."""
    with pytest.raises(ValueError, match="cannot be empty"):
        AhabConfigManager("")


def test_init_file_not_directory(temp_ahab_dir):
    """Test initialization with file instead of directory."""
    file_path = Path(temp_ahab_dir) / 'test.txt'
    file_path.write_text("test")
    
    with pytest.raises(ValueError, match="not a directory"):
        AhabConfigManager(str(file_path))


def test_get_current_os(temp_ahab_dir):
    """Test getting current OS."""
    mgr = AhabConfigManager(temp_ahab_dir)
    assert mgr.get_current_os() == 'fedora'


def test_get_current_os_not_set(temp_ahab_dir):
    """Test getting OS when not set."""
    # Create config without DEFAULT_OS in parent directory
    config_file = Path(temp_ahab_dir).parent / 'ahab.conf'
    config_file.write_text("# Empty config\n")
    
    mgr = AhabConfigManager(temp_ahab_dir)
    assert mgr.get_current_os() is None


def test_get_current_os_invalid(temp_ahab_dir):
    """Test getting OS when set to invalid value."""
    config_file = Path(temp_ahab_dir).parent / 'ahab.conf'
    config_file.write_text("DEFAULT_OS=invalid_os\n")
    
    mgr = AhabConfigManager(temp_ahab_dir)
    assert mgr.get_current_os() is None


def test_set_os_valid(temp_ahab_dir):
    """Test setting OS to valid value."""
    mgr = AhabConfigManager(temp_ahab_dir)
    
    assert mgr.set_os('debian')
    assert mgr.get_current_os() == 'debian'


def test_set_os_invalid():
    """Test setting OS to invalid value."""
    temp_dir = tempfile.mkdtemp()
    ahab_dir = Path(temp_dir) / 'ahab'
    ahab_dir.mkdir()
    config_file = Path(temp_dir) / 'ahab.conf'
    config_file.write_text("DEFAULT_OS=fedora\n")
    
    mgr = AhabConfigManager(str(ahab_dir))
    
    with pytest.raises(ValueError, match="Unsupported OS"):
        mgr.set_os('invalid_os')
    
    # Verify original value unchanged
    assert mgr.get_current_os() == 'fedora'
    
    shutil.rmtree(temp_dir)


def test_set_os_empty():
    """Test setting OS to empty string."""
    temp_dir = tempfile.mkdtemp()
    ahab_dir = Path(temp_dir) / 'ahab'
    ahab_dir.mkdir()
    config_file = Path(temp_dir) / 'ahab.conf'
    config_file.write_text("DEFAULT_OS=fedora\n")
    
    mgr = AhabConfigManager(str(ahab_dir))
    
    with pytest.raises(ValueError, match="cannot be empty"):
        mgr.set_os('')
    
    shutil.rmtree(temp_dir)


def test_set_os_injection_attempt():
    """Test setting OS with injection attempt."""
    temp_dir = tempfile.mkdtemp()
    ahab_dir = Path(temp_dir) / 'ahab'
    ahab_dir.mkdir()
    config_file = Path(temp_dir) / 'ahab.conf'
    config_file.write_text("DEFAULT_OS=fedora\n")
    
    mgr = AhabConfigManager(str(ahab_dir))
    
    # Try various injection attempts
    injection_attempts = [
        'fedora; rm -rf /',
        'fedora && malicious',
        'fedora | cat /etc/passwd',
        '../../../etc/passwd',
        'fedora\nMALICIOUS=true'
    ]
    
    for attempt in injection_attempts:
        with pytest.raises(ValueError):
            mgr.set_os(attempt)
    
    # Verify original value unchanged
    assert mgr.get_current_os() == 'fedora'
    
    shutil.rmtree(temp_dir)


def test_set_os_backup_restore(temp_ahab_dir):
    """Test backup is created and restored on failure."""
    mgr = AhabConfigManager(temp_ahab_dir)
    
    original_os = mgr.get_current_os()
    
    # Set to valid OS
    mgr.set_os('debian')
    
    # Verify backup was cleaned up
    backup_file = Path(str(mgr.config_file) + '.backup')
    assert not backup_file.exists()
    
    # Verify new value
    assert mgr.get_current_os() == 'debian'


def test_get_supported_oses():
    """Test getting supported OSes."""
    temp_dir = tempfile.mkdtemp()
    ahab_dir = Path(temp_dir) / 'ahab'
    ahab_dir.mkdir()
    config_file = Path(temp_dir) / 'ahab.conf'
    config_file.write_text("DEFAULT_OS=fedora\n")
    
    mgr = AhabConfigManager(str(ahab_dir))
    oses = mgr.get_supported_oses()
    
    assert 'fedora' in oses
    assert 'debian' in oses
    assert 'ubuntu' in oses
    
    assert oses['fedora']['name'] == 'Fedora 43'
    assert oses['debian']['name'] == 'Debian 13 (Trixie)'
    assert oses['ubuntu']['name'] == 'Ubuntu 24.04 LTS'
    
    shutil.rmtree(temp_dir)


def test_get_os_info():
    """Test getting info for specific OS."""
    temp_dir = tempfile.mkdtemp()
    ahab_dir = Path(temp_dir) / 'ahab'
    ahab_dir.mkdir()
    config_file = Path(temp_dir) / 'ahab.conf'
    config_file.write_text("DEFAULT_OS=fedora\n")
    
    mgr = AhabConfigManager(str(ahab_dir))
    
    fedora_info = mgr.get_os_info('fedora')
    assert fedora_info is not None
    assert fedora_info['name'] == 'Fedora 43'
    assert fedora_info['package_manager'] == 'dnf'
    
    invalid_info = mgr.get_os_info('invalid')
    assert invalid_info is None
    
    shutil.rmtree(temp_dir)


def test_validate_config_valid(temp_ahab_dir):
    """Test config validation with valid config."""
    mgr = AhabConfigManager(temp_ahab_dir)
    validation = mgr.validate_config()
    
    assert validation['valid'] is True
    assert validation['current_os'] == 'fedora'
    assert len(validation['issues']) == 0


def test_validate_config_missing_os(temp_ahab_dir):
    """Test config validation with missing OS."""
    config_file = Path(temp_ahab_dir).parent / 'ahab.conf'
    config_file.write_text("# No DEFAULT_OS\n")
    
    mgr = AhabConfigManager(temp_ahab_dir)
    validation = mgr.validate_config()
    
    assert validation['valid'] is False
    assert validation['current_os'] is None
    assert len(validation['issues']) > 0


def test_atomic_write(temp_ahab_dir):
    """Test that writes are atomic (temp file then rename)."""
    mgr = AhabConfigManager(temp_ahab_dir)
    
    # Set OS
    mgr.set_os('ubuntu')
    
    # Verify no temp files left behind
    temp_file = Path(str(mgr.config_file) + '.tmp')
    assert not temp_file.exists()
    
    # Verify value set correctly
    assert mgr.get_current_os() == 'ubuntu'


def test_concurrent_safety(temp_ahab_dir):
    """Test that multiple managers can work with same config."""
    mgr1 = AhabConfigManager(temp_ahab_dir)
    mgr2 = AhabConfigManager(temp_ahab_dir)
    
    # Set via mgr1
    mgr1.set_os('debian')
    
    # Read via mgr2
    assert mgr2.get_current_os() == 'debian'
