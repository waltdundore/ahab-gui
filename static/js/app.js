/**
 * Ahab GUI - Frontend Application
 * 
 * Handles WebSocket communication, UI updates, and user interactions.
 */

const app = {
    socket: null,
    currentCommand: null,
    
    /**
     * Initialize the application
     */
    init() {
        console.log('Initializing Ahab GUI...');
        this.connectWebSocket();
        this.updateStatus();
        
        // Update status every 5 seconds
        setInterval(() => this.updateStatus(), 5000);
    },
    
    /**
     * Connect to WebSocket server
     */
    connectWebSocket() {
        this.socket = io();
        
        this.socket.on('connected', (data) => {
            console.log('Connected to server:', data.message);
            this.showToast('Connected to Ahab GUI', 'success');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.showToast('Disconnected from server', 'warning');
        });
        
        this.socket.on('command_started', (data) => {
            console.log('Command started:', data.command);
            this.currentCommand = data.command;
            this.showOutput();
            this.showLoading(true);
            this.appendOutput(`\n=== Executing: make ${data.command} ===\n`);
        });
        
        this.socket.on('output', (data) => {
            this.appendOutput(data.line);
        });
        
        this.socket.on('command_complete', (data) => {
            console.log('Command complete:', data);
            this.currentCommand = null;
            this.showLoading(false);
            
            const status = data.success ? '✓ SUCCESS' : '✗ FAILED';
            const duration = data.duration.toFixed(2);
            
            this.appendOutput(`\n=== ${status} (${duration}s) ===\n`);
            
            document.getElementById('command-status').textContent = status;
            document.getElementById('command-duration').textContent = `Duration: ${duration}s`;
            document.getElementById('output-footer').style.display = 'flex';
            
            if (data.success) {
                this.showToast('Command completed successfully', 'success');
            } else {
                this.showToast('Command failed', 'error');
            }
            
            // Update status after command completes
            setTimeout(() => this.updateStatus(), 1000);
        });
        
        this.socket.on('error', (data) => {
            console.error('Error:', data.message);
            this.showToast(data.message, 'error');
            this.showLoading(false);
        });
        
        this.socket.on('status_update', (data) => {
            this.updateStatusDisplay(data);
        });
    },
    
    /**
     * Update system status
     */
    updateStatus() {
        fetch('/api/status')
            .then(response => response.json())
            .then(data => this.updateStatusDisplay(data))
            .catch(error => console.error('Failed to fetch status:', error));
    },
    
    /**
     * Update status display
     */
    updateStatusDisplay(status) {
        // Update workstation status
        const workstationStatus = document.getElementById('workstation-status');
        if (status.workstation_running) {
            workstationStatus.textContent = 'Running';
            workstationStatus.className = 'status-badge status-running';
        } else if (status.workstation_installed) {
            workstationStatus.textContent = 'Stopped';
            workstationStatus.className = 'status-badge status-stopped';
        } else {
            workstationStatus.textContent = 'Not Installed';
            workstationStatus.className = 'status-badge status-unknown';
        }
        
        // Update services count
        const servicesCount = document.getElementById('services-count');
        servicesCount.textContent = `${status.services.length} deployed`;
        
        // Show/hide sections based on status (progressive disclosure)
        this.updateVisibility(status);
    },
    
    /**
     * Update section visibility based on system status
     */
    updateVisibility(status) {
        const installCard = document.getElementById('install-card');
        const servicesCard = document.getElementById('services-card');
        const managementCard = document.getElementById('management-card');
        
        if (!status.workstation_installed) {
            // Show only install option
            installCard.style.display = 'block';
            servicesCard.style.display = 'none';
            managementCard.style.display = 'none';
        } else if (status.workstation_running) {
            // Show services and management
            installCard.style.display = 'none';
            servicesCard.style.display = 'block';
            managementCard.style.display = 'block';
        } else {
            // Workstation installed but not running
            installCard.style.display = 'none';
            servicesCard.style.display = 'none';
            managementCard.style.display = 'block';
        }
    },
    
    /**
     * Execute a make command
     */
    executeCommand(command) {
        if (this.currentCommand) {
            this.showToast('A command is already running', 'warning');
            return;
        }
        
        // Confirm destructive actions
        if (command === 'clean') {
            if (!confirm('This will destroy the workstation VM. Are you sure?')) {
                return;
            }
        }
        
        console.log('Executing command:', command);
        this.socket.emit('execute', { command: command });
    },
    
    /**
     * Deploy a service
     */
    deployService(service) {
        if (this.currentCommand) {
            this.showToast('A command is already running', 'warning');
            return;
        }
        
        if (confirm(`Deploy ${service}? This will install and configure the service.`)) {
            this.executeCommand(`install ${service}`);
        }
    },
    
    /**
     * Show command output section
     */
    showOutput() {
        document.getElementById('output-section').style.display = 'block';
        document.getElementById('output-footer').style.display = 'none';
    },
    
    /**
     * Append output to terminal
     */
    appendOutput(text) {
        const output = document.getElementById('terminal-output');
        const line = document.createElement('div');
        line.className = 'terminal-line';
        line.textContent = text;
        output.appendChild(line);
        
        // Auto-scroll to bottom
        const terminal = document.getElementById('terminal');
        terminal.scrollTop = terminal.scrollHeight;
    },
    
    /**
     * Clear terminal output
     */
    clearOutput() {
        document.getElementById('terminal-output').innerHTML = '';
        document.getElementById('output-footer').style.display = 'none';
    },
    
    /**
     * Show/hide loading overlay
     */
    showLoading(show) {
        document.getElementById('loading-overlay').style.display = show ? 'flex' : 'none';
    },
    
    /**
     * Show toast notification
     */
    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        // Remove after 5 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
};

// Make app globally available
window.app = app;
