#!/usr/bin/env bash
# Link Verification Script for Ahab GUI
# Validates all internal and external links before release
#
# Usage: ./scripts/check-links.sh
# Exit codes: 0 = all links valid, 1 = broken links found

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_LINKS=0
BROKEN_LINKS=0
WARNINGS=0

# Arrays to track issues
declare -a BROKEN_LINK_LIST
declare -a WARNING_LIST

echo -e "${BLUE}=== Ahab GUI Link Verification ===${NC}\n"

# Function to check if file exists
check_file_exists() {
    local file="$1"
    local referenced_from="$2"
    
    if [[ -f "$file" ]]; then
        return 0
    else
        BROKEN_LINKS=$((BROKEN_LINKS + 1))
        BROKEN_LINK_LIST+=("File not found: $file (referenced in $referenced_from)")
        return 1
    fi
}

# Function to check URL format
check_url_format() {
    local url="$1"
    local file="$2"
    
    # Check for common URL issues
    if [[ "$url" =~ \  ]]; then
        WARNINGS=$((WARNINGS + 1))
        WARNING_LIST+=("URL contains spaces: $url in $file")
        return 1
    fi
    
    return 0
}

echo -e "${BLUE}1. Checking static asset links...${NC}"

# Check CSS files referenced in base.html
echo "   Checking CSS files..."
CSS_FILES=(
    "static/css/design-system.css"
    "static/css/components.css"
    "static/css/utilities.css"
    "static/css/style.css"
)

for css in "${CSS_FILES[@]}"; do
    TOTAL_LINKS=$((TOTAL_LINKS + 1))
    if check_file_exists "$PROJECT_ROOT/$css" "templates/base.html"; then
        echo -e "   ${GREEN}✓${NC} $css"
    else
        echo -e "   ${RED}✗${NC} $css"
    fi
done

# Check JavaScript files
echo "   Checking JavaScript files..."
JS_FILES=(
    "static/js/app.js"
)

for js in "${JS_FILES[@]}"; do
    TOTAL_LINKS=$((TOTAL_LINKS + 1))
    if check_file_exists "$PROJECT_ROOT/$js" "templates/base.html"; then
        echo -e "   ${GREEN}✓${NC} $js"
    else
        echo -e "   ${RED}✗${NC} $js"
    fi
done

# Check logo image
echo "   Checking images..."
TOTAL_LINKS=$((TOTAL_LINKS + 1))
if check_file_exists "$PROJECT_ROOT/static/images/ahab-logo.png" "templates/base.html"; then
    echo -e "   ${GREEN}✓${NC} static/images/ahab-logo.png"
else
    echo -e "   ${RED}✗${NC} static/images/ahab-logo.png"
fi

echo ""
echo -e "${BLUE}2. Checking Flask route links...${NC}"

# Extract routes from app.py
if [[ -f "$PROJECT_ROOT/app.py" ]]; then
    ROUTES=$(grep -E "@app\.route\(" "$PROJECT_ROOT/app.py" | sed -E "s/.*@app\.route\('([^']+)'.*/\1/" || true)
    
    # Check navigation links against defined routes
    NAV_URLS=(
        "/"
        "/workstation"
        "/services"
        "/tests"
        "/help"
    )
    
    for url in "${NAV_URLS[@]}"; do
        TOTAL_LINKS=$((TOTAL_LINKS + 1))
        if echo "$ROUTES" | grep -q "^${url}$"; then
            echo -e "   ${GREEN}✓${NC} Route exists: $url"
        else
            BROKEN_LINKS=$((BROKEN_LINKS + 1))
            BROKEN_LINK_LIST+=("Route not found: $url (referenced in templates/base.html)")
            echo -e "   ${RED}✗${NC} Route missing: $url"
        fi
    done
else
    echo -e "   ${RED}✗${NC} app.py not found"
    BROKEN_LINKS=$((BROKEN_LINKS + 1))
fi

echo ""
echo -e "${BLUE}3. Checking API endpoints...${NC}"

# Check API endpoints referenced in JavaScript
API_ENDPOINTS=(
    "/api/status"
    "/api/execute"
)

for endpoint in "${API_ENDPOINTS[@]}"; do
    TOTAL_LINKS=$((TOTAL_LINKS + 1))
    if grep -q "@app.route('${endpoint}'" "$PROJECT_ROOT/app.py" 2>/dev/null; then
        echo -e "   ${GREEN}✓${NC} API endpoint exists: $endpoint"
    else
        BROKEN_LINKS=$((BROKEN_LINKS + 1))
        BROKEN_LINK_LIST+=("API endpoint not found: $endpoint (referenced in static/js/app.js)")
        echo -e "   ${RED}✗${NC} API endpoint missing: $endpoint"
    fi
done

echo ""
echo -e "${BLUE}4. Checking external links...${NC}"

# Check external links in templates and JavaScript
EXTERNAL_LINKS=(
    "https://cdn.socket.io/4.5.4/socket.io.min.js"
    "https://github.com/waltdundore/ahab"
)

