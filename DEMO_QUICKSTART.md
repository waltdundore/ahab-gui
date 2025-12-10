# Ahab GUI Demo - Quick Start

**Ready to test the progressive disclosure implementation!**

---

## Prerequisites

**Docker must be running!**

```bash
# Check if Docker is running
docker info

# If not, start Docker Desktop (macOS)
open -a Docker
```

---

## Quick Start (3 Steps)

### 1. Navigate to ahab directory

```bash
cd ahab
```

### 2. Start the GUI

```bash
make ui
```

This will:
- Check if Docker is running (and warn if not)
- Start Flask in a Docker container
- Mount the ahab directory (read-only)
- Expose the GUI on port 5001
- Use development mode with auto-reload

### 3. Open your browser

```
http://localhost:5001
```

---

## What to Test

Follow the test scenarios in `PROGRESSIVE_DISCLOSURE_DEMO.md` to verify:

✅ **Navigation (The Roadmap)**
- Main nav shows only available destinations
- Changes based on system state
- Always provides escape routes

✅ **Breadcrumbs**
- Shows where you are
- Provides quick navigation back

✅ **Context Indicator**
- Shows current system state
- Updates when state changes

✅ **Page Actions**
- Only shows actions relevant to THIS page
- Only shows actions possible in CURRENT state
- No disabled buttons (hidden instead)

---

## Alternative: Run from ahab-gui directory

If you want to run directly from ahab-gui:

```bash
cd ahab-gui
make demo
```

This runs the validation checks first, then starts the GUI.

---

## Stopping the Demo

Press `Ctrl+C` in the terminal where the GUI is running.

---

## Troubleshooting

### Docker Not Running

**Most common issue!**

```bash
# Start Docker Desktop (macOS)
open -a Docker

# Wait for it to start, then try again
make ui
```

### Port Already in Use

```bash
# Find what's using port 5001
lsof -i :5001

# Kill it
kill -9 <PID>
```

### More Help

See **TROUBLESHOOTING.md** for detailed solutions to common issues including:
- Docker not running
- Port conflicts
- Permission errors
- Connection issues
- And more...

---

## What's Different?

This implementation follows **progressive disclosure** principles:

### Before (Kitchen Sink Approach)
```
Every page showed:
[Install] [Deploy] [Test] [Status] [SSH] [Destroy]
[Apache] [MySQL] [PHP] [Configure] [Logs] [Restart]
```
**Problem**: Overwhelming, confusing, error-prone

### After (Progressive Disclosure)
```
Home page shows:
[Get Started]

Workstation page (no workstation) shows:
[Install Workstation]

Workstation page (installed) shows:
[Run Tests] [Check Status] [SSH] [Destroy]

Services page shows:
[Apache] [MySQL] [PHP] (only uninstalled ones)
```
**Benefit**: Clear, focused, impossible to make mistakes

---

## The Elevator Analogy

Think of the GUI like an elevator:

**Elevator car** (passenger view):
- Shows: Floor buttons, door controls
- Hides: Motor controls, cable tension, maintenance

**Maintenance panel** (technician view):
- Shows: Diagnostics, safety systems
- Hides: Passenger controls (not relevant)

**Each floor**:
- Shows: Call button, floor indicator
- Hides: Other floors, elevator internals

**Our GUI works the same way**: Each view shows ONLY what's relevant to that context.

---

## Success Criteria

The demo is successful if:

- [ ] You never see actions you can't perform
- [ ] You always know where you are
- [ ] You can always navigate elsewhere
- [ ] Each page shows ONLY relevant actions
- [ ] No disabled buttons (hidden instead)
- [ ] State changes update UI immediately

---

## Next Steps

1. **Test the scenarios** in PROGRESSIVE_DISCLOSURE_DEMO.md
2. **Provide feedback** on clarity and usability
3. **Report issues** if you find any
4. **Suggest improvements** based on your experience

---

## Documentation

- **Progressive Disclosure Principle**: `.kiro/steering/progressive-disclosure-ux.md`
- **Detailed Test Guide**: `PROGRESSIVE_DISCLOSURE_DEMO.md`
- **Implementation Details**: See comments in `static/js/app.js`

---

**Ready? Let's test!**

```bash
cd ahab && make ui
```

Then open: http://localhost:5001
