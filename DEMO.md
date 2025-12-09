# Ahab GUI Demo

## Quick Demo

### 1. Start the Application

```bash
./start.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 2. Open Your Browser

Navigate to: `http://localhost:5000`

### 3. What You'll See

#### Initial State (No Workstation)
- Clean, simple interface
- Single "Install Workstation" button
- System status showing "Not Installed"

#### After Installation
- Service deployment cards (Apache, MySQL, PHP)
- Management buttons (Verify, Test, Clean)
- Real-time command output terminal

#### During Command Execution
- Loading overlay
- Real-time streaming output
- ANSI color codes preserved
- Progress indicators

## Features Demonstrated

### Progressive Disclosure
The interface shows only what you need:
- **No workstation?** → See only install button
- **Workstation ready?** → See service options
- **Services deployed?** → See management tools

### Real-Time Streaming
Watch commands execute in real-time:
- Live output streaming via WebSocket
- ANSI colors preserved
- Auto-scrolling terminal
- Success/failure indicators

### Beginner-Friendly
Designed for non-technical users:
- Plain language explanations
- Confirmation dialogs for destructive actions
- Clear error messages
- Next-step suggestions

### Responsive Design
Works on all devices:
- Desktop (full layout)
- Tablet (adapted layout)
- Mobile (touch-friendly)

## Example Workflows

### Workflow 1: Install Workstation

1. Click "Install Workstation"
2. Watch real-time output
3. See success message
4. Service cards appear automatically

### Workflow 2: Deploy Apache

1. Click "Deploy Apache" in service card
2. Confirm deployment
3. Watch installation progress
4. See success notification

### Workflow 3: Run Tests

1. Click "Run Tests" button
2. Watch test execution
3. See pass/fail results
4. Review any failures

## Technical Details

### WebSocket Communication
- Real-time bidirectional communication
- Automatic reconnection
- Session management
- Multiple client support

### Command Execution
- Executes actual `make` commands
- Captures stdout/stderr
- Preserves ANSI codes
- Handles timeouts
- Prevents concurrent execution

### Security
- Command whitelist
- Input validation
- CSRF protection
- Optional authentication

## Customization

### Configuration (.env)
```bash
WUI_PORT=5000              # Change port
WUI_HOST=127.0.0.1         # Bind to specific IP
AHAB_PATH=../ahab          # Path to Ahab
COMMAND_TIMEOUT=3600       # Command timeout (seconds)
```

### Adding Services
Edit `templates/index.html` to add service cards:

```html
<div class="service-card">
    <h3>PostgreSQL</h3>
    <p>Database server for applications</p>
    <button class="btn btn-secondary" onclick="app.deployService('postgresql')">
        Deploy PostgreSQL
    </button>
</div>
```

### Styling
Edit `static/css/style.css` to customize appearance:
- Colors (CSS variables in `:root`)
- Layout (grid, flexbox)
- Typography
- Spacing

## Troubleshooting

### Port Already in Use
```bash
# Change port in .env
WUI_PORT=5001
```

### Ahab Not Found
```bash
# Update path in .env
AHAB_PATH=/path/to/ahab
```

### WebSocket Connection Failed
- Check firewall settings
- Ensure port is accessible
- Try different browser

## Next Steps

1. **Try it yourself**: `./start.sh`
2. **Customize it**: Edit templates and styles
3. **Contribute**: See CONTRIBUTING.md
4. **Report issues**: GitHub Issues

---

*For more information, see README.md*
