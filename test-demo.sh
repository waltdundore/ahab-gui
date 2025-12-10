#!/bin/bash
# Quick test script for Progressive Disclosure Demo

set -e

echo "🧪 Testing Ahab GUI Progressive Disclosure Implementation"
echo "=========================================================="
echo ""

# Check we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Must run from ahab-gui directory"
    exit 1
fi

echo "✅ In correct directory"

# Check Python files exist
echo ""
echo "📁 Checking files..."
files=(
    "app.py"
    "config.py"
    "templates/base.html"
    "templates/index.html"
    "static/js/app.js"
    "static/css/style.css"
    "PROGRESSIVE_DISCLOSURE_DEMO.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
        exit 1
    fi
done

# Check for key progressive disclosure elements in JavaScript
echo ""
echo "🔍 Checking progressive disclosure implementation..."

if grep -q "navigateTo" static/js/app.js; then
    echo "  ✅ Navigation system implemented"
else
    echo "  ❌ Navigation system missing"
    exit 1
fi

if grep -q "updateNavigation" static/js/app.js; then
    echo "  ✅ Dynamic navigation implemented"
else
    echo "  ❌ Dynamic navigation missing"
    exit 1
fi

if grep -q "setBreadcrumb" static/js/app.js; then
    echo "  ✅ Breadcrumb system implemented"
else
    echo "  ❌ Breadcrumb system missing"
    exit 1
fi

if grep -q "setContext" static/js/app.js; then
    echo "  ✅ Context indicator implemented"
else
    echo "  ❌ Context indicator missing"
    exit 1
fi

# Check for key CSS classes
echo ""
echo "🎨 Checking CSS styling..."

if grep -q "\.main-nav" static/css/style.css; then
    echo "  ✅ Main navigation styles"
else
    echo "  ❌ Main navigation styles missing"
    exit 1
fi

if grep -q "\.breadcrumb" static/css/style.css; then
    echo "  ✅ Breadcrumb styles"
else
    echo "  ❌ Breadcrumb styles missing"
    exit 1
fi

if grep -q "\.context-indicator" static/css/style.css; then
    echo "  ✅ Context indicator styles"
else
    echo "  ❌ Context indicator styles missing"
    exit 1
fi

# Check HTML templates
echo ""
echo "📄 Checking HTML templates..."

if grep -q "main-nav" templates/base.html; then
    echo "  ✅ Main navigation in template"
else
    echo "  ❌ Main navigation missing from template"
    exit 1
fi

if grep -q "breadcrumb" templates/base.html; then
    echo "  ✅ Breadcrumb in template"
else
    echo "  ❌ Breadcrumb missing from template"
    exit 1
fi

if grep -q "context-indicator" templates/index.html; then
    echo "  ✅ Context indicator in template"
else
    echo "  ❌ Context indicator missing from template"
    exit 1
fi

echo ""
echo "=========================================================="
echo "✅ All checks passed!"
echo ""
echo "🚀 Ready to test the demo!"
echo ""
echo "To start the GUI (from ahab directory):"
echo "  cd ../ahab"
echo "  make ui"
echo ""
echo "Or from ahab-gui directory:"
echo "  make demo"
echo ""
echo "Then open browser: http://localhost:5001"
echo ""
echo "📖 See PROGRESSIVE_DISCLOSURE_DEMO.md for testing guide"
echo "📖 See DEMO_QUICKSTART.md for quick start"
echo ""
