#!/usr/bin/env python3
"""
🚀 Klaro Doubt Solving API Server

FastAPI backend with:
- Doubt solving endpoints (text + image)
- User management & authentication
- Usage analytics & subscription management
- WhatsApp webhook integration
- Production-ready error handling
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import asyncio
import base64
import json
import os
from pathlib import Path

# Import our production doubt engine
from doubt_solving_engine_production import ProductionDoubtSolvingEngine, DoubtRequest, DoubtSolution, EnhancedDoubtAnalytics

# Database imports (we'll implement PostgreSQL next)
import sqlite3  # Temporary - will replace with PostgreSQL
import aiosqlite

app = FastAPI(
    title="Klaro Doubt Solving API",
    description="AI-powered educational doubt solving with cost optimization",
    version="1.0.0"
)

# CORS middleware for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global engine instance
doubt_engine: Optional[ProductionDoubtSolvingEngine] = None
analytics: Optional[EnhancedDoubtAnalytics] = None

# ================================================================================
# 📋 Pydantic Models
# ================================================================================

class TextDoubtRequest(BaseModel):
    question: str = Field(..., description="The doubt question text")
    subject: str = Field(default="Mathematics", description="Subject area")
    context: Optional[str] = Field(None, description="Additional context")

class DoubtResponse(BaseModel):
    question: str
    answer: str
    steps: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    mobile_format: Dict[str, Any]
    whatsapp_format: str

class UserAnalytics(BaseModel):
    user_metrics: Dict[str, Any]
    insights: Dict[str, Any]
    recommendations: List[str]
    cost_efficiency: Dict[str, Any]

class SubscriptionUpgrade(BaseModel):
    plan: str = Field(..., description="Target plan: basic or premium")
    payment_method: str = Field(..., description="Payment method")

class WhatsAppMessage(BaseModel):
    from_number: str
    message_text: Optional[str] = None
    media_url: Optional[str] = None
    message_type: str = "text"

# ================================================================================
# 🔐 Authentication & User Management
# ================================================================================

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Extract user info from JWT token - placeholder implementation"""
    
    # In production, verify JWT token here
    token = credentials.credentials
    
    # Mock user for development
    return {
        "user_id": "user_123",
        "plan": "basic",
        "name": "Test User",
        "email": "test@example.com"
    }

# ================================================================================
# 🚀 Startup & Configuration
# ================================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize the doubt solving engine on startup"""
    global doubt_engine, analytics
    
    # Load configuration from environment
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "wolfram_api_key": os.getenv("WOLFRAM_API_KEY"),
        "mathpix_api_key": os.getenv("MATHPIX_API_KEY"),
        "mathpix_api_secret": os.getenv("MATHPIX_API_SECRET"),
        "openai_timeout": 25.0,  # WhatsApp-friendly timeout
        "wolfram_timeout": 12.0,
        "mathpix_timeout": 18.0
    }
    
    # Initialize engine
    doubt_engine = ProductionDoubtSolvingEngine(config)
    analytics = EnhancedDoubtAnalytics(doubt_engine.usage_db, doubt_engine.route_analytics)
    
    print("🚀 Klaro API Server started successfully!")

# ================================================================================
# 📝 Doubt Solving Endpoints
# ================================================================================

