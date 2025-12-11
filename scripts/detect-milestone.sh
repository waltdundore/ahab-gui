#!/usr/bin/env bash
# ==============================================================================
# Detect Milestone
# ==============================================================================
# Detects if current state represents a critical milestone
# Returns 0 if milestone detected, 1 if not
#
# Milestone indicators:
# - Presence of MILESTONE_*.md files
# - Git tags
# - Specific commit messages
#
# ==============================================================================

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT" || exit 1

# Check for milestone marker files
MILESTONE_FILES=(
    "MILESTONE_OS_SELECTION_COMPLETE.md"
    "MILESTONE_AUTO_PUBLISH_COMPLETE.md"
    "MILESTONE_MULTI_OS_COMPLETE.md"
    "MILESTONE_DEPLOYMENT_READY.md"
    "MILESTONE_PRODUCTION_READY.md"
)

for file in "${MILESTONE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Milestone detected: $file"
        exit 0
    fi
done

# Check for git tags on current commit
if git describe --exact-match --tags HEAD 2>/dev/null; then
    echo "Milestone detected: Tagged release"
    exit 0
fi

# Check for milestone in commit message using safe git command
LAST_COMMIT_MSG=$(git --no-pager log -1 --pretty=%B)
if echo "$LAST_COMMIT_MSG" | grep -qi "milestone"; then
    echo "Milestone detected: Commit message contains 'milestone'"
    exit 0
fi

# No milestone detected
echo "No milestone detected"
exit 1