for url in "${EXTERNAL_LINKS[@]}"; do
    TOTAL_LINKS=$((TOTAL_LINKS + 1))
    check_url_format "$url" "templates/base.html or static/js/app.js"
    
    # Check if URL is reachable (with timeout)
    if command -v curl &> /dev/null; then
        if curl --output /dev/null --silent --head --fail --max-time 5 "$url" 2>/dev/null; then
            echo -e "   ${GREEN}✓${NC} $url"
        else
            WARNINGS=$((WARNINGS + 1))
            WARNING_LIST+=("External URL may be unreachable: $url")
            echo -e "   ${YELLOW}⚠${NC} $url (unreachable or timeout)"
        fi
    else
        echo -e "   ${YELLOW}⚠${NC} $url (curl not available, skipping check)"
        WARNINGS=$((WARNINGS + 1))
    fi
done

echo ""
echo -e "${BLUE}5. Checking template includes...${NC}"

# Check component templates referenced in base.html
COMPONENT_TEMPLATES=(
    "templates/components/skip-links.html"
    "templates/components/navigation.html"
    "templates/components/breadcrumbs.html"
)

for template in "${COMPONENT_TEMPLATES[@]}"; do
    TOTAL_LINKS=$((TOTAL_LINKS + 1))
    if check_file_exists "$PROJECT_ROOT/$template" "templates/base.html"; then
        echo -e "   ${GREEN}✓${NC} $template"
    else
        echo -e "   ${RED}✗${NC} $template"
    fi
done

# Check component templates referenced in index.html
TOTAL_LINKS=$((TOTAL_LINKS + 1))
if check_file_exists "$PROJECT_ROOT/templates/components/page-header.html" "templates/index.html"; then
    echo -e "   ${GREEN}✓${NC} templates/components/page-header.html"
else
    echo -e "   ${RED}✗${NC} templates/components/page-header.html"
fi

TOTAL_LINKS=$((TOTAL_LINKS + 1))
if check_file_exists "$PROJECT_ROOT/templates/components/loading-state.html" "templates/index.html"; then
    echo -e "   ${GREEN}✓${NC} templates/components/loading-state.html"
else
    echo -e "   ${RED}✗${NC} templates/components/loading-state.html"
fi

echo ""
echo -e "${BLUE}6. Checking url_for() references...${NC}"

# Extract all url_for() calls from templates
if command -v grep &> /dev/null; then
    URL_FOR_CALLS=$(grep -rh "url_for(" "$PROJECT_ROOT/templates/" 2>/dev/null | grep -oE "url_for\('[^']+',\s*filename='[^']+'\)" || true)
    
    if [[ -n "$URL_FOR_CALLS" ]]; then
        # Parse and check each url_for call
        while IFS= read -r call; do
            if [[ "$call" =~ filename=\'([^\']+)\' ]]; then
                filename="${BASH_REMATCH[1]}"
                TOTAL_LINKS=$((TOTAL_LINKS + 1))
                
                if check_file_exists "$PROJECT_ROOT/static/$filename" "templates (url_for)"; then
                    echo -e "   ${GREEN}✓${NC} static/$filename"
                else
                    echo -e "   ${RED}✗${NC} static/$filename"
                fi
            fi
        done <<< "$URL_FOR_CALLS"
    else
        echo "   No url_for() calls found (or already checked above)"
    fi
fi

echo ""
echo -e "${BLUE}7. Checking documentation links...${NC}"

# Check if README references are valid
DOC_FILES=(
    "README.md"
    "BRANDING.md"
    "CONTRIBUTING.md"
    "SECURITY.md"
)

for doc in "${DOC_FILES[@]}"; do
    TOTAL_LINKS=$((TOTAL_LINKS + 1))
    if check_file_exists "$PROJECT_ROOT/$doc" "project root"; then
        echo -e "   ${GREEN}✓${NC} $doc"
    else
        echo -e "   ${YELLOW}⚠${NC} $doc (optional documentation)"
        WARNINGS=$((WARNINGS + 1))
    fi
done

# Summary
echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo "Total links checked: $TOTAL_LINKS"
echo -e "${GREEN}Valid links: $((TOTAL_LINKS - BROKEN_LINKS - WARNINGS))${NC}"

if [[ $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
fi

if [[ $BROKEN_LINKS -gt 0 ]]; then
    echo -e "${RED}Broken links: $BROKEN_LINKS${NC}"
fi

# Print detailed issues
if [[ ${#BROKEN_LINK_LIST[@]} -gt 0 ]]; then
    echo ""
    echo -e "${RED}=== Broken Links ===${NC}"
    for issue in "${BROKEN_LINK_LIST[@]}"; do
        echo -e "${RED}✗${NC} $issue"
    done
fi

if [[ ${#WARNING_LIST[@]} -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}=== Warnings ===${NC}"
    for warning in "${WARNING_LIST[@]}"; do
        echo -e "${YELLOW}⚠${NC} $warning"
    done
fi

echo ""

# Exit with appropriate code
if [[ $BROKEN_LINKS -gt 0 ]]; then
    echo -e "${RED}❌ Link verification FAILED${NC}"
    echo "Fix broken links before release."
    exit 1
else
    if [[ $WARNINGS -gt 0 ]]; then
        echo -e "${YELLOW}⚠ Link verification PASSED with warnings${NC}"
        echo "Review warnings before release."
    else
        echo -e "${GREEN}✅ All links verified successfully${NC}"
    fi
    exit 0
fi
