#!/usr/bin/env python3
"""
Klaro Educational Platform - Android Backend API

Focused backend API server for Android app with quiz generation and educational features.
Built with FastAPI for high performance. CLI maintained for testing.
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field
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

class BlueprintConfig(BaseModel):
    total_questions: Optional[int] = None
    by_type: Optional[Dict[str, int]] = None  # e.g., {"mcq": 10, "short": 8, "long": 2}
    by_difficulty: Optional[Dict[str, int]] = None  # {"easy": 10, "medium": 8, "hard": 2}
    duration_minutes: Optional[int] = None

class SectionConfig(BaseModel):
    name: str
    types: List[str]
    count: int
    difficulty: Optional[Dict[str, int]] = None
    negative_marking: Optional[float] = 0.0

class QuizRequest(BaseModel):
    # Core generation parameters
    topics: List[str]
    num_questions: int = 10
    question_types: List[str] = ["mcq", "short"]
    difficulty_levels: List[str] = ["easy", "medium"]
    subject: str = "Mathematics"
    duration: Optional[int] = None
    title: Optional[str] = None
    # New customization fields
    domain: Optional[str] = None  # CBSE | JEE | NEET
    grade: Optional[str] = None   # 9 | 10 | 11 | 12 for CBSE
    subjects: Optional[List[str]] = None  # Multi-subject selection (JEE/NEET) or CBSE streams
    header: Optional[str] = None  # School/Institute header
    instructions: Optional[List[str]] = None  # Custom instructions
    # Advanced generation mode
    mode: Optional[str] = "mixed"  # mixed | source
    scope_filter: Optional[str] = None
    render: Optional[str] = "auto"  # auto | image | text
    books_dir: Optional[str] = None
    output_engine: Optional[str] = "reportlab"  # reportlab | latex
    include_solutions: Optional[bool] = False
    blueprint: Optional[BlueprintConfig] = None
    sections: Optional[List[SectionConfig]] = None
    marks: Optional[Dict[str, int]] = None  # marks per type
    # UI filter metadata (optional, stored in metadata only)
    streams: Optional[List[str]] = None
    class_filter: Optional[List[str]] = None  # 'class' is reserved word
    topic_tags: Optional[List[str]] = None
    subtopics: Optional[List[str]] = None
    levels: Optional[List[str]] = None
    source_material: Optional[List[str]] = None
    language: Optional[str] = None
    centers: Optional[List[str]] = None

class PreviewResponse(BaseModel):
    valid: bool
    totals: Dict[str, int]
    duration_estimate: int
    warnings: List[str] = Field(default_factory=list)
    normalized_blueprint: Optional[BlueprintConfig] = None

class QuizResponse(BaseModel):
    quiz_id: str
    title: str
    questions_file: str
    answers_file: str
    pdf_questions_file: Optional[str] = None
    pdf_answers_file: Optional[str] = None
    pdf_marking_scheme_file: Optional[str] = None
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
    Path("../generated_solutions").mkdir(exist_ok=True)
    
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


def _build_marking_scheme_reportlab(test_data: Dict[str, Any], output_prefix: str, out_dir: str = "../generated_tests") -> str:
    """Create a simple marking scheme PDF via ReportLab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors

    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{output_prefix}_marking_scheme.pdf"

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(out_path), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elems = []

    header = test_data.get('header')
    title = test_data.get('title') or 'Practice Test'
    subject = test_data.get('subject') or ''

    if header:
        elems.append(Paragraph(header, styles['Title']))
    elems.append(Paragraph(f"MARKING SCHEME - {title}", styles['Title']))
    elems.append(Paragraph(f"Subject: {subject}", styles['Normal']))
    elems.append(Spacer(1, 8))

    counts = test_data.get('marking_counts') or {}
    marks = test_data.get('marks_per_type') or {}

    label_map = {
        'single_correct': 'Single Correct (1M)',
        'assertion_reason': 'Assertion–Reason (1M)',
        'short2': 'Short Answer (2M)',
        'long3': 'Long Answer (3M)',
        'verylong5': 'Very Long Answer (5M)',
        'case_study': 'Case Study (4M)',
        'mcq': 'MCQ',
        'short': 'Short Answer',
        'long': 'Long Answer',
        'numerical': 'Numerical',
    }
    order_cbse = ['single_correct','assertion_reason','short2','long3','verylong5','case_study']

    keys = list(counts.keys())
    if any(k in order_cbse for k in keys):
        ordered = [k for k in order_cbse if counts.get(k)]
        for k in keys:
            if k not in ordered:
                ordered.append(k)
    else:
        ordered = sorted(keys)

    data = [["Question Type", "Count", "Marks/Item", "Subtotal"]]
    total_q = 0
    total_marks = 0
    for k in ordered:
        c = int(counts.get(k, 0) or 0)
        if c <= 0:
            continue
        pm = int(marks.get(k, marks.get('mcq', 1)))
        sub = c * pm
        data.append([label_map.get(k, k.title()), c, pm, sub])
        total_q += c
        total_marks += sub

    data.append(["TOTAL", total_q, "--", total_marks])

    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
    ]))
    elems.append(table)
    doc.build(elems)

    return str(out_path)

