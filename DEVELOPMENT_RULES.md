# Ahab GUI - Development Rules

**Everything developers need in one place.**

For user documentation, see [README.md](README.md).  
For standards compliance, see [STANDARDS.md](STANDARDS.md).

---

## Guiding Priorities

**Everything we do follows this order:**

1. **Student Achievement First** - Every decision serves student learning
2. **Bug-Free Software** - Quality before features. No release until tests pass.
3. **Marketing What We Do** - Share our work, maximize benefit for education

**Test every decision**: Does this serve students? Is it reliable? Will others learn from it?

---

## Absolute Rules (NO EXCEPTIONS)

### ABSOLUTE RULE #1: Follow STANDARDS.md

**CRITICAL**: ALL code must comply with [STANDARDS.md](STANDARDS.md)

**Why**: Professional, accessible, maintainable code is non-negotiable.

**Process**:
1. Read STANDARDS.md before writing ANY code
2. Run validation tools before EVERY commit
3. Fix ALL violations before proceeding
4. No exceptions, no shortcuts

**Validation**:
```bash
# Python
black .
isort .
pylint **/*.py  # Must score ≥ 9.0
mypy .
bandit -r .

# Tests
pytest --cov=. --cov-report=html  # Must be ≥ 80%

# Web
# Validate HTML: https://validator.w3.org/
# Check accessibility: https://wave.webaim.org/
# Verify contrast: https://webaim.org/resources/contrastchecker/
```

**Penalty for violation**: Code will not be merged.

---

### ABSOLUTE RULE #2: Test Everything

**CRITICAL**: Every function must have tests.

**Why**: Untested code is broken code waiting to happen.

**Requirements**:
- ✅ Unit tests for all functions
- ✅ Integration tests for workflows
- ✅ Property-based tests for validation
- ✅ Accessibility tests for UI
- ✅ Security tests for inputs
- ✅ Minimum 80% coverage

**Example**:
```python
def test_execute_command_with_valid_input():
    """Test command execution with valid input."""
    # Arrange
    executor = CommandExecutor('../ahab')
    command = 'help'
    
    # Act
    result = executor.execute(command)
    
    # Assert
    assert result.exit_code == 0
    assert result.success is True
    assert len(result.output) > 0

def test_execute_command_with_invalid_input():
    """Test command execution rejects invalid input."""
    # Arrange
    executor = CommandExecutor('../ahab')
    command = 'rm -rf /'  # Malicious command
    
    # Act & Assert
    with pytest.raises(ValueError, match="not allowed"):
        executor.execute(command)
```

**Penalty for violation**: Code will not be merged.

---

### ABSOLUTE RULE #3: Accessibility is Mandatory

**CRITICAL**: WCAG 2.1 AA compliance is required, not optional.

**Why**: Schools serve ALL students. Inaccessible software excludes students.

**Requirements**:
- ✅ All images have descriptive alt text
- ✅ All links have descriptive text (not "click here")
- ✅ All forms have proper labels
- ✅ Color contrast ≥ 4.5:1 for text
- ✅ Keyboard navigation works everywhere
- ✅ Screen readers can navigate
- ✅ Focus indicators are visible
- ✅ Reduced motion is supported

**Test with**:
- WAVE: https://wave.webaim.org/
- Keyboard only (no mouse)
- Screen reader (NVDA, JAWS, VoiceOver)

**Penalty for violation**: Code will not be merged.

---

### ABSOLUTE RULE #4: Security First

**CRITICAL**: All inputs must be validated. All secrets must be protected.

**Why**: Schools can't afford security breaches.

**Requirements**:
- ✅ Whitelist allowed commands
- ✅ Validate all user input
- ✅ Use environment variables for secrets
- ✅ Enable CSRF protection
- ✅ Sanitize all output
- ✅ Run security scans (bandit)

**Example**:
```python
# ✅ GOOD: Whitelist validation
ALLOWED_COMMANDS = ['install', 'test', 'verify-install']

def validate_command(command: str) -> bool:
    if command not in ALLOWED_COMMANDS:
        raise ValueError(f"Command not allowed: {command}")
    return True

# ❌ BAD: No validation
def execute_command(command: str):
    subprocess.run(command, shell=True)  # DANGEROUS!
```

**Penalty for violation**: Code will not be merged.

---

## Core Principles

### 1. Eat Your Own Dog Food

**Use what we document.**

- ✅ Use the web interface ourselves
- ✅ Test on real workstations
- ✅ Follow our own instructions
- ❌ Don't bypass the UI with direct commands

**Why**: If it's broken for us, it's broken for users.

---

### 2. Progressive Disclosure

**Show only what's needed.**

- ✅ No workstation? Show only "Install" button
- ✅ Workstation ready? Show service options
- ✅ Hide complexity until needed
- ❌ Don't overwhelm with options

**Why**: Beginners need simplicity, not feature lists.

---

### 3. Real-Time Feedback

**Users must know what's happening.**

- ✅ Stream command output in real-time
- ✅ Show loading indicators
- ✅ Display success/error messages
- ✅ Update status automatically
- ❌ Don't leave users guessing

**Why**: Waiting without feedback is frustrating.

---

### 4. Never Assume Success

**Verify everything.**

```python
# ✅ GOOD: Check result
result = executor.execute('install')
if not result.success:
    raise CommandError(
        "Installation failed",
        f"Exit code: {result.exit_code}",
        "Check logs for details",
        "/docs/troubleshooting"
    )

# ❌ BAD: Assume success
executor.execute('install')
# What if it failed?
```

**Why**: Silent failures are the worst kind.

---

### 5. Helpful Error Messages

**Every error must be actionable.**

**Structure**:
1. What went wrong?
2. What was being attempted?
3. How to fix it?
4. Where to get help?

