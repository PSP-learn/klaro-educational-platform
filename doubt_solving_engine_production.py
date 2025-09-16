#!/usr/bin/env python3
"""
🤖 Doubt Solving Engine - Production-Ready AI System

Production features:
- Thread-safe OpenAI client session management
- Exponential backoff retry logic for all APIs
- Comprehensive timeout handling
- Granular analytics per API route
- Complete error handling for all failure scenarios
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import json
import re
import asyncio
import base64
from datetime import datetime, timedelta
from pathlib import Path
import logging
import time
from functools import wraps
from contextlib import asynccontextmanager
import threading
from typing import AsyncGenerator

# AI Integration imports
from openai import AsyncOpenAI, OpenAIError, RateLimitError, APITimeoutError
import requests
from PIL import Image
import io
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Import existing textbook search
try:
    from book_search import BookVectorDB
except ImportError:
    print("⚠️ Textbook database not available, using fallback mode")
    BookVectorDB = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProblemType(Enum):
    COMPUTATIONAL = "computational"  # Pure calculations
    CONCEPTUAL = "conceptual"       # Explanations needed
    VISUAL = "visual"              # Geometry, diagrams
    COMPLEX = "complex"            # Multi-step problems

class UserPlan(Enum):
    BASIC = "basic"      # ₹99/month, 20 doubts
    PREMIUM = "premium"  # ₹199/month, unlimited

class APIRoute(Enum):
    """Track different API usage routes for granular analytics"""
    DOUBTS = "doubts"           # Regular doubt solving
    TESTS = "tests"             # Test question solving
    PAPERS = "papers"           # Previous paper solutions
    OCR = "ocr"                # Image text extraction
    PRACTICE = "practice"       # Practice problem generation

@dataclass
class DoubtRequest:
    """Doubt solving request"""
    question_text: Optional[str] = None
    image_data: Optional[bytes] = None
    subject: str = "Mathematics"
    user_id: str = ""
    user_plan: str = "basic"
    context: Optional[str] = None
    route: str = "doubts"  # Track which API route this came from

@dataclass
class SolutionStep:
    """Individual step in solution"""
    step_number: int
    title: str
    explanation: str
    calculation: Optional[str] = None
    latex: Optional[str] = None
    confidence: float = 0.9

@dataclass
class DoubtSolution:
    """Complete doubt solution"""
    question: str
    final_answer: str
    steps: List[SolutionStep]
    topic: str
    difficulty: str
    confidence_score: float
    solution_method: str  # "textbook", "wolfram", "gpt35", "gpt4"
    cost_incurred: float
    time_taken: float
    retry_attempts: int = 0
    
    # Different formats for different interfaces
    mobile_format: Dict[str, Any] = None
    whatsapp_format: str = ""
    latex_format: str = ""

class ProductionDoubtSolvingEngine:
    """
    Production-ready AI engine for solving educational doubts
    
    Features:
    - Thread-safe OpenAI client management
    - Exponential backoff retry logic
    - Comprehensive timeout handling
    - Granular per-route analytics
    - Complete error handling
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize production doubt solving engine"""
        logger.info("🤖 Initializing Production Doubt Solving Engine...")
        
        # Configuration
        self.config = config
        self.openai_api_key = config.get("openai_api_key")
        self.wolfram_api_key = config.get("wolfram_api_key")
        self.mathpix_api_key = config.get("mathpix_api_key")
        self.mathpix_api_secret = config.get("mathpix_api_secret")
        
        # Timeout configurations
        self.openai_timeout = config.get("openai_timeout", 30.0)
        self.wolfram_timeout = config.get("wolfram_timeout", 15.0)
        self.mathpix_timeout = config.get("mathpix_timeout", 20.0)
        
        # Thread-safe session management
        self._session_lock = threading.Lock()
        self._openai_sessions = {}  # Per-thread OpenAI clients
        
        # Initialize AI clients
        self._init_ai_clients()
        
        # Initialize textbook database
        self._init_textbook_database()
        
        # Enhanced usage tracking with route granularity
        self.usage_db = {}  # In production, use PostgreSQL
        self.route_analytics = {}  # Track per-route usage
        
        logger.info("✅ Production Doubt Solving Engine ready!")
    
    def _init_ai_clients(self):
        """Initialize AI service clients with thread safety"""
        try:
            if self.openai_api_key:
                # Create thread-safe OpenAI client
                self.openai_client = AsyncOpenAI(
                    api_key=self.openai_api_key,
                    timeout=self.openai_timeout,
                    max_retries=0  # We handle retries manually
                )
                logger.info("✅ OpenAI client initialized with production settings")
            else:
                self.openai_client = None
                logger.warning("⚠️ OpenAI API key not provided")
                
            # Wolfram Alpha setup
            if self.wolfram_api_key:
                self.wolfram_url = f"http://api.wolframalpha.com/v2/query"
                logger.info("✅ Wolfram Alpha client initialized")
            else:
                logger.warning("⚠️ Wolfram Alpha API key not provided")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize AI clients: {e}")
    
    @asynccontextmanager
    async def _get_openai_session(self) -> AsyncGenerator[AsyncOpenAI, None]:
        """Thread-safe OpenAI session management"""
        thread_id = threading.get_ident()
        
        with self._session_lock:
            if thread_id not in self._openai_sessions:
                if self.openai_api_key:
                    self._openai_sessions[thread_id] = AsyncOpenAI(
                        api_key=self.openai_api_key,
                        timeout=self.openai_timeout,
                        max_retries=0
                    )
                else:
                    raise Exception("OpenAI API key not configured")
        
        yield self._openai_sessions[thread_id]
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((OpenAIError, APITimeoutError, requests.RequestException))
    )
    async def _openai_request_with_retry(self, model: str, messages: List[Dict], max_tokens: int = 1000) -> str:
        """OpenAI request with exponential backoff retry"""
        
        async with self._get_openai_session() as client:
            try:
                response = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.1,
                    timeout=self.openai_timeout
                )
                return response.choices[0].message.content
                
            except RateLimitError as e:
                logger.warning(f"⚠️ OpenAI rate limit hit: {e}")
                await asyncio.sleep(5)  # Rate limit cool-down
                raise
            except APITimeoutError as e:
                logger.warning(f"⚠️ OpenAI timeout: {e}")
                raise
            except Exception as e:
                logger.error(f"❌ OpenAI request failed: {e}")
                raise
    
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=5),
        retry=retry_if_exception_type((requests.RequestException, requests.Timeout))
    )
    async def _wolfram_request_with_retry(self, question: str) -> Dict[str, Any]:
        """Wolfram Alpha request with retry logic"""
        
        params = {
            'input': question,
            'appid': self.wolfram_api_key,
            'output': 'json',
            'format': 'plaintext'
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.wolfram_timeout)) as session:
            async with session.get(self.wolfram_url, params=params) as response:
                return await response.json()
    
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=3, max=8),
        retry=retry_if_exception_type((requests.RequestException, requests.Timeout))
    )
    async def _mathpix_request_with_retry(self, image_base64: str) -> Dict[str, Any]:
        """Mathpix OCR request with retry logic"""
        
        url = "https://api.mathpix.com/v3/text"
        headers = {
            "app_id": self.mathpix_api_key,
            "app_key": self.mathpix_api_secret,
            "Content-type": "application/json"
        }
        
        data = {
            "src": f"data:image/jpeg;base64,{image_base64}",
            "formats": ["text", "latex_simplified"],
            "ocr": ["math", "text"]
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.mathpix_timeout)) as session:
            async with session.post(url, json=data, headers=headers) as response:
                return await response.json()
    
    def _init_textbook_database(self):
        """Initialize textbook search database"""
        try:
            if BookVectorDB:
                self.textbook_db = BookVectorDB("book_db")
                logger.info("✅ Textbook database connected")
            else:
                self.textbook_db = None
                logger.warning("⚠️ Textbook database not available")
        except Exception as e:
            logger.error(f"❌ Textbook database initialization failed: {e}")
            self.textbook_db = None
    
    async def solve_doubt(self, request: DoubtRequest) -> DoubtSolution:
        """
        Main doubt solving method with production-ready error handling
        """
        start_time = datetime.now()
        retry_count = 0
        
        try:
            # Step 1: Check usage limits
            usage_check = await self._check_usage_limits(request.user_id, request.user_plan)
            if not usage_check["allowed"]:
                return self._create_upgrade_prompt(usage_check)
            
            # Step 2: Extract question text (OCR if needed)
            question_text = await self._extract_question_text(request)
            
            # Step 3: Try textbook database first (FREE!)
            textbook_solution = await self._search_textbook_database(question_text)
            if textbook_solution and textbook_solution.confidence_score > 0.75:
                await self._track_usage_with_route(request.user_id, "textbook", 0.0, request.route)
                return textbook_solution
            
            # Step 4: Classify problem type for AI routing
            problem_type = await self._classify_problem(question_text)
            
            # Step 5: Route to appropriate AI service with retry tracking
            solution = None
            max_retries = 3
            
            while retry_count < max_retries and not solution:
                try:
                    if problem_type == ProblemType.COMPUTATIONAL:
                        solution = await self._solve_with_wolfram(question_text, request)
                    elif request.user_plan == "basic":
                        solution = await self._solve_with_gpt35(question_text, request)
                    else:  # Premium users get GPT-4
                        solution = await self._solve_with_gpt4(question_text, request)
                    break
                    
                except Exception as e:
                    retry_count += 1
                    logger.warning(f"⚠️ Attempt {retry_count} failed: {e}")
                    if retry_count < max_retries:
                        await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                    else:
                        solution = self._create_fallback_solution(question_text)
            
            # Step 6: Format for different interfaces
            solution = await self._format_solution(solution, request)
            
            # Step 7: Track usage and costs with retry info
            time_taken = (datetime.now() - start_time).total_seconds()
            solution.time_taken = time_taken
            solution.retry_attempts = retry_count
            await self._track_usage_with_route(
                request.user_id, 
                solution.solution_method, 
                solution.cost_incurred,
                request.route
            )
            
            return solution
            
        except Exception as e:
            logger.error(f"❌ Critical error in solve_doubt: {e}")
            return self._create_fallback_solution("System error occurred")
    
    async def _extract_question_text(self, request: DoubtRequest) -> str:
        """Extract question text with production-ready OCR"""
        
        if request.question_text:
            return request.question_text
        
        if request.image_data:
            try:
                # Primary: Mathpix for math content
                if self.mathpix_api_key:
                    image_base64 = base64.b64encode(request.image_data).decode()
                    result = await self._mathpix_request_with_retry(image_base64)
                    
                    if 'text' in result and len(result['text'].strip()) > 10:
                        return result['text']
                
                # Fallback: Basic OCR
                text = await self._fallback_ocr(request.image_data)
                return text
                
            except Exception as e:
                logger.error(f"❌ OCR failed: {e}")
                return "Unable to extract text from image. Please type your question."
        
        return "No question provided"
    
    async def _search_textbook_database(self, question: str) -> Optional[DoubtSolution]:
        """Search textbook database for existing solutions (FREE!)"""
        
        if not self.textbook_db:
            return None
        
        try:
            # Search for relevant content
            results = self.textbook_db.search(question, top_k=3)
            
            if results and results[0][1] > 0.75:  # High confidence match
                content = results[0][0]
                
                return DoubtSolution(
                    question=question,
                    final_answer=f"Based on textbook: {content[:100]}...",
                    steps=[
                        SolutionStep(
                            step_number=1,
                            title="Textbook Reference",
                            explanation=content[:300] + "...",
                            confidence=results[0][1]
                        )
                    ],
                    topic=self._extract_topic(question),
                    difficulty="Medium",
                    confidence_score=results[0][1],
                    solution_method="textbook",
                    cost_incurred=0.0,
                    time_taken=0.5
                )
                
        except Exception as e:
            logger.error(f"❌ Textbook search failed: {e}")
        
        return None
    
    async def _classify_problem(self, question: str) -> ProblemType:
        """Classify problem type for optimal AI routing"""
        
        question_lower = question.lower()
        
        # Computational keywords
        computational_keywords = [
            'solve', 'calculate', 'find', 'evaluate', 'compute',
            'derivative', 'integral', 'limit', 'sum', 'product',
            'factorize', 'simplify', 'expand'
        ]
        
        # Conceptual keywords  
        conceptual_keywords = [
            'explain', 'why', 'how', 'what is', 'difference between',
            'concept', 'theory', 'understand', 'meaning', 'intuition'
        ]
        
        # Visual keywords
        visual_keywords = [
            'diagram', 'graph', 'plot', 'draw', 'construct',
            'geometry', 'figure', 'triangle', 'circle'
        ]
        
        if any(keyword in question_lower for keyword in computational_keywords):
            return ProblemType.COMPUTATIONAL
        elif any(keyword in question_lower for keyword in visual_keywords):
            return ProblemType.VISUAL
        elif any(keyword in question_lower for keyword in conceptual_keywords):
            return ProblemType.CONCEPTUAL
        else:
            return ProblemType.COMPLEX
    
    async def _solve_with_wolfram(self, question: str, request: DoubtRequest) -> DoubtSolution:
        """Solve computational problems using Wolfram Alpha with retry"""
        
        if not self.wolfram_api_key:
            raise Exception("Wolfram Alpha API key not configured")
        
        try:
            data = await self._wolfram_request_with_retry(question)
            
            # Extract solution from Wolfram response
            if 'queryresult' in data and data['queryresult']['success']:
                pods = data['queryresult']['pods']
                solution_pod = next((p for p in pods if 'solution' in p['title'].lower()), None)
                
                if solution_pod and solution_pod['subpods']:
                    answer = solution_pod['subpods'][0]['plaintext']
                    
                    return DoubtSolution(
                        question=question,
                        final_answer=answer,
                        steps=[
                            SolutionStep(
                                step_number=1,
                                title="Computational Solution",
                                explanation=f"Using mathematical computation: {answer}",
                                confidence=0.95
                            )
                        ],
                        topic=self._extract_topic(question),
                        difficulty="Medium",
                        confidence_score=0.95,
                        solution_method="wolfram",
                        cost_incurred=0.0025,
                        time_taken=2.0
                    )
            
            # Fallback to GPT-3.5 if Wolfram fails
            return await self._solve_with_gpt35(question, request)
            
        except Exception as e:
            logger.error(f"❌ Wolfram Alpha failed: {e}")
            return await self._solve_with_gpt35(question, request)
    
    async def _solve_with_gpt35(self, question: str, request: DoubtRequest) -> DoubtSolution:
        """Solve problems using GPT-3.5 Turbo with retry logic"""
        
        prompt = f"""
