# Ahab GUI Makefile
# All Python execution happens in Docker containers
# Called from main ahab Makefile via: make ui

# Include shared configuration and common targets
include ../ahab/Makefile.config
include ../ahab/Makefile.common

.PHONY: help install test run stop status logs clean demo verify check-links publish

# Get absolute path to ahab directory
AHAB_PATH := $(shell cd .. && pwd)/ahab

help:
	$(call HELP_HEADER,Ahab Web Interface (GUI))
	@echo "🚀 QUICK START:"
	@echo "  cd ../ahab && make ui     → Start GUI from main directory (recommended)"
	@echo "  make run                  → Start GUI in background (~10 sec startup)"
	@echo "  make verify               → Test GUI is working (opens browser)"
	@echo "  make stop                 → Stop the GUI cleanly"
	@echo ""
	@echo "🖥️  GUI MANAGEMENT:"
	@echo "  make run                  → Start Flask GUI server in background"
	@echo "                              • Runs on http://localhost:5001"
	@echo "                              • Uses Docker container (Python 3.11)"
	@echo "                              • Auto-reloads on code changes"
	@echo "                              • Logs to gui.log"
	@echo "  make demo                 → Start with progressive disclosure demo guide"
	@echo "                              • Interactive tutorial mode"
	@echo "                              • Shows UX principles in action"
	@echo "                              • Educational overlay enabled"
	@echo "  make stop                 → Stop GUI server gracefully"
	@echo "                              • Saves state and closes connections"
	@echo "                              • Cleans up Docker containers"
	@echo "  make status               → Check if GUI is running"
	@echo "                              • Shows PID, port, memory usage"
	@echo "                              • Displays recent log entries"
	@echo "  make logs                 → View real-time GUI logs"
	@echo "                              • Shows Flask debug output"
	@echo "                              • Command execution logs"
	@echo "                              • Error traces and warnings"
	@echo ""
	@echo "✅ TESTING & VALIDATION:"
	@echo "  make verify               → Comprehensive GUI functionality test"
	@echo "                              • HTTP response check (200 OK)"
	@echo "                              • Page load validation"
	@echo "                              • JavaScript functionality"
	@echo "                              • Opens browser for manual verification"
	@echo "  make test                 → Run complete test suite (~1-2 min)"
	@echo "                              • Unit tests for all modules"
	@echo "                              • Integration tests with ahab commands"
	@echo "                              • Security validation"
	@echo "                              • Link checking"
	@echo "  make test-web             → Web compliance tests only"
	@echo "                              • HTML/CSS validation"
	@echo "                              • WCAG 2.1 AA accessibility"
	@echo "                              • Progressive disclosure UX"
	@echo "  make check-links          → Verify all internal/external links"
	@echo "                              • Tests navigation functionality"
	@echo "                              • Validates external resources"
	@echo "                              • Pre-release quality check"
	@echo ""
	@echo "🔧 DEVELOPMENT:"
	@echo "  make install              → Install Python dependencies"
	@echo "                              • Uses Docker container (no host pollution)"
	@echo "                              • Installs Flask, testing libraries"
	@echo "                              • Sets up development environment"
	@echo "  make clean                → Clean up generated files"
	@echo "                              • Removes __pycache__ directories"
	@echo "                              • Cleans log files and temp data"
	@echo "                              • Resets to clean state"
	@echo "  make publish              → Publish main branch to GitHub"
	@echo "                              • Uses standardized git publishing"
	@echo "                              • Handles GitHub push protection"
	@echo "                              • Shows transparent command execution"
	@echo "  make publish-all          → Publish all configured branches"
	@echo "  make publish-status       → Show git publishing status"
	@echo ""
	@echo "💡 COMMON WORKFLOWS:"
	@echo "  # Start GUI for development:"
	@echo "  make run && make verify"
	@echo ""
	@echo "  # Test changes before commit:"
	@echo "  make test && make publish"
	@echo ""
	@echo "  # Debug GUI issues:"
	@echo "  make logs                 # Check for errors"
	@echo "  make stop && make run     # Restart cleanly"
	@echo ""
	@echo "🌐 ACCESS POINTS:"
	@echo "  • Main Interface: http://localhost:5001"
	@echo "  • Status Page: http://localhost:5001/status"
	@echo "  • API Endpoint: http://localhost:5001/api/status"
	@echo ""
	@echo "⚠️  IMPORTANT NOTES:"
	@echo "  • GUI is in early development - expect changes"
	@echo "  • Always run 'make verify' after 'make run'"
	@echo "  • Use 'cd ../ahab && make ui' for best experience"
	@echo "  • All Python runs in Docker (no host dependencies)"
	$(call HELP_FOOTER)

