<div align="center">

# Ahab GUI Demo

![Ahab Logo](https://raw.githubusercontent.com/waltdundore/ahab/prod/docs/images/ahab-logo.png)

**See infrastructure automation in action - no command line required.**

[![Main Project](https://img.shields.io/badge/main%20project-ahab-blue)](https://github.com/waltdundore/ahab)
[![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE)

</div>

---

## What You'll See

This demo shows how Ahab GUI makes infrastructure automation accessible to students, educators, and anyone who prefers visual interfaces over command-line tools.

**Time Required**: 10-15 minutes  
**Prerequisites**: Docker running on your machine

---

## Quick Start

```bash
# Clone the repositories
git clone https://github.com/waltdundore/ahab.git
git clone https://github.com/waltdundore/ahab-gui.git

# Start the GUI
cd ahab
make ui

# Open browser to http://localhost:5001
```

---

## Demo Walkthrough

### 1. Home Page - Your Starting Point

**What you see:**
- Clean, uncluttered interface
- Current workstation status
- Clear next steps

**What you can do:**
- Create a new workstation VM
- View system status
- Navigate to different sections

**Key Features:**
- ✅ Progressive disclosure - only shows relevant actions
- ✅ Status indicators with color coding
- ✅ Helpful explanations for each action
- ✅ Breadcrumb navigation

**Educational Value:**
Students learn infrastructure concepts through visual feedback rather than cryptic command-line output.

---

### 2. Creating a Workstation

**Click: "Create Workstation"**

**What happens:**
1. GUI shows real-time progress
2. Terminal output displays in browser
3. Status updates as installation proceeds
4. Success/failure clearly indicated

**Behind the scenes:**
```bash
# GUI executes this command
cd ahab && make install
```

**What gets installed:**
- ✓ Fedora 43 VM (or Debian/Ubuntu if configured)
- ✓ Docker & Docker Compose
- ✓ Ansible automation tools
- ✓ Security hardening (SELinux, firewall)

**Time**: 5-10 minutes (depending on your machine)

**Educational Value:**
Students see the entire provisioning process, understand what's being installed, and learn patience with infrastructure tasks.

---

### 3. Workstation Page - Managing Your VM

**Navigate to: Workstation**

**What you see:**
- Current VM status (Running/Stopped/Not Created)
- Available actions based on current state
- System information
- Quick access to common tasks

**State-Aware Actions:**

**When VM is running:**
- Stop Workstation
- Restart Workstation
- SSH into Workstation
- Destroy Workstation

**When VM is stopped:**
- Start Workstation
- Destroy Workstation

**When VM doesn't exist:**
- Create Workstation

**Key Features:**
- ✅ Only shows actions that are possible right now
- ✅ No confusing disabled buttons
- ✅ Clear state indicators
- ✅ Helpful descriptions for each action

**Educational Value:**
Students learn state management - understanding that available actions depend on current system state.

---

### 4. Services Page - Deploying Applications

**Navigate to: Services**

**What you see:**
- List of available services (Apache, MySQL, PHP)
- Installation status for each
- Quick deploy buttons
- Service-specific actions

**Deploying Apache:**

1. Click "Deploy Apache"
2. Watch real-time installation progress
3. See Docker Compose configuration generated
4. Get confirmation when complete

**Behind the scenes:**
```bash
# GUI executes this command
cd ahab && make install apache
```

**What happens:**
- Ansible playbook runs
- Docker Compose file generated
- Apache container started
- Service verified and tested

**Educational Value:**
Students learn:
- How services are deployed
- What Docker Compose does
- How automation tools work
- Real-world DevOps workflows

---

### 5. Service Management

**Click on a deployed service (e.g., Apache)**

**What you see:**
- Service status (Running/Stopped)
- Configuration options
- Service-specific actions
- Logs and diagnostics

**Available Actions:**
- Configure service
- Restart service
- View logs
- Stop service
- Remove service

**Key Features:**
- ✅ Context-aware menu (only Apache actions shown)
- ✅ Real-time status updates
- ✅ Easy access to logs
- ✅ Safe service management

**Educational Value:**
Students learn service lifecycle management - deploy, configure, monitor, troubleshoot, remove.

---

### 6. Tests Page - Verifying Everything Works

**Navigate to: Tests**

**What you see:**
- Available test suites
- Test status and results
- Run tests with one click
- Clear pass/fail indicators

**Running Tests:**

1. Click "Run All Tests"
2. Watch tests execute in real-time
3. See detailed results
4. Get clear pass/fail status

**Behind the scenes:**
```bash
# GUI executes this command
cd ahab && make test
```

**What gets tested:**
- NASA Power of 10 safety standards
- Code quality checks
- Integration tests
- Property-based tests

**Educational Value:**
Students learn:
- Why testing matters
- How to verify infrastructure
- Industry-standard testing practices
- Debugging and troubleshooting

---

### 7. Help Page - Built-in Documentation

**Navigate to: Help**

**What you see:**
- Getting started guide
- Common tasks
- Troubleshooting tips
- Links to full documentation

**Key Features:**
- ✅ Context-sensitive help
- ✅ Common issues and solutions
- ✅ Links to detailed docs
- ✅ Video tutorials (coming soon)

**Educational Value:**
Students learn to find answers independently, building problem-solving skills.

---

## Progressive Disclosure in Action

### Example: Workstation Not Created

**What you see:**
- Status: "Workstation not created"
- Action: "Create Workstation" button
- Main Menu: Home, Help

**What you DON'T see:**
- Stop/Restart buttons (not possible yet)
- Service deployment (need workstation first)
- SSH access (nothing to SSH into)

### Example: Workstation Running

**What you see:**
- Status: "Workstation running"
- Actions: Stop, Restart, SSH, Destroy
- Main Menu: Home, Workstation, Services, Tests, Help

**What you DON'T see:**
- Create button (already created)
- Start button (already running)

**The Principle:**
Show only what's relevant. Hide complexity until needed. Guide users to the right place.

---

## Accessibility Features

### Keyboard Navigation

**Try this:**
1. Press `Tab` to move between elements
2. Press `Enter` to activate buttons
3. Press `Esc` to close dialogs

**Everything is keyboard accessible.**

### Screen Reader Support

**Try this:**
1. Enable VoiceOver (Mac) or NVDA (Windows)
2. Navigate through the interface
3. Hear descriptive labels for all elements

**All images have alt text. All buttons have labels.**

### Color Contrast

**All text meets WCAG AA standards:**
- Normal text: ≥ 4.5:1 contrast ratio
- Large text: ≥ 3:1 contrast ratio
- Interactive elements: ≥ 3:1 contrast ratio

**Verified combinations:**
- Ahab Blue (#0066cc) on white: 7.2:1 ✅
- Ahab Navy (#003d7a) on white: 12.6:1 ✅
- Gray text (#212529) on white: 15.8:1 ✅

### Mobile Responsive

**Try this:**
1. Resize your browser window
2. Open on a tablet or phone
3. Interface adapts to screen size

**Works on all devices.**

---

## Educational Standards Alignment

Ahab GUI supports [Georgia Computer Science Standards](https://github.com/waltdundore/ahab#educational-standards-alignment):

### IT-NSS (Network Systems and Services)
- **IT-NSS-10**: Network operation and administration
- **IT-NSS-11**: System configuration and management

### IT-ITS (IT Support Specialist)
- **IT-ITS-3**: System installation and configuration
- **IT-ITS-4**: Security implementation
- **IT-ITS-5**: Troubleshooting and diagnostics

### IT-CSP (Computer Science Principles)
- **IT-CSP-3**: Abstraction and automation
- **IT-CSP-6**: Internet operation

**See [ahab/feature-standards-map.yml](https://github.com/waltdundore/ahab/blob/prod/feature-standards-map.yml) for complete mappings.**

---

## Real-World Skills

Students using Ahab GUI learn the same tools used by:

- **Netflix** - Infrastructure automation at scale
- **Spotify** - Service deployment and management
- **NASA** - Safety-critical systems (Power of 10 rules)
- **Thousands of companies** - DevOps and infrastructure

**These aren't toy tools. This is real infrastructure automation.**

---

## Demo Scenarios

### Scenario 1: First-Time User

**Goal**: Create a workstation and deploy Apache

**Steps:**
1. Open GUI → See home page
2. Click "Create Workstation" → Watch installation
3. Navigate to Services → See available services
4. Click "Deploy Apache" → Watch deployment
5. Navigate to Apache → See running service
6. Success! Web server is running

**Time**: 10-15 minutes  
**Learning**: Infrastructure provisioning, service deployment, state management

---

### Scenario 2: Classroom Demo

**Goal**: Show students how infrastructure automation works

**Steps:**
1. Project GUI on screen
2. Explain what we're building (web server)
3. Click "Create Workstation" → Discuss what's happening
4. Show terminal output → Explain each step
5. Deploy Apache → Show Docker Compose generation
6. Test service → Verify it works
7. Show logs → Demonstrate troubleshooting

**Time**: 20-30 minutes  
**Learning**: DevOps workflow, automation benefits, real-world tools

---

### Scenario 3: Student Lab

**Goal**: Students deploy their own infrastructure

**Steps:**
1. Each student opens GUI on their machine
2. Follow guided workflow
3. Create workstation
4. Deploy multiple services (Apache, MySQL, PHP)
5. Test and verify
6. Troubleshoot any issues
7. Document what they learned

**Time**: 45-60 minutes  
**Learning**: Hands-on infrastructure management, problem-solving, documentation

---

## Technical Details

### Architecture

```
Browser (http://localhost:5001)
    ↓
Flask Web Server (Python)
    ↓
Command Executor (subprocess)
    ↓
Make Commands (cd ahab && make <target>)
    ↓
Ansible/Vagrant/Docker
    ↓
Infrastructure
```

### Security Model

**GUI runs as non-root:**
- ✅ No privileged access required
- ✅ Executes whitelisted make commands only
- ✅ Cannot modify host system
- ✅ All operations in isolated VM

**See [SECURITY.md](SECURITY.md) for details.**

### Technology Stack

**Frontend:**
- HTML5 semantic markup
- CSS3 with custom properties
- Vanilla JavaScript (no frameworks)
- Progressive enhancement

**Backend:**
- Python 3.11+
- Flask web framework
- Subprocess command execution
- Session management

**Infrastructure:**
- [Ahab](https://github.com/waltdundore/ahab) automation platform
- Vagrant for VM management
- Ansible for provisioning
- Docker for services

---

## Comparison: CLI vs GUI

### Command Line (Traditional)

```bash
# Create workstation
cd ahab
make install

# Deploy Apache
make install apache

# Check status
vagrant status

# View logs
vagrant ssh -c "docker logs apache"

# Run tests
make test
```

**Pros:**
- Fast for experienced users
- Scriptable and automatable
- Full control

**Cons:**
- Intimidating for beginners
- Easy to make mistakes
- No visual feedback
- Requires memorizing commands

### GUI (Ahab GUI)

**Click buttons. See results. Learn by doing.**

**Pros:**
- Beginner-friendly
- Visual feedback
- Guided workflow
- Hard to make mistakes
- Built-in help

**Cons:**
- Slightly slower for experts
- Not scriptable

**Best of Both Worlds:**
GUI teaches the concepts. CLI provides the power. Students can use both.

---

## Try It Yourself

### Option 1: Quick Demo (5 minutes)

```bash
# Clone and start
git clone https://github.com/waltdundore/ahab.git
cd ahab
make ui

# Open http://localhost:5001
# Click around, explore the interface
```

### Option 2: Full Demo (15 minutes)

```bash
# Clone and start
git clone https://github.com/waltdundore/ahab.git
cd ahab
make ui

# Follow the demo scenarios above
# Create workstation, deploy services, run tests
```

### Option 3: Classroom Demo (30 minutes)

```bash
# Project on screen
# Follow "Scenario 2: Classroom Demo" above
# Engage students with questions
# Show real-world applications
```

---

## What's Next?

### For Students
- Try deploying different services
- Experiment with configurations
- Break things and fix them
- Document what you learn

### For Educators
- Integrate into curriculum
- Create lab assignments
- Assess student understanding
- Share feedback with us

### For Developers
- Contribute to the project
- Report bugs and issues
- Suggest new features
- Improve documentation

---

## Get Involved

**Main Project**: https://github.com/waltdundore/ahab  
**GUI Project**: https://github.com/waltdundore/ahab-gui  
**Issues**: https://github.com/waltdundore/ahab-gui/issues  
**Discussions**: https://github.com/waltdundore/ahab/discussions

---

## License

CC BY-NC-SA 4.0 - Free for education, contact for commercial use.

---

**Ready to see it in action? Run `make ui` and open http://localhost:5001**
