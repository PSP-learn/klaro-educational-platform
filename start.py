#!/usr/bin/env python3
"""
🚀 Klaro Educational Platform - Python Startup Script
Minimal startup script for Railway deployment
"""

import os
import sys
import uvicorn

def main():
    """Start the FastAPI application with proper port handling"""
    
    # Get port from environment (Railway sets this dynamically)
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"🟢 Starting Klaro Educational Platform")
    print(f"🌐 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"🐍 Python Version: {sys.version}")
    
    # Start uvicorn with full-featured app
    uvicorn.run(
        "backend.main_with_supabase:app",
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
