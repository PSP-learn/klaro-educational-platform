#!/usr/bin/env python3
"""
Klaro Educational Platform - Android Backend API

Focused backend API server for Android app with quiz generation and educational features.
Built with FastAPI for high performance. CLI maintained for testing.
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import uvicorn
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Import our existing quiz generation logic
import sys
sys.path.append('..')
from smart_quiz_generator import SmartTestGenerator
from book_search import BookVectorDB

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Klaro Educational Platform API",
    description="Unified backend for quiz generation, textbook management, and educational assistance",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration for mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global instances
quiz_generator: Optional[SmartTestGenerator] = None
book_db: Optional[BookVectorDB] = None

# ================================================================================
# 📊 Data Models (API Request/Response Schemas)
# ================================================================================

class UserProfile(BaseModel):
    user_id: str
    email: EmailStr
    name: str
    grade_level: Optional[str] = None
    subjects: List[str] = []
    created_at: datetime

class QuizRequest(BaseModel):
    topics: List[str]
    num_questions: int = 10
    question_types: List[str] = ["mcq", "short"]
    difficulty_levels: List[str] = ["easy", "medium"]
    subject: str = "Mathematics"
    duration: Optional[int] = None
    title: Optional[str] = None

class QuizResponse(BaseModel):
    quiz_id: str
    title: str
    questions_file: str
    answers_file: str
    pdf_questions_file: Optional[str] = None
    pdf_answers_file: Optional[str] = None
    metadata: Dict[str, Any]
    created_at: datetime

class DoubtRequest(BaseModel):
    question: str
    subject: str = "Mathematics"
    grade_level: Optional[str] = None
    context: Optional[str] = None

class DoubtResponse(BaseModel):
    answer: str
    explanation: str
    related_topics: List[str]
    practice_suggestions: List[str]
    confidence_score: float

# ================================================================================
# 🔧 Startup and Initialization
# ================================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize the application components"""
    global quiz_generator, book_db
    
    logger.info("🚀 Starting Klaro Educational Platform...")
    
    # Initialize quiz generator
    try:
        quiz_generator = SmartTestGenerator("../book_db")
        logger.info("✅ Quiz generator initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize quiz generator: {e}")
    
    # Initialize book database
    try:
        book_db = BookVectorDB("../book_db")
        logger.info("✅ Book database initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize book database: {e}")
    
    # Create necessary directories
    Path("../generated_tests").mkdir(exist_ok=True)
    Path("../uploads").mkdir(exist_ok=True)
    
    logger.info("🎉 Klaro Educational Platform is ready!")

# ================================================================================
# 🔐 Authentication (Simplified for now)
# ================================================================================

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user (simplified implementation)"""
    # TODO: Implement proper JWT token validation
    # For now, return a mock user
    return {"user_id": "demo_user", "name": "Demo User"}

# ================================================================================
# 🎯 Quiz Generation Endpoints
# ================================================================================

@app.post("/api/quiz/create", response_model=QuizResponse)
async def create_quiz(
    quiz_request: QuizRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Create a new quiz based on user specifications"""
    
    if not quiz_generator:
        raise HTTPException(status_code=500, detail="Quiz generator not available")
    
    try:
        logger.info(f"Creating quiz for user {current_user['user_id']}")
        
        # Generate quiz using existing logic
        test_data = quiz_generator.create_test(
            topics=quiz_request.topics,
            num_questions=quiz_request.num_questions,
            question_types=quiz_request.question_types,
            difficulty_levels=quiz_request.difficulty_levels,
            subject=quiz_request.subject
        )
        
        # Generate unique quiz ID
        quiz_id = f"quiz_{current_user['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # Always use quiz_id as filename prefix to ensure downloads work
        output_prefix = quiz_id
        
        # Save files (TXT)
        test_file, answer_file = quiz_generator.save_test(test_data, output_prefix)
        
        # Also generate PDFs
        try:
            from smart_quiz_generator import SmartTestGenerator
            pdf_q, pdf_a = quiz_generator.save_test_pdf(test_data, output_prefix)
        except Exception as _e:
            pdf_q, pdf_a = None, None
        
        # Create response
        quiz_response = QuizResponse(
            quiz_id=quiz_id,
            title=quiz_request.title or f"Quiz on {', '.join(quiz_request.topics)}",
            questions_file=test_file,
            answers_file=answer_file,
            pdf_questions_file=pdf_q,
            pdf_answers_file=pdf_a,
            metadata=test_data['metadata'],
            created_at=datetime.now()
        )
        
        logger.info(f"✅ Quiz {quiz_id} created successfully")
        return quiz_response
        
    except Exception as e:
        logger.error(f"❌ Quiz creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Quiz creation failed: {str(e)}")