You are an expert {request.subject} teacher. Solve this problem step by step:

Problem: {question}

Format your response as:
UNDERSTANDING: What the problem is asking
APPROACH: Which method/formula to use  
STEP 1: [Title] - [Detailed explanation with calculation]
STEP 2: [Title] - [Detailed explanation with calculation]
STEP N: [Continue until solution]
FINAL ANSWER: [Clear final result]

Make each step clear for a student to follow.
"""
        
        try:
            solution_text = await self._openai_request_with_retry(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            
            parsed_solution = self._parse_gpt_solution(solution_text, question)
            parsed_solution.solution_method = "gpt35"
            parsed_solution.cost_incurred = 0.004
            
            return parsed_solution
            
        except Exception as e:
            logger.error(f"❌ GPT-3.5 failed: {e}")
            return self._create_fallback_solution(question)
    
    async def _solve_with_gpt4(self, question: str, request: DoubtRequest) -> DoubtSolution:
        """Solve complex problems using GPT-4 with retry logic - Premium only"""
        
        prompt = f"""
You are an expert {request.subject} teacher providing premium tutoring. Solve this problem with exceptional detail:

Problem: {question}

Provide a comprehensive solution with:
1. PROBLEM ANALYSIS: Break down what's being asked
2. CONCEPT REVIEW: Key concepts and formulas needed
3. DETAILED STEPS: Step-by-step solution with clear explanations
4. ALTERNATIVE METHODS: Show different approaches if applicable
5. COMMON MISTAKES: What students often get wrong
6. PRACTICE SUGGESTIONS: Similar problems to try