install:
	$(call SHOW_COMMAND,pip install -r requirements.txt,Install Python dependencies in Docker container)
	$(call CHECK_DOCKER)
	@$(PYTHON_DOCKER) sh -c "pip install -q --upgrade pip && pip install -q -r requirements.txt"
	@echo "✓ Dependencies installed"

test: check-links
	$(call SHOW_STATUS,Running Ahab GUI Tests)
	$(call RUN_PYTHON_TESTS,tests/)
	@echo "✅ All tests passed"

test-web:
	$(call SHOW_SECTION,Running Web Compliance Tests)
	$(call CHECK_DOCKER)
	@echo "→ Running Web compliance tests in Docker..."
	@docker run --rm \
		-v $(PWD):/workspace \
		-w /workspace \
		python:3.11-slim \
		sh -c "pip install -q -r requirements.txt && pytest tests/test_validators.py tests/test_formatters.py tests/test_accessibility.py tests/test_content.py tests/test_components.py -v --tb=short"
	@echo ""
	@echo "✅ Web compliance tests passed"

run:
	$(call CHECK_DOCKER)
	@echo ""
	@echo "Configuration:"
	@echo "  Port: 5001"
	@echo "  Ahab Path: $(AHAB_PATH)"
	@echo "  Mode: Development"
	@echo ""
	@echo "→ Starting Flask in Docker container (detached)..."
	@echo ""
	@# Stop any existing container
	@docker stop ahab-gui 2>/dev/null || true
	@docker rm ahab-gui 2>/dev/null || true
	@# Start new container in background
	@docker run -d \
		--name ahab-gui \
		-v $(PWD):/workspace \
		-v $(shell cd .. && pwd):/project:ro \
		-w /workspace \
		-p 5001:5001 \
		-e SECRET_KEY="dev-secret-key-change-in-production" \
		-e AHAB_PATH=/project/ahab \
		-e WUI_HOST=0.0.0.0 \
		-e WUI_PORT=5001 \
		-e DEBUG=true \
		python:3.11-slim \
		sh -c "pip install -q -r requirements.txt && python app.py" || \
		(echo ""; echo "❌ Failed to start GUI"; exit 1)
	@echo ""
	@echo "✅ GUI started successfully!"
	@echo ""
	@echo "📖 Next Steps:"
	@echo "  1. Open browser: http://localhost:5001"
	@echo "  2. Check status: make status"
	@echo "  3. View logs: make logs"
	@echo "  4. Stop GUI: make stop"
	@echo ""

demo: run
	@echo ""
	@echo "=========================================="
	@echo "📖 Demo Guide - Progressive Disclosure"
	@echo "=========================================="
	@echo ""
	@echo "→ Running: ./test-demo.sh"
	@echo "   Purpose: Validate progressive disclosure implementation before demo"
	@./test-demo.sh
	@echo ""
	@echo "🎯 Demo Objectives:"
	@echo "  • Navigation changes based on system state"
	@echo "  • Breadcrumbs show current location"
	@echo "  • Only relevant actions shown per page"
	@echo "  • Context indicator reflects workstation status"
	@echo ""
	@echo "📖 Test Scenarios:"
	@echo "  1. Open browser: http://localhost:5001"
	@echo "  2. Follow scenarios in PROGRESSIVE_DISCLOSURE_DEMO.md"
	@echo "  3. Test different workstation states (not created, running, etc.)"
	@echo ""
	@echo "🔧 Demo Commands:"
	@echo "  • View logs: make logs"
	@echo "  • Check status: make status"
	@echo "  • Stop GUI: make stop"
	@echo ""

