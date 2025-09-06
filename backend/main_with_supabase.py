#!/usr/bin/env python3
"""
🟢 Klaro Educational Platform - FastAPI Backend with Supabase Integration

Hybrid Architecture:
- Supabase: User auth, data storage, file storage
- Railway: AI processing, quiz generation, doubt solving
- FastAPI: API orchestration layer
"""

import os
import time
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    from pathlib import Path
    # Load from current working directory/root
    load_dotenv()
    # Also load backend/.env explicitly if present
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
except Exception:
    pass

# Import existing modules with fallbacks
try:
    from doubt_solver import DoubtSolverEngine
    DOUBT_SOLVER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Doubt solver not available: {e}")
    DOUBT_SOLVER_AVAILABLE = False
    DoubtSolverEngine = None

try:
    from pdf_quiz_generator import PDFQuizGenerator
    PDF_GENERATOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ PDF generator not available: {e}")
    PDF_GENERATOR_AVAILABLE = False
    PDFQuizGenerator = None

try:
    from jee_backend_wrapper import JEETestSystem
    JEE_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ JEE system not available: {e}")
    JEE_SYSTEM_AVAILABLE = False
    JEETestSystem = None

# Import new Supabase integration
try:
    # Use relative import so it works when running as a package (backend.main_with_supabase)
    from .supabase_client import get_supabase_client, SupabaseClient
    SUPABASE_CLIENT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Supabase client not available: {e}")
    SUPABASE_CLIENT_AVAILABLE = False
    get_supabase_client = None
    SupabaseClient = None

# ================================================================================
# 🚀 FastAPI App Configuration
# ================================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle app startup and shutdown"""
    print("🟢 Starting Klaro Educational Platform...")
    
    # Initialize all systems
    global doubt_solver, quiz_generator, jee_system, supabase_client
    
    try:
        # Initialize AI services (with fallbacks)
        if DOUBT_SOLVER_AVAILABLE and DoubtSolverEngine:
            doubt_solver = DoubtSolverEngine()
            print("✅ Doubt solver initialized")
        else:
            doubt_solver = None
            print("⚠️ Doubt solver not available")
            
        if PDF_GENERATOR_AVAILABLE and PDFQuizGenerator:
            quiz_generator = PDFQuizGenerator()
            print("✅ Quiz generator initialized")
        else:
            quiz_generator = None
            print("⚠️ Quiz generator not available")
            
        if JEE_SYSTEM_AVAILABLE and JEETestSystem:
            jee_system = JEETestSystem()
            print("✅ JEE system initialized")
        else:
            jee_system = None
            print("⚠️ JEE system not available")
        
        # Initialize Supabase client
        if SUPABASE_CLIENT_AVAILABLE and get_supabase_client:
            try:
                supabase_client = get_supabase_client()
                print("✅ Supabase client initialized")
                # reset init error on success
                global supabase_init_error
                supabase_init_error = None
            except Exception as supabase_error:
                print(f"❌ Supabase client initialization failed: {supabase_error}")
                print("🔍 Environment variables check:")
                print(f"  SUPABASE_URL: {'set' if os.getenv('SUPABASE_URL') else 'missing'}")
                print(f"  SUPABASE_ANON_KEY: {'set' if os.getenv('SUPABASE_ANON_KEY') else 'missing'}")
                print(f"  SUPABASE_SERVICE_ROLE_KEY: {'set' if os.getenv('SUPABASE_SERVICE_ROLE_KEY') else 'missing'}")
                supabase_client = None
                supabase_init_error = str(supabase_error)
        else:
            supabase_client = None
            print("⚠️ Supabase client not available")
        
        print("🟢 Application initialized (some features may be limited)")
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        print("🟠 Starting with limited functionality...")
        # Don't raise - allow app to start with limited functionality
    
    yield
    
    print("🔄 Shutting down Klaro Educational Platform...")

