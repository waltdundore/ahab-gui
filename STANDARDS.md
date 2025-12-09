# Ahab GUI - Project Standards

**Date**: December 8, 2025  
**Status**: MANDATORY - All code, documentation, and content must comply  
**Core Principles**: Professional, Accessible, Best Practices  
**Parent Standards**: Inherits from [Ahab STANDARDS.md](../ahab/docs/STANDARDS.md)

---

## Purpose

This document defines strict, non-negotiable standards for Ahab GUI:
- Python code layout and formatting (PEP 8)
- HTML/CSS/JavaScript best practices
- Web accessibility (WCAG 2.1 AA minimum)
- Error messages and user communication
- Testing and validation (pytest, property-based testing)
- Security and safety

**These are not guidelines. These are requirements.**

---

## 1. Python Code Standards

### 1.1 File Structure (MANDATORY)

```python
#!/usr/bin/env python3
"""Module docstring.

Detailed description of what this module does.
Why it exists and when to use it.

Example:
    Basic usage example::

        from module import function
        result = function(arg)
"""

import standard_library
import third_party
from local import module

# Constants (UPPER_SNAKE_CASE)
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Module-level code
```

### 1.2 Naming Conventions (MANDATORY)

- **Modules**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase` (e.g., `CommandExecutor`)
- **Functions**: `snake_case` (e.g., `execute_command`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_TIMEOUT`)
- **Private**: `_leading_underscore` (e.g., `_internal_method`)

### 1.3 Type Hints (MANDATORY)

```python
from typing import Optional, List, Dict, Callable

def execute_command(
    command: str,
    timeout: int = 3600,
    callback: Optional[Callable[[str], None]] = None
) -> ExecutionResult:
    """Execute a command with optional callback.
    
    Args:
        command: The command to execute
        timeout: Maximum execution time in seconds
        callback: Optional function to call with output lines
    
    Returns:
        ExecutionResult with command results
    
    Raises:
        ValueError: If command is invalid
        TimeoutError: If command exceeds timeout
    """
    pass
```

### 1.4 Docstrings (MANDATORY)

**Google Style** (MANDATORY):
```python
def function_name(arg1: str, arg2: int) -> bool:
    """Short one-line summary.
    
    Longer description explaining what this function does,
    why it exists, and when to use it.
    
    Args:
        arg1: Description of first argument
        arg2: Description of second argument
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When arg1 is invalid
        TypeError: When arg2 is wrong type
    
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

### 1.5 Error Handling (MANDATORY)

```python
# ✅ GOOD: Specific exceptions with context
try:
    result = execute_command(cmd)
except ValueError as e:
    logger.error(f"Invalid command: {cmd}", exc_info=True)
    raise CommandError(
        f"Command '{cmd}' is not allowed",
        context="Attempted to execute command",
        action="See allowed commands: Config.ALLOWED_COMMANDS",
        link="https://github.com/waltdundore/ahab-gui/blob/main/README.md"
    ) from e

# ❌ BAD: Bare except, no context
try:
    result = execute_command(cmd)
except:
    print("Error")
