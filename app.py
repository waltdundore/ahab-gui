"""
Ahab GUI - Secure web interface for Ahab infrastructure automation.
"""
import logging
import os
import sys
from datetime import datetime
from flask import Flask, render_template, jsonify, request, session
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_socketio import SocketIO
from flask_session import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Import configuration module (but don't create config yet)
from config import create_config

# Global config instance (created lazily)
_config = None


def get_config():
    """Get or create configuration instance (lazy loading)."""
    global _config
    if _config is None:
        try:
            _config = create_config()
            logger.info("Configuration loaded successfully", extra=_config.get_summary())
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            sys.exit(1)
    return _config


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Load configuration (lazy loading)
    config = get_config()
    app.config.from_object(config)
    
    # Initialize extensions
    csrf = CSRFProtect(app)
    Session(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Security headers middleware
    @app.after_request
    def set_security_headers(response):
        """Set security headers on all responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        if not app.config['DEBUG']:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    # Context processors
    @app.context_processor
    def inject_navigation():
        """Inject navigation items into all templates."""
        # Get current path for determining active nav item
        current_path = request.path
        
        # Define navigation items with progressive disclosure
        # Items are shown/hidden based on system state (to be implemented)
        nav_items = [
            {
                'label': 'Home',
                'url': '/',
                'is_current': current_path == '/',
                'is_available': True,
                'icon': 'home'
            },
            {
                'label': 'Workstation',
                'url': '/workstation',
                'is_current': current_path.startswith('/workstation'),
                'is_available': True,
                'icon': 'server'
            },
            {
                'label': 'Services',
                'url': '/services',
                'is_current': current_path.startswith('/services'),
                'is_available': True,
                'icon': 'grid'
            },
            {
                'label': 'Network',
                'url': '/network',
                'is_current': current_path.startswith('/network'),
                'is_available': True,
                'icon': 'network'
            },
            {
                'label': 'Tests',
                'url': '/tests',
                'is_current': current_path.startswith('/tests'),
                'is_available': True,
                'icon': 'check'
            },
            {
                'label': 'Help',
                'url': '/help',
                'is_current': current_path.startswith('/help'),
                'is_available': True,
                'icon': 'help'
            }
        ]
        
        return {'nav_items': nav_items}
    
    @app.context_processor
    def inject_breadcrumbs():
        """Inject breadcrumbs into templates based on current path."""
        current_path = request.path
        breadcrumbs = []
        
        # Always start with Home
        if current_path != '/':
            breadcrumbs.append({
                'label': 'Home',
                'url': '/',
                'is_current': False
            })
        
        # Parse path to generate breadcrumbs
        path_parts = [p for p in current_path.split('/') if p]
        
        if path_parts:
            # Build breadcrumbs from path
            current_url = ''
            for i, part in enumerate(path_parts):
                current_url += '/' + part
                is_last = (i == len(path_parts) - 1)
                
                # Capitalize and format label
                label = part.replace('-', ' ').title()
                
                breadcrumbs.append({
                    'label': label,
                    'url': current_url,
                    'is_current': is_last
                })
        
        return {'breadcrumbs': breadcrumbs if len(breadcrumbs) > 1 else []}
    
    # Error handlers
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        """Handle CSRF validation errors."""
        logger.warning(f"CSRF validation failed", extra={
            'session_id': session.get('id', 'unknown'),
            'source_ip': request.remote_addr,
            'error': str(e)
        })
        
        # Return JSON for API requests, HTML for browser requests
        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({
                'error': True,
                'message': 'Security validation failed. Please refresh the page.',
                'code': 'CSRF_ERROR'
            }), 403
        
        return render_template('errors/403.html', 
                             error_code='CSRF_ERROR',
                             error_title='Security Validation Failed',
                             error_message='Your session security token is invalid. This usually happens when your session expires.',
                             recovery_actions=[
                                 'Refresh the page to get a new security token',
                                 'Clear your browser cookies and try again',
                                 'Go back to the dashboard',
                                 'Contact support if the problem persists'
                             ]), 403
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        """Handle bad request errors."""
        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({
                'error': True,
                'message': 'Invalid request.',
                'code': 'BAD_REQUEST'
            }), 400
        
        return render_template('errors/400.html',
                             error_code='BAD_REQUEST',
                             error_title='Invalid Request',
                             error_message='The request you sent was not valid. This might be due to incorrect data or a malformed URL.',
                             recovery_actions=[
                                 'Check the URL for errors',
                                 'Go back and try again',
                                 'Return to the dashboard',
                                 'Contact support if you need help'
                             ]), 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """Handle not found errors."""
        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({
                'error': True,
                'message': 'Resource not found.',
                'code': 'NOT_FOUND'
            }), 404
        
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(429)
    def handle_rate_limit(e):
        """Handle rate limit errors."""
        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({
                'error': True,
                'message': 'Too many requests. Please wait a moment.',
                'code': 'RATE_LIMIT'
            }), 429
        
        return render_template('errors/429.html',
                             error_code='RATE_LIMIT',
                             error_title='Too Many Requests',
                             error_message='You\'ve made too many requests in a short time. Please wait a moment before trying again.',
                             recovery_actions=[
                                 'Wait 30 seconds and try again',
                                 'Avoid clicking buttons multiple times',
                                 'Return to the dashboard',
                                 'Contact support if you need immediate assistance'
                             ]), 429
    
    @app.errorhandler(500)
    def handle_server_error(e):
        """Handle internal server errors."""
        logger.error(f"Internal server error", extra={
            'session_id': session.get('id', 'unknown'),
            'error': str(e)
        })
        
        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({
                'error': True,
                'message': 'An error occurred. Please try again.',
                'code': 'SERVER_ERROR'
            }), 500
        
        return render_template('errors/500.html',
                             error_code='SERVER_ERROR',
                             technical_details=str(e) if app.debug else None), 500
    
    # Routes
    @app.route('/')
    def index():
        """Render main dashboard."""
        # Initialize session if needed
        if 'id' not in session:
            import uuid
            session['id'] = str(uuid.uuid4())
            session['created_at'] = str(os.times())
            logger.info(f"New session created", extra={'session_id': session['id']})
        
        return render_template('index.html')
    
    @app.route('/workstation')
    def workstation():
        """Render workstation management page."""
        return render_template('workstation.html')
    
    @app.route('/services')
    def services():
        """Render services overview page."""
        # TODO: Get actual service status from system
        # For now, use placeholder values
        service_status = {
            'apache_installed': False,
            'mysql_installed': False,
            'php_installed': False
        }
        
        return render_template('services.html', **service_status)
    
    @app.route('/tests')
    def tests():
        """Render tests page."""
        return render_template('tests.html')
    
    @app.route('/network')
    def network():
        """Render network management page."""
        return render_template('network.html')
    
    @app.route('/network/switches')
    def network_switches():
        """Render network switches management page."""
        return render_template('network/switches.html')
    
    @app.route('/help')
    def help_page():
        """Render help page."""
        return render_template('help.html')
    
    @app.route('/api/whitelist', methods=['GET'])
    def get_whitelist():
        """Return the command whitelist (read-only)."""
        # This will be implemented when we create the executor
        whitelist = {
            'commands': [
                'install',
                'test',
                'status',
                'clean',
                'ssh',
                'verify-install',
                'network-switches',
                'network-switches-version',
                'network-switches-test'
            ],
            'services': [
                'apache',
                'mysql',
                'php'
            ],
            'network': [
                'switches'
            ]
        }
        return jsonify(whitelist)
    
    @app.route('/api/os/current', methods=['GET'])
    def get_current_os():
        """Get currently configured OS."""
        try:
            from lib.config_manager import AhabConfigManager
            
            config_mgr = AhabConfigManager(config.AHAB_PATH)
            current_os = config_mgr.get_current_os()
            oses = config_mgr.get_supported_oses()
            
            return jsonify({
                'success': True,
                'current_os': current_os,
                'supported_oses': oses
            })
        except Exception as e:
            logger.error(f"Failed to get current OS: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'CONFIG_ERROR'
            }), 500
    
    @app.route('/api/os/set', methods=['POST'])
    def set_os():
        """Set OS in ahab.conf."""
        try:
            from lib.config_manager import AhabConfigManager
            
            data = request.get_json()
            os_name = data.get('os')
            
            if not os_name:
                return jsonify({
                    'error': True,
                    'message': 'Missing os parameter',
                    'code': 'MISSING_PARAMETER'
                }), 400
            
            config_mgr = AhabConfigManager(config.AHAB_PATH)
            
            # Validate OS name
            if os_name not in config_mgr.SUPPORTED_OSES:
                return jsonify({
                    'error': True,
                    'message': f'Unsupported OS: {os_name}',
                    'code': 'INVALID_OS',
                    'supported_oses': list(config_mgr.SUPPORTED_OSES.keys())
                }), 400
            
            # Set OS
            if config_mgr.set_os(os_name):
                logger.info(f"OS set to {os_name}")
                return jsonify({
                    'success': True,
                    'os': os_name,
                    'os_info': config_mgr.SUPPORTED_OSES[os_name]
                })
            else:
                return jsonify({
                    'error': True,
                    'message': 'Failed to update ahab.conf',
                    'code': 'UPDATE_FAILED'
                }), 500
                
        except ValueError as e:
            logger.warning(f"Invalid OS selection: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'VALIDATION_ERROR'
            }), 400
        except Exception as e:
            logger.error(f"Failed to set OS: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'SERVER_ERROR'
            }), 500
    
    @app.route('/api/os/validate', methods=['GET'])
    def validate_config():
        """Validate ahab.conf configuration."""
        try:
            from lib.config_manager import AhabConfigManager
            
            config_mgr = AhabConfigManager(config.AHAB_PATH)
            validation = config_mgr.validate_config()
            
            return jsonify({
                'success': True,
                **validation
            })
        except Exception as e:
            logger.error(f"Failed to validate config: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'VALIDATION_ERROR'
            }), 500
    
    @app.route('/api/status', methods=['GET'])
    def get_status():
        """Get system status."""
        try:
            from commands.executor import get_system_status, CommandExecutor
            
            # Get system status
            status = get_system_status(config.AHAB_PATH)
            
            # Check for running commands
            executor = CommandExecutor(config.AHAB_PATH)
            running_commands = executor.get_running_commands()
            
            status['command_running'] = len(running_commands) > 0
            status['running_commands'] = running_commands
            
            return jsonify(status)
            
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'STATUS_ERROR'
            }), 500
    
    @app.route('/api/execute', methods=['POST'])
    def execute_command():
        """Execute a whitelisted command."""
        from commands.executor import CommandExecutor
        
        data = request.get_json()
        
        if not data or 'command' not in data:
            return jsonify({
                'error': True,
                'message': 'Missing command parameter',
                'code': 'MISSING_COMMAND'
            }), 400
        
        command = data.get('command')
        
        # Validate command is whitelisted
        if command not in config.ALLOWED_COMMANDS:
            return jsonify({
                'error': True,
                'message': f'Command not allowed: {command}',
                'code': 'COMMAND_NOT_ALLOWED',
                'allowed_commands': config.ALLOWED_COMMANDS
            }), 400
        
        try:
            executor = CommandExecutor(config.AHAB_PATH, timeout=config.COMMAND_TIMEOUT)
            
            # Check if command is already running
            if executor.is_running(command):
                return jsonify({
                    'error': True,
                    'message': f'Command "{command}" is already running',
                    'code': 'COMMAND_RUNNING'
                }), 409
            
            # Execute command
            result = executor.execute(command)
            
            logger.info(f"Command executed: {command}", extra={
                'command': command,
                'exit_code': result.exit_code,
                'duration': result.duration,
                'success': result.success
            })
            
            return jsonify({
                'success': result.success,
                'command': command,
                'exit_code': result.exit_code,
                'output': result.output,
                'duration': result.duration,
                'timestamp': result.timestamp.isoformat()
            })
            
        except ValueError as e:
            logger.warning(f"Command validation failed: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'VALIDATION_ERROR'
            }), 400
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'EXECUTION_ERROR'
            }), 500
    
    # Service management routes
    @app.route('/services/<service_name>/install', methods=['POST'])
    def install_service(service_name):
        """Install a service."""
        # Validate service name
        valid_services = ['apache', 'mysql', 'php']
        if service_name not in valid_services:
            return jsonify({
                'error': True,
                'message': f'Invalid service: {service_name}',
                'code': 'INVALID_SERVICE'
            }), 400
        
        # TODO: Implement actual service installation via CommandExecutor
        # For now, return success
        logger.info(f"Installing service: {service_name}")
        
        return jsonify({
            'success': True,
            'message': f'{service_name} installed successfully',
            'service': service_name
        })
    
    @app.route('/services/<service_name>/restart', methods=['POST'])
    def restart_service(service_name):
        """Restart a service."""
        # Validate service name
        valid_services = ['apache', 'mysql', 'php']
        if service_name not in valid_services:
            return jsonify({
                'error': True,
                'message': f'Invalid service: {service_name}',
                'code': 'INVALID_SERVICE'
            }), 400
        
        # TODO: Implement actual service restart via CommandExecutor
        # For now, return success
        logger.info(f"Restarting service: {service_name}")
        
        return jsonify({
            'success': True,
            'message': f'{service_name} restarted successfully',
            'service': service_name
        })
    
    @app.route('/services/<service_name>/remove', methods=['POST'])
    def remove_service(service_name):
        """Remove a service."""
        # Validate service name
        valid_services = ['apache', 'mysql', 'php']
        if service_name not in valid_services:
            return jsonify({
                'error': True,
                'message': f'Invalid service: {service_name}',
                'code': 'INVALID_SERVICE'
            }), 400
        
        # TODO: Implement actual service removal via CommandExecutor
        # For now, return success
        logger.info(f"Removing service: {service_name}")
        
        return jsonify({
            'success': True,
            'message': f'{service_name} removed successfully',
            'service': service_name
        })
    
    # Status API endpoints for enhanced status displays
    @app.route('/api/workstation/status', methods=['GET'])
    def get_workstation_status():
        """Get workstation status with timestamp."""
        try:
            from commands.executor import get_system_status
            from datetime import datetime
            
            status = get_system_status(config.AHAB_PATH)
            
            # Enhanced status response with timestamp
            return jsonify({
                'success': True,
                'status_value': 'Running' if status.get('workstation_running') else 'Stopped' if status.get('workstation_installed') else 'Not Installed',
                'status_type': 'success' if status.get('workstation_running') else 'warning' if status.get('workstation_installed') else 'info',
                'description': 'Workstation VM is operational' if status.get('workstation_running') else 'Workstation VM exists but is stopped' if status.get('workstation_installed') else 'No workstation VM found',
                'last_updated': datetime.now().isoformat(),
                'workstation_installed': status.get('workstation_installed', False),
                'workstation_running': status.get('workstation_running', False)
            })
        except Exception as e:
            logger.error(f"Failed to get workstation status: {e}")
            return jsonify({
                'success': False,
                'status_value': 'Error',
                'status_type': 'error',
                'description': f'Failed to check status: {str(e)}',
                'last_updated': datetime.now().isoformat()
            }), 500
    
    @app.route('/api/services/<service_name>/status', methods=['GET'])
    def get_service_status(service_name):
        """Get service status with timestamp."""
        try:
            from commands.executor import get_system_status
            from datetime import datetime
            
            # Validate service name
            valid_services = ['apache', 'mysql', 'php', 'nginx']
            if service_name not in valid_services:
                return jsonify({
                    'success': False,
                    'status_value': 'Invalid Service',
                    'status_type': 'error',
                    'description': f'Service {service_name} is not supported',
                    'last_updated': datetime.now().isoformat()
                }), 400
            
            status = get_system_status(config.AHAB_PATH)
            service_key = f'{service_name}_installed'
            is_installed = status.get(service_key, False)
            
            # Enhanced status response
            return jsonify({
                'success': True,
                'status_value': 'Running' if is_installed else 'Not Installed',
                'status_type': 'success' if is_installed else 'info',
                'description': f'{service_name.title()} service is operational' if is_installed else f'{service_name.title()} service is not installed',
                'last_updated': datetime.now().isoformat(),
                'service_installed': is_installed
            })
        except Exception as e:
            logger.error(f"Failed to get {service_name} status: {e}")
            return jsonify({
                'success': False,
                'status_value': 'Error',
                'status_type': 'error',
                'description': f'Failed to check {service_name} status: {str(e)}',
                'last_updated': datetime.now().isoformat()
            }), 500
    
    # Network switch management API endpoints
    @app.route('/api/network/switches/version', methods=['POST'])
    def get_switches_version():
        """Get version information from network switches."""
        from commands.executor import CommandExecutor
        
        data = request.get_json()
        env = data.get('environment', 'dev')
        
        # Validate environment
        valid_envs = ['dev', 'prod']
        if env not in valid_envs:
            return jsonify({
                'error': True,
                'message': f'Invalid environment: {env}',
                'code': 'INVALID_ENVIRONMENT'
            }), 400
        
        try:
            executor = CommandExecutor(config.AHAB_PATH, timeout=config.COMMAND_TIMEOUT)
            
            # Execute network switches version command
            command = f'network-switches-version ENV={env}'
            result = executor.execute(command)
            
            logger.info(f"Network switches version command executed", extra={
                'command': command,
                'environment': env,
                'exit_code': result.exit_code,
                'success': result.success
            })
            
            return jsonify({
                'success': result.success,
                'command': command,
                'environment': env,
                'exit_code': result.exit_code,
                'output': result.output,
                'duration': result.duration,
                'timestamp': result.timestamp.isoformat()
            })
            
        except Exception as e:
            logger.error(f"Network switches version command failed: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'EXECUTION_ERROR'
            }), 500
    
    @app.route('/api/network/switches/test', methods=['POST'])
    def test_switches_connectivity():
        """Test connectivity to network switches."""
        from commands.executor import CommandExecutor
        
        data = request.get_json()
        env = data.get('environment', 'dev')
        
        # Validate environment
        valid_envs = ['dev', 'prod']
        if env not in valid_envs:
            return jsonify({
                'error': True,
                'message': f'Invalid environment: {env}',
                'code': 'INVALID_ENVIRONMENT'
            }), 400
        
        try:
            executor = CommandExecutor(config.AHAB_PATH, timeout=config.COMMAND_TIMEOUT)
            
            # Execute network switches test command
            command = f'network-switches-test ENV={env}'
            result = executor.execute(command)
            
            logger.info(f"Network switches test command executed", extra={
                'command': command,
                'environment': env,
                'exit_code': result.exit_code,
                'success': result.success
            })
            
            return jsonify({
                'success': result.success,
                'command': command,
                'environment': env,
                'exit_code': result.exit_code,
                'output': result.output,
                'duration': result.duration,
                'timestamp': result.timestamp.isoformat()
            })
            
        except Exception as e:
            logger.error(f"Network switches test command failed: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'EXECUTION_ERROR'
            }), 500
    
    @app.route('/api/network/switches/manage', methods=['POST'])
    def manage_switches():
        """Manage network switches (full management)."""
        from commands.executor import CommandExecutor
        
        data = request.get_json()
        env = data.get('environment', 'dev')
        
        # Validate environment
        valid_envs = ['dev', 'prod']
        if env not in valid_envs:
            return jsonify({
                'error': True,
                'message': f'Invalid environment: {env}',
                'code': 'INVALID_ENVIRONMENT'
            }), 400
        
        try:
            executor = CommandExecutor(config.AHAB_PATH, timeout=config.COMMAND_TIMEOUT)
            
            # Execute network switches management command
            command = f'network-switches ENV={env}'
            result = executor.execute(command)
            
            logger.info(f"Network switches management command executed", extra={
                'command': command,
                'environment': env,
                'exit_code': result.exit_code,
                'success': result.success
            })
            
            return jsonify({
                'success': result.success,
                'command': command,
                'environment': env,
                'exit_code': result.exit_code,
                'output': result.output,
                'duration': result.duration,
                'timestamp': result.timestamp.isoformat()
            })
            
        except Exception as e:
            logger.error(f"Network switches management command failed: {e}")
            return jsonify({
                'error': True,
                'message': str(e),
                'code': 'EXECUTION_ERROR'
            }), 500
    
    return app, socketio


# Create application
app, socketio = create_app()


if __name__ == '__main__':
    config = get_config()
    logger.info(f"Starting Ahab GUI on {config.WUI_HOST}:{config.WUI_PORT}")
    logger.info(f"Debug mode: {config.DEBUG}")
    logger.info(f"Ahab path: {config.AHAB_PATH}")
    
    socketio.run(
        app,
        host=config.WUI_HOST,
        port=config.WUI_PORT,
        debug=config.DEBUG
    )
