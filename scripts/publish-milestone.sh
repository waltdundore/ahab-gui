#!/usr/bin/env bash
# ==============================================================================
# Publish Milestone to All Branches
# ==============================================================================
# Publishes current state to dev, prod, and workstation branches
# Only run when a milestone is detected
#
# Security:
# - Requires milestone detection to pass
# - Logs all operations
# - Verifies push success for each branch
#
# ==============================================================================

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="$PROJECT_ROOT/.milestone-publish.log"

BRANCHES=("dev" "prod" "workstation")

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $*${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $*${NC}" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] $*${NC}" | tee -a "$LOG_FILE"
}

# Main
main() {
    log "Milestone publish started"
    
    cd "$PROJECT_ROOT" || exit 1
    
    # Verify milestone detection
    if ! "$SCRIPT_DIR/detect-milestone.sh"; then
        log_error "No milestone detected, aborting publish"
        exit 1
    fi
    
    # Get current commit
    CURRENT_COMMIT=$(git rev-parse HEAD)
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    
    log_info "Publishing commit $CURRENT_COMMIT from branch $CURRENT_BRANCH"
    
    # Publish to each branch
    local failed_branches=()
    
    for branch in "${BRANCHES[@]}"; do
        log_info "Publishing to $branch..."
        
        if git push origin "HEAD:$branch"; then
            log_success "✓ Published to $branch"
        else
            log_error "✗ Failed to publish to $branch"
            failed_branches+=("$branch")
        fi
    done
    
    # Summary
    echo ""
    log "=========================================="
    log "Milestone Publish Summary"
    log "=========================================="
    
    if [ ${#failed_branches[@]} -eq 0 ]; then
        log_success "All branches published successfully!"
        log_success "Branches: ${BRANCHES[*]}"
        return 0
    else
        log_error "Failed to publish to: ${failed_branches[*]}"
        log_info "Successfully published to: $(comm -23 <(printf '%s\n' "${BRANCHES[@]}" | sort) <(printf '%s\n' "${failed_branches[@]}" | sort) | tr '\n' ' ')"
        return 1
    fi
}

# Run main
main "$@"
