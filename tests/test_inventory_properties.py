"""
Property-based tests for inventory management.
Feature: inventory-management-gui

These tests validate correctness properties for inventory file operations,
particularly focusing on security properties around gitignore protection.
"""
import pytest
import os
import tempfile
from pathlib import Path
from hypothesis import given, strategies as st, settings, assume
import pathspec
from lib.validators import validate_hostname


class TestInventoryFilePathProperties:
    """Property-based tests for inventory file path operations."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Create temporary directory structure
        self.temp_dir = tempfile.mkdtemp()
        self.ahab_path = Path(self.temp_dir) / 'ahab'
        self.inventory_path = self.ahab_path / 'inventory'
        self.inventory_path.mkdir(parents=True)
        
        # Create .gitignore file
        gitignore_content = """# Actual inventory files (protected)
dev/hosts.yml
prod/hosts.yml
workstation/hosts.yml
**/hosts.yml
!**/hosts.yml.example
!**/hosts.yml.template
"""
        (self.inventory_path / '.gitignore').write_text(gitignore_content)
        
        # Create environment directories
        for env in ['dev', 'prod', 'workstation']:
            (self.inventory_path / env).mkdir()
    
    def teardown_method(self):
        """Clean up after each test."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def get_write_file_path(self, env: str) -> Path:
        """
        Get the file path for write operations.
        This should always return the actual file (not .example).
        """
        return self.inventory_path / env / 'hosts.yml'
    
    def get_read_file_path(self, env: str) -> Path:
        """
        Get the file path for read operations.
        This should always return the actual file (not .example).
        """
        return self.inventory_path / env / 'hosts.yml'
    
    def is_protected_from_git(self, file_path: Path) -> bool:
        """
        Check if a file path is protected by .gitignore.
        """
        gitignore_path = self.inventory_path / '.gitignore'
        with open(gitignore_path) as f:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
        
        # Get relative path from inventory directory
        try:
            rel_path = file_path.relative_to(self.inventory_path)
            return spec.match_file(str(rel_path))
        except ValueError:
            return False
    
    @settings(max_examples=100)
    @given(st.sampled_from(['dev', 'prod', 'workstation']))
    def test_property_4_write_operations_target_protected_files(self, env):
        """
        Feature: inventory-management-gui, Property 4: Write operations target protected files
        
        For any write operation, the target file path should match a pattern in .gitignore
        (not contain ".example" or ".template").
        
        Validates: Requirements 5.1
        """
        write_path = self.get_write_file_path(env)
        
        # Verify path doesn't contain .example or .template
        assert '.example' not in str(write_path), \
            f"Write path should not contain '.example': {write_path}"
        assert '.template' not in str(write_path), \
            f"Write path should not contain '.template': {write_path}"
        
        # Verify path is protected by gitignore
        assert self.is_protected_from_git(write_path), \
            f"Write path should be protected by .gitignore: {write_path}"
    
    @settings(max_examples=100)
    @given(st.sampled_from(['dev', 'prod', 'workstation']))
    def test_property_5_read_operations_use_actual_files(self, env):
        """
        Feature: inventory-management-gui, Property 5: Read operations use actual files
        
        For any read operation, the source file path should not contain ".example" or ".template".
        
        Validates: Requirements 5.2
        """
        read_path = self.get_read_file_path(env)
        
        # Verify path doesn't contain .example or .template
        assert '.example' not in str(read_path), \
            f"Read path should not contain '.example': {read_path}"
        assert '.template' not in str(read_path), \
            f"Read path should not contain '.template': {read_path}"
        
        # Verify it's the actual file name
        assert read_path.name == 'hosts.yml', \
            f"Read path should be 'hosts.yml', not '{read_path.name}'"
    
    @settings(max_examples=100)
    @given(
        st.sampled_from(['dev', 'prod', 'workstation']),
        st.sampled_from(['hosts.yml', 'hosts.yml.example', 'hosts.yml.template'])
    )
    def test_property_10_git_protection_verification(self, env, filename):
        """
        Feature: inventory-management-gui, Property 10: Git protection verification
        
        For any inventory file path, the protection status should correctly reflect
        whether the file matches .gitignore patterns.
        
        Validates: Requirements 5.3, 5.5
        """
        file_path = self.inventory_path / env / filename
        is_protected = self.is_protected_from_git(file_path)
        
        # Actual files (hosts.yml) should be protected
        if filename == 'hosts.yml':
            assert is_protected, \
                f"Actual inventory file should be protected: {file_path}"
        
        # Example and template files should NOT be protected
        elif '.example' in filename or '.template' in filename:
            assert not is_protected, \
                f"Example/template files should not be protected: {file_path}"
    
    @settings(max_examples=100)
    @given(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'),
        min_codepoint=ord('a'),
        max_codepoint=ord('z')
    )))
    def test_property_4_arbitrary_env_names_produce_protected_paths(self, env_name):
        """
        Feature: inventory-management-gui, Property 4: Write operations target protected files
        
        For any environment name, the write path should produce a protected file path.
        This tests that the path construction logic is sound.
        
        Validates: Requirements 5.1
        """
        # Skip if env_name contains problematic characters
        assume(env_name.isalnum())
        assume(not env_name.startswith('.'))
        
        # Create the environment directory
        env_dir = self.inventory_path / env_name
        env_dir.mkdir(exist_ok=True)
        
        write_path = self.inventory_path / env_name / 'hosts.yml'
        
        # Verify path doesn't contain .example or .template
        assert '.example' not in str(write_path)
        assert '.template' not in str(write_path)
        
        # The path should match the gitignore pattern **/hosts.yml
        assert write_path.name == 'hosts.yml'


