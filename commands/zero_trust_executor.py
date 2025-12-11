"""Zero Trust Command Executor - MANDATORY

This module provides command execution with Zero Trust principles:
- Never trust user input
- Always verify command results
- Assume operations can fail
- Check every return value
- Validate all assumptions

Replaces patterns that assume success with explicit verification.

Last Updated: December 10, 2025
Status: MANDATORY
"""

import subprocess
import threading
import time
import os
import signal
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Dict, List, Any
import re
import json
import logging

# Set up logging (don't assume it works)
try:
    logger = logging.getLogger(__name__)
except Exception:
    # Fallback if logging fails
    class FallbackLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
    logger = FallbackLogger()


@dataclass
class ZeroTrustExecutionResult:
    """Result of a zero trust command execution.
    
    Never assume success - always check all fields.
    """
    command: str
    exit_code: Optional[int]  # Can be None if process killed
    output: str
    error_output: str
    duration: float
    timestamp: datetime
    success: bool
    timeout_occurred: bool
    verification_passed: bool
    warnings: List[str]
    
    def is_completely_successful(self) -> bool:
        """Check if operation was completely successful.
        
        Returns True only if:
        - Command executed (exit_code is not None)
        - Exit code was 0
        - No timeout occurred
        - Verification passed
        - No warnings
        """
        return (
            self.exit_code is not None and
            self.exit_code == 0 and
            not self.timeout_occurred and
            self.verification_passed and
            len(self.warnings) == 0
        )
    
    def has_critical_failure(self) -> bool:
        """Check if there was a critical failure."""
        return (
            self.exit_code is None or  # Process killed/crashed
            self.timeout_occurred or
            not self.verification_passed
        )


@dataclass
class CommandState:
    """State of a running command - never assume it's valid."""
    command: str
    running: bool
    pid: Optional[int]
    started_at: Optional[datetime]
    process: Optional[subprocess.Popen]
    
    def is_actually_running(self) -> bool:
        """Verify the process is actually running.
        
        Don't trust the 'running' flag - check the actual process.
        """
        if not self.running or self.process is None:
            return False
        
        try:
            # Check if process is still alive
            self.process.poll()
            return self.process.returncode is None
        except Exception:
            return False


