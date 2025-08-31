#!/usr/bin/env python3
"""
🤖 Doubt Solving API Endpoints

Enhanced API endpoints for the doubt solving assistant with:
- Usage limits and tracking (20 doubts for ₹99 plan)  
- OCR integration for image upload
- Cost optimization and analytics
- Mobile app and WhatsApp bot support
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import asyncio
import base64
from datetime import datetime
import logging
from pathlib import Path

# Import our doubt solving engine
import sys
sys.path.append('..')
from doubt_solving_engine import DoubtSolvingEngine, DoubtRequest, DoubtSolution, DoubtAnalytics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================================================================================
# 📊 Pydantic Models for API
# ================================================================================

class TextDoubtRequest(BaseModel):
    question: str
    subject: str = "Mathematics"
    user_id: str
    user_plan: str = "basic"
    context: Optional[str] = None

class ImageDoubtRequest(BaseModel):
    image_base64: str
    subject: str = "Mathematics"
    user_id: str
    user_plan: str = "basic"
    context: Optional[str] = None

class DoubtResponse(BaseModel):
    success: bool
    solution: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    usage_info: Optional[Dict[str, Any]] = None
    cost_info: Optional[Dict[str, Any]] = None

class UsageResponse(BaseModel):
    user_id: str
    current_usage: Dict[str, Any]
    analytics: Dict[str, Any]
    recommendations: List[str]

class UpgradeRequest(BaseModel):
    user_id: str
    current_plan: str
    requested_plan: str

# ================================================================================
# 🚀 Doubt Solving API Class
# ================================================================================

class DoubtAPI:
    """FastAPI endpoints for doubt solving"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.engine: Optional[DoubtSolvingEngine] = None
        self.analytics: Optional[DoubtAnalytics] = None
        
        # Add routes
        self._add_routes()
    
    def _add_routes(self):
        """Add all doubt solving routes to FastAPI app"""
        
        @self.app.on_event("startup")
        async def startup_doubt_engine():
            """Initialize doubt solving engine on startup"""
            await self._initialize_engine()
        
        @self.app.post("/api/doubt/solve-text", response_model=DoubtResponse)
        async def solve_text_doubt(request: TextDoubtRequest):
            """Solve text-based doubt question"""
            return await self._solve_text_doubt(request)
        
        @self.app.post("/api/doubt/solve-image", response_model=DoubtResponse)
        async def solve_image_doubt(file: UploadFile = File(...), 
                                    user_id: str = "demo_user",
                                    user_plan: str = "basic",
                                    subject: str = "Mathematics"):
            """Solve doubt from uploaded image (OCR + AI)"""
            return await self._solve_image_doubt(file, user_id, user_plan, subject)
        
        @self.app.get("/api/doubt/usage/{user_id}", response_model=UsageResponse)
        async def get_user_usage(user_id: str):
            """Get user's doubt usage and analytics"""
            return await self._get_user_usage(user_id)
        
        @self.app.get("/api/doubt/history/{user_id}")
        async def get_doubt_history(user_id: str, limit: int = 20):
            """Get user's solved doubt history"""
            return await self._get_doubt_history(user_id, limit)
        
        @self.app.post("/api/doubt/upgrade")
        async def upgrade_user_plan(request: UpgradeRequest):
            \"\"\"Upgrade user's subscription plan\"\"\"\n            return await self._upgrade_user_plan(request)\n        \n        @self.app.post("/api/doubt/generate-practice/{user_id}")
        async def generate_practice_from_doubts(user_id: str, topic: str):
            \"\"\"Generate practice quiz based on user's doubt history\"\"\"\n            return await self._generate_practice_quiz(user_id, topic)\n        \n        @self.app.get("/api/doubt/analytics/admin")
        async def get_admin_analytics():
            \"\"\"Get platform-wide doubt solving analytics (admin only)\"\"\"\n            return await self._get_admin_analytics()\n    \n    async def _initialize_engine(self):\n        \"\"\"Initialize the doubt solving engine\"\"\"\n        try:\n            logger.info(\"🤖 Initializing Doubt Solving Engine...\")\n            \n            # Load configuration (in production, use environment variables)\n            config = {\n                \"openai_api_key\": None,  # Set your OpenAI API key\n                \"wolfram_api_key\": None,  # Set your Wolfram Alpha API key\n                \"mathpix_api_key\": None,  # Optional: Mathpix for OCR\n                \"mathpix_api_secret\": None\n            }\n            \n            self.engine = DoubtSolvingEngine(config)\n            self.analytics = DoubtAnalytics(self.engine.usage_db)\n            \n            logger.info(\"✅ Doubt Solving Engine initialized successfully!\")\n            \n        except Exception as e:\n            logger.error(f\"❌ Failed to initialize doubt engine: {e}\")\n            raise\n    \n    async def _solve_text_doubt(self, request: TextDoubtRequest) -> DoubtResponse:\n        \"\"\"Solve text-based doubt\"\"\"\n        \n        if not self.engine:\n            raise HTTPException(status_code=500, detail=\"Doubt engine not initialized\")\n        \n        try:\n            # Create doubt request\n            doubt_request = DoubtRequest(\n                question_text=request.question,\n                subject=request.subject,\n                user_id=request.user_id,\n                user_plan=request.user_plan,\n                context=request.context\n            )\n            \n            # Solve the doubt\n            solution = await self.engine.solve_doubt(doubt_request)\n            \n            # Get usage info\n            usage_check = await self.engine._check_usage_limits(request.user_id, request.user_plan)\n            \n            return DoubtResponse(\n                success=True,\n                solution=solution.mobile_format,\n                usage_info={\n                    \"remaining_doubts\": usage_check[\"remaining\"],\n                    \"used_this_month\": usage_check[\"used\"],\n                    \"plan\": usage_check[\"plan\"]\n                },\n                cost_info={\n                    \"method_used\": solution.solution_method,\n                    \"cost_incurred\": solution.cost_incurred,\n                    \"time_taken\": solution.time_taken\n                }\n            )\n            \n        except Exception as e:\n            logger.error(f\"❌ Text doubt solving failed: {e}\")\n            return DoubtResponse(\n                success=False,\n                error=f\"Failed to solve doubt: {str(e)}\"\n            )\n    \n    async def _solve_image_doubt(self, file: UploadFile, user_id: str, \n                                user_plan: str, subject: str) -> DoubtResponse:\n        \"\"\"Solve image-based doubt with OCR\"\"\"\n        \n        if not self.engine:\n            raise HTTPException(status_code=500, detail=\"Doubt engine not initialized\")\n        \n        try:\n            # Read image data\n            image_data = await file.read()\n            \n            # Validate image\n            if len(image_data) > 10 * 1024 * 1024:  # 10MB limit\n                raise HTTPException(status_code=400, detail=\"Image too large (max 10MB)\")\n            \n            # Create doubt request\n            doubt_request = DoubtRequest(\n                image_data=image_data,\n                subject=subject,\n                user_id=user_id,\n                user_plan=user_plan\n            )\n            \n            # Solve the doubt\n            solution = await self.engine.solve_doubt(doubt_request)\n            \n            # Get usage info\n            usage_check = await self.engine._check_usage_limits(user_id, user_plan)\n            \n            return DoubtResponse(\n                success=True,\n                solution=solution.mobile_format,\n                usage_info={\n                    \"remaining_doubts\": usage_check[\"remaining\"],\n                    \"used_this_month\": usage_check[\"used\"],\n                    \"plan\": usage_check[\"plan\"]\n                },\n                cost_info={\n                    \"method_used\": solution.solution_method,\n                    \"cost_incurred\": solution.cost_incurred,\n                    \"ocr_used\": True\n                }\n            )\n            \n        except Exception as e:\n            logger.error(f\"❌ Image doubt solving failed: {e}\")\n            return DoubtResponse(\n                success=False,\n                error=f\"Failed to process image: {str(e)}\"\n            )\n    \n    async def _get_user_usage(self, user_id: str) -> UsageResponse:\n        \"\"\"Get user usage statistics and analytics\"\"\"\n        \n        if not self.analytics:\n            raise HTTPException(status_code=500, detail=\"Analytics not available\")\n        \n        try:\n            # Get current usage\n            current_month = datetime.now().strftime(\"%Y-%m\")\n            user_key = f\"{user_id}_{current_month}\"\n            current_usage = self.engine.usage_db.get(user_key, {\n                \"doubts_used\": 0,\n                \"plan\": \"basic\",\n                \"total_cost\": 0.0\n            })\n            \n            # Get detailed analytics\n            analytics_data = self.analytics.get_user_analytics(user_id)\n            \n            return UsageResponse(\n                user_id=user_id,\n                current_usage=current_usage,\n                analytics=analytics_data,\n                recommendations=analytics_data[\"recommendations\"]\n            )\n            \n        except Exception as e:\n            logger.error(f\"❌ Failed to get user usage: {e}\")\n            raise HTTPException(status_code=500, detail=\"Failed to get usage data\")\n    \n    async def _get_doubt_history(self, user_id: str, limit: int) -> Dict[str, Any]:\n        \"\"\"Get user's doubt solving history\"\"\"\n        \n        # Placeholder - in production, query from database\n        return {\n            \"user_id\": user_id,\n            \"total_doubts_solved\": 45,\n            \"recent_doubts\": [\n                {\n                    \"question\": \"Solve quadratic equation\",\n                    \"topic\": \"Algebra\",\n                    \"solved_at\": \"2025-08-30T10:30:00\",\n                    \"method\": \"gpt35\",\n                    \"cost\": 0.004\n                },\n                {\n                    \"question\": \"Explain derivatives\",\n                    \"topic\": \"Calculus\", \n                    \"solved_at\": \"2025-08-30T09:15:00\",\n                    \"method\": \"textbook\",\n                    \"cost\": 0.0\n                }\n            ],\n            \"topic_distribution\": {\n                \"Algebra\": 15,\n                \"Calculus\": 12,\n                \"Geometry\": 8,\n                \"Trigonometry\": 10\n            }\n        }\n    \n    async def _upgrade_user_plan(self, request: UpgradeRequest) -> Dict[str, Any]:\n        \"\"\"Handle user plan upgrade\"\"\"\n        \n        try:\n            # In production, integrate with payment gateway\n            logger.info(f\"📈 Plan upgrade request: {request.user_id} from {request.current_plan} to {request.requested_plan}\")\n            \n            # Update user plan in database (mock for now)\n            current_month = datetime.now().strftime(\"%Y-%m\")\n            user_key = f\"{request.user_id}_{current_month}\"\n            \n            if user_key in self.engine.usage_db:\n                self.engine.usage_db[user_key][\"plan\"] = request.requested_plan\n            \n            return {\n                \"success\": True,\n                \"message\": f\"Successfully upgraded to {request.requested_plan} plan\",\n                \"new_benefits\": {\n                    \"doubts_limit\": \"unlimited\" if request.requested_plan == \"premium\" else 20,\n                    \"ai_model\": \"gpt-4\" if request.requested_plan == \"premium\" else \"gpt-3.5\",\n                    \"ocr_enabled\": request.requested_plan == \"premium\",\n                    \"priority_support\": request.requested_plan == \"premium\"\n                }\n            }\n            \n        except Exception as e:\n            logger.error(f\"❌ Plan upgrade failed: {e}\")\n            raise HTTPException(status_code=500, detail=\"Plan upgrade failed\")\n    \n    async def _generate_practice_quiz(self, user_id: str, topic: str) -> Dict[str, Any]:\n        \"\"\"Generate practice quiz based on user's doubt history\"\"\"\n        \n        try:\n            # Get user's weak topics from doubt history\n            analytics_data = self.analytics.get_user_analytics(user_id)\n            \n            # Integration with existing quiz generator\n            # This would call your existing quiz generation API\n            practice_quiz = {\n                \"quiz_id\": f\"practice_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}\",\n                \"title\": f\"Practice Quiz - {topic}\",\n                \"topic\": topic,\n                \"questions\": 10,\n                \"difficulty\": \"medium\",\n                \"generated_from\": \"doubt_history\",\n                \"estimated_time\": \"15 minutes\"\n            }\n            \n            return {\n                \"success\": True,\n                \"quiz\": practice_quiz,\n                \"message\": f\"Generated practice quiz for {topic} based on your doubt history\"\n            }\n            \n        except Exception as e:\n            logger.error(f\"❌ Practice quiz generation failed: {e}\")\n            raise HTTPException(status_code=500, detail=\"Failed to generate practice quiz\")\n    \n    async def _get_admin_analytics(self) -> Dict[str, Any]:\n        \"\"\"Get platform-wide analytics for admin dashboard\"\"\"\n        \n        try:\n            # Calculate platform statistics\n            total_users = len(set(key.split('_')[0] for key in self.engine.usage_db.keys()))\n            total_doubts = sum(usage.get(\"doubts_used\", 0) for usage in self.engine.usage_db.values())\n            total_costs = sum(usage.get(\"total_cost\", 0.0) for usage in self.engine.usage_db.values())\n            \n            # Method distribution\n            method_counts = {}\n            for usage in self.engine.usage_db.values():\n                for method, count in usage.get(\"methods_used\", {}).items():\n                    method_counts[method] = method_counts.get(method, 0) + count\n            \n            return {\n                \"platform_stats\": {\n                    \"total_active_users\": total_users,\n                    \"total_doubts_solved\": total_doubts,\n                    \"total_ai_costs\": round(total_costs, 4),\n                    \"average_cost_per_doubt\": round(total_costs / max(total_doubts, 1), 6)\n                },\n                \"method_distribution\": method_counts,\n                \"user_plans\": {\n                    \"basic\": len([u for u in self.engine.usage_db.values() if u.get(\"plan\") == \"basic\"]),\n                    \"premium\": len([u for u in self.engine.usage_db.values() if u.get(\"plan\") == \"premium\"])\n                },\n                \"cost_efficiency\": {\n                    \"free_textbook_usage\": method_counts.get(\"textbook\", 0),\n                    \"low_cost_ai_usage\": method_counts.get(\"wolfram\", 0) + method_counts.get(\"gpt35\", 0),\n                    \"premium_ai_usage\": method_counts.get(\"gpt4\", 0)\n                }\n            }\n            \n        except Exception as e:\n            logger.error(f\"❌ Failed to get admin analytics: {e}\")\n            raise HTTPException(status_code=500, detail=\"Failed to get analytics\")\n    \n    async def _initialize_engine(self):\n        \"\"\"Initialize doubt solving engine with configuration\"\"\"\n        \n        # In production, load from environment variables\n        config = {\n            \"openai_api_key\": None,  # os.getenv(\"OPENAI_API_KEY\")\n            \"wolfram_api_key\": None,  # os.getenv(\"WOLFRAM_API_KEY\")\n            \"mathpix_api_key\": None,  # os.getenv(\"MATHPIX_API_KEY\")\n            \"mathpix_api_secret\": None  # os.getenv(\"MATHPIX_API_SECRET\")\n        }\n        \n        self.engine = DoubtSolvingEngine(config)\n        self.analytics = DoubtAnalytics(self.engine.usage_db)\n        \n        logger.info(\"✅ Doubt API initialized successfully!\")\n\n# ================================================================================\n# 🧪 WhatsApp Bot Integration Helpers\n# ================================================================================\n\nclass WhatsAppBotHelper:\n    \"\"\"Helper functions for WhatsApp bot integration\"\"\"\n    \n    def __init__(self, doubt_engine: DoubtSolvingEngine):\n        self.engine = doubt_engine\n    \n    async def process_whatsapp_message(self, message: str, user_phone: str) -> str:\n        \"\"\"Process WhatsApp message and return formatted response\"\"\"\n        \n        try:\n            # Create doubt request from WhatsApp message\n            doubt_request = DoubtRequest(\n                question_text=message,\n                user_id=f\"whatsapp_{user_phone}\",\n                user_plan=\"basic\",  # WhatsApp users start with basic\n                subject=\"Mathematics\"\n            )\n            \n            # Solve doubt\n            solution = await self.engine.solve_doubt(doubt_request)\n            \n            # Return WhatsApp-formatted response\n            return solution.whatsapp_format\n            \n        except Exception as e:\n            logger.error(f\"❌ WhatsApp message processing failed: {e}\")\n            return \"Sorry, I couldn't process your question. Please try again or visit our app for better support.\"\n    \n    def create_whatsapp_menu(self) -> str:\n        \"\"\"Create WhatsApp bot menu\"\"\"\n        return \"\"\"\n🤖 *Welcome to Klaro Doubt Bot!*\n\n📚 I can help you with:\n1️⃣ Math problems and equations\n2️⃣ Concept explanations\n3️⃣ Step-by-step solutions\n\n💡 *How to use*:\n• Type your math question\n• Send a photo of your problem\n• Ask for explanations\n\n📱 *For unlimited doubts & premium features*:\nDownload Klaro app: [link]\n\n🚀 *Let's start! Ask me any math question...*\n\"\"\"\n\n# ================================================================================\n# 🔧 Demo and Testing Functions\n# ================================================================================\n\nasync def demo_doubt_api():\n    \"\"\"Demo the doubt solving API\"\"\"\n    \n    print(\"🧪 Doubt Solving API Demo\")\n    print(\"=\" * 60)\n    \n    # Create FastAPI app for testing\n    app = FastAPI(title=\"Doubt Solving API Demo\")\n    app.add_middleware(\n        CORSMiddleware,\n        allow_origins=[\"*\"],\n        allow_credentials=True,\n        allow_methods=[\"*\"],\n        allow_headers=[\"*\"],\n    )\n    \n    # Initialize doubt API\n    doubt_api = DoubtAPI(app)\n    await doubt_api._initialize_engine()\n    \n    print(\"\\n✅ Doubt API initialized successfully!\")\n    \n    # Test text doubt solving\n    print(\"\\n🧪 Testing Text Doubt Solving:\")\n    print(\"-\" * 40)\n    \n    test_request = TextDoubtRequest(\n        question=\"Solve x² + 5x + 6 = 0\",\n        subject=\"Mathematics\",\n        user_id=\"demo_user\",\n        user_plan=\"basic\"\n    )\n    \n    try:\n        response = await doubt_api._solve_text_doubt(test_request)\n        \n        if response.success:\n            print(f\"✅ Doubt solved successfully!\")\n            print(f\"   Method: {response.cost_info['method_used']}\")\n            print(f\"   Cost: ${response.cost_info['cost_incurred']:.4f}\")\n            print(f\"   Remaining doubts: {response.usage_info['remaining_doubts']}\")\n            print(f\"   Solution: {response.solution['answer'][:100]}...\")\n        else:\n            print(f\"❌ Failed: {response.error}\")\n            \n    except Exception as e:\n        print(f\"❌ API test failed: {e}\")\n    \n    # Test usage analytics\n    print(\"\\n📊 Testing Usage Analytics:\")\n    print(\"-\" * 40)\n    \n    try:\n        usage_response = await doubt_api._get_user_usage(\"demo_user\")\n        print(f\"✅ Usage data retrieved:\")\n        print(f\"   Doubts used: {usage_response.current_usage['doubts_used']}\")\n        print(f\"   Total cost: ${usage_response.current_usage['total_cost']:.4f}\")\n        print(f\"   Plan: {usage_response.current_usage['plan']}\")\n        \n    except Exception as e:\n        print(f\"❌ Usage analytics failed: {e}\")\n    \n    # Test WhatsApp integration\n    print(\"\\n💬 Testing WhatsApp Bot Helper:\")\n    print(\"-\" * 40)\n    \n    try:\n        whatsapp_helper = WhatsAppBotHelper(doubt_api.engine)\n        \n        # Test WhatsApp message processing\n        whatsapp_response = await whatsapp_helper.process_whatsapp_message(\n            \"Solve 2x + 5 = 15\", \n            \"+919876543210\"\n        )\n        \n        print(f\"✅ WhatsApp response generated:\")\n        print(f\"   Response length: {len(whatsapp_response)} chars\")\n        print(f\"   Preview: {whatsapp_response[:100]}...\")\n        \n        # Show menu\n        menu = whatsapp_helper.create_whatsapp_menu()\n        print(f\"\\n📱 WhatsApp Menu:\")\n        print(menu[:200] + \"...\")\n        \n    except Exception as e:\n        print(f\"❌ WhatsApp integration test failed: {e}\")\n    \n    print(\"\\n🎉 Doubt Solving API Demo Complete!\")\n    print(\"✅ Ready for integration with mobile app and WhatsApp bot\")\n\nif __name__ == \"__main__\":\n    asyncio.run(demo_doubt_api())\n"}}
</function_calls>

<function_calls>
<invoke name="mark_todo_as_done">
<parameter name="todo_ids">["f1c3c9cf-11ee-4632-895d-0777e80403ec", "d8e85be4-dc49-4feb-867c-0a0f57fefcc0"]