```

### 1.6 Code Quality (MANDATORY)

**Tools** (must pass):
- `black` - Code formatting
- `isort` - Import sorting
- `pylint` - Linting (score ≥ 9.0)
- `mypy` - Type checking
- `bandit` - Security scanning

**Run before commit**:
```bash
black .
isort .
pylint **/*.py
mypy .
bandit -r .
```

---

## 2. Web Standards (HTML/CSS/JavaScript)

### 2.1 HTML - Semantic Structure (MANDATORY)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Ahab GUI - Simple infrastructure automation">
    <title>Dashboard - Ahab GUI</title>
</head>
<body>
    <header role="banner">
        <nav role="navigation" aria-label="Main navigation">
            <!-- Navigation -->
        </nav>
    </header>
    
    <main role="main" id="main-content">
        <h1>Dashboard</h1>
        <!-- Main content -->
    </main>
    
    <footer role="contentinfo">
        <!-- Footer -->
    </footer>
</body>
</html>
```

### 2.2 Accessibility (MANDATORY - WCAG 2.1 AA)

**Images**:
```html
<!-- ✅ GOOD: Descriptive alt text -->
<img src="logo.png" alt="Ahab logo - whale tail symbol">

<!-- ❌ BAD: Missing or generic alt -->
<img src="logo.png" alt="logo">
<img src="logo.png">
```

**Links**:
```html
<!-- ✅ GOOD: Descriptive link text -->
<a href="/docs">Read the installation guide</a>

<!-- ❌ BAD: Generic link text -->
<a href="/docs">Click here</a>
```

**Forms**:
```html
<!-- ✅ GOOD: Proper labels and ARIA -->
<label for="command-input">Command to execute:</label>
<input 
    type="text" 
    id="command-input" 
    name="command"
    aria-describedby="command-help"
    required
>
<span id="command-help" class="help-text">
    Enter a make command (e.g., install, test)
</span>

<!-- ❌ BAD: No label, no ARIA -->
<input type="text" placeholder="Command">
```

**Buttons**:
```html
<!-- ✅ GOOD: Descriptive, accessible -->
<button 
    type="button"
    aria-label="Install workstation VM"
    onclick="app.executeCommand('install')"
>
    <span class="icon" aria-hidden="true">🚀</span>
    Install Workstation
</button>

<!-- ❌ BAD: Icon only, no label -->
<button onclick="install()">🚀</button>
```

**Keyboard Navigation**:
```html
<!-- ✅ GOOD: Skip link for keyboard users -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- ✅ GOOD: Focus management -->
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
    <h2 id="dialog-title">Confirm Action</h2>
    <button autofocus>Confirm</button>
    <button>Cancel</button>
</div>
```

### 2.3 Color Contrast (MANDATORY)

**Minimum Ratios**:
- Normal text: **4.5:1**
- Large text (18pt+): **3:1**
- UI components: **3:1**

**Test with**: https://webaim.org/resources/contrastchecker/

```css
/* ✅ GOOD: High contrast */
:root {
    --text-color: #1e293b;      /* Dark on light */
    --bg-color: #ffffff;
    /* Contrast ratio: 15.8:1 */
}

/* ❌ BAD: Low contrast */
:root {
    --text-color: #cccccc;      /* Light gray on white */
    --bg-color: #ffffff;
    /* Contrast ratio: 1.6:1 - FAILS */
}
```

### 2.4 CSS Standards (MANDATORY)

**Organization**:
```css
/* 1. CSS Variables */
:root {
    --color-primary: #2563eb;
    --spacing-unit: 8px;
    --font-family: system-ui, -apple-system, sans-serif;
}

/* 2. Reset/Base */
* {
    box-sizing: border-box;
}

/* 3. Layout */
.container {
    max-width: 1200px;
    margin: 0 auto;
}

/* 4. Components */
.button {
    /* Component styles */
}

/* 5. Utilities */
.text-center {
    text-align: center;
}

/* 6. Media Queries */
@media (min-width: 768px) {
    /* Responsive styles */
}

