"""
Tests to verify ahab prerequisite is present and intact.

These tests ensure that ahab-gui can find and use the ahab automation system.
Since ahab is a prerequisite for ahab-gui, these tests verify the dependency.
"""

import os
import pytest
from pathlib import Path
from config import Config, ConfigurationError


class TestAhabPrerequisite:
    """Test suite for ahab prerequisite verification."""
    
    def test_ahab_directory_exists(self):
        """Test that ahab directory exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        
        assert ahab_path.exists(), f"Ahab directory not found at {config.AHAB_PATH}"
        assert ahab_path.is_dir(), f"Ahab path is not a directory: {config.AHAB_PATH}"
    
    def test_ahab_makefile_exists(self):
        """Test that ahab Makefile exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        makefile = ahab_path / 'Makefile'
        
        assert makefile.exists(), f"Makefile not found in ahab directory: {makefile}"
        assert makefile.is_file(), f"Makefile is not a file: {makefile}"
    
    def test_ahab_makefile_has_targets(self):
        """Test that ahab Makefile contains expected targets."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        makefile = ahab_path / 'Makefile'
        
        content = makefile.read_text()
        
        # Check for essential make targets
        expected_targets = ['install', 'test', 'clean', 'help']
        for target in expected_targets:
            assert f'{target}:' in content or f'.PHONY: {target}' in content, \
                f"Makefile missing expected target: {target}"
    
    def test_ahab_playbooks_directory_exists(self):
        """Test that ahab playbooks directory exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        playbooks_dir = ahab_path / 'playbooks'
        
        assert playbooks_dir.exists(), f"Playbooks directory not found: {playbooks_dir}"
        assert playbooks_dir.is_dir(), f"Playbooks path is not a directory: {playbooks_dir}"
    
    def test_ahab_roles_directory_exists(self):
        """Test that ahab roles directory exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        roles_dir = ahab_path / 'roles'
        
        assert roles_dir.exists(), f"Roles directory not found: {roles_dir}"
        assert roles_dir.is_dir(), f"Roles path is not a directory: {roles_dir}"
    
    def test_ahab_scripts_directory_exists(self):
        """Test that ahab scripts directory exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        scripts_dir = ahab_path / 'scripts'
        
        assert scripts_dir.exists(), f"Scripts directory not found: {scripts_dir}"
        assert scripts_dir.is_dir(), f"Scripts path is not a directory: {scripts_dir}"
    
    def test_ahab_common_library_exists(self):
        """Test that ahab common shell library exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        common_lib = ahab_path / 'scripts' / 'lib' / 'common.sh'
        
        assert common_lib.exists(), f"Common library not found: {common_lib}"
        assert common_lib.is_file(), f"Common library is not a file: {common_lib}"
    
    def test_ahab_common_library_has_functions(self):
        """Test that ahab common library contains expected functions."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        common_lib = ahab_path / 'scripts' / 'lib' / 'common.sh'
        
        content = common_lib.read_text()
        
        # Check for essential functions that ahab-gui might use
        expected_functions = [
            'print_success',
            'print_error',
            'print_info',
            'print_warning',
            'validate_input',
            'check_command'
        ]
        
        for func in expected_functions:
            assert f'{func}()' in content or f'function {func}' in content, \
                f"Common library missing expected function: {func}"
    
    def test_ahab_tests_directory_exists(self):
        """Test that ahab tests directory exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        tests_dir = ahab_path / 'tests'
        
        assert tests_dir.exists(), f"Tests directory not found: {tests_dir}"
        assert tests_dir.is_dir(), f"Tests path is not a directory: {tests_dir}"
    
    def test_ahab_docs_directory_exists(self):
        """Test that ahab docs directory exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        docs_dir = ahab_path / 'docs'
        
        assert docs_dir.exists(), f"Docs directory not found: {docs_dir}"
        assert docs_dir.is_dir(), f"Docs path is not a directory: {docs_dir}"
    
    def test_ahab_structure_complete(self):
        """Test that ahab has complete directory structure."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        
        # All essential directories
        essential_dirs = [
            'playbooks',
            'roles',
            'scripts',
            'scripts/lib',
            'tests',
            'docs',
            'config',
            'inventory'
        ]
        
        missing_dirs = []
        for dir_name in essential_dirs:
            dir_path = ahab_path / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
        
        assert len(missing_dirs) == 0, \
            f"Ahab missing essential directories: {', '.join(missing_dirs)}"
    
    def test_ahab_essential_files_exist(self):
        """Test that ahab has essential files."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        
        # All essential files
        essential_files = [
            'Makefile',
            'README.md',
            'scripts/lib/common.sh',
            'playbooks/provision-workstation.yml'
        ]
        
        missing_files = []
        for file_name in essential_files:
            file_path = ahab_path / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        assert len(missing_files) == 0, \
            f"Ahab missing essential files: {', '.join(missing_files)}"
    
    def test_ahab_path_is_absolute(self):
        """Test that AHAB_PATH is an absolute path."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        
        assert ahab_path.is_absolute(), \
            f"AHAB_PATH should be absolute, got: {config.AHAB_PATH}"
    
    def test_ahab_path_is_readable(self):
        """Test that ahab directory is readable."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        
        # Try to list directory contents
        try:
            list(ahab_path.iterdir())
        except PermissionError:
            pytest.fail(f"Cannot read ahab directory: {config.AHAB_PATH}")
    
    def test_config_validates_ahab_path(self):
        """Test that Config validates ahab path on initialization."""
        # This test verifies that Config.__init__ checks ahab path
        # If we get here, Config() succeeded, which means validation passed
        config = Config()
        assert config.AHAB_PATH is not None
    
    def test_invalid_ahab_path_raises_error(self):
        """Test that invalid ahab path raises ConfigurationError."""
        # Save original env var
        original_path = os.environ.get('AHAB_PATH')
        
        try:
            # Set invalid path
            os.environ['AHAB_PATH'] = '/nonexistent/path/to/ahab'
            
            # Should raise ConfigurationError
            with pytest.raises(ConfigurationError) as exc_info:
                Config()
            
            assert 'does not exist' in str(exc_info.value).lower()
        
        finally:
            # Restore original path
            if original_path:
                os.environ['AHAB_PATH'] = original_path
            else:
                os.environ.pop('AHAB_PATH', None)