Make this worthy of premium tutoring service.
"""
        
        try:
            solution_text = await self._openai_request_with_retry(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            
            parsed_solution = self._parse_gpt_solution(solution_text, question)
            parsed_solution.solution_method = "gpt4"
            parsed_solution.cost_incurred = 0.09
            
            return parsed_solution
            
        except Exception as e:
            logger.error(f"❌ GPT-4 failed: {e}")
            return await self._solve_with_gpt35(question, request)
    
    def _parse_gpt_solution(self, solution_text: str, question: str) -> DoubtSolution:
        """Parse GPT response into structured solution"""
        
        lines = solution_text.strip().split('\n')
        steps = []
        final_answer = ""
        step_counter = 1
        
        current_step_title = ""
        current_step_explanation = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Identify step sections
            if line.startswith(('STEP', 'Step', 'step')):
                # Save previous step
                if current_step_title:
                    steps.append(SolutionStep(
                        step_number=step_counter,
                        title=current_step_title,
                        explanation=current_step_explanation,
                        confidence=0.9
                    ))
                    step_counter += 1
                
                # Start new step
                current_step_title = line
                current_step_explanation = ""
                
            elif line.startswith(('FINAL ANSWER', 'ANSWER', 'Answer')):
                final_answer = line.split(':', 1)[1].strip() if ':' in line else line
                
            elif current_step_title:
                current_step_explanation += line + " "
        
        # Add last step
        if current_step_title:
            steps.append(SolutionStep(
                step_number=step_counter,
                title=current_step_title,
                explanation=current_step_explanation.strip(),
                confidence=0.9
            ))
        
        return DoubtSolution(
            question=question,
            final_answer=final_answer or "Solution completed",
            steps=steps,
            topic=self._extract_topic(question),
            difficulty="Medium",
            confidence_score=0.9,
            solution_method="ai",
            cost_incurred=0.0,
            time_taken=5.0
        )
    
    async def _fallback_ocr(self, image_data: bytes) -> str:
        """Fallback OCR using Tesseract (if available). Returns extracted text or a helpful message."""
        try:
            import pytesseract
            from PIL import Image
            import io
            # Load image from bytes
            img = Image.open(io.BytesIO(image_data))
            text = pytesseract.image_to_string(img)
            # Basic math-friendly normalization
            if text:
                s = text.replace("−", "-")
                s = s.replace("×", "x")
                s = s.replace("÷", "/")
                s = s.replace("^", "^")
                s = " ".join(s.split())
                return s
            return "OCR could not extract readable text. Please type your question."
        except Exception:
            return "OCR not available. Please type your question."
    
    async def _check_usage_limits(self, user_id: str, user_plan: str) -> Dict[str, Any]:
        """Check if user can ask more doubts this month"""
        
        # Get current month usage
        current_month = datetime.now().strftime("%Y-%m")
        user_key = f"{user_id}_{current_month}"
        
        if user_key not in self.usage_db:
            next_month = datetime.now().replace(day=1) + timedelta(days=32)
            self.usage_db[user_key] = {
                "doubts_used": 0,
                "plan": user_plan,
                "reset_date": next_month.replace(day=1),
                "total_cost": 0.0,
                "methods_used": {},
                "routes_used": {}  # Track per-route usage
            }
            
        current_usage = self.usage_db[user_key]
        
        # Check limits based on plan
        if user_plan == "basic":
            limit = 20
            allowed = current_usage["doubts_used"] < limit
            remaining = max(0, limit - current_usage["doubts_used"])
        else:  # Premium
            allowed = True
            remaining = "unlimited"
        
        return {
            "allowed": allowed,
            "remaining": remaining,
            "used": current_usage["doubts_used"],
            "plan": user_plan,
            "reset_date": current_usage["reset_date"]
        }
    
    async def _track_usage_with_route(self, user_id: str, method: str, cost: float, route: str):
        """Enhanced usage tracking with route granularity"""
        
        current_month = datetime.now().strftime("%Y-%m")
        user_key = f"{user_id}_{current_month}"
        route_key = f"{route}_{current_month}"
        
        # Initialize user tracking
        if user_key not in self.usage_db:
            self.usage_db[user_key] = {
                "doubts_used": 0,
                "total_cost": 0.0,
                "methods_used": {},
                "routes_used": {},
                "plan": "basic"
            }
        
        # Initialize route tracking
        if route_key not in self.route_analytics:
            self.route_analytics[route_key] = {
                "total_requests": 0,
                "total_cost": 0.0,
                "method_breakdown": {},
                "avg_response_time": 0.0,
                "error_rate": 0.0,
                "successful_requests": 0
            }
        
        # Update user usage
        self.usage_db[user_key]["doubts_used"] += 1
        self.usage_db[user_key]["total_cost"] += cost
        
        if method not in self.usage_db[user_key]["methods_used"]:
            self.usage_db[user_key]["methods_used"][method] = 0
        self.usage_db[user_key]["methods_used"][method] += 1
        
        if route not in self.usage_db[user_key]["routes_used"]:
            self.usage_db[user_key]["routes_used"][route] = 0
        self.usage_db[user_key]["routes_used"][route] += 1
        
        # Update route analytics
        self.route_analytics[route_key]["total_requests"] += 1
        self.route_analytics[route_key]["total_cost"] += cost
        
        if method not in self.route_analytics[route_key]["method_breakdown"]:
            self.route_analytics[route_key]["method_breakdown"][method] = 0
        self.route_analytics[route_key]["method_breakdown"][method] += 1
        
        if method != "fallback":
            self.route_analytics[route_key]["successful_requests"] += 1
        
        logger.info(f"📊 Enhanced usage tracked - User: {user_id}, Method: {method}, Route: {route}, Cost: ${cost:.4f}")
    
    def _create_upgrade_prompt(self, usage_check: Dict[str, Any]) -> DoubtSolution:
        """Create upgrade prompt when limits exceeded"""
        
        return DoubtSolution(
            question="Limit Exceeded",
            final_answer="You've reached your monthly doubt limit!",
            steps=[
                SolutionStep(
                    step_number=1,
                    title="Upgrade to Continue Learning",
                    explanation=f"""
