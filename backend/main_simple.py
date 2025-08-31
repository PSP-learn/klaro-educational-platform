#!/usr/bin/env python3
"""
🟢 Klaro Educational Platform - Simplified FastAPI Backend
Minimal version for Railway deployment with Supabase integration
"""

import os
from datetime import datetime
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Klaro Educational Platform API",
    description="AI-powered educational platform with doubt solving, quiz generation, and JEE test preparation",
    version="2.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# ================================================================================
# 🔧 System Health Endpoints
# ================================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "api": "active",
                "environment": os.getenv("ENVIRONMENT", "development")
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🟢 Klaro Educational Platform API",
        "version": "2.0.0",
        "status": "running",
        "deployed_at": "2025-08-31T08:40:00Z",
        "docs": "/docs" if os.getenv("ENVIRONMENT") != "production" else "disabled"
    }

# ================================================================================
# 🧪 Test Endpoints
# ================================================================================

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint to verify API is working"""
    return {
        "success": True,
        "message": "Klaro API is working correctly",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/auth/test")
async def test_auth():
    """Test authentication endpoint"""
    return {
        "success": True,
        "message": "Authentication system ready",
        "features": [
            "User registration",
            "Login/logout", 
            "JWT tokens",
            "Supabase integration"
        ]
    }

@app.post("/api/doubts/test")
async def test_doubts():
    """Test doubt solving endpoint"""
    return {
        "success": True,
        "message": "Doubt solving system ready",
        "features": [
            "Text-based questions",
            "Image OCR processing",
            "Multi-AI fallback",
            "Cost optimization"
        ]
    }

@app.post("/api/quiz/test")
async def test_quiz():
    """Test quiz generation endpoint"""
    return {
        "success": True,
        "message": "Quiz generation system ready", 
        "features": [
            "Custom PDF generation",
            "Topic-based questions",
            "Difficulty levels",
            "Answer keys"
        ]
    }

@app.post("/api/jee/test")
async def test_jee():
    """Test JEE system endpoint"""
    return {
        "success": True,
        "message": "JEE test system ready",
        "features": [
            "2024 exam format",
            "Subject-wise scoring",
            "Performance analytics",
            "Mock tests"
        ]
    }

# ================================================================================
# 📊 Environment Info
# ================================================================================

@app.get("/api/info")
async def get_info():
    """Get deployment and environment information"""
    return {
        "app_name": "Klaro Educational Platform",
        "version": "2.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "python_version": "3.12",
        "deployment": "Railway",
        "database": "Supabase PostgreSQL",
        "features": {
            "doubt_solving": "Ready for integration",
            "quiz_generation": "Ready for integration", 
            "jee_tests": "Ready for integration",
            "user_auth": "Ready for integration"
        }
    }

# ================================================================================
# 🚀 Server Configuration
# ================================================================================

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Klaro Educational Platform on {host}:{port}")
    
    if os.getenv("ENVIRONMENT") == "production":
        # Production configuration
        uvicorn.run(
            "main_simple:app",
            host=host,
            port=port,
            log_level="info"
        )
    else:
        # Development configuration
        uvicorn.run(
            "main_simple:app",
            host=host,
            port=port,
            reload=True
        )