/* 7. Accessibility */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
    }
}
```

**Focus Indicators** (MANDATORY):
```css
/* ✅ GOOD: Visible focus */
a:focus,
button:focus,
input:focus {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

/* ❌ BAD: Removed focus */
*:focus {
    outline: none; /* NEVER DO THIS */
}
```

**Reduced Motion** (MANDATORY):
```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

### 2.5 JavaScript Standards (MANDATORY)

**Structure**:
```javascript
/**
 * Module description
 * @module app
 */

const app = {
    /**
     * Initialize the application
     * @returns {void}
     */
    init() {
        this.connectWebSocket();
        this.updateStatus();
    },
    
    /**
     * Execute a command
     * @param {string} command - The command to execute
     * @throws {Error} If command is invalid
     * @returns {void}
     */
    executeCommand(command) {
        if (!command) {
            throw new Error('Command is required');
        }
        // Implementation
    }
};
```

**Error Handling**:
```javascript
// ✅ GOOD: Specific error handling
try {
    const result = await fetch('/api/status');
    if (!result.ok) {
        throw new Error(`HTTP ${result.status}: ${result.statusText}`);
    }
    const data = await result.json();
    this.updateStatusDisplay(data);
} catch (error) {
    console.error('Failed to fetch status:', error);
    this.showToast('Unable to load status. Please refresh.', 'error');
}

// ❌ BAD: Silent failure
try {
    fetch('/api/status');
} catch (e) {
    // Nothing
}
```

---

## 3. Testing Standards

### 3.1 pytest Structure (MANDATORY)

```python
"""Tests for command executor."""

import pytest
from pathlib import Path
from commands.executor import CommandExecutor, ExecutionResult


class TestCommandExecutor:
    """Test suite for CommandExecutor class."""
    
    @pytest.fixture
    def executor(self):
        """Create a CommandExecutor instance for testing."""
        return CommandExecutor('../ahab', timeout=10)
    
    def test_execute_valid_command(self, executor):
        """Test executing a valid command."""
        # Arrange
        command = 'help'
        
        # Act
        result = executor.execute(command)
        
        # Assert
        assert result.exit_code == 0
        assert result.success is True
        assert len(result.output) > 0
    
    def test_execute_invalid_command_raises_error(self, executor):
        """Test that invalid command raises ValueError."""
        # Arrange
        command = 'invalid_command_xyz'
        
        # Act & Assert
        with pytest.raises(ValueError, match="not allowed"):
            executor.execute(command)
    
    @pytest.mark.parametrize("command,expected", [
        ('help', True),
        ('install', True),
        ('test', True),
    ])
    def test_allowed_commands(self, executor, command, expected):
        """Test that allowed commands are recognized."""
        # Act
        is_allowed = command in Config.ALLOWED_COMMANDS
        
        # Assert
        assert is_allowed == expected
```

### 3.2 Test Coverage (MANDATORY)

**Minimum Coverage**: 80%

**Required Tests**:
- ✅ Happy path (normal operation)
- ✅ Error conditions (exceptions)
- ✅ Edge cases (empty, null, max values)
- ✅ Invalid input (wrong types, formats)
- ✅ Security (injection, validation)

**Run tests**:
```bash
pytest                          # All tests
pytest --cov=. --cov-report=html  # With coverage
pytest -v tests/test_executor.py  # Specific file
```

### 3.3 Property-Based Testing (MANDATORY)

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=100))
def test_command_validation_with_random_input(command):
    """Test command validation with random strings."""
    executor = CommandExecutor('../ahab')
    
    # Property: Invalid commands should raise ValueError
    if command not in Config.ALLOWED_COMMANDS:
        with pytest.raises(ValueError):
            executor.execute(command)
```

---

## 4. Error Message Standards

### 4.1 Structure (MANDATORY)

Every error MUST include:
1. **Clear Message**: What went wrong?
2. **Context**: What was being attempted?
3. **Action**: Specific steps to fix
4. **Link**: Where to get help

**Python Example**:
```python
class CommandError(Exception):
    """Command execution error with helpful context."""
    
    def __init__(self, message: str, context: str, action: str, link: str):
        self.message = message
        self.context = context
        self.action = action
        self.link = link
        super().__init__(self.format_error())
    
    def format_error(self) -> str:
        return f"""
ERROR: {self.message}

Context: {self.context}
Action: {self.action}
Help: {self.link}
"""

# Usage
raise CommandError(
    message="Command 'deploy' is not allowed",
    context="Attempted to execute command via web interface",
    action="Use one of: install, test, verify-install",
    link="https://github.com/waltdundore/ahab-gui/blob/main/README.md#commands"
)
```

**JavaScript Example**:
```javascript
function showError(message, context, action) {
    const errorHtml = `
        <div class="error-message" role="alert">
            <h3>Error: ${escapeHtml(message)}</h3>
            <p><strong>Context:</strong> ${escapeHtml(context)}</p>
            <p><strong>Action:</strong> ${escapeHtml(action)}</p>
            <a href="/docs/troubleshooting">View troubleshooting guide</a>
        </div>
    `;
    document.getElementById('error-container').innerHTML = errorHtml;
}
```

---

## 5. Security Standards

### 5.1 Input Validation (MANDATORY)

```python
def validate_command(command: str) -> bool:
    """Validate command against whitelist.
    
    Args:
        command: The command to validate
    
    Returns:
        True if valid, False otherwise
    
    Raises:
        ValueError: If command is invalid
    """
    # Check not empty
    if not command or not command.strip():
        raise ValueError("Command cannot be empty")
    
    # Check against whitelist
    if command not in Config.ALLOWED_COMMANDS:
        raise ValueError(
            f"Command '{command}' is not allowed. "
            f"Allowed: {', '.join(Config.ALLOWED_COMMANDS)}"
        )
    
    # Check format (no special characters)
    if not command.replace('-', '').replace('_', '').isalnum():
        raise ValueError(f"Command '{command}' contains invalid characters")
    
    return True
