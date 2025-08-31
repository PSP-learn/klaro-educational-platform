#!/bin/bash
# 🚀 Klaro Educational Platform - Railway Startup Script

set -e  # Exit on any error

echo "🟢 Starting Klaro Educational Platform..."
echo "📍 Environment: ${ENVIRONMENT:-development}"
echo "🌐 Port: ${PORT:-8000}"
echo "🐍 Python Path: ${PYTHONPATH:-/app}"
echo "📁 Working Directory: $(pwd)"
echo "👤 User: $(whoami)"
echo "🐍 Python Version: $(python --version)"
echo "📦 Pip Version: $(pip --version)"

# Check if required files exist
echo "📋 Checking required files..."
if [ ! -f "backend/main_simple.py" ]; then
    echo "❌ ERROR: backend/main_simple.py not found!"
    ls -la backend/ || echo "❌ backend directory not found"
    exit 1
fi
echo "✅ backend/main_simple.py found"

# Check Python can import the app
echo "🧪 Testing Python import..."
python -c "import backend.main_simple; print('✅ Import successful')" || {
    echo "❌ ERROR: Cannot import backend.main_simple"
    echo "🔍 Python path:"
    python -c "import sys; print('\n'.join(sys.path))"
    echo "🔍 Backend directory contents:"
    ls -la backend/
    exit 1
}

# Set default port if not provided
export PORT=${PORT:-8000}
echo "🎯 Final port: $PORT"

# Start the FastAPI server
echo "🚀 Launching uvicorn..."
exec uvicorn backend.main_simple:app \
    --host 0.0.0.0 \
    --port $PORT \
    --log-level info \
    --access-log
