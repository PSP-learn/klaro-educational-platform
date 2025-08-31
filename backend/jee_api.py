#!/usr/bin/env python3
"""
JEE Main Online Test API

Backend endpoints for JEE Main online test functionality.
Integrates with existing quiz generator while adding JEE-specific features.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uvicorn
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Import JEE test modules
import sys
sys.path.append('..')
from jee_online_test import JEETestConfig, JEEOnlineTest, JEETestInterface, JEEScoring, JEESyllabus

# Import existing quiz generator
try:
    from smart_quiz_generator import SmartTestGenerator
except ImportError:
    print("⚠️ Smart quiz generator not available, using fallback mode")
    SmartTestGenerator = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Klaro JEE Main API",
    description="Backend API for JEE Main Online Tests",
    version="1.0.0",
    docs_url="/api/docs"
)

# CORS for web interface and mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for web interface
app.mount("/static", StaticFiles(directory="../web_interface"), name="static")

# Global instances
jee_test_system: Optional[JEEOnlineTest] = None
quiz_generator: Optional[SmartTestGenerator] = None

# ================================================================================
# 🎯 Data Models for JEE API
# ================================================================================

class JEETestRequest(BaseModel):
    test_name: str
    test_type: str  # "full_mock", "subject_practice", "topic_practice"
    subjects: List[str]
    selected_topics: Optional[Dict[str, List[str]]] = None
    total_questions: int = 75
    total_time_minutes: int = 180
    difficulty_levels: List[str] = ["easy", "medium", "hard"]

class JEETestResponse(BaseModel):
    test_id: str
    session_id: str
    test_config: Dict[str, Any]
    total_questions: int
    total_time_minutes: int
    interface_url: str
    created_at: str

class JEEAnswerSubmission(BaseModel):
    session_id: str
    question_id: str
    answer: str
    time_spent: int  # seconds

class JEETestSubmission(BaseModel):
    session_id: str
    answers: Dict[str, str]
    marked_for_review: List[str]
    total_time_taken: int
    subject_timings: Dict[str, int]

# ================================================================================
# 🚀 Startup and Initialization
# ================================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize JEE test system"""
    global jee_test_system, quiz_generator
    
    logger.info("🎓 Starting JEE Main Online Test System...")
    
    # Initialize quiz generator if available
    try:
        quiz_generator = SmartTestGenerator("../book_db")
        logger.info("✅ Quiz generator connected")
    except Exception as e:
        logger.warning(f"⚠️ Quiz generator not available: {e}")
        quiz_generator = None
    
    # Initialize JEE test system
    jee_test_system = JEEOnlineTest(quiz_generator)
    logger.info("✅ JEE test system initialized")
    
    # Create necessary directories
    Path("../generated_tests").mkdir(exist_ok=True)
    Path("../test_sessions").mkdir(exist_ok=True)
    
    logger.info("🎉 JEE Main API ready!")

# ================================================================================
# 🎯 JEE Test Management Endpoints
# ================================================================================

@app.get("/")
async def jee_home():
    """Serve JEE test interface"""
    with open("../web_interface/jee_test.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/jee/syllabus")
async def get_jee_syllabus():
    """Get complete JEE Main syllabus"""
    syllabus = JEESyllabus()
    return {"syllabus": syllabus.SUBJECTS}

@app.get("/api/jee/test-types")
async def get_jee_test_types():
    """Get available JEE test types"""
    return {
        "test_types": {
            "full_mock": {
                "name": "Full JEE Main Mock",
                "description": "Complete 75-question test (25 per subject)",
                "questions": 75,
                "duration": 180,
                "subjects": ["Physics", "Chemistry", "Mathematics"]
            },
            "subject_practice": {
                "name": "Subject-wise Practice",
                "description": "Practice one subject (25 questions)",
                "questions": 25,
                "duration": 60,
                "subjects": ["Physics OR Chemistry OR Mathematics"]
            },
            "topic_practice": {
                "name": "Topic-wise Practice", 
                "description": "Focus on specific topics",
                "questions": "5-50 (customizable)",
                "duration": "15-120 min (customizable)",
                "subjects": ["Any combination"]
            },
            "pyq_practice": {
                "name": "Previous Year Questions",
                "description": "Year-wise JEE Main papers",
                "questions": 75,
                "duration": 180,
                "years": ["2024", "2023", "2022", "2021", "2020"]
            }
        }
    }