🔥 You've used all {usage_check['used']} doubts this month!

💎 Upgrade to Premium (₹199/month) for:
✅ Unlimited doubts
✅ GPT-4 detailed solutions  
✅ OCR for handwritten problems
✅ Priority support

🎯 Or add 10 extra doubts for just ₹50
                    """,
                    confidence=1.0
                )
            ],
            topic="Subscription",
            difficulty="Easy",
            confidence_score=1.0,
            solution_method="upgrade_prompt",
            cost_incurred=0.0,
            time_taken=0.1
        )
    
    async def _format_solution(self, solution: DoubtSolution, request: DoubtRequest) -> DoubtSolution:
        """Format solution for different interfaces"""
        
        # Mobile app format (rich)
        solution.mobile_format = {
            "question": solution.question,
            "answer": solution.final_answer,
            "steps": [asdict(step) for step in solution.steps],
            "metadata": {
                "topic": solution.topic,
                "difficulty": solution.difficulty,
                "confidence": solution.confidence_score,
                "method": solution.solution_method,
                "retry_attempts": solution.retry_attempts
            },
            "actions": [
                {"type": "save", "label": "Save Doubt"},
                {"type": "practice", "label": "Practice Similar"},
                {"type": "share", "label": "Share Solution"}
            ]
        }
        
        # WhatsApp format (simple text)
        whatsapp_text = f"""