class ZeroTrustCommandExecutor:
    """Command executor that never assumes success.
    
    Core principles:
    - Validate all inputs
    - Check all return values
    - Handle all error conditions
    - Verify all assumptions
    - Provide detailed failure information
    """
    
    def __init__(self, ahab_path: str, timeout: int = 3600):
        """Initialize the zero trust command executor.
        
        Args:
            ahab_path: Path to the ahab directory containing Makefile
            timeout: Default timeout for commands in seconds
            
        Raises:
            ValueError: If ahab_path is invalid or inaccessible
        """
        # Validate ahab_path (don't assume it's valid)
        if not ahab_path or not isinstance(ahab_path, str):
            raise ValueError("ahab_path must be a non-empty string")
        
        self.ahab_path = Path(ahab_path)
        
        # Verify path exists and is accessible
        if not self._verify_path_accessible(self.ahab_path):
            raise ValueError(f"Ahab path does not exist or is not accessible: {ahab_path}")
        
        # Verify Makefile exists
        makefile = self.ahab_path / 'Makefile'
        if not self._verify_file_accessible(makefile):
            raise ValueError(f"Makefile not found or not accessible in: {ahab_path}")
        
        # Validate timeout
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("timeout must be a positive integer")
        
        self.timeout = timeout
        self._running_commands: Dict[str, CommandState] = {}
        self._lock = threading.Lock()
        
        # State tracking for debugging
        self._execution_history: List[Dict[str, Any]] = []
        self._max_history = 100  # Prevent memory leaks
        
        logger.info(f"ZeroTrustCommandExecutor initialized: {ahab_path}, timeout={timeout}")
    
    def _verify_path_accessible(self, path: Path) -> bool:
        """Verify a path exists and is accessible."""
        try:
            return path.exists() and os.access(str(path), os.R_OK)
        except Exception as e:
            logger.error(f"Path verification failed: {e}")
            return False
    
    def _verify_file_accessible(self, file_path: Path) -> bool:
        """Verify a file exists and is readable."""
        try:
            return file_path.is_file() and os.access(str(file_path), os.R_OK)
        except Exception as e:
            logger.error(f"File verification failed: {e}")
            return False
    
    def _validate_command(self, command: str) -> bool:
        """Validate command input for security.
        
        Args:
            command: The make target to validate
            
        Returns:
            True if command is safe, False otherwise
        """
        if not command or not isinstance(command, str):
            return False
        
        # Whitelist approach - only allow known safe characters
        if not re.match(r'^[a-zA-Z0-9_-]+$', command):
            logger.warning(f"Command contains invalid characters: {command}")
            return False
        
        # Check length (prevent DoS)
        if len(command) > 100:
            logger.warning(f"Command too long: {len(command)} characters")
            return False
        
        return True
    
    def _verify_makefile_target(self, target: str) -> bool:
        """Verify that a make target exists in the Makefile."""
        try:
            makefile = self.ahab_path / 'Makefile'
            with open(makefile, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for target definition
                pattern = f'^{re.escape(target)}:'
                return bool(re.search(pattern, content, re.MULTILINE))
        except Exception as e:
            logger.error(f"Makefile verification failed: {e}")
            return False
    
    def _record_execution(self, command: str, result: ZeroTrustExecutionResult):
        """Record execution for debugging and audit trail."""
        try:
            record = {
                'timestamp': result.timestamp.isoformat(),
                'command': command,
                'exit_code': result.exit_code,
                'duration': result.duration,
                'success': result.success,
                'timeout_occurred': result.timeout_occurred,
                'verification_passed': result.verification_passed,
                'warnings_count': len(result.warnings)
            }
            
            self._execution_history.append(record)
            
            # Prevent memory leaks
            if len(self._execution_history) > self._max_history:
                self._execution_history = self._execution_history[-self._max_history:]
                
        except Exception as e:
            logger.error(f"Failed to record execution: {e}")
    
    def execute(self, command: str, 
                callback: Optional[Callable[[str], None]] = None,
                verify_output: Optional[str] = None,
                timeout_override: Optional[int] = None) -> ZeroTrustExecutionResult:
        """Execute a make command with zero trust verification.
        
        Args:
            command: The make target to execute (e.g., 'install', 'test')
            callback: Optional callback function for streaming output line-by-line
            verify_output: Optional pattern to verify in output
            timeout_override: Optional timeout override for this command
        
        Returns:
            ZeroTrustExecutionResult with detailed execution information
        
        Raises:
            ValueError: If command is invalid or unsafe
        """
        # Validate inputs (never trust user input)
        if not self._validate_command(command):
            raise ValueError(f"Invalid or unsafe command: {command}")
        
        # Check if command is already running
        if self.is_running(command):
            raise ValueError(f"Command '{command}' is already running")
        
        # Verify make target exists
        if not self._verify_makefile_target(command):
            raise ValueError(f"Make target '{command}' not found in Makefile")
        
        # Use timeout override if provided and valid
        timeout = timeout_override if (
            timeout_override is not None and 
            isinstance(timeout_override, int) and 
            timeout_override > 0
        ) else self.timeout
        
        start_time = time.time()
        timestamp = datetime.now()
        output_lines = []
        error_lines = []
        warnings = []
        timeout_occurred = False
        verification_passed = False
        
        # Initialize result with failure state (assume failure until proven otherwise)
        result = ZeroTrustExecutionResult(
            command=command,
            exit_code=None,
            output="",
            error_output="",
            duration=0.0,
            timestamp=timestamp,
            success=False,
            timeout_occurred=False,
            verification_passed=False,
            warnings=[]
        )
        
        # Mark command as running
        with self._lock:
            self._running_commands[command] = CommandState(
                command=command,
                running=True,
                pid=None,
                started_at=timestamp,
                process=None
            )
        
        try:
            # Execute make command with explicit arguments
            process = subprocess.Popen(
                ['make', command],
                cwd=str(self.ahab_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True,
                # Security: Don't use shell=True
                shell=False
            )
            
            # Update process info
            with self._lock:
                if command in self._running_commands:
                    self._running_commands[command].pid = process.pid
                    self._running_commands[command].process = process
            
            # Set up timeout handling
            def timeout_handler():
                time.sleep(timeout)
                if process.poll() is None:  # Still running
                    try:
                        process.terminate()
                        time.sleep(5)  # Give it time to terminate gracefully
                        if process.poll() is None:
                            process.kill()  # Force kill if necessary
                    except Exception as e:
                        logger.error(f"Failed to terminate process: {e}")
            
            timeout_thread = threading.Thread(target=timeout_handler, daemon=True)
            timeout_thread.start()
            
            # Stream output line by line
            stdout_lines = []
            stderr_lines = []
            
            # Read stdout
            if process.stdout:
                for line in iter(process.stdout.readline, ''):
                    if not line:
                        break
                    stdout_lines.append(line)
                    output_lines.append(line)
                    if callback:
                        try:
                            callback(line.rstrip('\n'))
                        except Exception as e:
                            logger.warning(f"Callback failed: {e}")
                            warnings.append(f"Callback failed: {e}")
            
            # Wait for process to complete
            try:
                process.wait()
                exit_code = process.returncode
            except Exception as e:
                logger.error(f"Process wait failed: {e}")
                exit_code = None
                warnings.append(f"Process wait failed: {e}")
            
            # Read stderr if available
            if process.stderr:
                try:
                    stderr_content = process.stderr.read()
                    if stderr_content:
                        stderr_lines.append(stderr_content)
                        error_lines.append(stderr_content)
                except Exception as e:
                    logger.warning(f"Failed to read stderr: {e}")
                    warnings.append(f"Failed to read stderr: {e}")
            
            # Check if timeout occurred
            if exit_code is None or exit_code == -15 or exit_code == -9:
                timeout_occurred = True
                warnings.append("Command may have been terminated due to timeout")
            
        except subprocess.TimeoutExpired:
            timeout_occurred = True
            exit_code = 124  # Standard timeout exit code
            warnings.append("Command timed out")
            
            # Kill the process
            try:
                process.kill()
                process.wait()
            except Exception as e:
                logger.error(f"Failed to kill timed out process: {e}")
                warnings.append(f"Failed to kill timed out process: {e}")
                
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            exit_code = 1
            warnings.append(f"Execution error: {e}")
            
        finally:
            # Mark command as no longer running
            with self._lock:
                if command in self._running_commands:
                    del self._running_commands[command]
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Combine output
        output = ''.join(output_lines)
        error_output = ''.join(error_lines)
        
        # Determine success (be conservative)
        success = (
            exit_code is not None and 
            exit_code == 0 and 
            not timeout_occurred
        )
        
        # Verify output if pattern provided
        if verify_output and success:
            try:
                if re.search(verify_output, output, re.IGNORECASE | re.MULTILINE):
                    verification_passed = True
                else:
                    verification_passed = False
                    warnings.append(f"Output verification failed: pattern '{verify_output}' not found")
            except Exception as e:
                verification_passed = False
                warnings.append(f"Output verification error: {e}")
        else:
            # No verification requested or command failed
            verification_passed = success
        
        # Create final result
        result = ZeroTrustExecutionResult(
            command=command,
            exit_code=exit_code,
            output=output,
            error_output=error_output,
            duration=duration,
            timestamp=timestamp,
            success=success,
            timeout_occurred=timeout_occurred,
            verification_passed=verification_passed,
            warnings=warnings
        )
        
        # Record execution for audit trail
        self._record_execution(command, result)
        
        logger.info(f"Command '{command}' completed: success={success}, "
                   f"exit_code={exit_code}, duration={duration:.2f}s")
        
        return result
    
    def is_running(self, command: str) -> bool:
        """Check if a command is currently running.
        
        Args:
            command: The make target to check
        
        Returns:
            True if command is running, False otherwise
        """
        with self._lock:
            if command not in self._running_commands:
                return False
            
            state = self._running_commands[command]
            
            # Verify the process is actually running
            if not state.is_actually_running():
                # Clean up stale state
                del self._running_commands[command]
                return False
            
            return True
    
    def get_running_commands(self) -> List[str]:
        """Get list of currently running commands.
        
        Returns:
            List of command names that are currently running
        """
        with self._lock:
            # Verify each command is actually running
            actually_running = []
            to_remove = []
            
            for command, state in self._running_commands.items():
                if state.is_actually_running():
                    actually_running.append(command)
                else:
                    to_remove.append(command)
            
            # Clean up stale states
            for command in to_remove:
                del self._running_commands[command]
            
            return actually_running
    
    def kill(self, command: str) -> bool:
        """Kill a running command.
        
        Args:
            command: The make target to kill
        
        Returns:
            True if command was killed, False if not running or kill failed
        """
        with self._lock:
            if command not in self._running_commands:
                return False
            
            state = self._running_commands[command]
            
            if not state.process:
                # Clean up invalid state
                del self._running_commands[command]
                return False
            
            try:
                # Try graceful termination first
                state.process.terminate()
                
                # Wait a bit for graceful shutdown
                try:
                    state.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful termination failed
                    state.process.kill()
                    state.process.wait()
                
                # Clean up state
                del self._running_commands[command]
                
                logger.info(f"Successfully killed command: {command}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to kill command '{command}': {e}")
                # Clean up state anyway
                if command in self._running_commands:
                    del self._running_commands[command]
                return False
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history for debugging and audit.
        
        Returns:
            List of execution records
        """
        return self._execution_history.copy()
    
    def verify_system_health(self) -> Dict[str, Any]:
        """Verify the executor system is healthy.
        
        Returns:
            Dictionary with health check results
        """
        health = {
            'ahab_path_accessible': self._verify_path_accessible(self.ahab_path),
            'makefile_accessible': self._verify_file_accessible(self.ahab_path / 'Makefile'),
            'running_commands_count': len(self.get_running_commands()),
            'execution_history_count': len(self._execution_history),
            'timestamp': datetime.now().isoformat()
        }
        
        # Check for stale processes
        stale_processes = 0
        with self._lock:
            for state in self._running_commands.values():
                if not state.is_actually_running():
                    stale_processes += 1
        
        health['stale_processes'] = stale_processes
        health['healthy'] = (
            health['ahab_path_accessible'] and
            health['makefile_accessible'] and
            stale_processes == 0
        )
        
        return health


def get_system_status(ahab_path: str) -> Dict[str, Any]:
    """Get current system status using zero trust principles.
    
    Args:
        ahab_path: Path to the ahab directory
    
    Returns:
        Dictionary with system status information
    """
    # Validate input
    if not ahab_path or not isinstance(ahab_path, str):
        return {
            'error': 'Invalid ahab_path provided',
            'workstation_installed': False,
            'workstation_running': False,
            'services': [],
            'last_updated': datetime.now().isoformat()
        }
    
    ahab_path_obj = Path(ahab_path)
    
    # Initialize status with safe defaults (assume nothing works)
    status = {
        'workstation_installed': False,
        'workstation_running': False,
        'services': [],
        'last_updated': datetime.now().isoformat(),
        'errors': [],
        'warnings': []
    }
    
    try:
        # Create executor to run make status
        executor = ZeroTrustCommandExecutor(str(ahab_path_obj), timeout=30)
        
        # Execute make status command
        result = executor.execute('status', verify_output='Status Check Complete')
        
        if result.is_completely_successful():
            # Parse output to determine status
            output = result.output
            
            # Check workstation status
            if '✓ Workstation: Running' in output:
                status['workstation_installed'] = True
                status['workstation_running'] = True
            elif '⚠ Workstation: Stopped' in output:
                status['workstation_installed'] = True
                status['workstation_running'] = False
            elif '○ Workstation: Not Created' in output:
                status['workstation_installed'] = False
                status['workstation_running'] = False
            else:
                status['warnings'].append('Could not determine workstation status from output')
            
            # Parse services (look for docker container info)
            services = []
            lines = output.split('\n')
            for line in lines:
                if 'ahab_' in line and 'Up' in line:
                    # Extract service name from docker container name
                    parts = line.split()
                    if len(parts) >= 2:
                        container_name = parts[0]
                        if container_name.startswith('ahab_'):
                            service_name = container_name.replace('ahab_', '')
                            services.append({
                                'name': service_name,
                                'status': 'running',
                                'container': container_name
                            })
            
            status['services'] = services
            
        else:
            # Command failed - use fallback detection
            status['errors'].append(f'make status failed: exit_code={result.exit_code}')
            
            # Fallback: check if .vagrant directory exists
            vagrant_dir = ahab_path_obj / '.vagrant'
            if vagrant_dir.exists():
                status['workstation_installed'] = True
                status['warnings'].append('Workstation status detected via .vagrant directory (fallback)')
            
        # Add any warnings from the execution
        if result.warnings:
            status['warnings'].extend(result.warnings)
            
    except Exception as e:
        logger.error(f"System status check failed: {e}")
        status['errors'].append(f'System status check failed: {e}')
        
        # Ultimate fallback: check filesystem
        try:
            vagrant_dir = ahab_path_obj / '.vagrant'
            if vagrant_dir.exists():
                status['workstation_installed'] = True
                status['warnings'].append('Workstation detected via filesystem check (ultimate fallback)')
        except Exception as fallback_error:
            status['errors'].append(f'Fallback check failed: {fallback_error}')
    
    return status