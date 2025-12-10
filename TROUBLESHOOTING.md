# Ahab GUI Troubleshooting

Quick solutions to common issues.

---

## Docker Not Running

### Error Message
```
❌ ERROR: Docker is not running
```

### Solution (macOS)

**Option 1: Open Docker Desktop from Applications**
1. Open Finder
2. Go to Applications
3. Double-click "Docker"
4. Wait for Docker to start (whale icon in menu bar)
5. Try again: `make ui`

**Option 2: Use Terminal**
```bash
# Start Docker Desktop
open -a Docker

# Wait a few seconds for it to start
sleep 5

# Verify it's running
docker info

# Now try again
cd ahab && make ui
```

**Option 3: Check if Docker is installed**
```bash
# Check if Docker is installed
which docker

# If not found, install Docker Desktop:
# https://www.docker.com/products/docker-desktop
```

---

## Port Already in Use

### Error Message
```
Error starting userland proxy: listen tcp4 0.0.0.0:5001: bind: address already in use
```

### Solution

**Find what's using port 5001:**
```bash
lsof -i :5001
```

**Kill the process:**
```bash
kill -9 <PID>
```

**Or use a different port:**
Edit `ahab-gui/Makefile` and change `5001` to another port (e.g., `5002`)

---

## Cannot Connect to Ahab

### Error Message
```
❌ ahab-gui not found
Expected location: ../ahab-gui/
```

### Solution

**Check directory structure:**
```bash
# You should be in the ahab directory
pwd
# Should show: .../ahab

# Check if ahab-gui exists
ls -la ../ahab-gui

# If not, you're in the wrong place
cd /path/to/DockMaster/ahab
make ui
```

---

## Permission Denied

### Error Message
```
docker: Got permission denied while trying to connect to the Docker daemon socket
```

### Solution (macOS)

This usually means Docker Desktop isn't running properly.

```bash
# Restart Docker Desktop
killall Docker
open -a Docker

# Wait for it to start
sleep 10

# Try again
make ui
```

---

## Module Not Found

### Error Message
```
ModuleNotFoundError: No module named 'flask'
```

### Solution

This shouldn't happen since we install dependencies in the Docker container, but if it does:

```bash
# The Makefile should handle this automatically
# But you can manually install:
cd ahab-gui
make install

# Then try again
make run
```

---

## Browser Can't Connect

### Error Message
```
This site can't be reached
localhost refused to connect
```

### Solution

**Check if the GUI is actually running:**
```bash
# In the terminal where you ran 'make ui'
# You should see:
# "Running on http://0.0.0.0:5001"

# If not, check for errors in the output
```

**Check if port 5001 is listening:**
```bash
lsof -i :5001
# Should show python process
```

**Try a different browser:**
- Chrome: http://localhost:5001
- Firefox: http://localhost:5001
- Safari: http://localhost:5001

---

## GUI Starts But Shows Errors

### Error Message
```
Connection Error
Cannot connect to the Ahab backend
```

### Solution

This is expected if you haven't implemented the backend yet. The GUI is working, but the `/api/status` endpoint returns mock data.

**For demo purposes:**
- The GUI will show the "no workstation" state
- You can click through the UI to see progressive disclosure
- Commands won't actually execute (backend not implemented yet)

---

## Docker Container Exits Immediately

### Error Message
```
❌ Failed to start GUI
```

### Solution

**Check the error output:**
Look for Python errors in the output above the failure message.

**Common causes:**
1. Syntax error in Python code
2. Missing dependency in requirements.txt
3. Port already in use

**Debug:**
```bash
# Run with more verbose output
cd ahab-gui
docker run --rm -it \
  -v $(pwd):/workspace \
  -w /workspace \
  -p 5001:5001 \
  python:3.11-slim \
  sh -c "pip install -r requirements.txt && python app.py"
```

---

## Ctrl+C Doesn't Stop the GUI

### Solution

**Force kill:**
```bash
# Find the Docker container
docker ps

# Kill it
docker kill <container-id>

# Or kill all running containers
docker kill $(docker ps -q)
```

---

## Changes Not Showing Up

### Solution

**Hard refresh in browser:**
- Chrome/Firefox: `Cmd+Shift+R` (macOS) or `Ctrl+Shift+R` (Windows/Linux)
- Safari: `Cmd+Option+R`

**Or clear cache:**
- Chrome: Settings → Privacy → Clear browsing data
- Firefox: Preferences → Privacy → Clear Data
- Safari: Develop → Empty Caches

**Restart the GUI:**
```bash
# Stop with Ctrl+C
# Start again
make ui
```

---

## Quick Diagnostic

Run this to check everything:

```bash
# Check Docker
docker info

# Check if port is free
lsof -i :5001

# Check directory structure
pwd
ls -la ../ahab-gui

# Check files exist
ls -la ahab-gui/app.py
ls -la ahab-gui/Makefile

# Try to start
cd ahab && make ui
```

---

## Still Having Issues?

1. **Check the error message carefully** - it usually tells you what's wrong
2. **Read the output** - look for Python tracebacks or Docker errors
3. **Verify Docker is running** - `docker info` should work
4. **Check you're in the right directory** - `pwd` should show `.../ahab`
5. **Try the validation script** - `cd ahab-gui && ./test-demo.sh`

---

## Getting Help

If none of these solutions work:

1. Note the exact error message
2. Note what command you ran
3. Note what directory you're in (`pwd`)
4. Check if Docker is running (`docker info`)
5. Check the GitHub issues or create a new one

---

**Most common issue**: Docker not running. Start Docker Desktop and try again!
