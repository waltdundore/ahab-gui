"""
Property-based tests for configuration validation.
Feature: ahab-gui-secure-foundation
"""
import pytest
import os
import tempfile
from pathlib import Path
from hypothesis import given, strategies as st, settings
from config import Config, ConfigurationError, create_config


class TestConfigurationProperties:
    """Property-based tests for configuration validation."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Save original environment
        self.original_env = os.environ.copy()
        
        # Create temporary Ahab directory with Makefile
        self.temp_dir = tempfile.mkdtemp()
        self.ahab_path = Path(self.temp_dir) / 'ahab'
        self.ahab_path.mkdir()
        (self.ahab_path / 'Makefile').write_text('# Test Makefile\n')
    
    def teardown_method(self):
        """Clean up after each test."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)
        
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @settings(max_examples=100)
    @given(st.text(min_size=32, max_size=128, alphabet=st.characters(blacklist_categories=('Cs',), blacklist_characters='\x00')))
    def test_property_14_valid_secret_keys_accepted(self, secret_key):
        """
        Property 14: Configuration validation
        For any valid secret key (>= 32 chars), configuration should load successfully.
        Validates: Requirements 6.1
        """
        os.environ['SECRET_KEY'] = secret_key
        os.environ['AHAB_PATH'] = str(self.ahab_path)
        
        try:
            config = Config()
            assert config.SECRET_KEY == secret_key
        except ConfigurationError:
            pytest.fail("Valid secret key was rejected")
    
    @settings(max_examples=100)
    @given(st.text(max_size=31, alphabet=st.characters(blacklist_categories=('Cs',), blacklist_characters='\x00')))
    def test_property_15_invalid_secret_keys_rejected(self, secret_key):
        """
        Property 15: Configuration validation failure
        For any secret key < 32 chars, configuration should fail validation.
        Validates: Requirements 6.2
        """
        if not secret_key:  # Empty string case
            os.environ.pop('SECRET_KEY', None)
            with pytest.raises(ConfigurationError, match="SECRET_KEY environment variable must be set"):
                Config()
        else:
            os.environ['SECRET_KEY'] = secret_key
            os.environ['AHAB_PATH'] = str(self.ahab_path)
            
            with pytest.raises(ConfigurationError, match="at least 32 characters"):
                Config()
    
    @settings(max_examples=100)
    @given(st.integers(min_value=1, max_value=65535))
    def test_property_14_valid_ports_accepted(self, port):
        """
        Property 14: Configuration validation
        For any valid port (1-65535), configuration should accept it.
        Validates: Requirements 6.1
        """
        os.environ['SECRET_KEY'] = 'a' * 32
        os.environ['AHAB_PATH'] = str(self.ahab_path)
        os.environ['WUI_PORT'] = str(port)
        
        config = Config()
        assert config.WUI_PORT == port
    
    @settings(max_examples=100)
    @given(st.one_of(
        st.integers(max_value=0),
        st.integers(min_value=65536)
    ))
    def test_property_15_invalid_ports_rejected(self, port):
        """
        Property 15: Configuration validation failure
        For any invalid port (<1 or >65535), configuration should fail.
        Validates: Requirements 6.2
        """
        os.environ['SECRET_KEY'] = 'a' * 32
        os.environ['AHAB_PATH'] = str(self.ahab_path)
        os.environ['WUI_PORT'] = str(port)
        
        with pytest.raises(ConfigurationError, match="Invalid port"):
            Config()
    
    @settings(max_examples=100)
    @given(st.integers(min_value=1, max_value=1000))
    def test_property_14_valid_rate_limits_accepted(self, rate_limit):
        """
        Property 14: Configuration validation
        For any valid rate limit (>= 1), configuration should accept it.
        Validates: Requirements 6.1
        """
        os.environ['SECRET_KEY'] = 'a' * 32
        os.environ['AHAB_PATH'] = str(self.ahab_path)
        os.environ['RATE_LIMIT'] = str(rate_limit)
        
        config = Config()
        assert config.RATE_LIMIT == rate_limit
    
    @settings(max_examples=100)
    @given(st.integers(max_value=0))
    def test_property_15_invalid_rate_limits_rejected(self, rate_limit):
        """
        Property 15: Configuration validation failure
        For any invalid rate limit (<1), configuration should fail.
        Validates: Requirements 6.2
        """
        os.environ['SECRET_KEY'] = 'a' * 32
        os.environ['AHAB_PATH'] = str(self.ahab_path)
        os.environ['RATE_LIMIT'] = str(rate_limit)
        
        with pytest.raises(ConfigurationError, match="at least 1"):
            Config()
    
    def test_property_15_missing_ahab_path_rejected(self):
        """
        Property 15: Configuration validation failure
        For any non-existent Ahab path, configuration should fail.
        Validates: Requirements 6.2, 11.3
        """
        os.environ['SECRET_KEY'] = 'a' * 32
        os.environ['AHAB_PATH'] = '/nonexistent/path'
        
        with pytest.raises(ConfigurationError, match="does not exist"):
            Config()
    
    def test_property_15_ahab_path_without_makefile_rejected(self):
        """
        Property 15: Configuration validation failure
        For any Ahab path without Makefile, configuration should fail.
        Validates: Requirements 6.2, 11.3
        """
        # Create directory without Makefile
        no_makefile_path = Path(self.temp_dir) / 'no_makefile'
        no_makefile_path.mkdir()
        
        os.environ['SECRET_KEY'] = 'a' * 32
        os.environ['AHAB_PATH'] = str(no_makefile_path)
        
        with pytest.raises(ConfigurationError, match="Makefile not found"):
            Config()
    
    def test_property_15_missing_secret_key_rejected(self):
        """
        Property 15: Configuration validation failure
        When SECRET_KEY is missing, configuration should fail.
        Validates: Requirements 6.2
        """
        # Don't set SECRET_KEY
        os.environ.pop('SECRET_KEY', None)
        os.environ['AHAB_PATH'] = str(self.ahab_path)
        
        with pytest.raises(ConfigurationError, match="SECRET_KEY"):
            Config()
    
    def test_configuration_summary_excludes_sensitive_data(self):
        """
        Verify that configuration summary doesn't include sensitive data.
        Validates: Requirements 9.2
        """
        os.environ['SECRET_KEY'] = 'super-secret-key-that-should-not-be-logged'
        os.environ['AHAB_PATH'] = str(self.ahab_path)
        
        config = Config()
        summary = config.get_summary()
        
        # Ensure SECRET_KEY is not in summary
        assert 'SECRET_KEY' not in summary
        assert 'secret' not in str(summary).lower()
        
        # Ensure other config is present
        assert 'ahab_path' in summary
        assert 'port' in summary