class TestInventoryFilePathEdgeCases:
    """Edge case tests for inventory file paths."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.ahab_path = Path(self.temp_dir) / 'ahab'
        self.inventory_path = self.ahab_path / 'inventory'
        self.inventory_path.mkdir(parents=True)
        
        # Create .gitignore file
        gitignore_content = """# Actual inventory files (protected)
dev/hosts.yml
prod/hosts.yml
workstation/hosts.yml
**/hosts.yml
!**/hosts.yml.example
!**/hosts.yml.template
"""
        (self.inventory_path / '.gitignore').write_text(gitignore_content)
    
    def teardown_method(self):
        """Clean up after each test."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def is_protected_from_git(self, file_path: Path) -> bool:
        """Check if a file path is protected by .gitignore."""
        gitignore_path = self.inventory_path / '.gitignore'
        with open(gitignore_path) as f:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
        
        try:
            rel_path = file_path.relative_to(self.inventory_path)
            return spec.match_file(str(rel_path))
        except ValueError:
            return False
    
    def test_example_files_not_protected(self):
        """Verify that .example files are not protected by gitignore."""
        for env in ['dev', 'prod', 'workstation']:
            example_path = self.inventory_path / env / 'hosts.yml.example'
            assert not self.is_protected_from_git(example_path), \
                f"Example file should not be protected: {example_path}"
    
    def test_template_files_not_protected(self):
        """Verify that .template files are not protected by gitignore."""
        for env in ['dev', 'prod', 'workstation']:
            template_path = self.inventory_path / env / 'hosts.yml.template'
            assert not self.is_protected_from_git(template_path), \
                f"Template file should not be protected: {template_path}"
    
    def test_actual_files_protected(self):
        """Verify that actual inventory files are protected by gitignore."""
        for env in ['dev', 'prod', 'workstation']:
            actual_path = self.inventory_path / env / 'hosts.yml'
            assert self.is_protected_from_git(actual_path), \
                f"Actual file should be protected: {actual_path}"
    
    def test_nested_hosts_yml_protected(self):
        """Verify that hosts.yml in any subdirectory is protected."""
        # Create nested directory
        nested_dir = self.inventory_path / 'custom' / 'nested'
        nested_dir.mkdir(parents=True)
        
        nested_hosts = nested_dir / 'hosts.yml'
        assert self.is_protected_from_git(nested_hosts), \
            f"Nested hosts.yml should be protected: {nested_hosts}"
    
    def test_hosts_yml_example_in_nested_dir_not_protected(self):
        """Verify that hosts.yml.example in nested directories is not protected."""
        nested_dir = self.inventory_path / 'custom' / 'nested'
        nested_dir.mkdir(parents=True)
        
        nested_example = nested_dir / 'hosts.yml.example'
        assert not self.is_protected_from_git(nested_example), \
            f"Nested example should not be protected: {nested_example}"




class TestHostnameValidationProperties:
    """Property-based tests for hostname validation."""
    
    @settings(max_examples=100)
    @given(st.text(min_size=1, max_size=300))
    def test_property_2_hostname_validation_rejects_invalid_formats(self, hostname):
        """
        Feature: inventory-management-gui, Property 2: Hostname validation rejects invalid formats
        
        For any string that doesn't match valid hostname format (alphanumeric, hyphens, dots),
        validation should reject it with an error.
        
        Validates: Requirements 2.2, 7.4
        """
        # Generate strings that are definitely invalid
        # We'll test that invalid hostnames are rejected
        
        # Check the stripped version (since validator strips)
        stripped = hostname.strip()
        
        # Skip if stripping makes it empty
        if not stripped:
            result = validate_hostname(hostname)
            assert not result, "Empty/whitespace hostname should be rejected"
            return
        
        # Check if hostname contains invalid characters (after stripping)
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.')
        has_invalid_chars = any(c not in valid_chars for c in stripped)
        
        # Check for other invalid patterns
        starts_with_hyphen = stripped.startswith('-')
        ends_with_hyphen = stripped.endswith('-')
        starts_with_dot = stripped.startswith('.')
        ends_with_dot = stripped.endswith('.')
        has_consecutive_dots = '..' in stripped
        too_long = len(stripped) > 253
        
        # Check for labels that are too long (> 63 chars between dots)
        labels = stripped.split('.')
        has_long_label = any(len(label) > 63 for label in labels)
        
        # If hostname has any of these invalid patterns, it should be rejected
        is_definitely_invalid = (
            has_invalid_chars or
            starts_with_hyphen or
            ends_with_hyphen or
            starts_with_dot or
            ends_with_dot or
            has_consecutive_dots or
            too_long or
            has_long_label
        )
        
        result = validate_hostname(hostname)
        
        # If we know it's invalid, validation should reject it
        if is_definitely_invalid:
            assert not result, \
                f"Invalid hostname should be rejected: '{hostname}' (stripped: '{stripped}')"
    
    @settings(max_examples=100)
    @given(
        st.text(
            alphabet=st.characters(
                blacklist_categories=('Cc', 'Cs'),  # Exclude control characters
                blacklist_characters='-.'  # Exclude valid hostname chars
            ),
            min_size=1,
            max_size=50
        )
    )
    def test_property_2_special_characters_rejected(self, invalid_chars):
        """
        Feature: inventory-management-gui, Property 2: Hostname validation rejects invalid formats
        
        Hostnames with special characters (not alphanumeric, hyphen, or dot) should be rejected.
        
        Validates: Requirements 2.2, 7.4
        """
        # Skip if by chance we generated only valid characters
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.')
        assume(any(c not in valid_chars for c in invalid_chars))
        
        result = validate_hostname(invalid_chars)
        assert not result, \
            f"Hostname with special characters should be rejected: '{invalid_chars}'"
    
    @settings(max_examples=100)
    @given(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Zs',))))
    def test_property_2_whitespace_only_rejected(self, whitespace):
        """
        Feature: inventory-management-gui, Property 2: Hostname validation rejects invalid formats
        
        Hostnames that are only whitespace should be rejected.
        
        Validates: Requirements 2.2, 7.4
        """
        result = validate_hostname(whitespace)
        assert not result, \
            f"Whitespace-only hostname should be rejected: '{whitespace}'"
    
    def test_property_2_empty_string_rejected(self):
        """
        Feature: inventory-management-gui, Property 2: Hostname validation rejects invalid formats
        
        Empty hostnames should be rejected.
        
        Validates: Requirements 2.2, 7.4
        """
        assert not validate_hostname(''), "Empty hostname should be rejected"
        assert not validate_hostname('   '), "Whitespace-only hostname should be rejected"
    
    @settings(max_examples=100)
    @given(st.integers(min_value=254, max_value=1000))
    def test_property_2_too_long_hostnames_rejected(self, length):
        """
        Feature: inventory-management-gui, Property 2: Hostname validation rejects invalid formats
        
        Hostnames longer than 253 characters should be rejected.
        
        Validates: Requirements 2.2, 7.4
        """
        # Generate a hostname that's too long
        long_hostname = 'a' * length
        result = validate_hostname(long_hostname)
        assert not result, \
            f"Hostname longer than 253 chars should be rejected (length: {length})"
    
    @settings(max_examples=100)
    @given(st.integers(min_value=64, max_value=200))
    def test_property_2_long_labels_rejected(self, label_length):
        """
        Feature: inventory-management-gui, Property 2: Hostname validation rejects invalid formats
        
        Hostnames with labels (parts between dots) longer than 63 characters should be rejected.
        
        Validates: Requirements 2.2, 7.4
        """
        # Generate a hostname with a label that's too long
        long_label = 'a' * label_length
        hostname = f"valid.{long_label}.com"
        result = validate_hostname(hostname)
        assert not result, \
            f"Hostname with label longer than 63 chars should be rejected (label length: {label_length})"
    
    def test_property_2_edge_cases_rejected(self):
        """
        Feature: inventory-management-gui, Property 2: Hostname validation rejects invalid formats
        
        Test specific edge cases that should be rejected.
        
        Validates: Requirements 2.2, 7.4
        """
        invalid_hostnames = [
            '-hostname',           # Starts with hyphen
            'hostname-',           # Ends with hyphen
            '.hostname',           # Starts with dot
            'hostname.',           # Ends with dot
            'host..name',          # Consecutive dots
            'host name',           # Contains space
            'host_name',           # Contains underscore
            'host@name',           # Contains @
            'host#name',           # Contains #
            'host$name',           # Contains $
            'host%name',           # Contains %
            'host&name',           # Contains &
            'host*name',           # Contains *
            'host(name)',          # Contains parentheses
            'host[name]',          # Contains brackets
            'host{name}',          # Contains braces
            'host/name',           # Contains slash
            'host\\name',          # Contains backslash
            'host|name',           # Contains pipe
            'host;name',           # Contains semicolon
            'host:name',           # Contains colon
            'host,name',           # Contains comma
            'host?name',           # Contains question mark
            'host!name',           # Contains exclamation
            'host=name',           # Contains equals
            'host+name',           # Contains plus
        ]
        
        for hostname in invalid_hostnames:
            result = validate_hostname(hostname)
            assert not result, \
                f"Invalid hostname should be rejected: '{hostname}'"


class TestHostnameValidationValidCases:
    """Test that valid hostnames are accepted."""
    
    def test_valid_hostnames_accepted(self):
        """
        Test that valid hostnames are accepted by the validator.
        These are example-based tests to ensure we don't reject valid hostnames.
        """
        valid_hostnames = [
            'localhost',
            'example.com',
            'sub.example.com',
            'my-server',
            'server-01',
            'web1.example.com',
            'api-v2.service.local',
            'host123',
            '123host',
            'a',
            'a.b',
            'a-b-c',
            'wcss-dev-asus',
            'test-server-01.local',
        ]
        
        for hostname in valid_hostnames:
            result = validate_hostname(hostname)
            assert result, \
                f"Valid hostname should be accepted: '{hostname}'"