@app.post("/api/quiz/preview", response_model=PreviewResponse)
async def preview_quiz(quiz_request: QuizRequest, current_user: dict = Depends(get_current_user)):
    """Validate blueprint and return estimates/warnings. Does not generate files."""
    # Basic normalization
    bp = quiz_request.blueprint or BlueprintConfig()
    warnings: List[str] = []

    # Calculate totals
    total_from_types = sum((bp.by_type or {}).values()) if bp.by_type else None
    total_from_diff = sum((bp.by_difficulty or {}).values()) if bp.by_difficulty else None

    # Decide total
    total = bp.total_questions or total_from_types or total_from_diff or quiz_request.num_questions

    if bp.total_questions and total_from_types and bp.total_questions != total_from_types:
        warnings.append(f"total_questions ({bp.total_questions}) != sum(by_type) ({total_from_types})")
    if bp.total_questions and total_from_diff and bp.total_questions != total_from_diff:
        warnings.append(f"total_questions ({bp.total_questions}) != sum(by_difficulty) ({total_from_diff})")
    if total_from_types and total_from_diff and total_from_types != total_from_diff:
        warnings.append(f"sum(by_type) ({total_from_types}) != sum(by_difficulty) ({total_from_diff})")

    # Sections check
    if quiz_request.sections:
        section_total = sum(s.count for s in quiz_request.sections)
        if section_total != total:
            warnings.append(f"sum(sections.count) ({section_total}) != total ({total})")

    # Duration estimate
    per_type_minutes = {"mcq": 1.5, "short": 3.0, "long": 6.0, "numerical": 2.0, "proof": 8.0}
    duration_estimate = 0
    if bp.by_type:
        for t, c in bp.by_type.items():
            duration_estimate += int(round(per_type_minutes.get(t, 3.0) * c))
    else:
        duration_estimate = int(round(3.0 * total))

    # Total marks estimate (if marks mapping provided)
    total_marks = None
    if bp.by_type and quiz_request.marks:
        total_marks = 0
        for t, c in bp.by_type.items():
            per_mark = int(quiz_request.marks.get(t, 1))
            total_marks += per_mark * int(c)

    normalized = BlueprintConfig(
        total_questions=total,
        by_type=bp.by_type,
        by_difficulty=bp.by_difficulty,
        duration_minutes=bp.duration_minutes or duration_estimate
    )

    totals_payload: Dict[str, int] = {"total_questions": total}
    if total_marks is not None:
        totals_payload["total_marks"] = total_marks

    return PreviewResponse(
        valid=len(warnings) == 0,
        totals=totals_payload,
        duration_estimate=normalized.duration_minutes or duration_estimate,
        warnings=warnings,
        normalized_blueprint=normalized
    )

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
        
        # Normalize totals and type counts
        type_counts = None
        total_q = quiz_request.num_questions
        original_by_type = None
        if quiz_request.blueprint and quiz_request.blueprint.by_type:
            original_by_type = {k: int(v) for k, v in quiz_request.blueprint.by_type.items() if v and int(v) > 0}
            type_counts = original_by_type.copy()
            # If CBSE types present, map them to underlying generator types
            cbse_keys = {"single_correct", "assertion_reason", "short2", "long3", "verylong5", "case_study"}
            if any(k in cbse_keys for k in type_counts.keys()):
                mapping = {
                    "single_correct": "mcq",
                    "assertion_reason": "mcq",
                    "case_study": "mcq",
                    "short2": "short",
                    "long3": "long",
                    "verylong5": "long",
                }
                # Build underlying counts
                new_counts: Dict[str, int] = {}
                for k, v in type_counts.items():
                    tgt = mapping.get(k)
                    if not tgt:
                        tgt = k
                    new_counts[tgt] = new_counts.get(tgt, 0) + int(v)
                type_counts = {k: v for k, v in new_counts.items() if v > 0}
            if type_counts:
                total_q = sum(type_counts.values())
        elif quiz_request.blueprint and quiz_request.blueprint.total_questions:
            total_q = quiz_request.blueprint.total_questions

        # Adjust question_types to keys of type_counts if provided
        qtypes = quiz_request.question_types
        if type_counts:
            qtypes = list(type_counts.keys())

        # Generate quiz using existing logic
        test_data = quiz_generator.create_test(
            topics=quiz_request.topics,
            num_questions=total_q,
            question_types=qtypes,
            difficulty_levels=quiz_request.difficulty_levels,
            subject=quiz_request.subject,
            mode=quiz_request.mode or "mixed",
            scope_filter=quiz_request.scope_filter,
            render=quiz_request.render or "auto",
            books_dir=quiz_request.books_dir,
            type_counts=type_counts
        )

        # Annotate display types for CBSE, if requested
        if original_by_type:
            cbse_keys = {"single_correct", "assertion_reason", "short2", "long3", "verylong5", "case_study"}
            if any(k in cbse_keys for k in original_by_type.keys()):
                mapping = {
                    "single_correct": "mcq",
                    "assertion_reason": "mcq",
                    "case_study": "mcq",
                    "short2": "short",
                    "long3": "long",
                    "verylong5": "long",
                }
                # Build plan per underlying type: list of display types to assign
                plan: Dict[str, list] = {}
                for disp_type, count in original_by_type.items():
                    base = mapping.get(disp_type, disp_type)
                    plan.setdefault(base, [])
                    plan[base].extend([disp_type] * int(count))
                # Assign in order across generated questions
                for q in test_data.get('questions', []):
                    base = getattr(q, 'question_type', None)
                    alloc = plan.get(base)
                    if alloc:
                        setattr(q, 'display_type', alloc.pop(0))

        # Apply marks per type if provided
        if quiz_request.marks:
            try:
                for q in test_data.get('questions', []):
                    # Prefer display_type (CBSE), else underlying type
                    dt = getattr(q, 'display_type', None)
                    ut = getattr(q, 'question_type', None)
                    if dt and dt in quiz_request.marks:
                        setattr(q, 'points', int(quiz_request.marks[dt]))
                    elif ut and ut in quiz_request.marks:
                        setattr(q, 'points', int(quiz_request.marks[ut]))
                # Recompute totals
                test_data['total_points'] = sum(getattr(q, 'points', 1) for q in test_data.get('questions', []))
                test_data['marks_per_type'] = {k: int(v) for k, v in quiz_request.marks.items()}
            except Exception as _marks_e:
                logger.warning(f"Failed to apply marks mapping: {_marks_e}")

        # Attach header, instructions, labels
        if quiz_request.header:
            test_data['header'] = quiz_request.header
        if quiz_request.instructions and isinstance(quiz_request.instructions, list) and quiz_request.instructions:
            test_data['instructions'] = quiz_request.instructions
        else:
            # Default CBSE instructions if applicable
            if (quiz_request.domain or '').upper() == 'CBSE':
                test_data['instructions'] = [
                    'All questions are compulsory.',
                    'Read the questions carefully and write neatly.',
                    'Use appropriate units and significant figures.',
                ]
        # Compose subject/title for headers
        subj_label = quiz_request.subject or 'Mathematics'
        if quiz_request.domain:
            parts = [quiz_request.domain]
            if quiz_request.grade:
                parts.append(f"Grade {quiz_request.grade}")
            # Prefer explicit subjects list; else include single subject select
            if quiz_request.subjects:
                parts.append(', '.join(quiz_request.subjects))
            elif quiz_request.subject:
                parts.append(quiz_request.subject)
            subj_label = ' - '.join(parts)
        test_data['subject'] = subj_label
        if not test_data.get('title'):
            test_data['title'] = quiz_request.title or f"Practice Test - {quiz_request.domain or quiz_request.subject}"

        # attach UI metadata if provided
        test_data['ui_filters'] = {
            'streams': quiz_request.streams,
            'class': quiz_request.class_filter,
            'topic_tags': quiz_request.topic_tags,
            'subtopics': quiz_request.subtopics,
            'levels': quiz_request.levels,
            'source_material': quiz_request.source_material,
            'language': quiz_request.language,
            'centers': quiz_request.centers,
        }
        
        # Generate unique quiz ID
        quiz_id = f"quiz_{current_user['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # Always use quiz_id as filename prefix to ensure downloads work
        output_prefix = quiz_id
        
        # Save files (TXT)
        test_file, answer_file = quiz_generator.save_test(test_data, output_prefix)
        
        # Build marking scheme data (counts and per-type marks)
        marking_counts: Dict[str, int] = {}
        for q in test_data.get('questions', []):
            key = getattr(q, 'display_type', None) or getattr(q, 'question_type', None) or 'mcq'
            marking_counts[key] = marking_counts.get(key, 0) + 1
        test_data['marking_counts'] = marking_counts
        if 'marks_per_type' not in test_data and quiz_request.marks:
            test_data['marks_per_type'] = {k: int(v) for k, v in quiz_request.marks.items()}

        # Also generate PDFs
        pdf_q, pdf_a, pdf_ms = None, None, None
        try:
            if (quiz_request.output_engine or 'reportlab') == 'latex':
                from latex_renderer import render_quiz_pdfs, render_marking_scheme_pdf
                try:
                    pdf_q, pdf_a = render_quiz_pdfs(test_data, output_prefix, output_dir="../generated_tests")
                    pdf_ms = render_marking_scheme_pdf(test_data, output_prefix, output_dir="../generated_tests")
                except Exception as _latex_err:
                    # Fallback to ReportLab on any LaTeX failure
                    logger.warning(f"LaTeX render failed, falling back to ReportLab: {_latex_err}")
                    pdf_q, pdf_a = quiz_generator.save_test_pdf(test_data, output_prefix)
                    # Generate marking scheme via ReportLab
                    try:
                        pdf_ms = _build_marking_scheme_reportlab(test_data, output_prefix, out_dir="../generated_tests")
                    except Exception as _ms_err:
                        logger.warning(f"Marking scheme PDF (ReportLab) failed: {_ms_err}")
                        pdf_ms = None
            else:
                pdf_q, pdf_a = quiz_generator.save_test_pdf(test_data, output_prefix)
                try:
                    pdf_ms = _build_marking_scheme_reportlab(test_data, output_prefix, out_dir="../generated_tests")
                except Exception as _ms_err:
                    logger.warning(f"Marking scheme PDF (ReportLab) failed: {_ms_err}")
                    pdf_ms = None
        except Exception as _e:
            logger.warning(f"PDF render failed: {_e}")
            pdf_q, pdf_a, pdf_ms = None, None, None
        
        # Respect include_solutions flag in response (hide answers link if false)
        if not (quiz_request.include_solutions or False):
            pdf_a = None
        
        # Create response
        quiz_response = QuizResponse(
            quiz_id=quiz_id,
            title=quiz_request.title or f"Quiz on {', '.join(quiz_request.topics)}",
            questions_file=test_file,
            answers_file=answer_file,
            pdf_questions_file=pdf_q,
            pdf_answers_file=pdf_a,
            pdf_marking_scheme_file=pdf_ms,
            metadata=test_data,
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
    file_type: str = "questions",  # "questions" | "answers" | "marking_scheme"
    current_user: dict = Depends(get_current_user)
):
    """Download quiz file. Prefers PDF if available; falls back to TXT for questions/answers."""
    base_dir = Path("../generated_tests")
    # Prefer PDF
    if file_type == "marking_scheme":
        scheme_path = base_dir / f"{quiz_id}_marking_scheme.pdf"
        if scheme_path.exists():
            return FileResponse(path=scheme_path, filename=f"{quiz_id}_marking_scheme.pdf", media_type="application/pdf")
        raise HTTPException(status_code=404, detail="Marking scheme not found")
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