@app.get("/api/quiz/presets")
async def get_quiz_presets():
    """Get available quiz presets"""
    
    presets = {
        'class_10_algebra_basic': {
            'name': 'Class 10 - Algebra Basics',
            'description': 'Fundamental algebraic concepts',
            'topics': ['polynomials', 'linear equations', 'quadratic equations'],
            'types': ['mcq', 'short'],
            'difficulty': ['easy', 'medium'],
            'questions': 15,
            'duration': 45
        },
        'class_10_trigonometry': {
            'name': 'Class 10 - Trigonometry',
            'description': 'Trigonometric ratios and applications',
            'topics': ['trigonometry', 'trigonometric ratios'],
            'types': ['mcq', 'short'],
            'difficulty': ['medium', 'hard'],
            'questions': 10,
            'duration': 60
        },
        'quick_revision': {
            'name': 'Quick Revision Test',
            'description': 'Fast review of key concepts',
            'topics': ['quadratic equations', 'triangles', 'trigonometry'],
            'types': ['mcq'],
            'difficulty': ['easy'],
            'questions': 20,
            'duration': 30
        }
    }
    
    return {"presets": presets}

@app.post("/api/quiz/preset/{preset_name}")
async def create_quiz_from_preset(
    preset_name: str,
    current_user: dict = Depends(get_current_user)
):
    """Create quiz from a preset configuration"""
    
    presets_response = await get_quiz_presets()
    presets = presets_response["presets"]
    
    if preset_name not in presets:
        raise HTTPException(status_code=404, detail=f"Preset '{preset_name}' not found")
    
    preset = presets[preset_name]
    
    # Convert preset to QuizRequest
    quiz_request = QuizRequest(
        topics=preset['topics'],
        num_questions=preset['questions'],
        question_types=preset['types'],
        difficulty_levels=preset['difficulty'],
        duration=preset['duration'],
        title=preset['name']
    )
    
    return await create_quiz(quiz_request, BackgroundTasks(), current_user)

@app.get("/api/quiz/{quiz_id}/download")
async def download_quiz(
    quiz_id: str,
    file_type: str = "questions",  # "questions" or "answers"
    current_user: dict = Depends(get_current_user)
):
    """Download quiz file. Prefers PDF if available; falls back to TXT."""
    base_dir = Path("../generated_tests")
    # Prefer PDF
    pdf_suffix = "_questions.pdf" if file_type == "questions" else "_answers.pdf"
    txt_suffix = "_questions.txt" if file_type == "questions" else "_answers.txt"
    pdf_path = base_dir / f"{quiz_id}{pdf_suffix}"
    txt_path = base_dir / f"{quiz_id}{txt_suffix}"

    if pdf_path.exists():
        return FileResponse(
            path=pdf_path,
            filename=f"{quiz_id}_{file_type}.pdf",
            media_type="application/pdf"
        )
    if txt_path.exists():
        return FileResponse(
            path=txt_path,
            filename=f"{quiz_id}_{file_type}.txt",
            media_type="text/plain"
        )
    raise HTTPException(status_code=404, detail="Quiz file not found")

# ================================================================================
# 🤖 Enhanced Doubt Solving Endpoints
# ================================================================================