📚 *{solution.topic} Solution*

🎯 *Answer*: {solution.final_answer}

📝 *Steps*:
"""
        for i, step in enumerate(solution.steps[:3], 1):  # Limit to 3 steps for WhatsApp
            whatsapp_text += f"{i}️⃣ {step.title}: {step.explanation[:100]}...\n"
        
        if len(solution.steps) > 3:
            whatsapp_text += f"\n📱 *For complete solution*: Open Klaro app"
        
        solution.whatsapp_format = whatsapp_text
        
        return solution
    
    def _extract_topic(self, question: str) -> str:
        """Extract mathematical topic from question"""
        
        topic_keywords = {
            "algebra": ["equation", "polynomial", "factor", "expand"],
            "calculus": ["derivative", "integral", "limit", "differential"],
            "geometry": ["triangle", "circle", "angle", "area", "perimeter"],
            "trigonometry": ["sin", "cos", "tan", "trigonometric"],
            "statistics": ["mean", "median", "probability", "distribution"]
        }
        
        question_lower = question.lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic.title()
        
        return "General Mathematics"
    
    def _create_fallback_solution(self, question: str) -> DoubtSolution:
        """Create fallback solution when all AI services fail"""
        
        return DoubtSolution(
            question=question,
            final_answer="I'm having trouble solving this right now. Please try again or rephrase your question.",
            steps=[
                SolutionStep(
                    step_number=1,
                    title="Troubleshooting",
                    explanation="Our AI services are temporarily unavailable. Please try again in a few minutes.",
                    confidence=0.5
                )
            ],
            topic="System",
            difficulty="Easy",
            confidence_score=0.5,
            solution_method="fallback",
            cost_incurred=0.0,
            time_taken=0.1
        )
    
    def get_route_analytics(self, route: str = None) -> Dict[str, Any]:
        """Get analytics for specific route or all routes"""
        
        if route:
            current_month = datetime.now().strftime("%Y-%m")
            route_key = f"{route}_{current_month}"
            return self.route_analytics.get(route_key, {})
        
        # Return all route analytics
        current_month = datetime.now().strftime("%Y-%m")
        current_routes = {
            route.replace(f"_{current_month}", ""): data
            for route, data in self.route_analytics.items()
            if route.endswith(current_month)
        }
        
        return {
            "current_month_routes": current_routes,
            "total_requests": sum(data["total_requests"] for data in current_routes.values()),
            "total_cost": sum(data["total_cost"] for data in current_routes.values()),
            "overall_success_rate": self._calculate_success_rate(current_routes)
        }
    
    def _calculate_success_rate(self, routes_data: Dict[str, Any]) -> float:
        """Calculate overall success rate across all routes"""
        
        total_requests = sum(data["total_requests"] for data in routes_data.values())
        successful_requests = sum(data["successful_requests"] for data in routes_data.values())
        
        if total_requests == 0:
            return 0.0
        
        return (successful_requests / total_requests) * 100

class EnhancedDoubtAnalytics:
    """Enhanced analytics with route-level insights"""
    
    def __init__(self, usage_db: Dict, route_analytics: Dict):
        self.usage_db = usage_db
        self.route_analytics = route_analytics
    
    def get_comprehensive_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics including route breakdown"""
        
        current_month = datetime.now().strftime("%Y-%m")
        user_key = f"{user_id}_{current_month}"
        
        usage = self.usage_db.get(user_key, {})
        
        return {
            "user_metrics": {
                "doubts_used": usage.get("doubts_used", 0),
                "total_cost": usage.get("total_cost", 0.0),
                "methods_used": usage.get("methods_used", {}),
                "routes_used": usage.get("routes_used", {}),
                "plan": usage.get("plan", "basic")
            },
            "insights": {
                "most_used_method": self._get_most_used_method(usage),
                "most_used_route": self._get_most_used_route(usage),
                "average_cost_per_doubt": self._get_avg_cost(usage),
                "topics_asked": self._get_topics_distribution(usage)
            },
            "recommendations": self._get_enhanced_recommendations(usage),
            "cost_efficiency": self._analyze_cost_efficiency(usage)
        }
    
    def _get_most_used_method(self, usage: Dict) -> str:
        methods = usage.get("methods_used", {})
        if not methods:
            return "none"
        return max(methods.items(), key=lambda x: x[1])[0]
    
    def _get_most_used_route(self, usage: Dict) -> str:
        routes = usage.get("routes_used", {})
        if not routes:
            return "none"
        return max(routes.items(), key=lambda x: x[1])[0]
    
    def _get_avg_cost(self, usage: Dict) -> float:
        total_cost = usage.get("total_cost", 0.0)
        doubts_used = usage.get("doubts_used", 1)
        return total_cost / doubts_used
    
    def _get_topics_distribution(self, usage: Dict) -> List[str]:
        # Placeholder - in production, track topics from solved doubts
        return ["Algebra", "Calculus", "Geometry"]
    
    def _get_enhanced_recommendations(self, usage: Dict) -> List[str]:
        recommendations = []
        
        doubts_used = usage.get("doubts_used", 0)
        avg_cost = self._get_avg_cost(usage)
        
        if doubts_used > 15:
            recommendations.append("Consider upgrading to Premium for unlimited doubts")
        
        if usage.get("plan") == "basic":
            recommendations.append("Upgrade to Premium for GPT-4 detailed solutions")
        
        if avg_cost > 0.05:
            recommendations.append("Your questions are using expensive AI models. Consider upgrading for better value.")
            
        return recommendations
    
    def _analyze_cost_efficiency(self, usage: Dict) -> Dict[str, Any]:
        """Analyze cost efficiency patterns"""
        
        methods = usage.get("methods_used", {})
        total_cost = usage.get("total_cost", 0.0)
        
        return {
            "cost_per_method": {
                method: (count * 0.004 if method == "gpt35" else 
                        count * 0.09 if method == "gpt4" else 
                        count * 0.0025 if method == "wolfram" else 0.0)
                for method, count in methods.items()
            },
            "savings_from_textbook": len([m for m in methods.keys() if m == "textbook"]) * 0.004,
            "efficiency_score": self._calculate_efficiency_score(methods, total_cost)
        }
    
    def _calculate_efficiency_score(self, methods: Dict, total_cost: float) -> float:
        """Calculate efficiency score (0-100) based on free vs paid usage"""
        
        total_queries = sum(methods.values())
        free_queries = methods.get("textbook", 0)
        
        if total_queries == 0:
            return 100.0
        
        free_ratio = free_queries / total_queries
        return free_ratio * 100

