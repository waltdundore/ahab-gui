"""Command executor for running make commands and streaming output.

This module provides the CommandExecutor class which:
- Executes make commands via subprocess
- Captures stdout/stderr in real-time
- Preserves ANSI color codes
- Tracks command state (running/stopped)
- Handles timeouts
- Prevents concurrent execution of the same command
"""

import subprocess
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Dict
import re


@dataclass
class ExecutionResult:
    """Result of a command execution."""
    command: str
    exit_code: int
    output: str
    duration: float
    timestamp: datetime
    success: bool


@dataclass
class CommandState:
    """State of a running command."""
    command: str
    running: bool
    pid: Optional[int]
    started_at: Optional[datetime]
    process: Optional[subprocess.Popen]


class CommandExecutor:
    """Executes make commands and streams output."""
    
    def __init__(self, ahab_path: str, timeout: int = 3600):
        """Initialize the command executor.
        
        Args:
            ahab_path: Path to the ahab directory containing Makefile
            timeout: Default timeout for commands in seconds
        """
        self.ahab_path = Path(ahab_path)
        self.timeout = timeout
        self._running_commands: Dict[str, CommandState] = {}
        self._lock = threading.Lock()
        
        # Validate ahab path
        if not self.ahab_path.exists():
            raise ValueError(f"Ahab path does not exist: {ahab_path}")
        
        makefile = self.ahab_path / 'Makefile'
        if not makefile.exists():
            raise ValueError(f"Makefile not found in: {ahab_path}")
    
    def execute(self, command: str, callback: Optional[Callable[[str], None]] = None) -> ExecutionResult:
        """Execute a make command and optionally stream output.
        
        Args:
            command: The make target to execute (e.g., 'install', 'test')
            callback: Optional callback function for streaming output line-by-line
        
        Returns:
            ExecutionResult with command results
        
        Raises:
            ValueError: If command is already running
            subprocess.TimeoutExpired: If command exceeds timeout
        """
        # Check if command is already running
        if self.is_running(command):
            raise ValueError(f"Command '{command}' is already running")
        
        start_time = time.time()
        timestamp = datetime.now()
        output_lines = []
        
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
            # Execute make command
            process = subprocess.Popen(
                ['make', command],
                cwd=str(self.ahab_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )
            
            # Update process info
            with self._lock:
                if command in self._running_commands:
                    self._running_commands[command].pid = process.pid
                    self._running_commands[command].process = process
            
            # Stream output line by line
            for line in process.stdout:
                output_lines.append(line)
                if callback:
                    callback(line.rstrip('\n'))
            
            # Wait for process to complete
            process.wait(timeout=self.timeout)
            exit_code = process.returncode
            
        except subprocess.TimeoutExpired:
            # Kill the process if it times out
            if process:
                process.kill()
                process.wait()
            raise
        
        finally:
            # Mark command as no longer running
            with self._lock:
                if command in self._running_commands:
                    del self._running_commands[command]
        
        duration = time.time() - start_time
        output = ''.join(output_lines)
        
        return ExecutionResult(
            command=command,
            exit_code=exit_code,
            output=output,
            duration=duration,
            timestamp=timestamp,
            success=(exit_code == 0)
        )
    
    def is_running(self, command: str) -> bool:
        """Check if a command is currently running.
        
        Args:
            command: The make target to check
        
        Returns:
            True if command is running, False otherwise
        """
        with self._lock:
            return command in self._running_commands and self._running_commands[command].running
    
    def get_running_commands(self) -> list:
        """Get list of currently running commands.
        
        Returns:
            List of command names that are currently running
        """
        with self._lock:
            return list(self._running_commands.keys())
    
    def kill(self, command: str) -> bool:
        """Kill a running command.
        
        Args:
            command: The make target to kill
        
        Returns:
            True if command was killed, False if not running
        """
        with self._lock:
            if command not in self._running_commands:
                return False
            
            state = self._running_commands[command]
            if state.process:
                try:
                    state.process.kill()
                    state.process.wait()
                    return True
                except Exception:
                    return False
            
            return False
    
    @staticmethod
    def preserve_ansi_codes(text: str) -> str:
        """Preserve ANSI color codes in text for web display.
        
        Args:
            text: Text potentially containing ANSI codes
        
        Returns:
            Text with ANSI codes preserved
        """
        # ANSI codes are already in the text, just return as-is
        # The frontend will handle rendering them
        return text
    
    @staticmethod
    def strip_ansi_codes(text: str) -> str:
        """Strip ANSI color codes from text.
        
        Args:
            text: Text potentially containing ANSI codes
        
        Returns:
            Text with ANSI codes removed
        """
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)


def get_system_status(ahab_path: str) -> dict:
    """Get current system status by checking Vagrant and services.
    
    Args:
        ahab_path: Path to the ahab directory
    
    Returns:
        Dictionary with system status information
    """
    ahab_path = Path(ahab_path)
    
    # Check if workstation is installed (Vagrant directory exists)
    vagrant_dir = ahab_path / '.vagrant'
    workstation_installed = vagrant_dir.exists()
    
    # Check if workstation is running
    workstation_running = False
    if workstation_installed:
        try:
            result = subprocess.run(
                ['vagrant', 'status'],
                cwd=str(ahab_path),
                capture_output=True,
                text=True,
                timeout=10
            )
            workstation_running = 'running' in result.stdout.lower()
        except Exception:
            pass
    
    return {
        'workstation_installed': workstation_installed,
        'workstation_running': workstation_running,
        'services': [],  # Will be populated by service discovery
        'last_updated': datetime.now().isoformat()
    }