verify:
	@echo "=========================================="
	@echo "Verifying Ahab GUI"
	@echo "=========================================="
	@echo ""
	@echo "→ Checking if GUI is running..."
	@if ! curl -s http://localhost:5001/ > /dev/null 2>&1; then \
		echo "❌ ERROR: GUI is not running on port 5001"; \
		echo ""; \
		echo "To start the GUI:"; \
		echo "  make run    # Start in background"; \
		echo "  make status # Check if running"; \
		echo "  make logs   # View output"; \
		echo ""; \
		exit 1; \
	fi
	@echo "✓ GUI is running"
	@echo ""
	@echo "→ Testing API endpoint..."
	@curl -s http://localhost:5001/api/status | docker run --rm -i python:3.11-slim python -m json.tool || \
		(echo "❌ ERROR: API endpoint failed"; exit 1)
	@echo ""
	@echo "→ Testing page load..."
	@if curl -s http://localhost:5001/ | grep -q "Ahab GUI"; then \
		echo "✓ Page loads correctly"; \
	else \
		echo "❌ ERROR: Page content incorrect"; \
		exit 1; \
	fi
	@echo ""
	@echo "→ Testing JavaScript files..."
	@if curl -s http://localhost:5001/static/js/app.js | grep -q "Progressive Disclosure"; then \
		echo "✓ JavaScript loads correctly"; \
	else \
		echo "❌ ERROR: JavaScript not loading"; \
		exit 1; \
	fi
	@echo ""
	@echo "✅ All verification checks passed"
	@echo ""
	@echo "📖 GUI is ready:"
	@echo "  • Open browser: http://localhost:5001"
	@echo "  • View logs: make logs"
	@echo "  • Stop GUI: make stop"

check-links:
	@echo "=========================================="
	@echo "Verifying All Links in Ahab GUI"
	@echo "=========================================="
	@echo ""
	@./scripts/check-links.sh

stop:
	@echo "→ Stopping Ahab GUI..."
	@if docker ps | grep -q ahab-gui; then \
		docker stop ahab-gui >/dev/null 2>&1; \
		docker rm ahab-gui >/dev/null 2>&1; \
		echo "✓ GUI stopped"; \
	else \
		echo "ℹ GUI is not running"; \
	fi

status:
	@echo "→ Checking GUI status..."
	@if docker ps | grep -q ahab-gui; then \
		echo "✅ GUI is running"; \
		echo "   Container: $$(docker ps --format 'table {{.Names}}\t{{.Status}}' | grep ahab-gui)"; \
		echo "   URL: http://localhost:5001"; \
	else \
		echo "❌ GUI is not running"; \
		echo "   Start with: make run"; \
	fi

logs:
	@echo "→ Showing GUI logs (Ctrl+C to exit)..."
	@if docker ps | grep -q ahab-gui; then \
		docker logs -f ahab-gui; \
	else \
		echo "❌ GUI is not running"; \
		echo "   Start with: make run"; \
	fi

clean: stop
	$(call SHOW_COMMAND,cleanup,Remove temporary files and stop containers)
	$(call CLEAN_PYTHON)
	@echo "✓ Cleaned"

publish:
	@echo "→ Running: ./scripts/git-publish $(filter-out publish,$(MAKECMDGOALS))"
	@echo "   Purpose: Publish branch to GitHub for collaboration and visibility"
	@./scripts/git-publish $(filter-out publish,$(MAKECMDGOALS))

publish-all:
	@echo "→ Running: ./scripts/git-publish all"
	@echo "   Purpose: Publish all configured branches to GitHub"
	@./scripts/git-publish all

publish-status:
	@echo "→ Running: ./scripts/git-publish status"
	@echo "   Purpose: Show current git publishing status and branch sync state"
	@./scripts/git-publish status

publish-sync:
	@echo "→ Running: ./scripts/git-publish sync"
	@echo "   Purpose: Sync main branch with remote changes before publishing"
	@./scripts/git-publish sync
# Handle branch names as arguments to publish command
%:
	@: