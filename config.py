"""Configuration management for Ahab GUI.

Reads configuration from environment variables and ahab.conf file.
Provides defaults for all settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Application configuration."""
    
    # Load environment variables from .env file if it exists
    env_path = Path('.') / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Try to load from ahab.conf in parent directory
    ahab_conf_path = Path('..') / 'ahab.conf'
    if ahab_conf_path.exists():
        load_dotenv(ahab_conf_path)
    
    # Server configuration
    PORT = int(os.getenv('WUI_PORT', '5000'))
    HOST = os.getenv('WUI_HOST', '127.0.0.1')
    DEBUG = os.getenv('WUI_DEBUG', 'False').lower() in ('true', '1', 'yes')
    
    # Ahab paths
    AHAB_PATH = os.getenv('AHAB_PATH', str(Path('..') / 'ahab'))
    
    # Command execution
    COMMAND_TIMEOUT = int(os.getenv('COMMAND_TIMEOUT', '3600'))  # 1 hour default
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    WUI_ENABLE_AUTH = os.getenv('WUI_ENABLE_AUTH', 'false').lower() in ('true', '1', 'yes')
    WUI_USERNAME = os.getenv('WUI_USERNAME', 'admin')
    WUI_PASSWORD = os.getenv('WUI_PASSWORD', 'changeme')
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = Path('.') / 'sessions'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # WebSocket configuration
    SOCKETIO_ASYNC_MODE = 'eventlet'
    
    # Allowed make commands (whitelist for security)
    ALLOWED_COMMANDS = [
        'help',
        'install',
        'verify-install',
        'test',
        'test-unit',
        'test-integration',
        'test-e2e',
        'test-nasa',
        'ssh',
        'clean',
        'deploy',
        'audit',
    ]
    
    @classmethod
    def validate(cls):
        """Validate configuration settings.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        errors = []
        
        # Validate port
        if not (1 <= cls.PORT <= 65535):
            errors.append(f"Invalid port: {cls.PORT}. Must be between 1 and 65535.")
        
        # Validate Ahab path
        ahab_path = Path(cls.AHAB_PATH)
        if not ahab_path.exists():
            errors.append(f"Ahab path does not exist: {cls.AHAB_PATH}")
        elif not (ahab_path / 'Makefile').exists():
            errors.append(f"Makefile not found in Ahab path: {cls.AHAB_PATH}")
        
        # Validate timeout
        if cls.COMMAND_TIMEOUT < 1:
            errors.append(f"Invalid command timeout: {cls.COMMAND_TIMEOUT}. Must be positive.")
        
        # Validate authentication settings
        if cls.WUI_ENABLE_AUTH:
            if not cls.WUI_USERNAME or not cls.WUI_PASSWORD:
                errors.append("Authentication enabled but username or password not set.")
            if cls.WUI_PASSWORD == 'changeme':
                errors.append("WARNING: Using default password 'changeme'. Please change it!")
        
        if errors:
            return False, '\n'.join(errors)
        
        return True, None
    
    @classmethod
    def get_info(cls):
        """Get configuration information for display.
        
        Returns:
            dict: Configuration information
        """
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': cls.DEBUG,
            'ahab_path': cls.AHAB_PATH,
            'command_timeout': cls.COMMAND_TIMEOUT,
            'auth_enabled': cls.WUI_ENABLE_AUTH,
            'allowed_commands': cls.ALLOWED_COMMANDS,
        }


# Create session directory if it doesn't exist
Config.SESSION_FILE_DIR.mkdir(exist_ok=True)
