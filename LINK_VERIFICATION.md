# Link Verification Process

**Purpose**: Ensure all links in ahab-gui are valid before deployment.

**Status**: MANDATORY - All builds must pass link verification.

**Last Updated**: December 9, 2025

---

## Why Link Verification Matters

Broken links create a poor user experience:
- ❌ Navigation that goes nowhere frustrates users
- ❌ 404 errors make the application look unfinished
- ❌ Missing API endpoints break functionality
- ❌ Broken external links damage credibility

**Prevention is better than debugging in production.**

---

## What Gets Checked

### 1. Static Assets
- CSS files referenced in templates
- JavaScript files referenced in templates
- Images referenced in templates
- Fonts and other static resources

### 2. Flask Routes
- Navigation links (/, /workstation, /services, /tests, /help)
- Internal page links
- Form action targets
- Redirect destinations

### 3. API Endpoints
- REST API endpoints (/api/status, /api/execute, etc.)
- WebSocket endpoints
- AJAX call targets

### 4. External Links
- CDN resources (Socket.IO, etc.)
- Documentation links
- GitHub repository links
- External service URLs

### 5. Template Includes
- Component includes (navigation.html, breadcrumbs.html, etc.)
- Partial templates
- Layout inheritance

### 6. url_for() References
- Static file references
- Route references
- Blueprint references

---

## How to Run Link Verification

### Manual Check

```bash
cd ahab-gui
./scripts/check-links.sh
```

**Output**:
- ✓ Valid links (green)
- ✗ Broken links (red)
- Summary with counts
- Exit code 0 = all links valid
- Exit code 1 = broken links found

### Via Make Command

```bash
cd ahab-gui
make check-links
```

**Integrated into workflow**:
- Runs before tests
- Fails build if links broken
- Shows clear error messages

### Automated (CI/CD)

Link verification runs automatically:
- On every commit (pre-commit hook)
- On every pull request (GitHub Actions)
- Before deployment (release pipeline)

---

## Common Issues and Fixes

### Issue: Route not found

**Symptom**:
```
✗ Route not found: /workstation (referenced in templates/base.html)
```

**Fix**:
1. Add route to app.py:
```python
@app.route('/workstation')
def workstation():
    """Render workstation management page."""
    return render_template('workstation.html')
```

2. Create template:
```bash
touch templates/workstation.html
```

3. Verify:
```bash
./scripts/check-links.sh
```

### Issue: API endpoint missing

**Symptom**:
```
✗ API endpoint not found: /api/execute (referenced in static/js/app.js)
```

**Fix**:
1. Add endpoint to app.py:
```python
@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute a whitelisted command."""
    return jsonify({'success': True})
```

2. Verify:
```bash
./scripts/check-links.sh
```

### Issue: Static file missing

**Symptom**:
```
✗ static/css/custom.css (referenced in templates/base.html)
```

**Fix**:
1. Create the file:
```bash
touch static/css/custom.css
```

2. Or remove the reference if not needed

3. Verify:
```bash
./scripts/check-links.sh
```

### Issue: Template include missing

**Symptom**:
```
✗ templates/components/footer.html (included in templates/base.html)
```

**Fix**:
1. Create the component:
```bash
touch templates/components/footer.html
```

2. Add minimal content:
```html
<footer>
    <p>&copy; 2025 Ahab</p>
</footer>
```

3. Verify:
```bash
./scripts/check-links.sh
```

---

## Development Workflow

### Before Starting Work

```bash
# Verify current state is clean
cd ahab-gui
make check-links
```

**Expected**: All checks pass

### While Developing

**When adding navigation**:
1. Add route to app.py FIRST
2. Create template
3. Add navigation link
4. Run `make check-links`

**When adding API endpoints**:
1. Add endpoint to app.py FIRST
2. Add JavaScript calls
3. Run `make check-links`

**When adding static assets**:
1. Create file FIRST
2. Add reference in template
3. Run `make check-links`

### Before Committing

```bash
# Final verification
cd ahab-gui
make check-links
make test
```

**Both must pass before commit.**

---

## Integration with Testing

Link verification is part of the test suite:

```makefile
# ahab-gui/Makefile
test: check-links
	@pytest
```

**This ensures**:
- Links checked before unit tests
- Broken links fail the build
- No broken links reach production

---

## CI/CD Integration

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

cd ahab-gui
./scripts/check-links.sh || {
    echo "❌ Link verification failed"
    echo "Fix broken links before committing"
    exit 1
}
```

### GitHub Actions

```yaml
# .github/workflows/test.yml
- name: Check Links
  run: |
    cd ahab-gui
    ./scripts/check-links.sh
```

### Release Pipeline

```bash
# Before deployment
make check-links || {
    echo "❌ Cannot deploy with broken links"
    exit 1
}
```

---

## Maintenance

### Updating the Check Script

When adding new link types to check:

1. Edit `scripts/check-links.sh`
2. Add new check function
3. Add to main check sequence
4. Test with known broken link
5. Test with valid link
6. Document in this file

### Adding Exceptions

If a link should be excluded from checking:

1. Add to exclusion list in `check-links.sh`
2. Document WHY it's excluded
3. Add comment in code explaining exception

**Avoid exceptions unless absolutely necessary.**

---

## Troubleshooting

### Script hangs

**Cause**: External link check timing out

**Fix**: Add timeout to curl commands in script

### False positives

**Cause**: Dynamic routes not detected

**Fix**: Add route pattern to script's route detection

### False negatives

**Cause**: Link type not being checked

**Fix**: Add new check function to script

---

## Best Practices

1. **Check early, check often**
   - Run after every navigation change
   - Run before every commit
   - Run in CI/CD pipeline

2. **Fix immediately**
   - Don't commit broken links
   - Don't defer fixes
   - Broken links compound quickly

3. **Create placeholders**
   - Add route before navigation link
   - Create template before route
   - Create file before reference

4. **Document exceptions**
   - If link must be excluded, document why
   - Add comment in code
   - Update this documentation

5. **Automate everything**
   - Use make commands
   - Integrate into test suite
   - Add to CI/CD pipeline

---

## Related Documentation

- [scripts/check-links.sh](scripts/check-links.sh) - Link verification script
- [TESTING.md](TESTING.md) - Testing strategy
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development workflow
- [../LESSONS_LEARNED.md](../LESSONS_LEARNED.md) - Lesson 2025-12-09-001

---

## Summary

**Link verification is mandatory.**

- ✅ Run `make check-links` before committing
- ✅ Fix broken links immediately
- ✅ Create placeholders for planned features
- ✅ Integrate into CI/CD pipeline
- ❌ Never commit broken links
- ❌ Never skip link verification
- ❌ Never defer link fixes

**Broken links = broken user experience.**
