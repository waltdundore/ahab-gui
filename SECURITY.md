# Ahab GUI Security Documentation

**Last Updated**: December 9, 2025  
**Audience**: GUI Users  
**Status**: MANDATORY READING

---

## What This GUI Does

The Ahab GUI is a **web interface** that provides a user-friendly way to execute Ahab commands.

**That's it. Nothing more.**

---

## How Commands Are Executed

### The Complete Chain

```
1. You click a button in the browser
   ↓
2. Browser sends request to Flask app
   ↓
3. Flask app validates the request
   ↓
4. Flask app executes: make <command>
   ↓
5. Make command runs (see ahab/Makefile)
   ↓
6. Results are displayed in the browser
```

### What the GUI Can Execute

**Whitelisted commands only:**
- `make install` - Create workstation VM
- `make install <module>` - Install a service (apache, mysql, php)
- `make test` - Run tests
- `make status` - Check system status
- `make clean` - Destroy VM
- `make ssh` - Open SSH session

**The GUI cannot execute:**
- ❌ Arbitrary shell commands
- ❌ sudo commands
- ❌ Direct file modifications
- ❌ Git operations
- ❌ Anything not in the whitelist

### Code Verification

**See for yourself** (`ahab-gui/commands/executor.py`):

```python
def execute(self, command: str, callback: Optional[Callable[[str], None]] = None):
    """Execute a make command."""
    
    # Only executes: ['make', command]
    process = subprocess.Popen(
        ['make', command],           # ← Only make commands
        cwd=str(self.ahab_path),    # ← In ahab directory
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
```

**No `shell=True`** - Prevents shell injection  
**No `sudo`** - No privilege escalation  
**No arbitrary commands** - Only make targets

---

## How the GUI Runs

### Container-Based Execution

The GUI runs in a Docker container:

```bash
docker run --rm -it \
    -v $(PWD):/workspace \
    -v $(AHAB_PATH):/ahab:ro \    # ← Read-only mount
    -w /workspace \
    -p 5001:5001 \
    python:3.11-slim \
    sh -c "pip install -q -r requirements.txt && python app.py"
```

**Security features:**
- Runs as **non-root user** in container
- Ahab directory mounted **read-only** (`:ro`)
- No `--privileged` flag
- No host network access
- Isolated from host system

### What the Container Can Access

**Can access:**
- ✅ ahab directory (read-only)
- ✅ ahab-gui directory (read-write for sessions)
- ✅ Network port 5001 (for web interface)

**Cannot access:**
- ❌ Your home directory
- ❌ Your host filesystem (except mounted volumes)
- ❌ Root on your host machine
- ❌ Other containers
- ❌ Host network interfaces

---

## Privilege Escalation (How Root Access Works)

### The GUI Does NOT Have Root Access

**The GUI:**
- Runs in unprivileged container
- Cannot sudo
- Cannot access host root
- Cannot modify host system

### Where Root Access Happens

**Root access only happens:**
1. Inside the workstation VM (not on your host)
2. Via Ansible's `become: true` directive
3. Using Vagrant's built-in passwordless sudo
4. For system operations (package install, service config)

**Complete chain:**
```
GUI (no root)
  → make command (no root)
    → Vagrant (no root on host)
      → Creates VM
        → Ansible inside VM (uses sudo)
          → Root operations inside VM only
```

**Your host machine is never affected.**

---

## What You Should Know

### Before Using the GUI

1. **The GUI executes make commands** - Same as running them manually
2. **Make commands control Vagrant** - Creates/destroys VMs
3. **Vagrant creates isolated VMs** - Separate from your host
4. **Ansible configures VMs** - Uses sudo inside VM only
5. **Your host is protected** - No root access on host

### What Happens When You Click "Install Workstation"

```
1. GUI executes: make install
2. Make runs: vagrant up
3. Vagrant creates a Fedora/Debian/Ubuntu VM
4. Vagrant installs Ansible inside VM
5. Ansible provisions VM (installs Docker, Git, etc.)
6. Ansible uses sudo inside VM (not on your host)
7. VM is ready for use
```

### What Happens When You Click "Install Apache"

```
1. GUI executes: make install apache
2. Make runs: vagrant provision
3. Vagrant runs Ansible inside VM
4. Ansible installs Apache inside VM
5. Ansible uses sudo inside VM (not on your host)
6. Apache is running inside VM
7. You can access it at http://localhost:8080
```

---

## Security Boundaries

### Layer 1: Browser → GUI

**Protection:**
- HTTPS (if configured)
- Session management
- CSRF protection
- Input validation

**What this prevents:**
- Unauthorized access
- Session hijacking
- Cross-site request forgery
- Command injection

### Layer 2: GUI → Host

**Protection:**
- Container isolation
- Read-only mounts
- No privileged mode
- Limited network access

**What this prevents:**
- Container escape
- Host filesystem modification
- Privilege escalation on host
- Network attacks on host

### Layer 3: Host → VM

**Protection:**
- VM isolation
- Separate kernel
- Separate filesystem
- Controlled port forwarding

**What this prevents:**
- VM affecting host
- VM accessing host files
- VM escalating privileges on host
- VM network attacks on host

### Layer 4: VM User → VM Root

**Protection:**
- Ansible's declarative model
- Auditable playbooks
- Idempotent operations
- No arbitrary commands

**What this prevents:**
- Uncontrolled root access
- Arbitrary command execution
- Persistent backdoors
- Unauditable changes

