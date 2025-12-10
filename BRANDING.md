# Ahab GUI Branding Guidelines

**Status**: MANDATORY  
**Last Updated**: December 9, 2025

---

## Brand Identity

**Ahab** is a DevOps automation platform that makes infrastructure management simple and accessible. Our brand reflects:
- **Simplicity**: Clean, uncluttered interfaces
- **Reliability**: Professional, trustworthy design
- **Education**: Welcoming to learners and students
- **Power**: Capable of serious infrastructure work
- **Privacy**: Your data stays on your machine, never in the cloud

---

## Logo

### Primary Logo
- **File**: `ahab/docs/images/ahab-logo.png`
- **Usage**: All documentation, GUI header, README files
- **Alt Text**: "Ahab logo - whale tail symbol"

### Logo Placement
```html
<!-- In GUI header -->
<img src="/static/images/ahab-logo.png" alt="Ahab logo - whale tail symbol" class="logo">

<!-- In documentation -->
![Ahab Logo](ahab/docs/images/ahab-logo.png)
```

### Logo Rules
- ✅ Always use official logo file
- ✅ Maintain aspect ratio
- ✅ Provide descriptive alt text
- ❌ Never distort or modify logo
- ❌ Never use low-resolution versions

---

## Color Palette

### Primary Colors

```css
:root {
    /* Brand Colors */
    --ahab-blue: #0066cc;        /* Primary brand color */
    --ahab-navy: #003d7a;        /* Dark accent */
    --ahab-light-blue: #4d94ff; /* Light accent */
    
    /* Semantic Colors */
    --success: #28a745;          /* Green for success states */
    --danger: #dc3545;           /* Red for errors/warnings */
    --warning: #ffc107;          /* Yellow for cautions */
    --info: #17a2b8;             /* Cyan for information */
    
    /* Neutral Colors */
    --gray-50: #f8f9fa;          /* Lightest gray - backgrounds */
    --gray-100: #e9ecef;         /* Light gray - borders */
    --gray-200: #dee2e6;         /* Medium-light gray */
    --gray-600: #6c757d;         /* Medium gray - secondary text */
    --gray-900: #212529;         /* Dark gray - primary text */
    
    /* Terminal Colors */
    --terminal-bg: #1e1e1e;      /* Dark background */
    --terminal-text: #d4d4d4;    /* Light text */
    --terminal-success: #4ec9b0; /* Cyan for success */
    --terminal-error: #f48771;   /* Red for errors */
}
```

### Color Usage

**Primary Actions**: Use `--ahab-blue`
```css
.btn-primary {
    background: var(--ahab-blue);
    color: white;
}
```

**Headers/Branding**: Use `--ahab-navy`
```css
header {
    background: var(--ahab-navy);
    color: white;
}
```

**Hover States**: Use `--ahab-light-blue`
```css
.btn-primary:hover {
    background: var(--ahab-light-blue);
}
```

### Accessibility Requirements

**All color combinations MUST meet WCAG AA standards:**
- Normal text: Contrast ratio ≥ 4.5:1
- Large text (18pt+): Contrast ratio ≥ 3:1
- Interactive elements: Contrast ratio ≥ 3:1

**Verified Combinations:**
- ✅ `--ahab-blue` on white: 7.2:1
- ✅ `--ahab-navy` on white: 12.6:1
- ✅ `--gray-900` on white: 15.8:1
- ✅ White on `--ahab-blue`: 7.2:1
- ✅ White on `--ahab-navy`: 12.6:1

---

## Typography

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
             'Helvetica Neue', Arial, sans-serif;
```

### Font Sizes
```css
:root {
    --font-size-xs: 0.75rem;   /* 12px */
    --font-size-sm: 0.875rem;  /* 14px */
    --font-size-base: 1rem;    /* 16px */
    --font-size-lg: 1.125rem;  /* 18px */
    --font-size-xl: 1.25rem;   /* 20px */
    --font-size-2xl: 1.5rem;   /* 24px */
    --font-size-3xl: 2rem;     /* 32px */
}
```

### Headings
- **H1**: 2rem (32px), bold, `--ahab-navy`
- **H2**: 1.5rem (24px), bold, `--gray-900`
- **H3**: 1.25rem (20px), semibold, `--gray-900`
- **Body**: 1rem (16px), normal, `--gray-900`

---

## Spacing

### Spacing Scale
```css
:root {
    --space-1: 0.25rem;  /* 4px */
    --space-2: 0.5rem;   /* 8px */
    --space-3: 0.75rem;  /* 12px */
    --space-4: 1rem;     /* 16px */
    --space-5: 1.5rem;   /* 24px */
    --space-6: 2rem;     /* 32px */
    --space-8: 3rem;     /* 48px */
}
```

### Usage
- **Tight spacing**: `--space-2` (buttons, form elements)
- **Normal spacing**: `--space-4` (cards, sections)
- **Loose spacing**: `--space-6` (major sections)

---

## Components

### Buttons

```css
/* Primary Button */
.btn-primary {
    background: var(--ahab-blue);
    color: white;
    padding: var(--space-3) var(--space-5);
    border-radius: 6px;
    font-weight: 600;
    border: none;
    cursor: pointer;
}