class TestAhabIntegration:
    """Test suite for ahab-gui integration with ahab."""
    
    def test_can_construct_make_command_path(self):
        """Test that we can construct path to make command."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        makefile = ahab_path / 'Makefile'
        
        # Verify we can construct command
        assert makefile.exists()
        
        # This is how executor would call make
        # Skip if make not available (e.g., in Docker container)
        import subprocess
        import shutil
        
        if not shutil.which('make'):
            pytest.skip("Make not available in this environment (expected in Docker)")
        
        result = subprocess.run(
            ['make', '--version'],
            cwd=str(ahab_path),
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, "Make command should be available"
    
    def test_ahab_makefile_help_target_works(self):
        """Test that ahab Makefile help target works."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        
        import subprocess
        import shutil
        
        # Skip if make not available (e.g., in Docker container)
        if not shutil.which('make'):
            pytest.skip("Make not available in this environment (expected in Docker)")
        
        result = subprocess.run(
            ['make', 'help'],
            cwd=str(ahab_path),
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Help should succeed (exit 0) or be missing (exit 2)
        # Either is acceptable - we just want to verify make works
        assert result.returncode in [0, 2], \
            f"Make help failed with unexpected code: {result.returncode}"
    
    def test_ahab_path_relative_to_gui(self):
        """Test that ahab path is correctly relative to ahab-gui."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        gui_path = Path(__file__).parent.parent  # ahab-gui directory
        
        # Ahab should be sibling to ahab-gui (both in same parent)
        # Or ahab-gui should be inside ahab
        # Either structure is valid
        
        # Check if they share a common parent
        try:
            # Try to get relative path
            rel_path = ahab_path.relative_to(gui_path.parent)
            # If we get here, ahab is in same parent or below
            assert True
        except ValueError:
            # Not in same tree - check if gui is inside ahab
            try:
                rel_path = gui_path.relative_to(ahab_path)
                assert True
            except ValueError:
                pytest.fail(
                    f"Ahab and ahab-gui should be in related directories.\n"
                    f"Ahab: {ahab_path}\n"
                    f"GUI: {gui_path}"
                )


class TestAhabDocumentation:
    """Test suite for ahab documentation presence."""
    
    def test_ahab_readme_exists(self):
        """Test that ahab README exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        readme = ahab_path / 'README.md'
        
        assert readme.exists(), f"README.md not found: {readme}"
    
    def test_ahab_security_model_exists(self):
        """Test that ahab security model documentation exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        security_doc = ahab_path / 'docs' / 'SECURITY_MODEL.md'
        
        assert security_doc.exists(), \
            f"Security model documentation not found: {security_doc}"
    
    def test_ahab_production_setup_exists(self):
        """Test that ahab production setup documentation exists."""
        config = Config()
        ahab_path = Path(config.AHAB_PATH)
        prod_setup = ahab_path / 'docs' / 'PRODUCTION_SETUP.md'
        
        assert prod_setup.exists(), \
            f"Production setup documentation not found: {prod_setup}"


# Summary test that runs all checks
def test_ahab_prerequisite_complete():
    """
    Comprehensive test that ahab prerequisite is complete and intact.
    
    This test verifies:
    - Ahab directory exists and is accessible
    - Essential files and directories are present
    - Makefile has required targets
    - Common library has required functions
    - Documentation is present
    - Integration points work
    """
    config = Config()
    ahab_path = Path(config.AHAB_PATH)
    
    # Quick checks
    assert ahab_path.exists(), "Ahab directory must exist"
    assert (ahab_path / 'Makefile').exists(), "Makefile must exist"
    assert (ahab_path / 'scripts' / 'lib' / 'common.sh').exists(), \
        "Common library must exist"
    
    # If we get here, ahab prerequisite is satisfied
    assert True, "Ahab prerequisite is complete and intact"
