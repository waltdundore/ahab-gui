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
	$(call HELP_HEADER,Ahab GUI)
	@echo "  make run         - Start GUI in background (use from ahab: make ui)"
	@echo "  make demo        - Start GUI with progressive disclosure demo guide"
	@echo "  make stop        - Stop the GUI"
	@echo "  make status      - Check if GUI is running"
	@echo "  make logs        - View GUI logs"
	@echo "  make verify      - Verify GUI is working (run after 'make run')"
	@echo "  make test        - Run all tests"
	@echo "  make test-web    - Run Web compliance tests (utility library)"
	@echo "  make check-links - Verify all links work (pre-release check)"
	@echo "  make install     - Install dependencies (for testing)"
	@echo "  make clean       - Clean up generated files"
	@echo "  make publish     - Commit and push current branch"
	@echo ""
	@echo "Recommended: Run from ahab directory"
	@echo "  cd ../ahab && make ui"
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
	@echo "=========================================="
	@echo "Publishing Ahab GUI"
	@echo "=========================================="
	@echo ""
	@echo "→ Running: git push origin main"
	@echo "   Purpose: Publish GUI updates to GitHub"
	@echo ""
	@git push origin main
	@echo ""
	@echo "✅ Published to GitHub"