```

### 5.2 CSRF Protection (MANDATORY)

```python
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
csrf = CSRFProtect(app)

# Exempt WebSocket endpoints
@csrf.exempt
@socketio.on('execute')
def handle_execute(data):
    # Validate session instead
    if not session.get('authenticated'):
        emit('error', {'message': 'Not authenticated'})
        return
    # Process command
```

### 5.3 Secrets Management (MANDATORY)

```python
# ✅ GOOD: Environment variables
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")

# ❌ BAD: Hardcoded secrets
SECRET_KEY = "hardcoded-secret-key-123"  # NEVER DO THIS
```

---

## 6. Documentation Standards

### 6.1 README Structure (MANDATORY)

```markdown
# Project Title

**One-line description**

[![Tests](badge)](link)
[![License](badge)](link)

## Quick Start

\`\`\`bash
# Minimal commands to get started
\`\`\`

## Features

- Feature 1
- Feature 2

## Installation

Detailed installation steps

## Usage

Examples and common workflows

## Documentation

- [Link](path) - Description

## Contributing

See CONTRIBUTING.md

## License

License information
```

### 6.2 Code Comments (MANDATORY)

```python
# ✅ GOOD: Explain WHY, not WHAT
# Retry 3 times because network can be flaky during VM startup
for attempt in range(3):
    try:
        result = check_vm_status()
        break
    except ConnectionError:
        if attempt == 2:
            raise
        time.sleep(5)

# ❌ BAD: Explain WHAT (code already shows this)
# Loop 3 times
for attempt in range(3):
    check_vm_status()
```

---

## 7. Git Standards

### 7.1 Commit Messages (MANDATORY)

```
Short summary (50 chars max)

Detailed explanation of what changed and why.
Wrap at 72 characters.

- Bullet points for multiple changes
- Reference issues: Fixes #123
- Reference docs: See DESIGN.md

Validates: Requirements 1.2, 3.4
```

---

## 8. Validation Checklist

### Before Every Commit (MANDATORY):

- [ ] Code formatted: `black .` and `isort .`
- [ ] Linting passes: `pylint **/*.py` (score ≥ 9.0)
- [ ] Type checking passes: `mypy .`
- [ ] Security scan passes: `bandit -r .`
- [ ] All tests pass: `pytest`
- [ ] Coverage ≥ 80%: `pytest --cov=.`
- [ ] HTML validates: https://validator.w3.org/
- [ ] Accessibility passes: https://wave.webaim.org/
- [ ] Color contrast ≥ 4.5:1
- [ ] Documentation updated
- [ ] No secrets committed

### Before Every Release (MANDATORY):

- [ ] All tests pass on all platforms
- [ ] Security audit passed
- [ ] Accessibility audit passed (WCAG 2.1 AA)
- [ ] Documentation complete
- [ ] CHANGELOG.md updated
- [ ] Version number incremented

---

## 9. Tools (MANDATORY)

### Python:
```bash
pip install black isort pylint mypy bandit pytest pytest-cov hypothesis
```

### Web:
- **HTML Validator**: https://validator.w3.org/
- **CSS Validator**: https://jigsaw.w3.org/css-validator/
- **WAVE**: https://wave.webaim.org/
- **Contrast Checker**: https://webaim.org/resources/contrastchecker/

---

## 10. Enforcement

**Non-compliance = Code rejected. No exceptions.**

Every change must be reviewed for:
- Standards compliance
- Error message quality
- Test coverage
- Documentation accuracy
- Accessibility
- Security

---

**Last Updated**: December 8, 2025  
**Status**: ACTIVE - MANDATORY COMPLIANCE  
**Parent**: [Ahab STANDARDS.md](../ahab/docs/STANDARDS.md)
