/**
 * Ahab GUI - Progressive Disclosure Implementation
 * 
 * Like an elevator: only show what's relevant to the current context.
 * 
 * Navigation Structure:
 * - Main Nav (Roadmap): WHERE can I go? (Home, Workstation, Services, Help)
 * - Page Actions: WHAT can I do HERE? (Context-specific buttons)
 * - Breadcrumbs: WHERE am I? (Visual context indicator)
 */

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
let socket = null;
let commandRunning = false;
let currentState = null;
let currentView = 'home'; // home, workstation, services, service-detail, help

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    try {
        connectWebSocket();
        console.log('WebSocket connected');
        loadStatus();
        console.log('Loading status...');
    } catch (error) {
        console.error('Initialization error:', error);
        showErrorState();
    }
});

/**
 * Connect to WebSocket for real-time command output
 */
function connectWebSocket() {
    socket = io();
    
    socket.on('connect', () => console.log('Connected to server'));
    socket.on('disconnect', () => showOutput('Connection lost. Reconnecting...', 'error'));
    
    socket.on('output', (data) => showOutput(data.line));
    
    socket.on('complete', (data) => {
        commandRunning = false;
        if (data.success) {
            showOutput('\n✅ Command completed successfully!', 'success');
            announceToScreenReader('Command completed successfully');
        } else {
            showOutput('\n❌ Command failed', 'error');
            announceToScreenReader('Command failed');
        }
        setTimeout(() => loadStatus(), 1000);
    });
    
    socket.on('error', (data) => {
        commandRunning = false;
        showOutput(`\n❌ Error: ${data.message}`, 'error');
        announceToScreenReader(`Error: ${data.message}`);
        setTimeout(() => loadStatus(), 1000);
    });
}

/**
 * Load system status and update UI
 */
function loadStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(status => {
            currentState = status;
            updateNavigation();
            renderCurrentView();
        })
        .catch(error => {
            console.error('Status error:', error);
            showErrorState();
        });
}

/**
 * Update main navigation based on system state
 * This is the "roadmap" - shows WHERE you can go
 */
function updateNavigation() {
    const nav = document.getElementById('main-nav');
    
    // Always show Home
    let navItems = [
        {id: 'home', label: 'Home', icon: '🏠'}
    ];
    
    // Show Workstation if it exists
    if (currentState.workstation_installed) {
        navItems.push({id: 'workstation', label: 'Workstation', icon: '🖥️'});
    }
    
    // Show Services if workstation exists
    if (currentState.workstation_installed) {
        navItems.push({id: 'services', label: 'Services', icon: '📦'});
    }
    
    // Always show Help
    navItems.push({id: 'help', label: 'Help', icon: '❓'});
    
    // Render navigation
    nav.innerHTML = navItems.map((item, index) => {
        const active = currentView === item.id ? 'active' : '';
        const separator = index < navItems.length - 1 ? '<span class="nav-separator">|</span>' : '';
        return `
            <a href="#" class="nav-link ${active}" onclick="navigateTo('${item.id}'); return false;">
                ${item.icon} ${item.label}
            </a>
            ${separator}
        `;
    }).join('');
}

/**
 * Navigate to a different view
 */
function navigateTo(view) {
    currentView = view;
    updateNavigation();
    renderCurrentView();
}

/**
 * Render the current view based on state and context
 */
function renderCurrentView() {
    // Don't change view if command is running
    if (commandRunning) {
        return;
    }
    
    // For home view, render directly on the page
    if (currentView === 'home') {
        renderHomeView();
        return;
    }
    
    // For other views, navigate to their routes
    switch(currentView) {
        case 'workstation':
            window.location.href = '/workstation';
            break;
        case 'services':
            window.location.href = '/services';
            break;
        case 'help':
            window.location.href = '/help';
            break;
        default:
            renderHomeView();
    }
}

/**
 * HOME VIEW
 * Shows: Quick status overview and next recommended action
 * Uses: Action Card components with progressive disclosure
 */