@app.post("/api/jee/test/create", response_model=JEETestResponse)
async def create_jee_test(test_request: JEETestRequest):
    """Create a new JEE test session"""
    
    if not jee_test_system:
        raise HTTPException(status_code=500, detail="JEE test system not available")
    
    try:
        logger.info(f"🎯 Creating JEE test: {test_request.test_name}")
        
        # Create test configuration
        config = JEETestConfig(
            test_name=test_request.test_name,
            test_type=test_request.test_type,
            subjects=test_request.subjects,
            selected_topics=test_request.selected_topics,
            total_questions=test_request.total_questions,
            total_time_minutes=test_request.total_time_minutes
        )
        
        # Set default questions per subject for full mock
        if test_request.test_type == "full_mock":
            config.questions_per_subject = {
                "Physics": 25,
                "Chemistry": 25, 
                "Mathematics": 25
            }
        
        # Generate questions
        questions = jee_test_system.generate_jee_questions(config)
        
        # Create test session
        interface = JEETestInterface()
        session = interface.create_test_session(config, questions)
        
        # Save session data
        session_file = Path("../test_sessions") / f"{session['session_id']}.json"
        with open(session_file, 'w') as f:
            # Convert sets to lists for JSON serialization
            session_copy = session.copy()
            session_copy['test_state']['marked_for_review'] = list(session_copy['test_state']['marked_for_review'])
            json.dump(session_copy, f, indent=2, default=str)
        
        test_id = f"jee_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return JEETestResponse(
            test_id=test_id,
            session_id=session['session_id'],
            test_config=session['test_config'],
            total_questions=len(questions),
            total_time_minutes=config.total_time_minutes,
            interface_url=f"/test/{session['session_id']}",
            created_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ JEE test creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Test creation failed: {str(e)}")

@app.get("/api/jee/test/{session_id}")
async def get_jee_test_session(session_id: str):
    """Get JEE test session data"""
    
    session_file = Path("../test_sessions") / f"{session_id}.json"
    
    if not session_file.exists():
        raise HTTPException(status_code=404, detail="Test session not found")
    
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        return session_data
        
    except Exception as e:
        logger.error(f"❌ Failed to load session: {e}")
        raise HTTPException(status_code=500, detail="Failed to load test session")

@app.post("/api/jee/test/{session_id}/answer")
async def submit_answer(session_id: str, answer_data: JEEAnswerSubmission):
    """Submit answer for a specific question"""
    
    try:
        # Load session
        session_file = Path("../test_sessions") / f"{session_id}.json"
        
        if not session_file.exists():
            raise HTTPException(status_code=404, detail="Session not found")
        
        with open(session_file, 'r') as f:
            session = json.load(f)
        
        # Update answer
        session['test_state']['answers'][answer_data.question_id] = answer_data.answer
        
        # Save updated session
        with open(session_file, 'w') as f:
            json.dump(session, f, indent=2, default=str)
        
        return {"status": "success", "message": "Answer saved"}
        
    except Exception as e:
        logger.error(f"❌ Answer submission failed: {e}")
        raise HTTPException(status_code=500, detail="Answer submission failed")

@app.post("/api/jee/test/{session_id}/submit")
async def submit_jee_test(session_id: str, submission: JEETestSubmission):
    """Submit complete JEE test and calculate results"""
    
    try:
        # Load session
        session_file = Path("../test_sessions") / f"{session_id}.json"
        
        if not session_file.exists():
            raise HTTPException(status_code=404, detail="Session not found")
        
        with open(session_file, 'r') as f:
            session = json.load(f)
        
        # Calculate results
        config = JEETestConfig(**session['test_config'])
        questions = session['questions']
        
        results = JEEScoring.calculate_score(
            submission.answers,
            questions,
            config
        )
        
        # Add timing analysis
        results['time_analysis'] = {
            'total_time_taken': submission.total_time_taken,
            'time_per_question': submission.total_time_taken // len(questions),
            'subject_timings': submission.subject_timings
        }
        
        # Save results
        results_file = Path("../test_sessions") / f"{session_id}_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"✅ JEE test {session_id} completed - Score: {results['overall']['score']}")
        
        return {
            "session_id": session_id,
            "results": results,
            "submitted_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Test submission failed: {e}")
        raise HTTPException(status_code=500, detail="Test submission failed")

@app.get("/test/{session_id}")
async def serve_jee_test_interface(session_id: str):
    """Serve the JEE test interface for a specific session"""
    
    # Load session data and serve customized interface
    try:
        session_file = Path("../test_sessions") / f"{session_id}.json"
        
        if session_file.exists():
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # TODO: Customize HTML template with actual session data
            with open("../web_interface/jee_test.html", "r") as f:
                html_content = f.read()
                
            return HTMLResponse(content=html_content)
        else:
            return HTMLResponse(content="<h1>❌ Test session not found</h1>")
            
    except Exception as e:
        return HTMLResponse(content=f"<h1>❌ Error loading test: {e}</h1>")

# ================================================================================
# 📊 Analytics and Results Endpoints
# ================================================================================

@app.get("/api/jee/results/{session_id}")
async def get_jee_test_results(session_id: str):
    """Get detailed JEE test results and analysis"""
    
    results_file = Path("../test_sessions") / f"{session_id}_results.json"
    
    if not results_file.exists():
        raise HTTPException(status_code=404, detail="Results not found")
    
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Failed to load results: {e}")
        raise HTTPException(status_code=500, detail="Failed to load results")