# Import enhanced doubt solving system
try:
    from doubt_solving_engine import DoubtSolvingEngine, DoubtRequest as EnhancedDoubtRequest, DoubtAnalytics
    doubt_engine: Optional[DoubtSolvingEngine] = None
    doubt_analytics: Optional[DoubtAnalytics] = None
except ImportError:
    logger.warning("⚠️ Enhanced doubt solving engine not available")
    doubt_engine = None
    doubt_analytics = None

class EnhancedDoubtRequest(BaseModel):
    question: str
    subject: str = "Mathematics"
    user_id: str
    user_plan: str = "basic"
    context: Optional[str] = None
    image_data: Optional[str] = None  # Base64 encoded image

class EnhancedDoubtResponse(BaseModel):
    success: bool
    solution: Optional[Dict[str, Any]] = None
    usage_info: Optional[Dict[str, Any]] = None
    cost_info: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.on_event("startup")
async def init_doubt_engine():
    """Initialize enhanced doubt solving engine"""
    global doubt_engine, doubt_analytics
    
    if DoubtSolvingEngine:
        try:
            config = {
                "openai_api_key": None,  # Set from environment
                "wolfram_api_key": None,  # Set from environment
                "mathpix_api_key": None,
                "mathpix_api_secret": None
            }
            
            doubt_engine = DoubtSolvingEngine(config)
            doubt_analytics = DoubtAnalytics(doubt_engine.usage_db)
            logger.info("✅ Enhanced doubt solving engine initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize doubt engine: {e}")

@app.post("/api/doubt/solve", response_model=DoubtResponse)
async def solve_doubt(doubt_request: DoubtRequest):
    """Legacy doubt solving endpoint (basic functionality)"""
    
    if not book_db:
        raise HTTPException(status_code=500, detail="Knowledge base not available")
    
    try:
        # Search for relevant content
        results = book_db.search(doubt_request.question, top_k=5)
        
        if not results:
            return DoubtResponse(
                answer="I'd be happy to help! Could you provide more context?",
                explanation="I couldn't find specific content in the textbook database.",
                related_topics=[],
                practice_suggestions=["Try rephrasing with more specific terms"],
                confidence_score=0.3
            )
        
        best_result = results[0]
        content = best_result[0]
        
        return DoubtResponse(
            answer=f"Based on textbook: {content[:200]}...",
            explanation=f"Reference content: {content[:300]}...",
            related_topics=doubt_request.question.split()[:3],
            practice_suggestions=["Try solving similar problems", "Review the concept"],
            confidence_score=best_result[1]
        )
        
    except Exception as e:
        logger.error(f"❌ Basic doubt solving failed: {e}")
        raise HTTPException(status_code=500, detail="Doubt solving failed")