@app.post("/api/v1/doubts/text", response_model=DoubtResponse)
async def solve_text_doubt(
    request: TextDoubtRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Solve text-based doubt"""
    
    if not doubt_engine:
        raise HTTPException(status_code=500, detail="Doubt engine not initialized")
    
    doubt_request = DoubtRequest(
        question_text=request.question,
        subject=request.subject,
        user_id=user["user_id"],
        user_plan=user["plan"],
        context=request.context,
        route="doubts"
    )
    
    try:
        solution = await doubt_engine.solve_doubt(doubt_request)
        
        return DoubtResponse(
            question=solution.question,
            answer=solution.final_answer,
            steps=[{
                "step_number": step.step_number,
                "title": step.title,
                "explanation": step.explanation,
                "confidence": step.confidence
            } for step in solution.steps],
            metadata={
                "topic": solution.topic,
                "difficulty": solution.difficulty,
                "confidence": solution.confidence_score,
                "method": solution.solution_method,
                "cost": solution.cost_incurred,
                "time_taken": solution.time_taken,
                "retry_attempts": solution.retry_attempts
            },
            mobile_format=solution.mobile_format or {},
            whatsapp_format=solution.whatsapp_format
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error solving doubt: {str(e)}")

@app.post("/api/v1/doubts/image", response_model=DoubtResponse)
async def solve_image_doubt(
    file: UploadFile = File(...),
    subject: str = Form(default="Mathematics"),
    context: Optional[str] = Form(None),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Solve image-based doubt using OCR"""
    
    if not doubt_engine:
        raise HTTPException(status_code=500, detail="Doubt engine not initialized")
    
    # Read image data
    image_data = await file.read()
    
    doubt_request = DoubtRequest(
        image_data=image_data,
        subject=subject,
        user_id=user["user_id"],
        user_plan=user["plan"],
        context=context,
        route="doubts"
    )
    
    try:
        solution = await doubt_engine.solve_doubt(doubt_request)
        
        return DoubtResponse(
            question=solution.question,
            answer=solution.final_answer,
            steps=[{
                "step_number": step.step_number,
                "title": step.title,
                "explanation": step.explanation,
                "confidence": step.confidence
            } for step in solution.steps],
            metadata={
                "topic": solution.topic,
                "difficulty": solution.difficulty,
                "confidence": solution.confidence_score,
                "method": solution.solution_method,
                "cost": solution.cost_incurred,
                "time_taken": solution.time_taken,
                "retry_attempts": solution.retry_attempts
            },
            mobile_format=solution.mobile_format or {},
            whatsapp_format=solution.whatsapp_format
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error solving image doubt: {str(e)}")

# ================================================================================
# 📊 Analytics Endpoints
# ================================================================================

@app.get("/api/v1/analytics/user", response_model=UserAnalytics)
async def get_user_analytics(user: Dict[str, Any] = Depends(get_current_user)):
    """Get detailed user analytics"""
    
    if not analytics:
        raise HTTPException(status_code=500, detail="Analytics not initialized")
    
    try:
        user_analytics = analytics.get_comprehensive_analytics(user["user_id"])
        
        return UserAnalytics(
            user_metrics=user_analytics["user_metrics"],
            insights=user_analytics["insights"],
            recommendations=user_analytics["recommendations"],
            cost_efficiency=user_analytics["cost_efficiency"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting analytics: {str(e)}")

@app.get("/api/v1/analytics/routes")
async def get_route_analytics(user: Dict[str, Any] = Depends(get_current_user)):
    """Get route-level analytics"""
    
    if not doubt_engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    try:
        route_data = doubt_engine.get_route_analytics()
        return route_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting route analytics: {str(e)}")

# ================================================================================
# 💳 Subscription Management
# ================================================================================

@app.post("/api/v1/subscription/upgrade")
async def upgrade_subscription(
    upgrade: SubscriptionUpgrade,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Upgrade user subscription"""
    
    # In production, integrate with payment gateway
    try:
        # Mock subscription upgrade
        return {
            "success": True,
            "message": f"Successfully upgraded to {upgrade.plan}",
            "new_plan": upgrade.plan,
            "benefits": [
                "Unlimited doubts" if upgrade.plan == "premium" else "20 doubts/month",
                "GPT-4 solutions" if upgrade.plan == "premium" else "GPT-3.5 solutions",
                "OCR support",
                "Priority support" if upgrade.plan == "premium" else "Standard support"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error upgrading subscription: {str(e)}")

@app.get("/api/v1/subscription/status")
async def get_subscription_status(user: Dict[str, Any] = Depends(get_current_user)):
    """Get current subscription status"""
    
    # Mock subscription status
    return {
        "user_id": user["user_id"],
        "plan": user["plan"],
        "doubts_remaining": 15 if user["plan"] == "basic" else "unlimited",
        "renewal_date": (datetime.now() + timedelta(days=20)).isoformat(),
        "features": {
            "unlimited_doubts": user["plan"] == "premium",
            "gpt4_access": user["plan"] == "premium",
            "ocr_support": True,
            "priority_support": user["plan"] == "premium"
        }
    }

# ================================================================================
# 📱 WhatsApp Bot Webhook
# ================================================================================

@app.post("/api/v1/whatsapp/webhook")
async def whatsapp_webhook(message: WhatsAppMessage):
    """Handle incoming WhatsApp messages"""
    
    if not doubt_engine:
        raise HTTPException(status_code=500, detail="Doubt engine not initialized")
    
    try:
        # Extract user info from phone number
        user_id = f"whatsapp_{message.from_number}"
        
        # Create doubt request
        doubt_request = DoubtRequest(
            question_text=message.message_text,
            user_id=user_id,
            user_plan="basic",  # WhatsApp users start with basic
            route="whatsapp"
        )
        
        # Solve doubt
        solution = await doubt_engine.solve_doubt(doubt_request)
        
        # Return WhatsApp-formatted response
        return {
            "to": message.from_number,
            "message": solution.whatsapp_format,
            "message_type": "text"
        }
        
    except Exception as e:
        return {
            "to": message.from_number,
            "message": "Sorry, I'm having trouble right now. Please try again later.",
            "message_type": "text"
        }

# ================================================================================
# 🧪 Test & Practice Endpoints
# ================================================================================

@app.post("/api/v1/tests/solve")
async def solve_test_question(
    request: TextDoubtRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Solve test/exam questions"""
    
    if not doubt_engine:
        raise HTTPException(status_code=500, detail="Doubt engine not initialized")
    
    doubt_request = DoubtRequest(
        question_text=request.question,
        subject=request.subject,
        user_id=user["user_id"],
        user_plan=user["plan"],
        route="tests"
    )
    
    solution = await doubt_engine.solve_doubt(doubt_request)
    
    return {
        "question": solution.question,
        "answer": solution.final_answer,
        "steps": solution.steps,
        "metadata": {
            "topic": solution.topic,
            "difficulty": solution.difficulty,
            "method": solution.solution_method
        }
    }

@app.get("/api/v1/practice/generate")
async def generate_practice_problems(
    topic: str,
    difficulty: str = "medium",
    count: int = 5,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate practice problems for a topic"""
    
    # Mock practice problems - in production, use AI to generate
    practice_problems = [
        {
            "id": f"practice_{i}",
            "question": f"Practice {topic} problem {i}",
            "difficulty": difficulty,
            "topic": topic,
            "hints": [f"Hint {j} for problem {i}" for j in range(1, 3)]
        }
        for i in range(1, count + 1)
    ]
    
    return {
        "topic": topic,
        "difficulty": difficulty,
        "problems": practice_problems,
        "total_count": count
    }

# ================================================================================
# 👤 User Management
# ================================================================================

@app.get("/api/v1/user/profile")
async def get_user_profile(user: Dict[str, Any] = Depends(get_current_user)):
    """Get user profile information"""
    
    return {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "plan": user["plan"],
        "joined_date": "2024-01-15",  # Mock data
        "total_doubts_solved": 45,
        "favorite_subjects": ["Mathematics", "Physics"],
        "achievements": [
            {"name": "First Doubt", "earned": "2024-01-15"},
            {"name": "Problem Solver", "earned": "2024-02-01"}
        ]
    }

@app.put("/api/v1/user/profile")
async def update_user_profile(
    profile_data: Dict[str, Any],
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Update user profile"""
    
    # In production, validate and update database
    return {
        "success": True,
        "message": "Profile updated successfully",
        "updated_fields": list(profile_data.keys())
    }

# ================================================================================
# 📚 History & Saved Doubts
# ================================================================================

@app.get("/api/v1/doubts/history")
async def get_doubt_history(
    limit: int = 20,
    offset: int = 0,
    subject: Optional[str] = None,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get user's doubt solving history"""
    
    # Mock history data - in production, query database
    mock_history = [
        {
            "id": f"doubt_{i}",
            "question": f"Sample question {i}",
            "answer": f"Sample answer {i}",
            "subject": subject or "Mathematics",
            "solved_at": (datetime.now() - timedelta(days=i)).isoformat(),
            "method": "gpt35",
            "topic": "Algebra"
        }
        for i in range(1, limit + 1)
    ]
    
    return {
        "doubts": mock_history,
        "total_count": 100,  # Mock total
        "has_more": offset + limit < 100
    }

@app.post("/api/v1/doubts/{doubt_id}/save")
async def save_doubt(
    doubt_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Save a doubt to favorites"""
    
    return {
        "success": True,
        "message": "Doubt saved to favorites",
        "doubt_id": doubt_id
    }

# ================================================================================
# 🏥 Health Check & System Status
# ================================================================================

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "doubt_engine": doubt_engine is not None,
            "analytics": analytics is not None,
            "database": True  # Will check actual DB connection in production
        }
    }

@app.get("/api/v1/system/stats")
async def get_system_stats():
    """Get system-wide statistics"""
    
    if not doubt_engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    route_stats = doubt_engine.get_route_analytics()
    
    return {
        "total_requests_today": route_stats.get("total_requests", 0),
        "total_cost_today": route_stats.get("total_cost", 0.0),
        "success_rate": route_stats.get("overall_success_rate", 0.0),
        "active_routes": list(route_stats.get("current_month_routes", {}).keys()),
        "ai_methods_used": {
            "textbook": "Free textbook search",
            "wolfram": "Computational ($0.0025)",
            "gpt35": "Basic AI ($0.004)",
            "gpt4": "Premium AI ($0.09)"
        }
    }

# ================================================================================
# 🎯 Specialized Endpoints
# ================================================================================

@app.post("/api/v1/papers/solve")
async def solve_previous_paper(
    request: TextDoubtRequest,
    paper_year: int = Form(...),
    exam_board: str = Form(...),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Solve previous year paper questions"""
    
    if not doubt_engine:
        raise HTTPException(status_code=500, detail="Doubt engine not initialized")
    
    # Add paper context to the request
    enhanced_context = f"Previous {exam_board} paper ({paper_year}). {request.context or ''}"
    
    doubt_request = DoubtRequest(
        question_text=request.question,
        subject=request.subject,
        user_id=user["user_id"],
        user_plan=user["plan"],
        context=enhanced_context,
        route="papers"
    )
    
    solution = await doubt_engine.solve_doubt(doubt_request)
    
    return {
        "question": solution.question,
        "answer": solution.final_answer,
        "steps": solution.steps,
        "paper_info": {
            "year": paper_year,
            "exam_board": exam_board,
            "difficulty": solution.difficulty
        },
        "metadata": {
            "topic": solution.topic,
            "method": solution.solution_method
        }
    }

# ================================================================================
# 🚨 Error Handlers
# ================================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    
    return {
        "error": True,
        "message": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    
    return {
        "error": True,
        "message": "Internal server error occurred",
        "status_code": 500,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
