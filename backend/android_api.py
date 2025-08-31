#!/usr/bin/env python3
"""
Klaro Educational Platform - Android Backend API

Simplified, focused backend for Android app development.
Keeps CLI for testing while building mobile experience.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import json
from datetime import datetime
from pathlib import Path
import logging

# Import existing quiz logic
import sys
sys.path.append('..')
try:
    from smart_quiz_generator import SmartTestGenerator
    from book_search import BookVectorDB
except ImportError as e:
    print(f"⚠️ Could not import quiz modules: {e}")
    print("🔧 Will use fallback quiz generation")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Klaro Android API",
    description="Backend API for Klaro Educational Android App",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
quiz_generator: Optional[SmartTestGenerator] = None

# ================================================================================
# 📊 Data Models for Android
# ================================================================================

class QuizRequest(BaseModel):
    topics: List[str]
    num_questions: int = 10
    question_types: List[str] = ["mcq", "short"]
    difficulty_levels: List[str] = ["easy", "medium"]
    title: Optional[str] = None

class QuizResponse(BaseModel):
    quiz_id: str
    title: str
    total_questions: int
    total_points: int
    created_at: str
    download_url: str

class PresetInfo(BaseModel):
    preset_id: str
    name: str
    description: str
    topics: List[str]
    questions: int
    duration: int
    difficulty: List[str]

# ================================================================================
# 🎯 Core Android API Endpoints
# ================================================================================

@app.get("/")
async def root():
    """API welcome message"""
    return {
        "message": "🎓 Klaro Educational Platform API",
        "platform": "Android-focused backend",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "quiz_create": "/quiz/create",
            "quiz_presets": "/quiz/presets"
        }
    }

@app.get("/health")
async def health_check():
    """Health check for Android app"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "quiz_generator": quiz_generator is not None,
            "api_server": True
        }
    }

@app.get("/quiz/presets")
async def get_quiz_presets():
    """Get available quiz presets for Android"""
    
    presets = {
        'algebra_basic': {
            'name': 'Algebra Basics',
            'description': 'Fundamental algebraic concepts',
            'topics': ['polynomials', 'linear equations', 'quadratic equations'],
            'questions': 15,
            'duration': 45,
            'difficulty': ['easy', 'medium']
        },
        'trigonometry': {
            'name': 'Trigonometry',
            'description': 'Trigonometric ratios and applications',
            'topics': ['trigonometry', 'trigonometric ratios'],
            'questions': 10,
            'duration': 60,
            'difficulty': ['medium', 'hard']
        },
        'quick_revision': {
            'name': 'Quick Revision',
            'description': 'Fast review of key concepts',
            'topics': ['quadratic equations', 'triangles'],
            'questions': 20,
            'duration': 30,
            'difficulty': ['easy']
        }
    }
    
    return {"presets": presets}

@app.post("/quiz/create")
async def create_quiz_for_android(quiz_request: QuizRequest):
    """Create quiz for Android app"""
    
    try:
        logger.info(f"📱 Android app creating quiz: {quiz_request.topics}")
        
        if quiz_generator:
            # Use real quiz generator
            test_data = quiz_generator.create_test(
                topics=quiz_request.topics,
                num_questions=quiz_request.num_questions,
                question_types=quiz_request.question_types,
                difficulty_levels=quiz_request.difficulty_levels
            )
            
            quiz_id = f"android_quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            output_prefix = quiz_request.title.replace(' ', '_').lower() if quiz_request.title else quiz_id
            
            test_file, answer_file = quiz_generator.save_test(test_data, output_prefix)
            
            return QuizResponse(
                quiz_id=quiz_id,
                title=quiz_request.title or f"Quiz on {', '.join(quiz_request.topics)}",
                total_questions=test_data['metadata']['total_questions'],
                total_points=test_data['metadata']['total_points'],
                created_at=datetime.now().isoformat(),
                download_url=f"/quiz/{quiz_id}/download"
            )
        else:
            # Fallback for development
            quiz_id = f"demo_quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            return QuizResponse(
                quiz_id=quiz_id,
                title=quiz_request.title or f"Demo Quiz on {', '.join(quiz_request.topics)}",
                total_questions=quiz_request.num_questions,
                total_points=quiz_request.num_questions * 2,
                created_at=datetime.now().isoformat(),
                download_url=f"/quiz/{quiz_id}/download"
            )
            
    except Exception as e:
        logger.error(f"❌ Quiz creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Quiz creation failed: {str(e)}")

@app.get("/quiz/{quiz_id}/download")
async def download_quiz_for_android(quiz_id: str, file_type: str = "questions"):
    """Download quiz files for Android app"""
    
    file_suffix = "_questions.txt" if file_type == "questions" else "_answers.txt"
    file_path = Path("../generated_tests") / f"{quiz_id}{file_suffix}"
    
    if file_path.exists():
        return FileResponse(
            path=file_path,
            filename=f"{quiz_id}_{file_type}.txt",
            media_type="text/plain"
        )
    else:
        # Return demo content for development
        demo_content = f"""
📝 Demo Quiz - {quiz_id}
Generated for Android app testing

Q1. What is a quadratic equation?
A. ax² + bx + c = 0
B. ax + b = 0  
C. ax³ + bx² + c = 0
D. ax⁴ + bx² + c = 0

Q2. Solve: x² - 5x + 6 = 0
Answer: ________________

✅ This is demo content for Android development.
🔄 Real content will be generated when textbook database is ready.
"""
        
        # Save demo file
        file_path.parent.mkdir(exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(demo_content)
        
        return FileResponse(
            path=file_path,
            filename=f"{quiz_id}_{file_type}.txt", 
            media_type="text/plain"
        )

@app.get("/user/dashboard")
async def get_android_dashboard():
    """Get dashboard data for Android app"""
    
    return {
        "welcome_message": "Welcome back! Ready to create some quizzes?",
        "study_streak": 5,
        "recent_quizzes": [
            {"title": "Algebra Practice", "score": 85, "date": "2025-08-29"},
            {"title": "Trigonometry Test", "score": 92, "date": "2025-08-28"}
        ],
        "recommendations": [
            {"topic": "Quadratic Equations", "reason": "Popular this week"},
            {"topic": "Circle Geometry", "reason": "You haven't practiced recently"}
        ],
        "stats": {
            "total_quizzes": 12,
            "average_score": 78.5,
            "favorite_topic": "Algebra"
        }
    }

# ================================================================================
# 🚀 Startup
# ================================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize for Android development"""
    global quiz_generator
    
    logger.info("🚀 Starting Klaro Android Backend...")
    
    try:
        quiz_generator = SmartTestGenerator("../book_db")
        logger.info("✅ Quiz generator ready")
    except Exception as e:
        logger.warning(f"⚠️ Quiz generator not available: {e}")
        logger.info("🔧 Using fallback mode for development")
    
    # Ensure directories exist
    Path("../generated_tests").mkdir(exist_ok=True)
    logger.info("🎉 Android backend ready!")

if __name__ == "__main__":
    print("📱 Klaro Educational Platform - Android Backend")
    print("🎯 Focused on mobile app development")
    print("🌐 API Docs: http://localhost:8000/docs")
    print("🔧 CLI tools still available for testing")
    print("=" * 50)
    
    uvicorn.run(
        "android_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