function renderHomeView() {
    // Update status cards
    updateStatusCards();
    
    // Render action cards based on system state
    const container = document.getElementById('action-cards-container');
    
    // State 1: No workstation - Show only install workstation card
    if (!currentState.workstation_installed) {
        container.innerHTML = renderActionCard({
            title: 'Install Workstation',
            description: 'Set up a Fedora 43 virtual machine with Docker and Ansible',
            icon: 'server',
            benefits: [
                'Takes 5-10 minutes',
                'Fully automated setup',
                'Ready for service deployment',
                'Includes security hardening'
            ],
            action_label: 'Install Workstation',
            action_onclick: 'installWorkstation()',
            card_style: 'primary'
        });
        return;
    }
    
    // State 2: Workstation exists - Show context-aware actions
    const services = currentState.services;
    const installedServices = Object.keys(services).filter(s => services[s]);
    const availableServices = Object.keys(services).filter(s => !services[s]);
    const serviceCount = installedServices.length;
    
    let cards = [];
    
    // Card 1: Manage Workstation (always available when workstation exists)
    cards.push(renderActionCard({
        title: 'Manage Workstation',
        description: 'View status, run tests, or access your workstation via SSH',
        icon: 'server',
        benefits: [
            'Check system health',
            'Run automated tests',
            'SSH terminal access',
            'View detailed status'
        ],
        action_label: 'Manage Workstation',
        action_onclick: 'navigateTo("workstation")',
        card_style: 'default'
    }));
    
    // Card 2: Deploy Services (if services available) or Manage Services (if all installed)
    if (availableServices.length > 0) {
        cards.push(renderActionCard({
            title: 'Deploy Services',
            description: `Install web services on your workstation. ${availableServices.length} service${availableServices.length > 1 ? 's' : ''} available.`,
            icon: 'grid',
            benefits: [
                'Apache Web Server',
                'MySQL Database',
                'PHP Runtime',
                'Quick 2-5 minute setup'
            ],
            action_label: 'View Available Services',
            action_onclick: 'navigateTo("services")',
            card_style: 'primary'
        }));
    } else if (serviceCount > 0) {
        cards.push(renderActionCard({
            title: 'Manage Services',
            description: `All ${serviceCount} service${serviceCount > 1 ? 's are' : ' is'} installed and running.`,
            icon: 'grid',
            benefits: [
                `${serviceCount} service${serviceCount > 1 ? 's' : ''} running`,
                'View service status',
                'Access service logs',
                'Restart services'
            ],
            action_label: 'Manage Services',
            action_onclick: 'navigateTo("services")',
            card_style: 'success'
        }));
    }
    
    // Card 3: Run Tests (always available when workstation exists)
    cards.push(renderActionCard({
        title: 'Run Tests',
        description: 'Verify your workstation and services are working correctly',
        icon: 'check',
        benefits: [
            'Automated health checks',
            'Takes 1-2 minutes',
            'Detailed test results',
            'Catch issues early'
        ],
        action_label: 'Run Tests',
        action_onclick: 'runTests()',
        card_style: 'default'
    }));
    
    container.innerHTML = cards.join('');
}

/**
 * Update status cards with current system state
 */
function updateStatusCards() {
    // Workstation status
    const workstationStatus = document.getElementById('workstation-status-text');
    const workstationMeta = document.getElementById('workstation-status-meta');
    
    if (currentState.workstation_installed) {
        workstationStatus.textContent = 'Running';
        workstationStatus.className = 'status-card-value status-success';
        workstationMeta.textContent = 'Ready for service deployment';
    } else {
        workstationStatus.textContent = 'Not Installed';
        workstationStatus.className = 'status-card-value status-neutral';
        workstationMeta.textContent = 'Install to get started';
    }
    
    // Services status
    const servicesStatus = document.getElementById('services-status-text');
    const servicesMeta = document.getElementById('services-status-meta');
    const services = currentState.services;
    const installedServices = Object.keys(services).filter(s => services[s]);
    const serviceCount = installedServices.length;
    const totalServices = Object.keys(services).length;
    
    if (serviceCount === 0) {
        servicesStatus.textContent = 'None Installed';
        servicesStatus.className = 'status-card-value status-neutral';
        servicesMeta.textContent = `${totalServices} services available`;
    } else if (serviceCount === totalServices) {
        servicesStatus.textContent = `${serviceCount} Installed`;
        servicesStatus.className = 'status-card-value status-success';
        servicesMeta.textContent = 'All services running';
    } else {
        servicesStatus.textContent = `${serviceCount} of ${totalServices}`;
        servicesStatus.className = 'status-card-value status-warning';
        servicesMeta.textContent = `${totalServices - serviceCount} more available`;
    }
}

/**
 * Render an action card component
 * Validates: Requirements 1.4, 2.3, 6.2, 6.3, 8.5
 */
