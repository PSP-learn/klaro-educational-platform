#!/usr/bin/env python3
"""
🤖 Doubt Solving Engine - Core AI System

Cost-optimized doubt solving assistant with:
- Smart AI routing (Textbook → Wolfram → GPT-3.5 → GPT-4)
- Usage tracking and limits (20 doubts for ₹99 plan)
- OCR integration for handwritten problems
- Step-by-step solution generation
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
from openai import AsyncOpenAI
import requests
from PIL import Image
import io
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from fractions import Fraction

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

@dataclass
class DoubtRequest:
    """Doubt solving request"""
    question_text: Optional[str] = None
    image_data: Optional[bytes] = None
    subject: str = "Mathematics"
    user_id: str = ""
    user_plan: str = "basic"
    context: Optional[str] = None

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
    
    # Different formats for different interfaces
    mobile_format: Dict[str, Any] = None
    whatsapp_format: str = ""
    latex_format: str = ""

class DoubtSolvingEngine:
    """
    Core AI engine for solving educational doubts
    
    Features:
    - Cost-optimized AI routing
    - Multiple solution sources
    - Usage tracking and limits
    - OCR for handwritten problems
    - Production-ready concurrency and retry logic
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize doubt solving engine"""
        logger.info("🤖 Initializing Doubt Solving Engine...")
        
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
        
        # Usage tracking with route granularity
        self.usage_db = {}  # In production, use PostgreSQL
        self.route_analytics = {}  # Track per-route usage
        
        logger.info("✅ Doubt Solving Engine ready!")
    
    def _init_ai_clients(self):
        """Initialize AI service clients"""
        try:
            if self.openai_api_key:
                self.openai_client = AsyncOpenAI(api_key=self.openai_api_key)
                logger.info("✅ OpenAI client initialized")
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
        Main doubt solving method with cost optimization
        
        Strategy:
        1. Check usage limits
        2. Try textbook database first (FREE)
        3. Classify problem type
        4. Route to appropriate AI service
        5. Format response for different interfaces
        """
        start_time = datetime.now()
        
        # Step 1: Check usage limits
        usage_check = await self._check_usage_limits(request.user_id, request.user_plan)
        if not usage_check["allowed"]:
            return self._create_upgrade_prompt(usage_check)
        
        # Step 2: Extract question text (OCR if needed)
        question_text = await self._extract_question_text(request)
        
        # Step 3: Try textbook database first (FREE!)
        textbook_solution = await self._search_textbook_database(question_text)
        if textbook_solution and textbook_solution.confidence_score > 0.75:
            await self._track_usage(request.user_id, "textbook", 0.0)
            return textbook_solution
        
        # Step 4: Classify problem type for AI routing
        problem_type = await self._classify_problem(question_text)
        
        # Step 5: Route to appropriate AI service
        if problem_type == ProblemType.COMPUTATIONAL:
            solution = await self._solve_with_wolfram(question_text, request)
        elif request.user_plan == "basic":
            solution = await self._solve_with_gpt35(question_text, request)
        else:  # Premium users get GPT-4
            solution = await self._solve_with_gpt4(question_text, request)
        
        # Step 5.5: Apply math verification/guardrails for monotonicity-type questions
        try:
            solution = self._apply_monotonicity_guard(question_text, solution)
        except Exception as _e:
            # Do not fail the request if guard fails
            pass
        
        # Step 6: Format for different interfaces
        solution = await self._format_solution(solution, request)
        
        # Step 7: Track usage and costs
        time_taken = (datetime.now() - start_time).total_seconds()
        solution.time_taken = time_taken
        await self._track_usage(request.user_id, solution.solution_method, solution.cost_incurred)
        
        return solution
    
    async def _extract_question_text(self, request: DoubtRequest) -> str:
        """Extract question text from image or return provided text"""
        
        if request.question_text:
            return request.question_text
        
        if request.image_data:
            # Try OCR extraction
            try:
                # Primary: Mathpix for math content
                if self.mathpix_api_key:
                    text = await self._mathpix_ocr(request.image_data)
                    if text and len(text.strip()) > 10:
                        return text
                
                # Fallback: Basic OCR (implement with Tesseract or similar)
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
        """Solve computational problems using Wolfram Alpha ($0.0025/query)"""
        
        # If no API key configured, skip directly to GPT-3.5
        if not self.wolfram_api_key:
            return await self._solve_with_gpt35(question, request)
        
        try:
            # Wolfram Alpha API call
            params = {
                'input': question,
                'appid': self.wolfram_api_key,
                'output': 'json',
                'format': 'plaintext'
            }
            
            response = requests.get(self.wolfram_url, params=params, timeout=10)
            data = response.json()
            
            # Extract solution from Wolfram response
            if 'queryresult' in data and data['queryresult']['success']:
                pods = data['queryresult']['pods']
                solution_pod = next((p for p in pods if 'solution' in p['title'].lower()), None)
                
                if solution_pod:
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
        """Solve problems using GPT-3.5 Turbo ($0.004/query)"""
        
        try:
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
            
            if not self.openai_client:
                raise Exception("OpenAI client not initialized")
                
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.1
            )
            
            solution_text = response.choices[0].message.content
            parsed_solution = self._parse_gpt_solution(solution_text, question)
            parsed_solution.solution_method = "gpt35"
            parsed_solution.cost_incurred = 0.004
            
            return parsed_solution
            
        except Exception as e:
            logger.error(f"❌ GPT-3.5 failed: {e}")
            return self._create_fallback_solution(question)
    
    async def _solve_with_gpt4(self, question: str, request: DoubtRequest) -> DoubtSolution:
        """Solve complex problems using GPT-4 ($0.09/query) - Premium only"""
        
        try:
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
            
            if not self.openai_client:
                raise Exception("OpenAI client not initialized")
                
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.1
            )
            
            solution_text = response.choices[0].message.content
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
    
    async def _mathpix_ocr(self, image_data: bytes) -> str:
        """Extract text from image using Mathpix API"""
        
        if not self.mathpix_api_key:
            raise Exception("Mathpix API key not configured")
        
        try:
            # Encode image for Mathpix
            image_base64 = base64.b64encode(image_data).decode()
            
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
            
            response = requests.post(url, json=data, headers=headers, timeout=15)
            result = response.json()
            
            if 'text' in result:
                return result['text']
            else:
                raise Exception("No text extracted")
                
        except Exception as e:
            logger.error(f"❌ Mathpix OCR failed: {e}")
            raise
    
    async def _fallback_ocr(self, image_data: bytes) -> str:
        """Fallback OCR using basic methods"""
        # Placeholder for Tesseract or similar
        return "OCR extraction failed. Please type your question."
    
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
                # Ensure keys expected by _track_usage exist from the start
                "total_cost": 0.0,
                "methods_used": {}
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
    
    async def _track_usage(self, user_id: str, method: str, cost: float):
        """Track user usage and costs"""
        
        current_month = datetime.now().strftime("%Y-%m")
        user_key = f"{user_id}_{current_month}"
        
        if user_key not in self.usage_db:
            self.usage_db[user_key] = {
                "doubts_used": 0,
                "total_cost": 0.0,
                "methods_used": {},
                "plan": "basic"
            }
        
        # Update usage
        self.usage_db[user_key]["doubts_used"] += 1
        self.usage_db[user_key]["total_cost"] += cost
        
        if method not in self.usage_db[user_key]["methods_used"]:
            self.usage_db[user_key]["methods_used"][method] = 0
        self.usage_db[user_key]["methods_used"][method] += 1
        
        logger.info(f"📊 Usage tracked - User: {user_id}, Method: {method}, Cost: ${cost:.4f}")
    
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
                "method": solution.solution_method
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
    
    def _apply_monotonicity_guard(self, question: str, solution: DoubtSolution) -> DoubtSolution:
        """Guardrail for monotonicity questions on polynomials.
        If the question asks for increasing/decreasing intervals and includes a
        cubic polynomial in the form ax^3 + bx^2 + cx + d, compute f'(x) and
        correct the intervals deterministically.
        """
        q = (question or "").lower().replace(" ", "").replace("−", "-")
        if not ("increasing" in q or "decreasing" in q):
            return solution
        # Try to extract cubic coefficients a, b, c
        import re
        def _coef(match: Optional[str]) -> Optional[float]:
            if match is None:
                return None
            s = match.strip()
            if s in ("", "+"): return 1.0
            if s == "-": return -1.0
            try:
                return float(s)
            except Exception:
                return None
        # Patterns for terms
        a_m = re.search(r"([+\-]?[0-9]*\.?[0-9]*)x\^3", q)
        b_m = re.search(r"([+\-]?[0-9]*\.?[0-9]*)x\^2", q)
        c_m = re.search(r"([+\-]?[0-9]*\.?[0-9]*)x(?!\^)", q)
        a = _coef(a_m.group(1)) if a_m else None
        b = _coef(b_m.group(1)) if b_m else 0.0
        c = _coef(c_m.group(1)) if c_m else 0.0
        if a is None:
            # Try quadratic (ax^2+bx+c) guard if no cubic term
            aq_m = re.search(r"([+\-]?[0-9]*\.?[0-9]*)x\^2", q)
            bq_m = re.search(r"([+\-]?[0-9]*\.?[0-9]*)x(?!\^)", q)
            cq_m = re.search(r"([+\-]?[0-9]+\.?[0-9]*)($|[^x^0-9])", q)
            aq = _coef(aq_m.group(1)) if aq_m else None
            bq = _coef(bq_m.group(1)) if bq_m else 0.0
            cq = _coef(cq_m.group(1)) if cq_m else 0.0
            if aq is None:
                return solution
            # f'(x) = 2aq x + bq  → linear, decreasing where derivative < 0
            A1, B1 = 2*aq, bq
            # If A1 == 0, derivative constant
            if abs(A1) < 1e-12:
                if B1 < 0 and "decreasing" in q:
                    solution.final_answer = "Decreasing on (-∞, ∞)"
                elif B1 > 0 and "increasing" in q:
                    solution.final_answer = "Increasing on (-∞, ∞)"
                return solution
            x0 = -B1 / A1
            if "decreasing" in q:
                # For linear derivative with positive slope, derivative <0 for x < x0
                # with negative slope, derivative <0 for x > x0
                if A1 > 0:
                    interval = f"(-∞, {self._nice_num(x0)})"
                else:
                    interval = f"({self._nice_num(x0)}, ∞)"
                solution.final_answer = f"Decreasing on {interval}"
            else:
                if A1 > 0:
                    interval = f"({self._nice_num(x0)}, ∞)"
                else:
                    interval = f"(-∞, {self._nice_num(x0)})"
                solution.final_answer = f"Increasing on {interval}"
            # Append verification step
            solution.steps.append(SolutionStep(
                step_number=len(solution.steps)+1,
                title="Verification (derivative)",
                explanation=f"Computed derivative and sign to verify monotonicity.",
                confidence=0.98,
            ))
            return solution
        # Derivative f'(x) = 3a x^2 + 2b x + c
        A, B, C = 3.0*a, 2.0*b, c
        if abs(A) < 1e-12:
            # Falls back to linear derivative case
            if abs(B) < 1e-12:
                return solution
            x0 = -C / B
            if "decreasing" in q:
                interval = f"(-∞, {self._nice_num(x0)})" if B > 0 else f"({self._nice_num(x0)}, ∞)"
                solution.final_answer = f"Decreasing on {interval}"
            else:
                interval = f"({self._nice_num(x0)}, ∞)" if B > 0 else f"(-∞, {self._nice_num(x0)})"
                solution.final_answer = f"Increasing on {interval}"
            solution.steps.append(SolutionStep(
                step_number=len(solution.steps)+1,
                title="Verification (derivative)",
                explanation=f"Computed derivative and sign to verify monotonicity.",
                confidence=0.98,
            ))
            return solution
        disc = B*B - 4*A*C
        if disc >= 0:
            import math
            r1 = (-B - math.sqrt(disc)) / (2*A)
            r2 = (-B + math.sqrt(disc)) / (2*A)
            lo, hi = (r1, r2) if r1 <= r2 else (r2, r1)
            if "decreasing" in q:
                interval = f"({self._nice_num(lo)}, {self._nice_num(hi)})"
                solution.final_answer = f"Decreasing on {interval}"
            if "increasing" in q:
                interval = f"(-∞, {self._nice_num(lo)}) ∪ ({self._nice_num(hi)}, ∞)"
                solution.final_answer = f"Increasing on {interval}"
            solution.steps.append(SolutionStep(
                step_number=len(solution.steps)+1,
                title="Verification (derivative roots)",
                explanation=f"f'(x)=0 at x={self._nice_num(lo)}, {self._nice_num(hi)}; sign between gives monotonicity.",
                confidence=0.98,
            ))
            return solution
        else:
            # No real roots: derivative keeps a constant sign
            x0 = -B/(2*A)
            min_val = A*x0*x0 + B*x0 + C
            if min_val > 0:
                # Derivative > 0 for all x
                solution.final_answer = "Increasing on (-∞, ∞)"
            elif min_val < 0:
                solution.final_answer = "Decreasing on (-∞, ∞)"
            solution.steps.append(SolutionStep(
                step_number=len(solution.steps)+1,
                title="Verification (no real critical points)",
                explanation=f"f'(x) has no real roots; sign is constant across ℝ.",
                confidence=0.98,
            ))
            return solution
    
    def _nice_num(self, x: float) -> str:
        """Render a number as a simple fraction if near-rational, else 3-decimal float."""
        try:
            frac = Fraction(x).limit_denominator(24)
            if abs(float(frac) - x) < 1e-6:
                if frac.denominator == 1:
                    return f"{frac.numerator}"
                return f"{frac.numerator}/{frac.denominator}"
        except Exception:
            pass
        return f"{x:.3f}"
    
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

