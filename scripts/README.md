# Ahab GUI Scripts

This directory contains utility scripts for validating and maintaining the Ahab GUI.

## Available Scripts

### check-links.sh

**Purpose**: Verify all links in the GUI work correctly before release.

**Usage**:
```bash
# From ahab-gui directory
make check-links

# Or run directly
./scripts/check-links.sh
```

**What it checks**:

1. **Static Asset Links**
   - CSS files (design-system.css, components.css, utilities.css, style.css)
   - JavaScript files (app.js)
   - Images (ahab-logo.png)

2. **Flask Route Links**
   - Navigation URLs (/, /workstation, /services, /tests, /help)
   - Verifies routes are defined in app.py

3. **API Endpoints**
   - /api/status
   - /api/execute
   - Verifies endpoints exist in app.py

4. **External Links**
   - CDN resources (Socket.IO)
   - GitHub repository links
   - Checks if URLs are reachable (requires curl)

5. **Template Includes**
   - Component templates (skip-links.html, navigation.html, breadcrumbs.html, etc.)
   - Verifies all {% include %} references resolve

6. **url_for() References**
   - Extracts all url_for() calls from templates
   - Verifies static files exist

7. **Documentation Links**
   - README.md, BRANDING.md, CONTRIBUTING.md, SECURITY.md
   - Warns if optional docs are missing

**Exit codes**:
- `0` - All links valid
- `1` - Broken links found

**Output**:
- ✓ Green checkmarks for valid links
- ✗ Red X for broken links
- ⚠ Yellow warnings for unreachable external URLs or missing optional files

**Example output**:
```
=== Ahab GUI Link Verification ===

1. Checking static asset links...
   ✓ static/css/design-system.css
   ✓ static/css/components.css
   ✗ static/css/missing.css

=== Summary ===
Total links checked: 30
Valid links: 29
Broken links: 1

=== Broken Links ===
✗ File not found: static/css/missing.css (referenced in templates/base.html)

❌ Link verification FAILED
Fix broken links before release.
```

**Integration with CI/CD**:

Add to your pre-release checklist:
```bash
cd ahab-gui
make check-links || exit 1
```

**When to run**:
- Before every release
- After adding new routes or pages
- After modifying templates
- After updating static assets
- As part of CI/CD pipeline

**Troubleshooting**:

If external links fail:
- Check your internet connection
- Verify the URL is still valid
- External link failures are warnings, not errors

If routes are missing:
- Check app.py for @app.route() definitions
- Verify route paths match navigation URLs
- Update templates/base.html if routes changed

If static files are missing:
- Check file paths in templates
- Verify files exist in static/ directory
- Check for typos in url_for() calls

**Adding new checks**:

To add a new link type to check:

1. Add to appropriate section in check-links.sh
2. Increment TOTAL_LINKS counter
3. Use check_file_exists() for local files
4. Use curl for external URLs
5. Add to BROKEN_LINK_LIST if check fails

Example:
```bash
# Check new static file
TOTAL_LINKS=$((TOTAL_LINKS + 1))
if check_file_exists "$PROJECT_ROOT/static/new-file.js" "templates/new.html"; then
    echo -e "   ${GREEN}✓${NC} static/new-file.js"
else
    echo -e "   ${RED}✗${NC} static/new-file.js"
fi
```

---

## Future Scripts

Additional validation scripts to be added:

- `validate-branding.sh` - Check brand compliance
- `validate-accessibility.sh` - Check WCAG compliance
- `validate-security.sh` - Check for security issues
- `validate-performance.sh` - Check page load times

---

**Last Updated**: December 9, 2025