function renderActionCard(config) {
    const {
        title,
        description,
        icon,
        benefits = [],
        action_label,
        action_onclick,
        card_style = 'default',
        secondary_actions = [],
        help_link = null,
        help_link_text = 'Learn more'
    } = config;
    
    const benefitsList = benefits.length > 0 ? `
        <ul class="benefits-list" aria-label="Benefits">
            ${benefits.map(benefit => `
                <li class="benefit-item">
                    <i class="icon-check" aria-hidden="true">✓</i>
                    <span>${benefit}</span>
                </li>
            `).join('')}
        </ul>
    ` : '';
    
    const secondaryActionsHtml = secondary_actions.length > 0 ? `
        <div class="card-actions-secondary">
            ${secondary_actions.map(action => `
                <button class="btn btn-secondary btn-sm" onclick="${action.onclick}">
                    ${action.icon ? `<i class="icon-${action.icon}" aria-hidden="true">${action.icon}</i>` : ''}
                    ${action.label}
                </button>
            `).join('')}
        </div>
    ` : '';
    
    const helpLinkHtml = help_link ? `
        <div class="card-footer">
            <a href="${help_link}" class="help-link">
                <i class="icon-help-circle" aria-hidden="true">?</i>
                ${help_link_text}
            </a>
        </div>
    ` : '';
    
    return `
        <article class="action-card card-${card_style}" role="article">
            <div class="card-header">
                ${icon ? `<div class="card-icon" aria-hidden="true">${icon === 'server' ? '🖥️' : icon === 'grid' ? '📦' : icon === 'check' ? '✓' : icon}</div>` : ''}
                <div class="card-header-content">
                    <h3 class="card-title">${title}</h3>
                </div>
            </div>
            
            <div class="card-body">
                <p class="card-description">${description}</p>
                ${benefitsList}
            </div>
            
            <div class="card-actions">
                <button class="btn btn-primary card-action-primary" onclick="${action_onclick}">
                    ${action_label}
                    <i class="icon-arrow-right" aria-hidden="true">→</i>
                </button>
                ${secondaryActionsHtml}
            </div>
            
            ${helpLinkHtml}
        </article>
    `;
}

/**
 * WORKSTATION VIEW
 * Shows: Only workstation-specific actions based on current state
 */
function renderWorkstationView() {
    setBreadcrumb([
        {label: 'Home', link: 'home'},
        {label: 'Workstation'}
    ]);
    
    const card = document.getElementById('card-content');
    
    // State 1: No workstation - Only show install
    if (!currentState.workstation_installed) {
        setContext('No workstation installed');
        card.innerHTML = `
            <h2>🖥️ Workstation Setup</h2>
            <p class="description">Create a virtual machine to run your infrastructure services.</p>
            <p class="time-estimate">⏱️ Takes about 5-10 minutes</p>
            
            <div class="info-box">
                <h4>What gets installed:</h4>
                <ul class="feature-list">
                    <li>✓ Fedora 43 VM (default)</li>
                    <li>✓ Also supports: Debian 13, Ubuntu 24.04</li>
                    <li>✓ Docker & Docker Compose</li>
                    <li>✓ Ansible automation tools</li>
                    <li>✓ Security hardening (SELinux/AppArmor, firewall)</li>
                </ul>
            </div>
            
            <button class="btn btn-primary btn-large" onclick="installWorkstation()">
                Install Workstation
            </button>
        `;
        return;
    }
    
    // State 2: Workstation exists - Show management actions
    setContext('Workstation is running');
    card.innerHTML = `
        <h2>🖥️ Workstation Management</h2>
        <p class="description">Your workstation is ready. What would you like to do?</p>
        
        <div class="management-menu">
            <button class="btn-action" onclick="runTests()">
                <span class="action-icon">🧪</span>
                <span class="action-name">Run Tests</span>
                <span class="action-desc">Verify system health</span>
            </button>
            
            <button class="btn-action" onclick="checkStatus()">
                <span class="action-icon">📊</span>
                <span class="action-name">Check Status</span>
                <span class="action-desc">View detailed info</span>
            </button>
            
            <button class="btn-action" onclick="sshWorkstation()">
                <span class="action-icon">💻</span>
                <span class="action-name">SSH Access</span>
                <span class="action-desc">Connect to terminal</span>
            </button>
            
            <button class="btn-action btn-danger" onclick="confirmDestroy()">
                <span class="action-icon">🗑️</span>
                <span class="action-name">Destroy</span>
                <span class="action-desc">Remove workstation</span>
            </button>
        </div>
        
        <button class="btn btn-secondary btn-small" onclick="navigateTo('services')">
            Manage Services →
        </button>
    `;
}

/**
 * SERVICES VIEW
 * Shows: Only service-related actions based on what's installed
 */
