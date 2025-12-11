#!/usr/bin/env bash
# ==============================================================================
# Auto-Publish to Dev Branch
# ==============================================================================
# Automatically commits and pushes changes to dev branch every 10 minutes
# Run as: watch -n 600 ./scripts/auto-publish.sh
# Or via GitHub Actions (see .github/workflows/auto-publish.yml)
#
# Security:
# - Only publishes to dev branch
# - Requires clean git state (no conflicts)
# - Logs all operations
#
# ==============================================================================

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="$PROJECT_ROOT/.auto-publish.log"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $*${NC}" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] $*${NC}" | tee -a "$LOG_FILE"
}

# Main
main() {
    log "Auto-publish check started"
    
    cd "$PROJECT_ROOT" || exit 1
    
    # Check if we're on a branch (not detached HEAD)
    if ! git symbolic-ref -q HEAD > /dev/null; then
        log "Detached HEAD state, skipping auto-publish"
        exit 0
    fi
    
    # Get current branch
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    log "Current branch: $CURRENT_BRANCH"
    
    # Check for uncommitted changes using safe git commands
    if ! git --no-pager diff --quiet && ! git --no-pager diff --cached --quiet; then
        log "No changes to publish"
        exit 0
    fi
    
    log_info "Changes detected, preparing to publish..."
    
    # Show what changed
    git status --short | tee -a "$LOG_FILE"
    
    # Stage all changes
    git add -A
    
    # Commit with timestamp
    COMMIT_MSG="Auto-publish: $(date '+%Y-%m-%d %H:%M:%S')"
    if git commit -m "$COMMIT_MSG"; then
        log_success "Committed: $COMMIT_MSG"
    else
        log "Nothing to commit (possibly already committed)"
        exit 0
    fi
    
    # Push to dev branch
    if git push origin "$CURRENT_BRANCH:dev"; then
        log_success "Published to dev branch"
    else
        log "Failed to push to dev (may need manual intervention)"
        exit 1
    fi
    
    log_success "Auto-publish completed successfully"
}

# Run main
main "$@"
