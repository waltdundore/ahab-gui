# Ahab GUI

**Simple web interface for Ahab infrastructure automation**

A beginner-friendly graphical interface that makes infrastructure automation accessible to everyone. No command-line knowledge required.

## What This Does

Ahab GUI provides a web-based interface for managing Ahab infrastructure:

- **Install workstations** with a single click
- **Deploy services** (Apache, MySQL, etc.) through simple menus
- **Monitor status** with real-time updates
- **Run tests** and see results instantly
- **Stream command output** in real-time

## Quick Start

```bash
# From the ahab directory
make ui

# Open browser to http://localhost:5000
```

## Architecture

```
┌─────────────────┐
│   Web Browser   │
│  (User Client)  │
└────────┬────────┘
         │ HTTP/WebSocket
         ▼
┌─────────────────┐
│  Flask Server   │
│  (Python)       │
└────────┬────────┘
         │ subprocess
         ▼
┌─────────────────┐
│  Make Commands  │
│  (Makefile)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Ahab Platform   │
│ (Ansible/Docker)│
└─────────────────┘
```

## Features

### Progressive Disclosure
Shows only what you need, when you need it:
- No workstation? See only "Install" button
- Workstation ready? See service deployment options
- Service deployed? See management options

### Real-Time Streaming
Watch commands execute in real-time:
- Live output streaming
- ANSI color preservation
- Progress indicators
- Clear success/error messages

### Beginner-Friendly
Designed for non-technical users:
- Plain language explanations
- Confirmation dialogs
- Helpful error messages
- Next-step suggestions

## Technology Stack

**Backend:**
- Flask (Python web framework)
- Flask-SocketIO (WebSocket support)
- subprocess (Execute make commands)

**Frontend:**
- Vanilla JavaScript (no framework dependencies)
- CSS Grid/Flexbox (responsive layout)
- Socket.IO client (real-time communication)

## Repository Structure

```
ahab-gui/
├── app.py                 # Flask application entry point
├── requirements.txt       # Python dependencies
├── config.py             # Configuration management
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   ├── js/
│   │   └── app.js        # Frontend JavaScript
│   └── images/
│       └── logo.png      # Ahab logo
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Main dashboard
│   └── components/       # Reusable UI components
├── commands/
│   └── executor.py       # Make command execution wrapper
├── tests/
│   └── test_app.py       # Application tests
└── README.md
```

## Configuration

Configuration is read from `ahab.conf`:

```bash
# Web UI Configuration
WUI_PORT=5000
WUI_HOST=127.0.0.1
WUI_ENABLE_AUTH=false
WUI_USERNAME=admin
WUI_PASSWORD=changeme
```

## Development

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Open browser to http://localhost:5000
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_app.py
```

## Design Principles

### 1. Progressive Disclosure
Show users only what they need at each step. Hide complexity until needed.

### 2. Real-Time Feedback
Stream command output in real-time. Users always know what's happening.

### 3. Plain Language
No jargon. Clear explanations. Helpful error messages.

### 4. Same Commands as CLI
Execute the exact same `make` commands as the CLI. No separate code paths.

### 5. Responsive Design
Works on desktop, tablet, and mobile. Touch-friendly interface.

## Security

- Command whitelist (only allowed make targets)
- CSRF protection
- Input validation
- Rate limiting
- Secure headers

## License

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

- **Free for schools, non-profits, and educational institutions**
- **For-profit entities**: Contact us to negotiate commercial terms

## Support

- **GitHub**: https://github.com/waltdundore/ahab-gui
- **Issues**: https://github.com/waltdundore/ahab-gui/issues
- **Main Project**: https://github.com/waltdundore/ahab

---

*Part of the Ahab infrastructure automation project*