@app.get("/api/jee/analytics/performance")
async def get_performance_analytics():
    """Get JEE performance analytics across all tests"""
    
    # Mock analytics data for demonstration
    return {
        "overall_stats": {
            "tests_taken": 15,
            "average_score": 245,
            "average_percentile": 87.5,
            "best_score": 289,
            "improvement_trend": "+12% over last month"
        },
        "subject_performance": {
            "Physics": {"avg_score": 78, "accuracy": 72, "time_per_q": 2.1},
            "Chemistry": {"avg_score": 85, "accuracy": 78, "time_per_q": 1.9},
            "Mathematics": {"avg_score": 82, "accuracy": 75, "time_per_q": 2.3}
        },
        "weak_areas": [
            {"topic": "Electromagnetic Induction", "subject": "Physics", "accuracy": 45},
            {"topic": "Organic Reactions", "subject": "Chemistry", "accuracy": 52},
            {"topic": "Definite Integration", "subject": "Mathematics", "accuracy": 38}
        ],
        "recommendations": [
            {"type": "practice", "topic": "Modern Physics", "reason": "Low recent performance"},
            {"type": "revision", "topic": "Coordinate Geometry", "reason": "Haven't practiced recently"},
            {"type": "speed", "topic": "Algebra", "reason": "Taking too much time"}
        ]
    }

# ================================================================================
# 🎯 Test Configuration Endpoints
# ================================================================================

@app.post("/api/jee/configure/custom")
async def create_custom_jee_test(
    subjects: List[str],
    topics_per_subject: Dict[str, List[str]],
    questions_per_subject: Dict[str, int],
    time_minutes: int = 60
):
    """Create custom JEE test configuration"""
    
    total_questions = sum(questions_per_subject.values())
    
    config = JEETestConfig(
        test_name=f"Custom JEE Test - {', '.join(subjects)}",
        test_type="custom",
        subjects=subjects,
        selected_topics=topics_per_subject,
        total_questions=total_questions,
        total_time_minutes=time_minutes,
        questions_per_subject=questions_per_subject
    )
    
    # Generate test using configuration
    test_request = JEETestRequest(
        test_name=config.test_name,
        test_type=config.test_type,
        subjects=config.subjects,
        selected_topics=config.selected_topics,
        total_questions=config.total_questions,
        total_time_minutes=config.total_time_minutes
    )
    
    return await create_jee_test(test_request)

@app.get("/api/jee/presets")
async def get_jee_presets():
    """Get JEE test presets"""
    
    return {
        "presets": {
            "full_mock_easy": {
                "name": "JEE Main Mock - Easy Level",
                "description": "Practice test with easier questions",
                "subjects": ["Physics", "Chemistry", "Mathematics"],
                "questions": 75,
                "duration": 180,
                "difficulty": ["easy", "medium"]
            },
            "full_mock_hard": {
                "name": "JEE Main Mock - Advanced Level", 
                "description": "Challenging test for high scorers",
                "subjects": ["Physics", "Chemistry", "Mathematics"],
                "questions": 75,
                "duration": 180,
                "difficulty": ["medium", "hard"]
            },
            "physics_intensive": {
                "name": "Physics Intensive Practice",
                "description": "Physics-focused preparation",
                "subjects": ["Physics"],
                "questions": 50,
                "duration": 90,
                "difficulty": ["medium", "hard"]
            },
            "quick_revision": {
                "name": "Quick Revision Test",
                "description": "Fast review across all subjects",
                "subjects": ["Physics", "Chemistry", "Mathematics"],
                "questions": 30,
                "duration": 45,
                "difficulty": ["easy"]
            }
        }
    }

# ================================================================================
# 📊 Health and Status Endpoints
# ================================================================================

@app.get("/api/health")
async def jee_health_check():
    """Health check for JEE system"""
    return {
        "status": "healthy",
        "service": "JEE Main Online Tests",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "jee_test_system": jee_test_system is not None,
            "quiz_generator": quiz_generator is not None,
            "web_interface": True
        }
    }

@app.get("/api/jee/stats")
async def get_jee_system_stats():
    """Get JEE system statistics"""
    
    session_dir = Path("../test_sessions")
    if not session_dir.exists():
        return {"total_sessions": 0, "active_sessions": 0}
    
    session_files = list(session_dir.glob("jee_session_*.json"))
    result_files = list(session_dir.glob("*_results.json"))
    
    return {
        "total_sessions": len(session_files),
        "completed_tests": len(result_files),
        "active_sessions": len(session_files) - len(result_files),
        "system_status": "operational"
    }

# ================================================================================
# 🚀 Development and Testing Endpoints
# ================================================================================

@app.post("/api/jee/demo/create")
async def create_demo_jee_test():
    """Create a demo JEE test for development"""
    
    demo_request = JEETestRequest(
        test_name="Demo JEE Main Mock Test",
        test_type="full_mock",
        subjects=["Physics", "Chemistry", "Mathematics"],
        total_questions=75,
        total_time_minutes=180
    )
    
    return await create_jee_test(demo_request)

if __name__ == "__main__":
    print("🎓 JEE Main Online Test API Server")
    print("🎯 Features: Custom tests, NTA Abhyas interface, Real-time scoring")
    print("🌐 Test Interface: http://localhost:8000/")
    print("📊 API Documentation: http://localhost:8000/api/docs")
    print("=" * 60)
    
    uvicorn.run(
        "jee_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
