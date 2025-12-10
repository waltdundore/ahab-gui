# Running Ahab GUI

## Quick Start

```bash
# From ahab directory (recommended)
cd ahab
make ui

# Or from ahab-gui directory
cd ahab-gui
make run
```

The GUI now runs in the background - no need to keep a terminal open!

## Managing the GUI

### Start the GUI
```bash
make run
```

**What happens:**
- GUI starts in a Docker container (background mode)
- Runs on http://localhost:5001
- You get your terminal back immediately
- Container is named `ahab-gui` for easy management

### Check Status
```bash
make status
```

Shows if the GUI is running and provides the URL.

### View Logs
```bash
make logs
```

Shows real-time logs from the GUI. Press Ctrl+C to exit (GUI keeps running).

### Stop the GUI
```bash
make stop
```

Stops and removes the GUI container.

### Verify It's Working
```bash
make verify
```

Runs automated checks to ensure the GUI is responding correctly.

## Workflow Examples

### Development Workflow
```bash
# Start GUI
make run

# Open browser to http://localhost:5001
# Make changes to code

# Restart to see changes
make stop
make run

# Check logs if something's wrong
make logs
```

### Testing Workflow
```bash
# Run tests (doesn't require GUI to be running)
make test

# Start GUI for manual testing
make run

# Verify it works
make verify

# Stop when done
make stop
```

### Demo Workflow
```bash
# Start demo (includes validation + GUI startup)
make demo

# Follow instructions in browser
# Stop when done
make stop
```

## Troubleshooting

### GUI Won't Start

**Check Docker is running:**
```bash
docker info
```

If not running, start Docker Desktop.

**Check if port 5001 is in use:**
```bash
lsof -i :5001
```

If something else is using port 5001, stop it first.

**Check for existing container:**
```bash
docker ps -a | grep ahab-gui
```

If found, remove it:
```bash
make stop
```

### GUI Not Responding

**Check if container is running:**
```bash
make status
```

**Check logs for errors:**
```bash
make logs
```

**Restart the GUI:**
```bash
make stop
make run
```

### Can't Access http://localhost:5001

**Verify GUI is running:**
```bash
make status
```

**Check port mapping:**
```bash
docker ps | grep ahab-gui
```

Should show: `0.0.0.0:5001->5001/tcp`

**Try explicit IP:**
```bash
# Instead of localhost, try:
http://127.0.0.1:5001
```

## Technical Details

### Container Configuration

The GUI runs in a Docker container with:
- **Image**: `python:3.11-slim`
- **Name**: `ahab-gui`
- **Port**: 5001 (host) → 5001 (container)
- **Volumes**:
  - `ahab-gui/` → `/workspace` (read-write, for GUI code)
  - `ahab/` → `/ahab` (read-only, for executing commands)
- **Mode**: Detached (background)

### Why Background Mode?

**Before (interactive mode):**
- ❌ Terminal blocked - can't use it
- ❌ Must Ctrl+C to exit
- ❌ Confusing for users
- ❌ Not documented

**After (background mode):**
- ✅ Terminal free - keep working
- ✅ Explicit stop command
- ✅ Clear workflow
- ✅ Well documented

### Security

The GUI container:
- Runs as non-root user (Python image default)
- Has read-only access to ahab code
- Can only execute whitelisted make commands
- Isolated from host system

See [SECURITY.md](SECURITY.md) for complete security documentation.

## Related Documentation

- [BRANDING.md](BRANDING.md) - Brand guidelines
- [SECURITY.md](SECURITY.md) - Security model
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed troubleshooting
- [PROGRESSIVE_DISCLOSURE_DEMO.md](PROGRESSIVE_DISCLOSURE_DEMO.md) - UX demo guide

---

**Last Updated**: December 9, 2025
