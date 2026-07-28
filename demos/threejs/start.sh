#!/bin/bash
# Startup script for COGNITIVE-SYNC v1.1 Demo

set -e

echo "=========================================="
echo "COGNITIVE-SYNC v1.1 Demo"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python version: $PYTHON_VERSION"

# Check if dependencies are installed
echo ""
echo "Checking dependencies..."
if python3 -c "import fastapi" 2>/dev/null; then
    echo "✓ Dependencies already installed"
else
    echo "📦 Installing dependencies..."
    pip install -r demo_app/requirements.txt --quiet
    echo "✓ Dependencies installed"
fi

# Check SILENT simulator reference
echo ""
echo "Checking SILENT_SIMULATOR reference..."
if [ ! -f "../SILENT-001/firmware/SILENT_SIMULATOR.py" ] && [ ! -f "SILENT-001/firmware/SILENT_SIMULATOR.py" ]; then
    echo "⚠️  Warning: SILENT_SIMULATOR.py not found in expected location"
    echo "   Expected: ../SILENT-001/firmware/SILENT_SIMULATOR.py"
fi

# Check COGNITIVE-SYNC modules
echo ""
echo "Checking COGNITIVE-SYNC modules..."
if [ ! -f "thought_node.py" ]; then
    echo "⚠️  Warning: thought_node.py not found in parent directory"
    echo "   The simulator uses mock data"
fi

echo ""
echo "=========================================="
echo "🚀 Starting server..."
echo "=========================================="
echo ""
echo "Web Interface: http://localhost:8000"
echo "WebSocket:     ws://localhost:8000/ws"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start server
cd demo_app
exec python3 server.py