class DoubtAnalytics:
    """Analytics and insights for doubt solving usage"""
    
    def __init__(self, usage_db: Dict):
        self.usage_db = usage_db
    
    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get detailed analytics for a user"""
        
        current_month = datetime.now().strftime("%Y-%m")
        user_key = f"{user_id}_{current_month}"
        
        usage = self.usage_db.get(user_key, {})
        
        return {
            "current_month": {
                "doubts_used": usage.get("doubts_used", 0),
                "total_cost": usage.get("total_cost", 0.0),
                "methods_used": usage.get("methods_used", {}),
                "plan": usage.get("plan", "basic")
            },
            "insights": {
                "most_used_method": self._get_most_used_method(usage),
                "average_cost_per_doubt": self._get_avg_cost(usage),
                "topics_asked": self._get_topics_distribution(usage)
            },
            "recommendations": self._get_recommendations(usage)
        }
    
    def _get_most_used_method(self, usage: Dict) -> str:
        methods = usage.get("methods_used", {})
        if not methods:
            return "none"
        return max(methods.items(), key=lambda x: x[1])[0]
    
    def _get_avg_cost(self, usage: Dict) -> float:
        total_cost = usage.get("total_cost", 0.0)
        doubts_used = usage.get("doubts_used", 1)
        return total_cost / doubts_used
    
    def _get_topics_distribution(self, usage: Dict) -> List[str]:
        # Placeholder - in production, track topics from solved doubts
        return ["Algebra", "Calculus", "Geometry"]
    
    def _get_recommendations(self, usage: Dict) -> List[str]:
        recommendations = []
        
        doubts_used = usage.get("doubts_used", 0)
        
        if doubts_used > 15:
            recommendations.append("Consider upgrading to Premium for unlimited doubts")
        
        if usage.get("plan") == "basic":
            recommendations.append("Upgrade to Premium for GPT-4 detailed solutions")
            
        return recommendations

# ================================================================================
# 🧪 Demo and Testing Functions
# ================================================================================

async def demo_doubt_solving():
    """Demo the doubt solving engine with cost tracking"""
    
    print("🤖 Doubt Solving Engine Demo")
    print("=" * 60)
    
    # Mock configuration
    config = {
        "openai_api_key": "sk-test-key",  # Add your real key
        "wolfram_api_key": "test-key",   # Add your real key
        "mathpix_api_key": None,         # Optional
        "mathpix_api_secret": None
    }
    
    # Initialize engine
    engine = DoubtSolvingEngine(config)
    analytics = DoubtAnalytics(engine.usage_db)
    
    # Test different types of doubts
    test_doubts = [
        DoubtRequest(
            question_text="Solve x² + 5x + 6 = 0",
            subject="Mathematics",
            user_id="student_123",
            user_plan="basic"
        ),
        DoubtRequest(
            question_text="Explain the concept of derivatives",
            subject="Mathematics", 
            user_id="student_123",
            user_plan="basic"
        ),
        DoubtRequest(
            question_text="Find the integral of sin(x) dx",
            subject="Mathematics",
            user_id="student_456", 
            user_plan="premium"
        )
    ]
    
    print("\n🧪 Testing Different Problem Types:")
    print("-" * 40)
    
    total_cost = 0.0
    
    for i, doubt in enumerate(test_doubts, 1):
        print(f"\n📝 Test {i}: {doubt.question_text}")
        print(f"   User: {doubt.user_id} ({doubt.user_plan})")
        
        try:
            solution = await engine.solve_doubt(doubt)
            
            print(f"   ✅ Solved using: {solution.solution_method}")
            print(f"   💰 Cost: ${solution.cost_incurred:.4f}")
            print(f"   ⏱️ Time: {solution.time_taken:.1f}s")
            print(f"   🎯 Answer: {solution.final_answer[:50]}...")
            print(f"   📊 Steps: {len(solution.steps)}")
            
            total_cost += solution.cost_incurred
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print(f"\n💰 Total Demo Cost: ${total_cost:.4f}")
    
    # Show analytics
    print(f"\n📊 User Analytics:")
    for user_id in ["student_123", "student_456"]:
        analytics_data = analytics.get_user_analytics(user_id)
        print(f"   {user_id}: {analytics_data['current_month']['doubts_used']} doubts used")

if __name__ == "__main__":
    asyncio.run(demo_doubt_solving())
