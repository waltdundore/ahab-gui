#!/usr/bin/env python3
"""Ahab GUI - Web interface for Ahab infrastructure automation.

A simple, beginner-friendly web interface that makes infrastructure
automation accessible to everyone.
"""

from flask import Flask, render_template, jsonify, request, session
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()

from config import Config
from commands.executor import CommandExecutor, get_system_status

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SocketIO
socketio = SocketIO(
    app,
    async_mode='eventlet',
    cors_allowed_origins="*"  # For development; restrict in production
)

# Initialize command executor
try:
    executor = CommandExecutor(Config.AHAB_PATH, Config.COMMAND_TIMEOUT)
except ValueError as e:
    print(f"ERROR: Failed to initialize command executor: {e}")
    print(f"Please ensure Ahab is installed at: {Config.AHAB_PATH}")
    exit(1)


@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html')


@app.route('/api/status')
def api_status():
    """Get current system status.
    
    Returns:
        JSON response with system status
    """
    try:
        status = get_system_status(Config.AHAB_PATH)
        status['running_commands'] = executor.get_running_commands()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/config')
def api_config():
    """Get configuration information.
    
    Returns:
        JSON response with configuration info
    """
    return jsonify(Config.get_info())


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to Ahab GUI'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print(f"Client disconnected: {request.sid}")


@socketio.on('execute')
def handle_execute(data):
    """Handle command execution request.
    
    Args:
        data: Dictionary with 'command' key
    """
    command = data.get('command', '')
    
    # Validate command
    if not command:
        emit('error', {'message': 'No command specified'})
        return
    
    if command not in Config.ALLOWED_COMMANDS:
        emit('error', {'message': f'Command not allowed: {command}'})
        return
    
    # Check if already running
    if executor.is_running(command):
        emit('error', {'message': f'Command already running: {command}'})
        return
    
    print(f"Executing command: {command}")
    emit('command_started', {'command': command})
    
    def output_callback(line):
        """Callback for streaming command output."""
        socketio.emit('output', {'line': line}, room=request.sid)
    
    try:
        # Execute command with streaming output
        result = executor.execute(command, output_callback)
        
        # Send completion event
        emit('command_complete', {
            'command': result.command,
            'exit_code': result.exit_code,
            'success': result.success,
            'duration': result.duration
        })
        
    except ValueError as e:
        emit('error', {'message': str(e)})
    except Exception as e:
        emit('error', {'message': f'Command failed: {str(e)}'})


@socketio.on('kill')
def handle_kill(data):
    """Handle request to kill a running command.
    
    Args:
        data: Dictionary with 'command' key
    """
    command = data.get('command', '')
    
    if not command:
        emit('error', {'message': 'No command specified'})
        return
    
    success = executor.kill(command)
    
    if success:
        emit('command_killed', {'command': command})
    else:
        emit('error', {'message': f'Failed to kill command: {command}'})


@socketio.on('get_status')
def handle_get_status():
    """Handle status request."""
    try:
        status = get_system_status(Config.AHAB_PATH)
        status['running_commands'] = executor.get_running_commands()
        emit('status_update', status)
    except Exception as e:
        emit('error', {'message': f'Failed to get status: {str(e)}'})


def main():
    """Main entry point."""
    # Validate configuration
    is_valid, error = Config.validate()
    if not is_valid:
        print("ERROR: Configuration validation failed:")
        print(error)
        exit(1)
    
    print("=" * 60)
    print("Ahab GUI - Web Interface")
    print("=" * 60)
    print(f"Server: http://{Config.HOST}:{Config.PORT}")
    print(f"Ahab Path: {Config.AHAB_PATH}")
    print(f"Debug Mode: {Config.DEBUG}")
    print(f"Authentication: {'Enabled' if Config.WUI_ENABLE_AUTH else 'Disabled'}")
    print("=" * 60)
    print("Press Ctrl+C to stop")
    print()
    
    # Run the server
    socketio.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )


if __name__ == '__main__':
    main()
