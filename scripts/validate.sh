#!/usr/bin/env bash
# ==============================================================================
# Ahab GUI - Standards Validation Script
# ==============================================================================
# Validates code against STANDARDS.md requirements
# Must pass before every commit
#
# Usage: ./scripts/validate.sh
# ==============================================================================

set -euo pipefail

# Source shared color definitions (DRY)
# Note: ahab-gui is separate repo, so we define colors locally
# If ahab-gui moves into ahab/, source ../ahab/lib/colors.sh instead
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
CHECKS_RUN=0
CHECKS_PASSED=0
CHECKS_FAILED=0

# Functions
print_header() {
    echo ""
    echo "=========================================="
    echo "$1"
    echo "=========================================="
    echo ""
}

print_check() {
    echo -n "→ $1... "
    CHECKS_RUN=$((CHECKS_RUN + 1))
}

print_pass() {
    echo -e "${GREEN}✓ PASS${NC}"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
}

print_fail() {
    echo -e "${RED}✗ FAIL${NC}"
    echo "  $1"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
}

print_skip() {
    echo -e "${YELLOW}⊘ SKIP${NC} ($1)"
}

# Main validation
print_header "Ahab GUI - Standards Validation"

# Check Python formatting
print_check "Python formatting (black)"
if command -v black &> /dev/null; then
    if black --check . &> /dev/null; then
        print_pass
    else
        print_fail "Run: black ."
    fi
else
    print_skip "black not installed"
fi

# Check import sorting
print_check "Import sorting (isort)"
if command -v isort &> /dev/null; then
    if isort --check-only . &> /dev/null; then
        print_pass
    else
        print_fail "Run: isort ."
    fi
else
    print_skip "isort not installed"
fi

# Check linting
print_check "Linting (pylint)"
if command -v pylint &> /dev/null; then
    SCORE=$(pylint **/*.py 2>/dev/null | grep "Your code has been rated" | awk '{print $7}' | cut -d'/' -f1 || echo "0")
    if (( $(echo "$SCORE >= 9.0" | bc -l) )); then
        print_pass
    else
        print_fail "Score: $SCORE (must be ≥ 9.0). Run: pylint **/*.py"
    fi
else
    print_skip "pylint not installed"
fi

# Check type hints
print_check "Type checking (mypy)"
if command -v mypy &> /dev/null; then
    if mypy . &> /dev/null; then
        print_pass
    else
        print_fail "Run: mypy ."
    fi
else
    print_skip "mypy not installed"
fi

# Check security
print_check "Security scan (bandit)"
if command -v bandit &> /dev/null; then
    if bandit -r . -ll &> /dev/null; then
        print_pass
    else
        print_fail "Run: bandit -r ."
    fi
else
    print_skip "bandit not installed"
fi

# Check tests
print_check "Tests (pytest)"
if command -v pytest &> /dev/null; then
    if pytest &> /dev/null; then
        print_pass
    else
        print_fail "Run: pytest"
    fi
else
    print_skip "pytest not installed"
fi

# Check test coverage
print_check "Test coverage (≥80%)"
if command -v pytest &> /dev/null; then
    COVERAGE=$(pytest --cov=. --cov-report=term 2>/dev/null | grep "TOTAL" | awk '{print $4}' | sed 's/%//' || echo "0")
    if (( $(echo "$COVERAGE >= 80" | bc -l) )); then
        print_pass
    else
        print_fail "Coverage: $COVERAGE% (must be ≥ 80%). Run: pytest --cov=."
    fi
else
    print_skip "pytest not installed"
fi

# Check for secrets
print_check "No secrets committed"
if git grep -i "password\|secret\|api_key" -- '*.py' '*.js' '*.html' &> /dev/null; then
    print_fail "Found potential secrets in code"
else
    print_pass
fi

# Check for TODO/FIXME
print_check "No TODO/FIXME in code"
TODO_COUNT=$(git grep -i "TODO\|FIXME" -- '*.py' '*.js' | wc -l || echo "0")
if [ "$TODO_COUNT" -eq 0 ]; then
    print_pass
else
    print_fail "Found $TODO_COUNT TODO/FIXME comments"
fi

# Summary
print_header "Validation Summary"
echo "Checks run:    $CHECKS_RUN"
echo "Checks passed: $CHECKS_PASSED"
echo "Checks failed: $CHECKS_FAILED"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL CHECKS PASSED${NC}"
    echo ""
    echo "Code is ready to commit!"
    exit 0
else
    echo -e "${RED}❌ VALIDATION FAILED${NC}"
    echo ""
    echo "Fix the issues above before committing."
    echo "See STANDARDS.md for requirements."
    exit 1
fi
