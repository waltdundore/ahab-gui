"""
Configuration module for Ahab GUI.
Loads and validates all configuration with secure defaults.
"""
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration validation fails."""
    pass


class Config:
    """Application configuration with validation and secure defaults."""
    
    def __init__(self):
        """Initialize configuration and validate all values."""
        self._load_configuration()
        self._validate_configuration()
        logger.info("Configuration loaded successfully", extra={
            'ahab_path': self.AHAB_PATH,
            'host': self.WUI_HOST,
            'port': self.WUI_PORT,
            'debug': self.DEBUG
        })
    
    def _load_configuration(self):
        """Load configuration from environment variables with secure defaults."""
        # Flask configuration
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ConfigurationError("SECRET_KEY environment variable must be set")
        
        # Ahab path configuration
        ahab_path = os.environ.get('AHAB_PATH', '../ahab')
        self.AHAB_PATH = str(Path(ahab_path).resolve())
        
        # Server configuration
        self.WUI_HOST = os.environ.get('WUI_HOST', '127.0.0.1')
        self.WUI_PORT = int(os.environ.get('WUI_PORT', '5000'))
        
        # Environment
        flask_env = os.environ.get('FLASK_ENV', 'production')
        self.DEBUG = flask_env == 'development'
        
        # Security configuration
        self.SESSION_COOKIE_HTTPONLY = True
        self.SESSION_COOKIE_SECURE = not self.DEBUG  # Only secure in production
        self.SESSION_COOKIE_SAMESITE = 'Lax'
        self.WTF_CSRF_ENABLED = True
        self.WTF_CSRF_TIME_LIMIT = None  # No time limit on CSRF tokens
        
        # Session configuration
        self.SESSION_TYPE = 'filesystem'
        self.SESSION_PERMANENT = False
        self.PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
        self.SESSION_FILE_DIR = Path('/tmp/ahab-gui-sessions')
        self.SESSION_FILE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting
        self.RATE_LIMIT = int(os.environ.get('RATE_LIMIT', '10'))
        self.RATE_LIMIT_WINDOW = 60  # 1 minute
        
        # Command execution
        self.COMMAND_TIMEOUT = int(os.environ.get('COMMAND_TIMEOUT', '300'))
        
        # Allowed make commands (whitelist)
        self.ALLOWED_COMMANDS = [
            'install', 
            'test', 
            'status', 
            'clean', 
            'ssh',
            'network-switches',
            'network-switches-version',
            'network-switches-test'
        ]
    
    def _validate_configuration(self):
        """Validate all configuration values."""
        # Validate SECRET_KEY
        if len(self.SECRET_KEY) < 32:
            raise ConfigurationError("SECRET_KEY must be at least 32 characters")
        
        # Validate Ahab path
        ahab_path = Path(self.AHAB_PATH)
        if not ahab_path.exists():
            raise ConfigurationError(f"Ahab directory does not exist: {self.AHAB_PATH}")
        
        if not ahab_path.is_dir():
            raise ConfigurationError(f"Ahab path is not a directory: {self.AHAB_PATH}")
        
        makefile_path = ahab_path / 'Makefile'
        if not makefile_path.exists():
            raise ConfigurationError(f"Makefile not found in Ahab directory: {self.AHAB_PATH}")
        
        # Validate port
        if not (1 <= self.WUI_PORT <= 65535):
            raise ConfigurationError(f"Invalid port number: {self.WUI_PORT}")
        
        # Validate rate limit
        if self.RATE_LIMIT < 1:
            raise ConfigurationError(f"Rate limit must be at least 1: {self.RATE_LIMIT}")
        
        # Validate timeout
        if self.COMMAND_TIMEOUT < 1:
            raise ConfigurationError(f"Command timeout must be at least 1 second: {self.COMMAND_TIMEOUT}")
        
        # Validate debug mode in production
        if not self.DEBUG and self.SESSION_COOKIE_SECURE is False:
            logger.warning("Running in production mode but SESSION_COOKIE_SECURE is False")
    
    def get_summary(self):
        """Get configuration summary for logging (without sensitive data)."""
        return {
            'ahab_path': self.AHAB_PATH,
            'host': self.WUI_HOST,
            'port': self.WUI_PORT,
            'debug': self.DEBUG,
            'rate_limit': self.RATE_LIMIT,
            'command_timeout': self.COMMAND_TIMEOUT,
            'csrf_enabled': self.WTF_CSRF_ENABLED,
            'session_timeout': self.PERMANENT_SESSION_LIFETIME
        }
    
    def get_info(self):
        """Get configuration info (alias for get_summary for backwards compatibility)."""
        info = self.get_summary()
        info['allowed_commands'] = self.ALLOWED_COMMANDS
        return info


def create_config():
    """Factory function to create and validate configuration."""
    try:
        config = Config()
        return config
    except ConfigurationError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        raise ConfigurationError(f"Failed to load configuration: {e}")