function renderServicesView() {
    setBreadcrumb([
        {label: 'Home', link: 'home'},
        {label: 'Services'}
    ]);
    
    const card = document.getElementById('card-content');
    
    // Can't access services without workstation
    if (!currentState.workstation_installed) {
        setContext('Workstation required');
        card.innerHTML = `
            <h2>📦 Services</h2>
            <p class="description">You need a workstation before deploying services.</p>
            <button class="btn btn-primary" onclick="navigateTo('workstation')">
                Set Up Workstation First
            </button>
        `;
        return;
    }
    
    const services = currentState.services;
    const installedServices = Object.keys(services).filter(s => services[s]);
    const availableServices = Object.keys(services).filter(s => !services[s]);
    
    setContext(`${installedServices.length} service(s) installed`);
    
    let html = '<h2>📦 Services</h2>';
    
    // Show installed services
    if (installedServices.length > 0) {
        html += '<h3>Installed Services</h3>';
        html += '<div class="service-list">';
        installedServices.forEach(service => {
            const info = getServiceInfo(service);
            html += `
                <div class="service-card installed">
                    <span class="service-icon">${info.icon}</span>
                    <div class="service-info">
                        <div class="service-name">${info.name}</div>
                        <div class="service-desc">${info.desc}</div>
                    </div>
                    <span class="service-status">✅ Running</span>
                </div>
            `;
        });
        html += '</div>';
    }
    
    // Show available services
    if (availableServices.length > 0) {
        html += '<h3>Available to Install</h3>';
        html += '<div class="service-menu">';
        availableServices.forEach(service => {
            const info = getServiceInfo(service);
            html += `
                <button class="btn-service" onclick="deployService('${service}')">
                    <span class="service-icon">${info.icon}</span>
                    <span class="service-name">${info.name}</span>
                    <span class="service-desc">${info.desc}</span>
                </button>
            `;
        });
        html += '</div>';
    } else {
        html += '<p class="description">✅ All available services are installed!</p>';
    }
    
    card.innerHTML = html;
}

/**
 * HELP VIEW
 * Shows: Documentation and support information
 */
function renderHelpView() {
    setBreadcrumb([
        {label: 'Home', link: 'home'},
        {label: 'Help'}
    ]);
    setContext('');
    
    const card = document.getElementById('card-content');
    card.innerHTML = `
        <h2>❓ Help & Documentation</h2>
        
        <div class="help-section">
            <h3>Getting Started</h3>
            <ol class="help-list">
                <li>Install the workstation (creates a VM)</li>
                <li>Deploy services (Apache, MySQL, PHP)</li>
                <li>Run tests to verify everything works</li>
            </ol>
        </div>
        
        <div class="help-section">
            <h3>Common Tasks</h3>
            <ul class="help-list">
                <li><strong>Install Workstation:</strong> Go to Workstation → Install</li>
                <li><strong>Deploy Service:</strong> Go to Services → Choose service</li>
                <li><strong>Run Tests:</strong> Go to Workstation → Run Tests</li>
                <li><strong>SSH Access:</strong> Go to Workstation → SSH Access</li>
            </ul>
        </div>
        
        <div class="help-section">
            <h3>Need More Help?</h3>
            <p>Check the <a href="https://github.com/waltdundore/ahab" target="_blank">GitHub repository</a> for detailed documentation.</p>
        </div>
        
        <button class="btn btn-primary" onclick="navigateTo('home')">
            ← Back to Home
        </button>
    `;
}

/**
 * Helper: Get service information
 */
function getServiceInfo(service) {
    const info = {
        apache: {icon: '🌐', name: 'Apache', desc: 'Web Server'},
        mysql: {icon: '🗄️', name: 'MySQL', desc: 'Database'},
        php: {icon: '🐘', name: 'PHP', desc: 'Programming Language'}
    };
    return info[service] || {icon: '📦', name: service, desc: 'Service'};
}

/**
 * Helper: Announce to screen readers
 * Validates: Requirements 3.5 (ARIA live regions)
 */
function announceToScreenReader(message) {
    const liveRegion = document.getElementById('aria-live-region');
    if (liveRegion) {
        liveRegion.textContent = message;
        // Clear after announcement
        setTimeout(() => {
            liveRegion.textContent = '';
        }, 1000);
    }
}

/**
 * COMMAND EXECUTION
 */

function installWorkstation() {
    executeCommand('install', null, '⏳ Installing workstation...\nThis takes 5-10 minutes.\n');
}

function deployService(service) {
    const info = getServiceInfo(service);
    executeCommand('install', service, `⏳ Installing ${info.name}...\nThis takes 2-5 minutes.\n`);
}