@app.post("/api/doubt/solve-enhanced", response_model=EnhancedDoubtResponse)
async def solve_doubt_enhanced(request: EnhancedDoubtRequest):
    """Enhanced AI-powered doubt solving with usage limits"""
    
    if not doubt_engine:
        # Fallback to basic doubt solving
        basic_request = DoubtRequest(
            question=request.question,
            subject=request.subject
        )
        basic_response = await solve_doubt(basic_request)
        
        return EnhancedDoubtResponse(
            success=True,
            solution={
                "answer": basic_response.answer,
                "explanation": basic_response.explanation,
                "method": "textbook_fallback"
            },
            usage_info={"note": "Using basic mode - enhanced AI not available"}
        )
    
    try:
        # Create enhanced doubt request
        doubt_request = EnhancedDoubtRequest(
            question_text=request.question,
            subject=request.subject,
            user_id=request.user_id,
            user_plan=request.user_plan,
            context=request.context
        )
        
        # Add image data if provided
        if request.image_data:
            import base64
            doubt_request.image_data = base64.b64decode(request.image_data)
        
        # Solve the doubt
        solution = await doubt_engine.solve_doubt(doubt_request)
        
        # Get usage information
        usage_check = await doubt_engine._check_usage_limits(request.user_id, request.user_plan)
        
        return EnhancedDoubtResponse(
            success=True,
            solution=solution.mobile_format,
            usage_info={
                "remaining_doubts": usage_check["remaining"],
                "used_this_month": usage_check["used"],
                "plan": usage_check["plan"],
                "reset_date": str(usage_check["reset_date"])
            },
            cost_info={
                "method_used": solution.solution_method,
                "cost_incurred": solution.cost_incurred,
                "time_taken": solution.time_taken
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Enhanced doubt solving failed: {e}")
        return EnhancedDoubtResponse(
            success=False,
            error=f"Failed to solve doubt: {str(e)}"
        )

@app.post("/api/doubt/solve-image")
async def solve_doubt_from_image(
    file: UploadFile = File(...),
    user_id: str = "demo_user",
    user_plan: str = "basic",
    subject: str = "Mathematics"
):
    """Solve doubt from uploaded image using OCR"""
    
    if not doubt_engine:
        raise HTTPException(status_code=500, detail="Enhanced doubt engine not available")
    
    try:
        # Read and validate image
        image_data = await file.read()
        
        if len(image_data) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="Image too large (max 10MB)")
        
        # Create doubt request
        doubt_request = EnhancedDoubtRequest(
            image_data=image_data,
            subject=subject,
            user_id=user_id,
            user_plan=user_plan
        )
        
        # Solve the doubt
        solution = await doubt_engine.solve_doubt(doubt_request)
        
        return {
            "success": True,
            "extracted_text": solution.question,
            "solution": solution.mobile_format,
            "cost_info": {
                "method": solution.solution_method,
                "cost": solution.cost_incurred,
                "ocr_used": True
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Image doubt solving failed: {e}")
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

@app.get("/api/doubt/usage/{user_id}")
async def get_doubt_usage(user_id: str):
    """Get user's doubt usage statistics"""
    
    if not doubt_analytics:
        return {"error": "Analytics not available"}
    
    try:
        analytics_data = doubt_analytics.get_user_analytics(user_id)
        return analytics_data
        
    except Exception as e:
        logger.error(f"❌ Failed to get usage data: {e}")
        raise HTTPException(status_code=500, detail="Failed to get usage data")

# ================================================================================
# 📚 Textbook Management Endpoints
# ================================================================================

@app.post("/api/textbooks/upload")
async def upload_textbook(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload and process a new textbook"""
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save uploaded file
        upload_dir = Path("../uploads")
        file_path = upload_dir / f"{current_user['user_id']}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # TODO: Process PDF and add to vector database
        # This would run in background
        
        return {
            "message": "Textbook uploaded successfully",
            "file_path": str(file_path),
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"❌ Textbook upload failed: {e}")
        raise HTTPException(status_code=500, detail="Textbook upload failed")

@app.get("/api/textbooks/search")
async def search_textbooks(
    query: str,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Search through textbook content"""
    
    if not book_db:
        raise HTTPException(status_code=500, detail="Book database not available")
    
    try:
        results = book_db.search(query, top_k=limit)
        
        formatted_results = []
        for content, score in results:
            formatted_results.append({
                "content": content[:300] + "..." if len(content) > 300 else content,
                "relevance_score": score,
                "preview": content[:100] + "..."
            })
        
        return {
            "query": query,
            "results": formatted_results,
            "total_found": len(results)
        }
        
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

# ================================================================================
# 👤 User Management Endpoints
# ================================================================================

@app.post("/api/auth/register")
async def register_user(email: EmailStr, name: str, password: str):
    """Register a new user"""
    # TODO: Implement proper user registration with password hashing
    return {
        "message": "User registered successfully",
        "user_id": f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "status": "active"
    }

@app.post("/api/auth/login")
async def login_user(email: EmailStr, password: str):
    """User login"""
    # TODO: Implement proper authentication
    return {
        "access_token": "demo_token_123",
        "token_type": "bearer",
        "user_id": "demo_user"
    }

@app.get("/api/user/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get user profile information"""
    return {
        "user_id": current_user["user_id"],
        "name": current_user["name"],
        "email": "demo@example.com",
        "grade_level": "Class 10",
        "subjects": ["Mathematics", "Physics"],
        "quiz_count": 15,
        "total_points": 1250
    }

@app.get("/api/user/quizzes")
async def get_user_quizzes(current_user: dict = Depends(get_current_user)):
    """Get user's quiz history"""
    
    # Get recent quiz files
    quiz_dir = Path("../generated_tests")
    if not quiz_dir.exists():
        return {"quizzes": []}
    
    quiz_files = list(quiz_dir.glob("*_questions.txt"))
    quiz_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    
    quizzes = []
    for quiz_file in quiz_files[:10]:  # Last 10 quizzes
        quiz_name = quiz_file.stem.replace('_questions', '')
        metadata_file = quiz_file.parent / f"{quiz_name}_metadata.json"
        
        quiz_info = {
            "quiz_id": quiz_name,
            "title": quiz_name.replace('_', ' ').title(),
            "created_at": datetime.fromtimestamp(quiz_file.stat().st_mtime).isoformat(),
            "file_path": str(quiz_file)
        }
        
        # Load metadata if available
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                quiz_info.update({
                    "total_questions": metadata.get('total_questions', 0),
                    "total_points": metadata.get('total_points', 0),
                    "duration": metadata.get('duration', 30)
                })
            except Exception:
                pass
        
        quizzes.append(quiz_info)
    
    return {"quizzes": quizzes}

# ================================================================================
# 📊 Analytics and Statistics Endpoints
# ================================================================================

@app.get("/api/analytics/dashboard")
async def get_dashboard_analytics(current_user: dict = Depends(get_current_user)):
    """Get dashboard analytics for mobile apps"""
    
    return {
        "user_stats": {
            "total_quizzes_created": 15,
            "total_quizzes_taken": 12,
            "average_score": 78.5,
            "study_streak": 7,
            "favorite_topics": ["Algebra", "Geometry", "Trigonometry"]
        },
        "recent_activity": [
            {"action": "Created quiz", "topic": "Quadratic Equations", "date": "2025-08-30"},
            {"action": "Completed test", "score": 85, "date": "2025-08-29"},
            {"action": "Asked doubt", "topic": "Trigonometry", "date": "2025-08-29"}
        ],
        "recommendations": [
            {"type": "practice", "topic": "Polynomial Factorization", "reason": "Low recent scores"},
            {"type": "revision", "topic": "Circle Geometry", "reason": "Haven't practiced recently"},
            {"type": "challenge", "topic": "Advanced Algebra", "reason": "Ready for next level"}
        ]
    }

# ================================================================================
# 🎯 Health Check and Status Endpoints
# ================================================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "quiz_generator": quiz_generator is not None,
            "book_database": book_db is not None
        }
    }

@app.get("/api/status")
async def get_system_status():
    """Get detailed system status"""
    
    status = {
        "platform": "Klaro Educational Platform",
        "version": "1.0.0",
        "uptime": "Just started",
        "active_users": 1,
        "total_quizzes": len(list(Path("../generated_tests").glob("*_questions.txt"))) if Path("../generated_tests").exists() else 0
    }
    
    if book_db:
        try:
            # Get database stats
            status["textbook_database"] = {
                "total_books": "Available",
                "total_chunks": "Available", 
                "status": "Active"
            }
        except Exception:
            status["textbook_database"] = {"status": "Error"}
    
    return status

# ================================================================================
# 🚀 Main Application Entry Point
# ================================================================================

if __name__ == "__main__":
    print("🎓 Starting Klaro Educational Platform Backend...")
    print("📱 Supporting: Android App, iOS App, WhatsApp Bot")
    print("🌐 API Documentation: http://localhost:8000/api/docs")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