**Example**:
```python
raise CommandError(
    message="Ahab directory not found",
    context="Attempted to initialize CommandExecutor",
    action="Set AHAB_PATH in .env file: AHAB_PATH=../ahab",
    link="https://github.com/waltdundore/ahab-gui/blob/main/README.md#configuration"
)
```

**Why**: Cryptic errors waste time and frustrate users.

---

## Development Workflow

### 1. Before Writing Code

```bash
# Read requirements
cat .kiro/specs/ux-simplicity-interface/requirements.md

# Read design
cat .kiro/specs/ux-simplicity-interface/design.md

# Read standards
cat STANDARDS.md

# Understand WHAT, WHY, and HOW before coding
```

---

### 2. While Writing Code

```bash
# Format as you go
black file.py
isort file.py

# Check types
mypy file.py

# Write tests alongside code
# For every function, write:
# - Happy path test
# - Error condition test
# - Edge case test
```

---

### 3. Before Committing

```bash
# Run all checks
black .
isort .
pylint **/*.py
mypy .
bandit -r .
pytest --cov=. --cov-report=html

# Validate web content
# - HTML: https://validator.w3.org/
# - Accessibility: https://wave.webaim.org/
# - Contrast: https://webaim.org/resources/contrastchecker/

# Check coverage
# Must be ≥ 80%

# Review changes
git diff

# Commit with descriptive message
git commit -m "Add feature: Brief description

- Detailed point 1
- Detailed point 2

Validates: Requirements 1.2, 3.4"
```

---

### 4. Before Releasing

```bash
# All tests pass
pytest

# Security scan passes
bandit -r .

# Accessibility audit passes
# Test with WAVE, keyboard, screen reader

# Documentation updated
# - README.md
# - CHANGELOG.md
# - DEMO.md

# Version incremented
# Update version in:
# - CHANGELOG.md
# - PROJECT_SUMMARY.md
```

---

## Testing Strategy

### Unit Tests

**Test individual functions**:
```python
def test_validate_command_with_valid_input():
    """Test that valid commands pass validation."""
    assert validate_command('install') is True
    assert validate_command('test') is True

def test_validate_command_with_invalid_input():
    """Test that invalid commands raise ValueError."""
    with pytest.raises(ValueError):
        validate_command('rm -rf /')
```

---

### Integration Tests

**Test workflows**:
```python
def test_install_workflow():
    """Test complete installation workflow."""
    # 1. Check initial state
    status = get_system_status()
    assert not status['workstation_installed']
    
    # 2. Execute install
    result = executor.execute('install')
    assert result.success
    
    # 3. Verify final state
    status = get_system_status()
    assert status['workstation_installed']
```

---

### Property-Based Tests

**Test with random inputs**:
```python
from hypothesis import given, strategies as st

@given(st.text())
def test_command_validation_rejects_invalid_input(command):
    """Test that validation rejects invalid commands."""
    if command not in ALLOWED_COMMANDS:
        with pytest.raises(ValueError):
            validate_command(command)
```

---

### Accessibility Tests

**Test with tools and manual testing**:
- WAVE: Automated accessibility scan
- Keyboard: Navigate without mouse
- Screen reader: Test with NVDA/JAWS/VoiceOver
- Color contrast: Verify ≥ 4.5:1

---

## Common Mistakes to Avoid

### ❌ Mistake #1: Skipping Tests

**Wrong**:
```python
# Write code
def execute_command(cmd):
    # Implementation
    pass

# Ship it!
```

**Right**:
```python
# Write code
def execute_command(cmd):
    # Implementation
    pass

# Write tests
def test_execute_command():
    result = execute_command('help')
    assert result.success

# Then ship it
```

---

### ❌ Mistake #2: Poor Error Messages

**Wrong**:
```python
raise ValueError("Error")
```

**Right**:
```python
raise CommandError(
    message="Command 'deploy' is not allowed",
    context="Attempted to execute command via web interface",
    action="Use one of: install, test, verify-install",
    link="https://github.com/waltdundore/ahab-gui/blob/main/README.md"
)
```

---

### ❌ Mistake #3: Ignoring Accessibility

**Wrong**:
```html
<button onclick="install()">Install</button>
```

**Right**:
```html
<button 
    type="button"
    aria-label="Install workstation virtual machine"
    onclick="app.executeCommand('install')"
>
    <span class="icon" aria-hidden="true">🚀</span>
    Install Workstation
</button>
```

---

### ❌ Mistake #4: Hardcoding Secrets

**Wrong**:
```python
SECRET_KEY = "my-secret-key-123"
```

**Right**:
```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set")
```

---

## Resources

### Documentation
- [STANDARDS.md](STANDARDS.md) - Mandatory standards
- [README.md](README.md) - User documentation
- [DEMO.md](DEMO.md) - Demo walkthrough
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide

### Tools
- **black**: Code formatting
- **isort**: Import sorting
- **pylint**: Linting
- **mypy**: Type checking
- **bandit**: Security scanning
- **pytest**: Testing
- **hypothesis**: Property-based testing

### Web Standards
- **WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/
- **WAVE**: https://wave.webaim.org/
- **HTML Validator**: https://validator.w3.org/
- **Contrast Checker**: https://webaim.org/resources/contrastchecker/

---

## Questions?

- Read STANDARDS.md first
- Check existing code for examples
- Ask in GitHub Discussions
- Open an issue for bugs

---

**Remember**: Quality is not optional. Accessibility is not optional. Testing is not optional.

**We build software that teaches. We build software that lasts. We build software that matters.**

**Do it right, or don't do it at all.**

---

**Last Updated**: December 8, 2025  
**Status**: ACTIVE - MANDATORY COMPLIANCE