function runTests() {
    executeCommand('test', null, '🧪 Running tests...\nThis takes 1-2 minutes.\n');
}

function checkStatus() {
    executeCommand('status', null, '📊 Checking status...\n');
}

function sshWorkstation() {
    const card = document.getElementById('card-content');
    card.innerHTML = `
        <h2>💻 SSH Access</h2>
        <p class="description">To connect to your workstation, open a terminal and run:</p>
        <div class="code-block">
            <code>cd ahab && make ssh</code>
        </div>
        <p class="description">This will connect you to the workstation's command line.</p>
        <button class="btn btn-primary" onclick="renderWorkstationView()">
            ← Back
        </button>
    `;
}

function confirmDestroy() {
    const card = document.getElementById('card-content');
    card.innerHTML = `
        <h2>⚠️ Destroy Workstation?</h2>
        <p class="description warning">This will permanently delete:</p>
        <ul class="warning-list">
            <li>Your workstation VM</li>
            <li>All installed services</li>
            <li>All data and configurations</li>
        </ul>
        <p class="description warning"><strong>This cannot be undone.</strong></p>
        <button class="btn btn-danger btn-large" onclick="destroyWorkstation()">
            Yes, Destroy Everything
        </button>
        <button class="btn btn-secondary" onclick="renderWorkstationView()">
            Cancel
        </button>
    `;
}

function destroyWorkstation() {
    executeCommand('clean', null, '🗑️ Destroying workstation...\nThis takes 1-2 minutes.\n');
}

/**
 * Execute a command via the API
 * Validates: Requirements 9.2 (Progress feedback), 9.3 (Loading states)
 */
function executeCommand(target, arg, message) {
    if (commandRunning) return;
    
    commandRunning = true;
    
    // Hide action cards, show output
    const actionCardsSection = document.getElementById('action-cards-section');
    if (actionCardsSection) {
        actionCardsSection.style.display = 'none';
    }
    
    const outputSection = document.getElementById('output-section');
    outputSection.style.display = 'block';
    
    const output = document.getElementById('command-output');
    output.innerHTML = '';
    
    // Show command and message
    const cmd = arg ? `make ${target} ${arg}` : `make ${target}`;
    showOutput(`$ ${cmd}\n`, 'prompt');
    showOutput(message, 'info');
    
    // Announce to screen readers
    announceToScreenReader(`Starting command: ${cmd}`);
    
    // Send request
    const data = {target, csrf_token: csrfToken};
    if (arg) data.arg = arg;
    
    fetch('/api/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message || 'Command failed');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) throw new Error(data.message);
    })
    .catch(error => {
        commandRunning = false;
        showOutput(`\n❌ ${error.message}`, 'error');
        announceToScreenReader(`Command failed: ${error.message}`);
        setTimeout(() => hideOutput(), 3000);
    });
}

/**
 * Show output in terminal
 */
function showOutput(text, type = 'normal') {
    const output = document.getElementById('command-output');
    const line = document.createElement('span');
    
    line.textContent = text;
    
    if (type === 'error') line.className = 'terminal-error';
    else if (type === 'success') line.className = 'terminal-success';
    else if (type === 'prompt') line.className = 'terminal-prompt';
    else if (type === 'info') line.className = 'terminal-info';
    
    output.appendChild(line);
    output.appendChild(document.createTextNode('\n'));
    output.scrollTop = output.scrollHeight;
}

/**
 * Hide output and return to current view
 * Validates: Requirements 9.4 (Success confirmation)
 */
function hideOutput() {
    document.getElementById('output-section').style.display = 'none';
    const actionCardsSection = document.getElementById('action-cards-section');
    if (actionCardsSection) {
        actionCardsSection.style.display = 'block';
    }
    announceToScreenReader('Command output hidden');
    loadStatus();
}

/**
 * Show error state
 * Validates: Requirements 9.5 (Network error recovery), 12.3 (Error messages)
 */
function showErrorState() {
    const container = document.getElementById('action-cards-container');
    if (container) {
        container.innerHTML = renderActionCard({
            title: 'Connection Error',
            description: 'Cannot connect to the Ahab backend. Make sure the server is running.',
            icon: '❌',
            benefits: [
                'Check server is running',
                'Verify network connection',
                'Try refreshing the page'
            ],
            action_label: 'Try Again',
            action_onclick: 'loadStatus()',
            card_style: 'danger'
        });
    }
    announceToScreenReader('Connection error. Cannot connect to server.');
}