# Import enhanced doubt solving system (production engine)
try:
    from doubt_solving_engine_production import ProductionDoubtSolvingEngine as DoubtSolvingEngine, DoubtRequest as EngineDoubtRequest
    doubt_engine: Optional[DoubtSolvingEngine] = None
except ImportError:
    logger.warning("⚠️ Production doubt solving engine not available")
    doubt_engine = None

class EnhancedDoubtRequestModel(BaseModel):
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
    global doubt_engine
    
    if DoubtSolvingEngine:
        try:
            config = {
                "openai_api_key": os.getenv("OPENAI_API_KEY"),
                "wolfram_api_key": os.getenv("WOLFRAM_API_KEY"),
                "mathpix_api_key": os.getenv("MATHPIX_APP_ID"),
                "mathpix_api_secret": os.getenv("MATHPIX_APP_KEY")
            }
            present = {k: bool(v) for k, v in config.items()}
            logger.info(f"🔑 Doubt engine keys present: {present}")
            doubt_engine = DoubtSolvingEngine(config)
            logger.info("✅ Production doubt solving engine initialized")
            
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
async def solve_doubt_enhanced(request: EnhancedDoubtRequestModel):
    """Enhanced AI-powered doubt solving with usage limits"""
    
    if not doubt_engine:
        # Fallback to basic doubt solving
        basic_request = DoubtRequest(
            question=request.question,
            subject=request.subject
        )
        basic_response = await solve_doubt(basic_request)
        
        # Attempt to render handwritten from basic data
        handwritten_url = None
        handwritten_images = []
        try:
            from handwriting_renderer import render_handwritten
            payload = {
                "question": request.question,
                "answer": basic_response.answer,
                "steps": [
                    {"title": f"Related: {t}", "explanation": ""} for t in basic_response.related_topics
                ],
                "mobile_format": {
                    "shortAnswer": basic_response.answer,
                    "keySteps": basic_response.practice_suggestions,
                }
            }
            prefix = f"hs_{request.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result = render_handwritten(payload, prefix, out_dir="../generated_solutions", image_format="png", also_pdf=True)
            # Build URLs
            for ip in result.get("images", []) or []:
                handwritten_images.append(f"/api/doubt/handwritten/{Path(ip).name}")
            if result.get("pdf"):
                handwritten_url = f"/api/doubt/handwritten/{Path(result['pdf']).name}"
        except Exception:
            handwritten_url = None
            handwritten_images = []
        
        return EnhancedDoubtResponse(
            success=True,
            solution={
                "answer": basic_response.answer,
                "explanation": basic_response.explanation,
                "method": "textbook_fallback",
                "handwritten_pdf_url": handwritten_url,
                "handwritten_images": handwritten_images
            },
            usage_info={"note": "Using basic mode - enhanced AI not available"}
        )
    
    try:
        # Create enhanced doubt request for engine
        engine_req = EngineDoubtRequest(
            question_text=request.question,
            subject=request.subject,
            user_id=request.user_id,
            user_plan=request.user_plan,
            context=request.context
        )
        
        # Add image data if provided
        if request.image_data:
            import base64
            engine_req.image_data = base64.b64decode(request.image_data)
        
        # Solve the doubt
        solution = await doubt_engine.solve_doubt(engine_req)
        
        # Render handwritten from solution payload (best-effort)
        handwritten_url = None
        handwritten_images = []
        try:
            from handwriting_renderer import render_handwritten
            payload = {
                "question": getattr(solution, 'question', request.question),
                "answer": getattr(solution, 'final_answer', None) or getattr(solution, 'answer', None),
                "steps": [
                    {"title": getattr(s, 'title', None) or getattr(s, 'heading', None) or f"Step {i+1}",
                     "explanation": getattr(s, 'explanation', None) or getattr(s, 'detail', None) or ""}
                    for i, s in enumerate(getattr(solution, 'steps', []) or [])
                ],
                "mobile_format": getattr(solution, 'mobile_format', None) or {}
            }
            prefix = f"hs_{request.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result = render_handwritten(payload, prefix, out_dir="../generated_solutions", image_format="png", also_pdf=True)
            for ip in result.get("images", []) or []:
                handwritten_images.append(f"/api/doubt/handwritten/{Path(ip).name}")
            if result.get("pdf"):
                handwritten_url = f"/api/doubt/handwritten/{Path(result['pdf']).name}"
        except Exception as _hw_e:
            logger.warning(f"Handwritten render failed: {_hw_e}")
            handwritten_url = None
            handwritten_images = []
        
        # Get usage information
        usage_check = await doubt_engine._check_usage_limits(request.user_id, request.user_plan)
        
        return EnhancedDoubtResponse(
            success=True,
            solution={
                **(getattr(solution, 'mobile_format', {}) or {}),
                "handwritten_pdf_url": handwritten_url,
                "handwritten_images": handwritten_images
            },
            usage_info={
                "remaining_doubts": usage_check["remaining"],
                "used_this_month": usage_check["used"],
                "plan": usage_check["plan"],
                "reset_date": str(usage_check["reset_date"])
            },
            cost_info={
                "method_used": getattr(solution, 'solution_method', None),
                "cost_incurred": getattr(solution, 'cost_incurred', 0.0),
                "time_taken": getattr(solution, 'time_taken', 0.0)
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
        
        # Create engine request
        engine_req = EngineDoubtRequest(
            image_data=image_data,
            subject=subject,
            user_id=user_id,
            user_plan=user_plan
        )
        
        # Solve the doubt
        solution = await doubt_engine.solve_doubt(engine_req)
        
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
    """Get user's doubt usage statistics (from engine usage_db)."""
    
    if not doubt_engine:
        return {"error": "Doubt engine not available"}
    
    try:
        current_month = datetime.now().strftime("%Y-%m")
        user_key = f"{user_id}_{current_month}"
        usage = getattr(doubt_engine, 'usage_db', {}).get(user_key, {})
        return {
            "current_month": {
                "doubts_used": usage.get("doubts_used", 0),
                "total_cost": usage.get("total_cost", 0.0),
                "methods_used": usage.get("methods_used", {}),
                "plan": usage.get("plan", "basic"),
                "reset_date": str(usage.get("reset_date", ""))
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get usage data: {e}")
        raise HTTPException(status_code=500, detail="Failed to get usage data")

# ================================================================================
# 📝 Handwritten Solution Download Endpoint
# ================================================================================

@app.get("/api/doubt/handwritten/{filename}")
async def download_handwritten(filename: str):
    base_dir = Path("../generated_solutions")
    fpath = base_dir / filename
    if not fpath.exists() or not fpath.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    # Detect media type by extension
    ext = fpath.suffix.lower()
    if ext == ".pdf":
        mt = "application/pdf"
    elif ext in (".png", ".apng"):
        mt = "image/png"
    elif ext in (".jpg", ".jpeg"):
        mt = "image/jpeg"
    else:
        mt = "application/octet-stream"
    return FileResponse(path=str(fpath), filename=filename, media_type=mt)

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
# 🧩 Static UI: Quiz Builder
# ================================================================================

# Mount /static for simple HTML/JS UI
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/ui/quiz", response_class=HTMLResponse)
async def quiz_ui():
    """Serve the quiz builder UI."""
    index_path = static_dir / "quiz" / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    # Fallback simple HTML if file missing
    return HTMLResponse("<h1>Quiz UI not found</h1><p>Add files under backend/static/quiz/</p>", status_code=200)

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
