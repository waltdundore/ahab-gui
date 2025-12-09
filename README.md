<div align="center">

# Ahab GUI

![Ahab Logo](https://raw.githubusercontent.com/waltdundore/ahab/prod/docs/images/ahab-logo.png)

**Simple Web Interface for Infrastructure Automation**

*Point-and-click infrastructure management for K-12 schools and non-profits.*  
*No command-line required. Perfect for students and educators.*

[![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange)](https://github.com/waltdundore/ahab-gui)
[![Main Project](https://img.shields.io/badge/main%20project-ahab-blue)](https://github.com/waltdundore/ahab)

</div>

---

## What Is This?

**Ahab GUI** is a web interface for [Ahab](https://github.com/waltdundore/ahab), an infrastructure automation platform built for K-12 schools.

Instead of typing commands, you click buttons. Instead of reading documentation, the interface guides you. Perfect for:
- 🎓 **Students** learning DevOps and infrastructure
- 👨‍🏫 **Educators** teaching real-world IT skills
- 🏫 **Schools** managing their own infrastructure
- 🚀 **Anyone** who prefers visual interfaces

**Prerequisites**: [Ahab](https://github.com/waltdundore/ahab) must be installed first.

---

## Quick Start

**Prerequisites**: Docker must be running!

```bash
# Start Docker (macOS)
open -a Docker

# Start the GUI (from ahab directory)
cd ahab
make ui

# Or from ahab-gui directory
cd ahab-gui
make demo
```

Open browser to: **http://localhost:5001**

📖 **[See Full Demo Guide](DEMO.md)** - Screenshots, walkthroughs, and educational scenarios

## What You Can Do

- ✅ **Create Workstation** - One-click Fedora VM setup
- ✅ **Deploy Services** - Apache, MySQL, PHP with visual feedback
- ✅ **Monitor Status** - Real-time workstation and service status
- ✅ **Run Tests** - Verify everything works correctly
- ✅ **Get Help** - Built-in documentation and troubleshooting

## Features

### Progressive Disclosure UX
Shows only what's relevant to your current task. No overwhelming menus or confusing options.

### Educational Focus
Designed for students learning infrastructure automation. Clear explanations, helpful feedback, real-world tools.

### Standards-Aligned
Supports [Georgia Computer Science Standards](https://github.com/waltdundore/ahab#educational-standards-alignment) for K-12 education.

### Accessibility
- WCAG AA compliant color contrast
- Keyboard navigation
- Screen reader friendly
- Mobile responsive

## Configuration

Edit `.env` file (created automatically on first run):

```bash
SECRET_KEY=auto-generated-do-not-change
AHAB_PATH=../ahab
WUI_PORT=5000
```

That's it. The GUI explains everything else.

## Pre-Release Verification

Before any release, verify all links work:

```bash
cd ahab-gui
make check-links
```

This checks:
- Static assets (CSS, JS, images)
- Flask routes and API endpoints
- External links (CDN, GitHub)
- Template includes
- Documentation files

See `scripts/README.md` for details.

## Troubleshooting

**Can't find Ahab?** Edit `AHAB_PATH` in `.env`

**Port in use?** Change `WUI_PORT` in `.env`

**Need help?** Open an issue on GitHub

## Documentation

- **[DEMO.md](DEMO.md)** - Complete demo guide with screenshots and scenarios
- **[BRANDING.md](BRANDING.md)** - Design system and branding guidelines
- **[SECURITY.md](SECURITY.md)** - Security model and best practices
- **[Main Project](https://github.com/waltdundore/ahab)** - Ahab infrastructure automation

## For Educators

Ahab GUI is designed for K-12 education and aligns with [Georgia Computer Science Standards](https://github.com/waltdundore/ahab#educational-standards-alignment).

**Classroom Use:**
- Visual interface perfect for students
- Progressive disclosure reduces cognitive load
- Real-world tools (same as Netflix, Spotify)
- Hands-on learning with immediate feedback

**See [DEMO.md](DEMO.md) for classroom scenarios and lab ideas.**

## Contributing

We welcome contributions! Please:
1. Read [BRANDING.md](BRANDING.md) for design guidelines
2. Check [issues](https://github.com/waltdundore/ahab-gui/issues) for open tasks
3. Submit pull requests with clear descriptions
4. Follow progressive disclosure principles

## Support

- **GUI Issues**: https://github.com/waltdundore/ahab-gui/issues
- **Main Project Issues**: https://github.com/waltdundore/ahab/issues
- **Discussions**: https://github.com/waltdundore/ahab/discussions

## License

CC BY-NC-SA 4.0 - Free for education, contact for commercial use.
