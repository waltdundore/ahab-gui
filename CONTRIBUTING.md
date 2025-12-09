# Contributing to Ahab GUI

Thank you for your interest in contributing to Ahab GUI!

## Getting Started

### Prerequisites

- Python 3.8 or later
- Git
- Ahab installed (for testing)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/waltdundore/ahab-gui.git
cd ahab-gui

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy example environment file
cp .env.example .env

# Edit .env to point to your Ahab installation
# AHAB_PATH=../ahab

# Run the application
python app.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py

# Run with coverage
pytest --cov=. --cov-report=html
```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused

### Frontend Guidelines

- Use vanilla JavaScript (no frameworks)
- Keep CSS organized and commented
- Ensure responsive design works on all devices
- Test on multiple browsers

### Commit Messages

Use clear, descriptive commit messages:

```
Add feature: Brief description

- Detailed point 1
- Detailed point 2
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes
6. Push to your fork
7. Open a Pull Request

### What to Contribute

**Good First Issues:**
- Documentation improvements
- Bug fixes
- UI/UX enhancements
- Additional service cards
- Test coverage improvements

**Feature Ideas:**
- Service status monitoring
- Log viewing
- Configuration editor
- Multi-user support
- Dark mode

## Design Principles

### Progressive Disclosure

Show users only what they need at each step:
- No workstation? Show only "Install" button
- Workstation ready? Show service deployment options
- Service deployed? Show management options

### Beginner-Friendly

- Use plain language (no jargon)
- Provide clear explanations
- Show helpful error messages
- Suggest next steps

### Real-Time Feedback

- Stream command output in real-time
- Show loading indicators
- Display success/error messages
- Update status automatically

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (CC BY-NC-SA 4.0).