# Create FastAPI app
app = FastAPI(
    title="Klaro Educational Platform API",
    description="AI-powered educational platform with doubt solving, quiz generation, and JEE test preparation",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None
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

# Global variables (initialized in lifespan)
doubt_solver: DoubtSolverEngine = None
quiz_generator: PDFQuizGenerator = None
jee_system: JEETestSystem = None
supabase_client: SupabaseClient = None
supabase_init_error: Optional[str] = None

# ================================================================================
# 🔐 Authentication & Authorization
# ================================================================================

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token with Supabase and return user"""
    try:
        token = credentials.credentials
        
        # Verify token with Supabase
        user_response = supabase_client.client.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # Get user profile from database
        user_profile = await supabase_client.get_user_profile(user_response.user.id)
        
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        return user_profile
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

# ================================================================================
# 👤 User Management Endpoints
# ================================================================================

@app.post("/api/auth/register")
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...)
):
    """Register a new user"""
    try:
        result = await supabase_client.create_user(email, password, name)
        
        if result["success"]:
            return {
                "success": True,
                "message": "User registered successfully. Please check your email to verify your account.",
                "user_id": result["user"].id
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/api/auth/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    """Authenticate user and return access token"""
    try:
        result = await supabase_client.authenticate_user(email, password)
        
        if result["success"]:
            return {
                "success": True,
                "access_token": result["access_token"],
                "user": {
                    "id": result["user"].id,
                    "email": result["user"].email,
                    "name": result["user"].user_metadata.get("name", "")
                }
            }
        else:
            raise HTTPException(status_code=401, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.get("/api/user/profile")
async def get_user_profile(current_user: Dict = Depends(get_current_user)):
    """Get current user's profile"""
    return {
        "success": True,
        "user": current_user
    }

@app.get("/api/user/analytics")
async def get_user_analytics(
    days: int = 30,
    current_user: Dict = Depends(get_current_user)
):
    """Get user analytics and usage statistics"""
    try:
        analytics = await supabase_client.get_user_analytics(current_user["id"], days)
        
        return {
            "success": True,
            "analytics": analytics,
            "period_days": days
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

# ================================================================================
# 🤔 Doubt Solving Endpoints
# ================================================================================

@app.post("/api/doubts/solve")
async def solve_doubt(
    background_tasks: BackgroundTasks,
    question: str = Form(...),
    image: Optional[UploadFile] = File(None),
    current_user: Dict = Depends(get_current_user)
):
    """Solve a doubt with optional image input"""
    start_time = time.time()
    
    try:
        # Process the doubt
        if image:
            # Handle image-based doubt
            image_content = await image.read()
            result = await doubt_solver.solve_doubt_with_image(image_content, question)
        else:
            # Handle text-based doubt
            result = await doubt_solver.solve_doubt_text(question)
        
        # Calculate metrics
        processing_time = time.time() - start_time
        cost = result.get("cost", 0.0)
        
        # Save to database in background
        doubt_data = {
            "question": question,
            "solution": result,
            "subject": result.get("subject", "Mathematics"),
            "method": result.get("method", "unknown"),
            "cost": cost,
            "time_taken": processing_time,
            "confidence": result.get("confidence", 0.0),
            "route": "doubts"
        }
        
        background_tasks.add_task(
            supabase_client.save_doubt, 
            current_user["id"], 
            doubt_data
        )
        
        background_tasks.add_task(
            supabase_client.record_usage,
            current_user["id"],
            "doubts",
            result.get("method", "unknown"),
            cost,
            True
        )
        
        return {
            "success": True,
            "solution": result,
            "processing_time": processing_time,
            "cost": cost
        }
        
    except Exception as e:
        # Record failed attempt
        background_tasks.add_task(
            supabase_client.record_usage,
            current_user["id"],
            "doubts",
            "error",
            0.0,
            False
        )
        
        raise HTTPException(status_code=500, detail=f"Failed to solve doubt: {str(e)}")

@app.get("/api/doubts/history")
async def get_doubt_history(
    limit: int = 20,
    offset: int = 0,
    current_user: Dict = Depends(get_current_user)
):
    """Get user's doubt solving history"""
    try:
        doubts = await supabase_client.get_user_doubts(current_user["id"], limit, offset)
        
        return {
            "success": True,
            "doubts": doubts,
            "total": len(doubts),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get doubt history: {str(e)}")

# ================================================================================
# 📄 PDF Quiz Generation Endpoints
# ================================================================================

@app.post("/api/quiz/generate")
async def generate_quiz(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    topics: str = Form(...),  # Comma-separated
    questions_count: int = Form(10),
    difficulty: str = Form("mixed"),
    current_user: Dict = Depends(get_current_user)
):
    """Generate a custom PDF quiz"""
    start_time = time.time()
    
    try:
        # Parse topics
        topic_list = [topic.strip() for topic in topics.split(",")]
        
        # Generate quiz
        quiz_result = await quiz_generator.generate_quiz(
            title=title,
            topics=topic_list,
            questions_count=questions_count,
            difficulty_levels=[difficulty] if difficulty != "mixed" else ["easy", "medium", "hard"]
        )
        
        # Calculate metrics
        processing_time = time.time() - start_time
        
        # Save to database in background
        quiz_data = {
            "title": title,
            "topics": topic_list,
            "questions_count": questions_count,
            "difficulty_levels": [difficulty],
            "file_url": quiz_result.get("file_url", "")
        }
        
        background_tasks.add_task(
            supabase_client.save_quiz,
            current_user["id"],
            quiz_data
        )
        
        background_tasks.add_task(
            supabase_client.record_usage,
            current_user["id"],
            "quiz",
            "pdf_generation",
            quiz_result.get("cost", 0.0),
            True
        )
        
        return {
            "success": True,
            "quiz": quiz_result,
            "processing_time": processing_time
        }
        
    except Exception as e:
        background_tasks.add_task(
            supabase_client.record_usage,
            current_user["id"],
            "quiz",
            "pdf_generation",
            0.0,
            False
        )
        
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

@app.get("/api/quiz/history")
async def get_quiz_history(
    limit: int = 20,
    current_user: Dict = Depends(get_current_user)
):
    """Get user's quiz generation history"""
    try:
        quizzes = await supabase_client.get_user_quizzes(current_user["id"], limit)
        
        return {
            "success": True,
            "quizzes": quizzes,
            "total": len(quizzes)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get quiz history: {str(e)}")

@app.get("/api/quiz/download/{quiz_id}")
async def download_quiz(
    quiz_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Download a generated quiz PDF"""
    try:
        # Verify user owns this quiz
        quizzes = await supabase_client.get_user_quizzes(current_user["id"], 100)
        user_quiz = next((q for q in quizzes if q["id"] == quiz_id), None)
        
        if not user_quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        # Return file download
        file_path = f"generated_quizzes/{quiz_id}.pdf"
        
        if os.path.exists(file_path):
            return FileResponse(
                file_path,
                media_type="application/pdf",
                filename=f"{user_quiz['quiz_title']}.pdf"
            )
        else:
            raise HTTPException(status_code=404, detail="Quiz file not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download quiz: {str(e)}")

# ================================================================================
# 🎯 JEE Test System Endpoints
# ================================================================================

@app.get("/api/jee/tests/available")
async def get_available_tests(current_user: Dict = Depends(get_current_user)):
    """Get list of available JEE tests"""
    try:
        tests = await jee_system.get_available_tests()
        
        return {
            "success": True,
            "tests": tests
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tests: {str(e)}")

@app.get("/api/jee/test/{test_id}")
async def get_test_questions(
    test_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get questions for a specific test"""
    try:
        test_data = await jee_system.get_test_questions(test_id)
        
        return {
            "success": True,
            "test": test_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get test: {str(e)}")

@app.post("/api/jee/test/{test_id}/submit")
async def submit_test(
    test_id: str,
    background_tasks: BackgroundTasks,
    answers: Dict = Form(...),
    time_taken: int = Form(...),
    current_user: Dict = Depends(get_current_user)
):
    """Submit test answers and get results"""
    try:
        # Process test submission
        result = await jee_system.evaluate_test(test_id, answers, time_taken)
        
        # Save to database in background
        test_result_data = {
            "test_id": test_id,
            "test_type": result.get("test_type", "full_mock"),
            "total_score": result.get("total_score", 0),
            "max_score": result.get("max_score", 300),
            "subject_scores": result.get("subject_scores", {}),
            "time_taken": time_taken
        }
        
        background_tasks.add_task(
            supabase_client.save_jee_result,
            current_user["id"],
            test_result_data
        )
        
        background_tasks.add_task(
            supabase_client.record_usage,
            current_user["id"],
            "jee",
            "test_submission",
            0.0,  # JEE tests are free
            True
        )
        
        return {
            "success": True,
            "result": result
        }
        
    except Exception as e:
        background_tasks.add_task(
            supabase_client.record_usage,
            current_user["id"],
            "jee",
            "test_submission",
            0.0,
            False
        )
        
        raise HTTPException(status_code=500, detail=f"Failed to submit test: {str(e)}")

@app.get("/api/jee/results")
async def get_jee_results(
    limit: int = 10,
    current_user: Dict = Depends(get_current_user)
):
    """Get user's JEE test results"""
    try:
        results = await supabase_client.get_user_jee_results(current_user["id"], limit)
        
        return {
            "success": True,
            "results": results,
            "total": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get results: {str(e)}")

# ================================================================================
# 📁 File Management Endpoints
# ================================================================================

@app.post("/api/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    file_type: str = Form(...),
    current_user: Dict = Depends(get_current_user)
):
    """Upload file to Supabase Storage"""
    try:
        # Validate file type
        allowed_types = ["pdf_quiz", "doubt_image", "profile_image"]
        if file_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {allowed_types}")
        
        # Read file content
        file_content = await file.read()
        
        # Upload to Supabase Storage
        timestamp = int(time.time())
        file_name = f"{current_user['id']}/{file_type}/{timestamp}_{file.filename}"
        
        storage_response = supabase_client.client.storage.from_("klaro-files").upload(
            file_name, file_content
        )
        
        if storage_response.get("error"):
            raise HTTPException(status_code=500, detail="Failed to upload file")
        
        # Get public URL
        public_url = supabase_client.client.storage.from_("klaro-files").get_public_url(file_name)
        
        # Save metadata to database
        file_metadata = {
            "user_id": current_user["id"],
            "file_name": file.filename,
            "file_type": file_type,
            "file_size": len(file_content),
            "storage_path": file_name,
            "public_url": public_url.get("publicUrl", ""),
            "is_public": file_type == "pdf_quiz"  # PDFs can be public
        }
        
        metadata_response = supabase_client.client.table('file_metadata').insert(file_metadata).execute()
        
        return {
            "success": True,
            "file_id": metadata_response.data[0]["id"],
            "public_url": public_url.get("publicUrl", ""),
            "message": "File uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# ================================================================================
# 🔔 Notification Endpoints
# ================================================================================

@app.get("/api/notifications")
async def get_notifications(
    limit: int = 20,
    current_user: Dict = Depends(get_current_user)
):
    """Get user notifications"""
    try:
        response = supabase_client.client.table('notifications').select('*').eq('user_id', current_user["id"]).order('created_at', desc=True).limit(limit).execute()
        
        return {
            "success": True,
            "notifications": response.data or [],
            "unread_count": len([n for n in response.data or [] if not n.get("is_read", False)])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get notifications: {str(e)}")

@app.patch("/api/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Mark notification as read"""
    try:
        response = supabase_client.client.table('notifications').update({
            "is_read": True
        }).eq('id', notification_id).eq('user_id', current_user["id"]).execute()
        
        return {
            "success": True,
            "message": "Notification marked as read"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update notification: {str(e)}")

# ================================================================================
# 📚 Catalog Endpoints
# ================================================================================

@app.get("/catalog/chapters")
@app.get("/api/catalog/chapters")
async def get_catalog_chapters(subject: Optional[str] = None, grade: Optional[str] = None):
    """Get grade-wise chapters from topics_simple view.
    Optional filters: subject (e.g., 'Mathematics'), grade (e.g., 'Class 12')."""
    try:
        global supabase_client
        if not supabase_client:
            # Try lazy-initializing the client
            if SUPABASE_CLIENT_AVAILABLE and get_supabase_client:
                try:
                    supabase_client = get_supabase_client()
                except Exception:
                    raise HTTPException(status_code=503, detail="Database not available")
            else:
                raise HTTPException(status_code=503, detail="Database not available")

        query = supabase_client.client.table('topics_simple').select('*')
        if subject:
            query = query.eq('subject', subject)
        if grade:
            query = query.eq('grade', grade)

        response = query.order('subject').order('grade').order('chapter').execute()
        rows = response.data or []
        chapters = [row.get('chapter') for row in rows if row.get('chapter')]

        return {
            "success": True,
            "count": len(chapters),
            "chapters": chapters
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chapters: {str(e)}")

@app.get("/catalog/subtopics")
@app.get("/api/catalog/subtopics")
async def get_catalog_subtopics(subject: str, grade: str, chapter: str):
    """Get subtopics for a given subject, grade, and chapter.
    Uses topics table directly: parent (chapter) -> child (subtopic)."""
    try:
        global supabase_client
        if not supabase_client:
            if SUPABASE_CLIENT_AVAILABLE and get_supabase_client:
                try:
                    supabase_client = get_supabase_client()
                except Exception:
                    raise HTTPException(status_code=503, detail="Database not available")
            else:
                raise HTTPException(status_code=503, detail="Database not available")

        # Resolve subject_id and grade_id
        s_resp = supabase_client.client.table('subjects').select('id').eq('name', subject).limit(1).execute()
        g_resp = supabase_client.client.table('grades').select('id').eq('name', grade).limit(1).execute()
        if not s_resp.data or not g_resp.data:
            return {"success": True, "count": 0, "subtopics": []}
        subject_id = s_resp.data[0]['id']
        grade_id = g_resp.data[0]['id']

        # Find parent chapter row (prefer parent_id is null)
        p_resp = (
            supabase_client.client
            .table('topics')
            .select('id,parent_id')
            .eq('subject_id', subject_id)
            .eq('grade_id', grade_id)
            .eq('name', chapter)
            .execute()
        )
        if not p_resp.data:
            return {"success": True, "count": 0, "subtopics": []}
        parent_candidates = p_resp.data
        parent = next((row for row in parent_candidates if not row.get('parent_id')), parent_candidates[0])
        parent_id = parent['id']

        # Fetch children (subtopics)
        c_resp = (
            supabase_client.client
            .table('topics')
            .select('name')
            .eq('parent_id', parent_id)
            .order('name')
            .execute()
        )
        names = [row.get('name') for row in (c_resp.data or []) if row.get('name')]
        # Dedupe while preserving order
        seen = set()
        unique_subtopics = []
        for st in names:
            if st not in seen:
                seen.add(st)
                unique_subtopics.append(st)

        return {
            "success": True,
            "count": len(unique_subtopics),
            "subtopics": unique_subtopics
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch subtopics: {str(e)}")

# ================================================================================
# 🔧 System Health Endpoints
# ================================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    try:
        # Check if supabase_client is available
        database_status = "not_connected"
        if supabase_client and hasattr(supabase_client, 'client') and supabase_client.client:
            try:
                # Quick database connectivity check
                response = supabase_client.client.table('users').select('id').limit(1).execute()
                database_status = "connected"
            except Exception as db_e:
                print(f"⚠️ Database connectivity check failed: {db_e}")
                database_status = "connection_failed"
        
        services_status = {
            "database": database_status,
            "doubt_solver": "active" if doubt_solver else "inactive",
            "quiz_generator": "active" if quiz_generator else "inactive",
            "jee_system": "active" if jee_system else "inactive",
            "supabase_client": "available" if supabase_client else "unavailable"
        }
        
        # Determine overall health status
        is_healthy = database_status in ["connected", "not_connected"]  # Allow running without DB for basic health check
        
        return {
            "status": "healthy" if is_healthy else "degraded",
            "timestamp": datetime.now().isoformat(),
            "services": services_status
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

@app.get("/health/env")
async def health_env():
    """Non-secret environment diagnostics (set/missing flags only)."""
    try:
        def present(name: str) -> bool:
            return bool(os.getenv(name))
        env_status = {
            "SUPABASE_URL": present("SUPABASE_URL"),
            "NEXT_PUBLIC_SUPABASE_URL": present("NEXT_PUBLIC_SUPABASE_URL"),
            "SUPABASE_ANON_KEY": present("SUPABASE_ANON_KEY"),
            "SUPABASE_KEY": present("SUPABASE_KEY"),
            "NEXT_PUBLIC_SUPABASE_ANON_KEY": present("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
            "NEXT_PUBLIC_SUPABASE_KEY": present("NEXT_PUBLIC_SUPABASE_KEY"),
            "SUPABASE_SERVICE_ROLE_KEY": present("SUPABASE_SERVICE_ROLE_KEY"),
            "SUPABASE_SERVICE_KEY": present("SUPABASE_SERVICE_KEY"),
            "OPENAI_API_KEY": present("OPENAI_API_KEY"),
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "").lower() or "unset",
            "supabase_client": bool(supabase_client),
            "supabase_init_error": (supabase_init_error or "")[:200],
        }
        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "env": env_status,
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "error": str(e)})

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🟢 Klaro Educational Platform API",
        "version": "2.0.0",
        "status": "running",
        "deployed_at": "2025-08-31T12:10:00Z",
        "docs": "/docs" if os.getenv("ENVIRONMENT") != "production" else "disabled"
    }

# ================================================================================
# 🚀 Server Configuration
# ================================================================================

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 1))
    log_level = os.getenv("LOG_LEVEL", "info")
    
    print(f"🚀 Starting Klaro Educational Platform on {host}:{port}")
    print(f"📊 Workers: {workers}, Log Level: {log_level}")
    
    if os.getenv("ENVIRONMENT") == "production":
        # Production configuration
        uvicorn.run(
            "backend.main_with_supabase:app",
            host=host,
            port=port,
            workers=workers,
            log_level=log_level,
            access_log=True
        )
    else:
        # Development configuration
        uvicorn.run(
            "backend.main_with_supabase:app",
            host=host,
            port=port,
            reload=True,
            log_level=log_level
        )
