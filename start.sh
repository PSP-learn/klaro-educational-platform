#!/bin/bash
# 🚀 Klaro Educational Platform - Railway Startup Script

echo "🟢 Starting Klaro Educational Platform..."
echo "📍 Environment: ${ENVIRONMENT:-development}"
echo "🌐 Port: ${PORT:-8000}"
echo "🐍 Python Path: ${PYTHONPATH:-/app}"

# Set default port if not provided
export PORT=${PORT:-8000}

# Start the FastAPI server
exec uvicorn backend.main_simple:app \
    --host 0.0.0.0 \
    --port $PORT \
    --log-level info \
    --no-access-log
