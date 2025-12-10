# Ahab GUI Makefile
# All Python execution happens in Docker containers
# Called from main ahab Makefile via: make ui

.PHONY: help install test run stop status logs clean demo verify check-links

# Python Docker command (ALWAYS run Python in Docker)
PYTHON_DOCKER = docker run --rm -v $(PWD):/workspace -w /workspace python:3.11-slim

# Get absolute path to ahab directory
AHAB_PATH := $(shell cd .. && pwd)/ahab

help:
	@echo "Ahab GUI - Available Commands"
	@echo ""
	@echo "  make run         - Start GUI in background (use from ahab: make ui)"
	@echo "  make stop        - Stop the GUI"
	@echo "  make status      - Check if GUI is running"
	@echo "  make logs        - View GUI logs"
	@echo "  make verify      - Verify GUI is working (run after 'make run')"
	@echo "  make demo        - Run demo with test script"
	@echo "  make test        - Run all tests"
	@echo "  make test-web    - Run Web compliance tests (utility library)"
	@echo "  make check-links - Verify all links work (pre-release check)"
	@echo "  make install     - Install dependencies (for testing)"
	@echo "  make clean       - Clean up generated files"
	@echo ""
	@echo "Recommended: Run from ahab directory"
	@echo "  cd ../ahab && make ui"
	@echo ""

install:
	@echo "→ Checking Docker..."
	@if ! docker info >/dev/null 2>&1; then \
		echo "❌ ERROR: Docker is not running"; \
		echo "Please start Docker Desktop and try again"; \
		exit 1; \
	fi
	@echo "→ Installing dependencies in Docker..."
	@$(PYTHON_DOCKER) sh -c "pip install -q --upgrade pip && pip install -q -r requirements.txt"
	@echo "✓ Dependencies installed"

test: check-links
	@echo "=========================================="
	@echo "Running Ahab GUI Tests"
	@echo "=========================================="
	@echo ""
	@echo "→ Checking Docker..."
	@if ! docker info >/dev/null 2>&1; then \
		echo ""; \
		echo "❌ ERROR: Docker is not running"; \
		echo "Please start Docker Desktop and try again"; \
		echo ""; \
		exit 1; \
	fi
	@echo "→ Running tests in Docker..."
	@docker run --rm \
		-v $(PWD):/workspace \
		-v $(shell cd .. && pwd):/project:ro \
		-w /workspace \
		-e SECRET_KEY="test-secret-key-minimum-32-characters-long-for-testing" \
		-e AHAB_PATH="/project/ahab" \
		-e WUI_HOST="127.0.0.1" \
		-e WUI_PORT="5000" \
		-e DEBUG="true" \
		python:3.11-slim \
		sh -c "pip install -q -r requirements.txt && pytest tests/ -v --tb=short"
	@echo ""
	@echo "✅ All tests passed"

test-web:
	@echo "=========================================="
	@echo "Running Web Compliance Tests"
	@echo "=========================================="
	@echo ""
	@echo "→ Checking Docker..."
	@if ! docker info >/dev/null 2>&1; then \
		echo ""; \
		echo "❌ ERROR: Docker is not running"; \
		echo "Please start Docker Desktop and try again"; \
		echo ""; \
		exit 1; \
	fi
	@echo "→ Running Web compliance tests in Docker..."
	@docker run --rm \
		-v $(PWD):/workspace \
		-w /workspace \
		python:3.11-slim \
		sh -c "pip install -q -r requirements.txt && pytest tests/test_validators.py tests/test_formatters.py tests/test_accessibility.py tests/test_content.py tests/test_components.py -v --tb=short"
	@echo ""
	@echo "✅ Web compliance tests passed"

run:
	@echo "=========================================="
	@echo "Starting Ahab GUI"
	@echo "=========================================="
	@echo ""
	@echo "→ Checking Docker..."
	@if ! docker info >/dev/null 2>&1; then \
		echo ""; \
		echo "❌ ERROR: Docker is not running"; \
		echo ""; \
		echo "Please start Docker Desktop:"; \
		echo "  • macOS: Open Docker Desktop from Applications"; \
		echo "  • Or run: open -a Docker"; \
		echo ""; \
		echo "Then try again: make run"; \
		echo ""; \
		exit 1; \
	fi
	@echo "✓ Docker is running"
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

demo:
	@echo "=========================================="
	@echo "Ahab GUI - Progressive Disclosure Demo"
	@echo "=========================================="
	@echo ""
	@echo "→ Running validation checks..."
	@./test-demo.sh
	@echo ""
	@echo "→ Starting GUI in background..."
	@$(MAKE) run
	@echo ""
	@echo "=========================================="
	@echo "📖 Demo Guide"
	@echo "=========================================="
	@echo ""
	@echo "1. Open browser: http://localhost:5001"
	@echo "2. Follow test scenarios in PROGRESSIVE_DISCLOSURE_DEMO.md"
	@echo "3. Run 'make stop' when done"
	@echo ""
	@echo "Key things to test:"
	@echo "  • Navigation changes based on state"
	@echo "  • Breadcrumbs show current location"
	@echo "  • Only relevant actions shown per page"
	@echo "  • Context indicator shows system state"
	@echo ""
	@echo "Commands:"
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
	@echo "→ Cleaning up..."
	@rm -rf __pycache__ .pytest_cache .coverage htmlcov
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned"