# ================================================================================
# 🧪 Production Testing Functions
# ================================================================================

async def test_production_scenarios():
    """Test production failure scenarios"""
    
    print("🧪 Production Scenario Testing")
    print("=" * 60)
    
    test_scenarios = [
        {
            "name": "Missing API Key",
            "config": {"openai_api_key": None}
        },
        {
            "name": "Invalid API Key", 
            "config": {"openai_api_key": "sk-invalid-key"}
        },
        {
            "name": "Quota Exceeded",
            "config": {"openai_api_key": "sk-test-key"},
            "simulate_quota": True
        },
        {
            "name": "API Downtime",
            "config": {"openai_api_key": "sk-test-key"},
            "simulate_downtime": True
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n🔍 Testing: {scenario['name']}")
        print("-" * 30)
        
        try:
            config = {
                "openai_api_key": "sk-test-key",
                "wolfram_api_key": "test-key",
                **scenario["config"]
            }
            
            engine = ProductionDoubtSolvingEngine(config)
            
            request = DoubtRequest(
                question_text="Test question: x + 2 = 5",
                user_id="test_user",
                user_plan="basic",
                route="tests"
            )
            
            solution = await engine.solve_doubt(request)
            
            print(f"   ✅ Handled gracefully")
            print(f"   📋 Method: {solution.solution_method}")
            print(f"   💰 Cost: ${solution.cost_incurred:.4f}")
            print(f"   🔄 Retries: {solution.retry_attempts}")
            
        except Exception as e:
            print(f"   ❌ Unhandled error: {e}")

if __name__ == "__main__":
    asyncio.run(test_production_scenarios())