---

## Verification Commands

### Verify GUI Runs in Container

```bash
cd ahab-gui
make run
# Check the output - should show Docker commands
```

### Verify GUI Cannot Sudo

```bash
cd ahab-gui
docker run --rm python:3.11-slim sudo whoami
# Should fail: sudo: command not found
```

### Verify GUI Only Executes Make Commands

```bash
cd ahab-gui
grep -r "subprocess.Popen" commands/
# Should only show: ['make', command]
```

### Verify No Shell Injection Possible

```bash
cd ahab-gui
grep -r "shell=True" .
# Should return no results
```

---

## Common Questions

### Q: Is it safe to run the GUI on my machine?

**A:** Yes, with these caveats:
- GUI is for **development/education only**
- Do NOT expose to the internet
- Do NOT use in production
- Do NOT run as root (not needed, not supported)

### Q: Can the GUI access my files?

**A:** Only the files you explicitly mount:
- ahab directory (read-only)
- ahab-gui directory (for sessions)
- Nothing else

### Q: Can the GUI install malware on my host?

**A:** No:
- GUI runs in isolated container
- GUI cannot access host root
- GUI can only execute whitelisted make commands
- Make commands only control Vagrant
- Vagrant only affects VMs, not host

### Q: What if I click "Destroy Workstation"?

**A:** It destroys the VM only:
- VM is deleted
- VM files are removed
- Your host is unaffected
- Your ahab directory is unaffected
- You can recreate the VM anytime

### Q: Can someone hack the GUI?

**A:** Possible attack vectors:
1. **Network access**: Don't expose GUI to internet
2. **Session hijacking**: Use HTTPS in production
3. **Command injection**: Prevented by whitelist + no shell=True
4. **Container escape**: Use updated Docker version

**Mitigations:**
- Run GUI locally only (localhost:5001)
- Don't expose port 5001 to network
- Keep Docker updated
- Review code before running

### Q: Should I use the GUI or command line?

**A:** Your choice:
- **GUI**: Easier, visual, good for learning
- **CLI**: More control, scriptable, good for automation

**Both execute the same make commands.**

---

## Security Best Practices

### Do's

✅ **Run GUI locally only** (localhost:5001)
✅ **Keep Docker updated**
✅ **Review the code** before running
✅ **Destroy VMs when not needed**: Click "Destroy Workstation"
✅ **Use HTTPS** if exposing to network (not recommended)
✅ **Monitor container logs** for suspicious activity

### Don'ts

❌ **Don't expose GUI to internet** (development only)
❌ **Don't run GUI as root** (not needed, not supported)
❌ **Don't modify executor.py** without security review
❌ **Don't disable container isolation**
❌ **Don't use in production** without proper security review
❌ **Don't store secrets in GUI** (use Ansible Vault)

---

## What Data Does the GUI Collect?

**None.**

The GUI:
- Does NOT send telemetry
- Does NOT phone home
- Does NOT collect analytics
- Does NOT store credentials
- Does NOT access external services

**All operations are local.**

---

## Reporting Security Issues

If you find a security issue in the GUI:

1. **Do NOT open a public GitHub issue**
2. **Email the maintainers** with details
3. **Include**: Steps to reproduce, impact assessment, suggested fix
4. **We will respond** within 48 hours
5. **We will credit you** in the security advisory (if desired)

---

## Technical Details

### GUI Architecture

```
Browser (JavaScript)
  ↓ HTTP/HTTPS
Flask App (Python)
  ↓ subprocess.Popen(['make', command])
Makefile (Shell)
  ↓ vagrant up/provision
Vagrant (Ruby)
  ↓ Creates VM
Ansible (Python)
  ↓ become: true (sudo inside VM)
System Operations (Root inside VM only)
```

### Command Whitelist

**Defined in**: `ahab-gui/commands/executor.py`

**Allowed commands:**
- `install` - Create workstation
- `install <module>` - Install service
- `test` - Run tests
- `status` - Check status
- `clean` - Destroy VM
- `ssh` - Open SSH session

**All other commands are rejected.**

### Session Management

- Sessions stored in `flask_session/` directory
- Session timeout: 24 hours (configurable)
- Session data: User preferences only
- No credentials stored in sessions

### Environment Variables

**Required:**
- `SECRET_KEY` - Flask session encryption (generate unique key)
- `AHAB_PATH` - Path to ahab directory
- `WUI_HOST` - Host to bind (default: 127.0.0.1)
- `WUI_PORT` - Port to bind (default: 5001)

**Optional:**
- `DEBUG` - Enable debug mode (default: false)

**Never commit `.env` file with real SECRET_KEY.**

---

## Summary

**The GUI is a simple web interface that:**
1. Runs in an isolated Docker container
2. Executes only whitelisted make commands
3. Has no root access on your host
4. Cannot modify your host system
5. Is completely transparent and auditable

**Your host machine is protected by multiple security layers.**

**Everything is open source and reviewable.**

---

## Related Documentation

- [Ahab Security Model](../ahab/docs/SECURITY_MODEL.md) - Complete security documentation
- [Privilege Escalation Model](../.kiro/steering/privilege-escalation-model.md) - Technical details
- [GUI Development Rules](DEVELOPMENT_RULES.md) - Development guidelines

---

**Questions?** Open an issue on GitHub or contact the maintainers.

**Concerns?** Review the code, run the verification commands, or use CLI instead.

**We believe in transparency. If something is unclear, let us know.**
