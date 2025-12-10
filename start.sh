#!/bin/bash
# Quick start script for Ahab GUI

set -e

echo "=== Ahab GUI Quick Start ==="
echo

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    
    # Generate a random secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    # Update .env with generated secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here-at-least-32-characters-long/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-here-at-least-32-characters-long/$SECRET_KEY/" .env
    fi
    
    echo "✓ Created .env file with generated SECRET_KEY"
    echo
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo

# Check if Ahab directory exists
AHAB_PATH=$(grep AHAB_PATH .env | cut -d '=' -f2)
if [ ! -d "$AHAB_PATH" ]; then
    echo "⚠ Warning: Ahab directory not found at: $AHAB_PATH"
    echo "Please update AHAB_PATH in .env file"
    echo
fi

# Start the application
echo "Starting Ahab GUI..."
echo "Press Ctrl+C to stop"
echo
python app.py