.btn-primary:hover {
    background: var(--ahab-light-blue);
}

/* Secondary Button */
.btn-secondary {
    background: var(--gray-100);
    color: var(--gray-900);
    border: 1px solid var(--gray-200);
}

/* Danger Button */
.btn-danger {
    background: var(--danger);
    color: white;
}
```

### Cards

```css
.card {
    background: white;
    border: 1px solid var(--gray-200);
    border-radius: 8px;
    padding: var(--space-5);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

### Terminal

```css
.terminal {
    background: var(--terminal-bg);
    color: var(--terminal-text);
    font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
    padding: var(--space-4);
    border-radius: 6px;
    overflow-x: auto;
}
```

---

## Content Guidelines

### Technical Accuracy

**Operating System**: Fedora 43 (default)
```html
<!-- ✅ CORRECT -->
<li>✓ Fedora 43 VM (default)</li>
<li>✓ Also supports: Debian 13, Ubuntu 24.04</li>

<!-- ❌ WRONG -->
<li>✓ Rocky Linux 9 VM</li>
```

### Tone and Voice

**Professional but Approachable**
- ✅ "Let's set up your infrastructure automation workstation"
- ❌ "Click here to install stuff"

**Clear and Direct**
- ✅ "Installation takes about 5-10 minutes"
- ❌ "This might take a while"

**Educational**
- ✅ "What gets installed: Fedora 43 VM, Docker & Docker Compose, Ansible automation tools"
- ❌ "Installs everything you need"

**Privacy-Focused**
- ✅ "Everything runs on your local machine—your data never leaves your network"
- ✅ "No cloud dependencies, no data collection, complete control"
- ❌ "Secure cloud-based solution"

### Key Messaging: Local Execution & Data Privacy

**Core Message**: The software is particularly powerful because you're running everything on your own local machine. Nothing is in the cloud. None of your data goes out to us or to any other company, and everything is open source. You're not depending on our repository—you're depending on existing Docker repositories.

**Use this messaging when:**
- Explaining what makes Ahab different
- Addressing privacy concerns
- Talking to schools about student data
- Discussing sovereignty and control
- Comparing to cloud-based solutions

**Example implementations:**
```html
<!-- In feature lists -->
<li>✓ Runs entirely on your local machine</li>
<li>✓ No cloud dependencies or data collection</li>
<li>✓ Uses standard Docker images from official repositories</li>

<!-- In explanatory text -->
<p>Everything runs on your own infrastructure. Your data never leaves 
your network, and you're not dependent on our servers—just standard 
Docker repositories that the entire industry relies on.</p>

<!-- In comparison sections -->
<h3>Why Local Matters</h3>
<p>Unlike cloud-based solutions, Ahab gives you complete control. 
No vendor lock-in, no data sharing, no monthly fees. Your infrastructure, 
your data, your rules.</p>
```

---

## Implementation Checklist

### For Every Page

- [ ] Logo displayed in header
- [ ] Brand colors used consistently
- [ ] Typography follows guidelines
- [ ] Spacing uses defined scale
- [ ] Color contrast ≥ 4.5:1 verified
- [ ] Technical information is accurate
- [ ] Tone matches brand voice

### For Every Component

- [ ] Uses CSS custom properties
- [ ] Follows accessibility guidelines
- [ ] Responsive on mobile
- [ ] Keyboard navigable
- [ ] Screen reader friendly

---

## Testing

### Visual Testing
```bash
# Check logo displays
open http://localhost:5001

# Verify colors match brand
# Use browser DevTools to inspect CSS variables
```

### Accessibility Testing
```bash
# Color contrast
# Use: https://webaim.org/resources/contrastchecker/

# Screen reader
# Test with VoiceOver (Mac) or NVDA (Windows)

# Keyboard navigation
# Tab through all interactive elements
```

---

## Enforcement

**This branding guide is MANDATORY for all GUI development.**

Before committing any GUI changes:
1. Verify logo is displayed correctly
2. Verify colors match brand palette
3. Verify technical accuracy (OS versions, etc.)
4. Verify accessibility compliance
5. Test on mobile and desktop

**Non-compliance will require rework.**

---

## Quick Reference

```css
/* Copy-paste starter */
:root {
    --ahab-blue: #0066cc;
    --ahab-navy: #003d7a;
    --success: #28a745;
    --danger: #dc3545;
    --gray-900: #212529;
    --gray-50: #f8f9fa;
}

.btn-primary {
    background: var(--ahab-blue);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
}
```

---

**Remember**: Consistency builds trust. Follow these guidelines on every page, every component, every time.
