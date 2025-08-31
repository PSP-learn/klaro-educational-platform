#!/usr/bin/env python3
"""
📱 WhatsApp Business API Integration for Klaro

Complete WhatsApp bot with:
- Webhook handling for incoming messages
- Text and image doubt solving
- User registration & subscription management
- Message formatting optimized for mobile
"""

import asyncio
import base64
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

import aiohttp
import requests
from twilio.rest import Client as TwilioClient

# Import our core components
from doubt_solving_engine_production import ProductionDoubtSolvingEngine, DoubtRequest
from database import KlaroDatabase, User, get_database

# ================================================================================
# 📱 WhatsApp Message Models
# ================================================================================

@dataclass
class WhatsAppMessage:
    """Incoming WhatsApp message"""
    from_number: str
    message_id: str
    message_type: str  # 'text', 'image', 'audio'
    text_content: Optional[str] = None
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    timestamp: Optional[datetime] = None

@dataclass
class WhatsAppResponse:
    """Outgoing WhatsApp message"""
    to_number: str
    message_type: str
    content: str
    media_url: Optional[str] = None
    
# ================================================================================
# 🤖 WhatsApp Bot Engine
# ================================================================================

class WhatsAppBot:
    """WhatsApp Business API bot for doubt solving"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.twilio_client = None
        self.doubt_engine: Optional[ProductionDoubtSolvingEngine] = None
        self.database: Optional[KlaroDatabase] = None
        
        # WhatsApp Business API credentials
        self.whatsapp_token = config.get("whatsapp_access_token")
        self.phone_number_id = config.get("whatsapp_phone_number_id")
        self.verify_token = config.get("whatsapp_verify_token")
        
        # Twilio fallback credentials
        self.twilio_account_sid = config.get("twilio_account_sid")
        self.twilio_auth_token = config.get("twilio_auth_token")
        self.twilio_whatsapp_number = config.get("twilio_whatsapp_number")
        
        # User session management
        self.user_sessions: Dict[str, Dict] = {}
        
    async def initialize(self, doubt_engine: ProductionDoubtSolvingEngine):
        """Initialize the WhatsApp bot"""
        self.doubt_engine = doubt_engine
        self.database = await get_database()
        
        # Initialize Twilio client if credentials available
        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = TwilioClient(self.twilio_account_sid, self.twilio_auth_token)
        
        print("📱 WhatsApp bot initialized successfully")
    
    def get_or_create_user_session(self, phone_number: str) -> Dict:
        """Get or create user session"""
        if phone_number not in self.user_sessions:
            self.user_sessions[phone_number] = {
                "user_id": f"whatsapp_{phone_number.replace('+', '')}",
                "plan": "basic",
                "doubt_count_today": 0,
                "last_activity": datetime.now(),
                "current_context": None
            }
        
        return self.user_sessions[phone_number]
    
    async def process_webhook(self, webhook_data: Dict) -> List[WhatsAppResponse]:
        """Process incoming WhatsApp webhook"""
        
        try:
            # Parse webhook data (Meta WhatsApp Business API format)
            entry = webhook_data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})\n            \n            messages = value.get("messages", [])\n            responses = []\n            \n            for message_data in messages:\n                message = self._parse_message(message_data)\n                if message:\n                    response = await self._handle_message(message)\n                    if response:\n                        responses.append(response)\n            \n            return responses\n            \n        except Exception as e:\n            print(f"❌ Error processing webhook: {e}")\n            return []\n    \n    def _parse_message(self, message_data: Dict) -> Optional[WhatsAppMessage]:\n        """Parse incoming message data"""
        \n        try:\n            from_number = message_data.get("from")\n            message_id = message_data.get("id")\n            message_type = message_data.get("type")\n            timestamp = datetime.fromtimestamp(int(message_data.get("timestamp", 0)))\n            \n            if message_type == "text":\n                text_content = message_data.get("text", {}).get("body")\n                return WhatsAppMessage(\n                    from_number=from_number,\n                    message_id=message_id,\n                    message_type=message_type,\n                    text_content=text_content,\n                    timestamp=timestamp\n                )\n            \n            elif message_type == "image":\n                image_data = message_data.get("image", {})\n                return WhatsAppMessage(\n                    from_number=from_number,\n                    message_id=message_id,\n                    message_type=message_type,\n                    media_url=image_data.get("id"),  # Media ID from Meta API\n                    media_type="image",\n                    timestamp=timestamp\n                )\n            \n            return None\n            \n        except Exception as e:\n            print(f"❌ Error parsing message: {e}")\n            return None
    \n    async def _handle_message(self, message: WhatsAppMessage) -> Optional[WhatsAppResponse]:\n        """Handle individual message"""
        \n        session = self.get_or_create_user_session(message.from_number)\n        user_id = session["user_id"]\n        \n        # Check daily limits for basic users\n        if session["plan"] == "basic" and session["doubt_count_today"] >= 5:\n            return WhatsAppResponse(\n                to_number=message.from_number,\n                message_type="text",\n                content="🚫 Daily limit reached! Upgrade to Premium for unlimited doubts.\\n\\nReply *UPGRADE* to learn more."\n            )\n        \n        # Handle special commands\n        if message.text_content:\n            text = message.text_content.strip().upper()\n            \n            if text in ["HI", "HELLO", "START"]:\n                return await self._send_welcome_message(message.from_number)\n            \n            elif text == "HELP":\n                return await self._send_help_message(message.from_number)\n            \n            elif text == "UPGRADE":\n                return await self._send_upgrade_info(message.from_number)\n            \n            elif text == "STATS":\n                return await self._send_user_stats(message.from_number, session)\n        \n        # Process doubt solving\n        if message.message_type == "text" and message.text_content:\n            return await self._solve_text_doubt(message, session)\n        \n        elif message.message_type == "image":\n            return await self._solve_image_doubt(message, session)\n        \n        return WhatsAppResponse(\n            to_number=message.from_number,\n            message_type="text",\n            content="I can help solve your math doubts! 🤓\\n\\nSend me:\\n📝 Text questions\\n📸 Photos of problems\\n\\nType *HELP* for more options."\n        )
    \n    async def _solve_text_doubt(self, message: WhatsAppMessage, session: Dict) -> WhatsAppResponse:\n        """Solve text-based doubt"""
        \n        try:\n            # Create doubt request\n            doubt_request = DoubtRequest(\n                question_text=message.text_content,\n                user_id=session["user_id"],\n                user_plan=session["plan"],\n                route="whatsapp"\n            )\n            \n            # Solve using our production engine\n            solution = await self.doubt_engine.solve_doubt(doubt_request)\n            \n            # Update session\n            session["doubt_count_today"] += 1\n            session["last_activity"] = datetime.now()\n            \n            # Return formatted response\n            return WhatsAppResponse(\n                to_number=message.from_number,\n                message_type="text",\n                content=solution.whatsapp_format\n            )\n            \n        except Exception as e:\n            return WhatsAppResponse(\n                to_number=message.from_number,\n                message_type="text",\n                content="Sorry, I encountered an error solving your doubt. Please try again! 🤔"\n            )\n    \n    async def _solve_image_doubt(self, message: WhatsAppMessage, session: Dict) -> WhatsAppResponse:\n        """Solve image-based doubt using OCR"""
        \n        try:\n            # Download image from WhatsApp\n            image_data = await self._download_media(message.media_url)\n            if not image_data:\n                return WhatsAppResponse(\n                    to_number=message.from_number,\n                    message_type="text",\n                    content="Sorry, I couldn't download your image. Please try again! 📸"\n                )\n            \n            # Create doubt request\n            doubt_request = DoubtRequest(\n                image_data=image_data,\n                user_id=session["user_id"],\n                user_plan=session["plan"],\n                route="whatsapp"\n            )\n            \n            # Solve using our production engine\n            solution = await self.doubt_engine.solve_doubt(doubt_request)\n            \n            # Update session\n            session["doubt_count_today"] += 1\n            session["last_activity"] = datetime.now()\n            \n            return WhatsAppResponse(\n                to_number=message.from_number,\n                message_type="text",\n                content=solution.whatsapp_format\n            )\n            \n        except Exception as e:\n            return WhatsAppResponse(\n                to_number=message.from_number,\n                message_type="text",\n                content="Sorry, I had trouble processing your image. Please try sending it again! 📷"\n            )\n    \n    async def _download_media(self, media_id: str) -> Optional[bytes]:\n        """Download media from WhatsApp Business API"""
        \n        if not media_id or not self.whatsapp_token:\n            return None\n        \n        try:\n            # Get media URL\n            media_url_endpoint = f"https://graph.facebook.com/v18.0/{media_id}"\n            headers = {\n                "Authorization": f"Bearer {self.whatsapp_token}"\n            }\n            \n            async with aiohttp.ClientSession() as session:\n                # Get media URL\n                async with session.get(media_url_endpoint, headers=headers) as response:\n                    if response.status == 200:\n                        media_info = await response.json()\n                        download_url = media_info.get("url")\n                        \n                        # Download actual media\n                        async with session.get(download_url, headers=headers) as download_response:\n                            if download_response.status == 200:\n                                return await download_response.read()\n            \n            return None\n            \n        except Exception as e:\n            print(f"❌ Error downloading media: {e}")\n            return None
    \n    async def _send_welcome_message(self, phone_number: str) -> WhatsAppResponse:\n        """Send welcome message to new users"""
        \n        welcome_text = """\n🎓 *Welcome to Klaro!*\n\nI'm your AI doubt solving assistant! 🤖\n\n*What I can do:*\n📝 Solve text math problems\n📸 Read & solve photo problems\n📊 Track your learning progress\n\n*How to use:*\n• Just send me your question\n• Or take a photo of the problem\n• I'll solve it step-by-step!\n\n*Commands:*\n• *HELP* - Show all commands\n• *STATS* - Your learning stats\n• *UPGRADE* - Get unlimited access\n\nReady to solve some doubts? 🚀\n        """
        \n        return WhatsAppResponse(\n            to_number=phone_number,\n            message_type="text",\n            content=welcome_text.strip()\n        )
    \n    async def _send_help_message(self, phone_number: str) -> WhatsAppResponse:\n        """Send help message"""
        \n        help_text = """\n🔧 *Klaro Commands*\n\n*Basic Usage:*\n📝 Send text questions directly\n📸 Send photos of math problems\n\n*Commands:*\n• *HI* - Welcome message\n• *HELP* - This help menu\n• *STATS* - Your usage statistics\n• *UPGRADE* - Premium subscription info\n\n*Tips:*\n• Be specific with your questions\n• Include subject (Math, Physics, etc.)\n• Photos should be clear and well-lit\n\n*Need more help?*\nContact support: help@klaro.app\n        """
        \n        return WhatsAppResponse(\n            to_number=phone_number,\n            message_type="text",\n            content=help_text.strip()\n        )
    \n    async def _send_upgrade_info(self, phone_number: str) -> WhatsAppResponse:\n        """Send subscription upgrade information"""
        \n        upgrade_text = """\n💎 *Klaro Premium*\n\n*Basic Plan (Current):*\n• 5 doubts per day\n• GPT-3.5 solutions\n• OCR support\n\n*Premium Plan - ₹299/month:*\n• ✅ Unlimited doubts\n• ✅ GPT-4 solutions (more accurate)\n• ✅ Priority support\n• ✅ Detailed analytics\n• ✅ Practice problem generator\n\n*Upgrade now:*\nVisit: klaro.app/upgrade\nOr download our Android app!\n\n🎯 *Free trial: 3 days!*\n        """
        \n        return WhatsAppResponse(\n            to_number=phone_number,\n            message_type="text",\n            content=upgrade_text.strip()\n        )
    \n    async def _send_user_stats(self, phone_number: str, session: Dict) -> WhatsAppResponse:\n        """Send user statistics"""
        \n        try:\n            # Get analytics from database\n            if self.database:\n                analytics = await self.database.analytics.get_user_analytics(session["user_id"], days=30)\n                total_usage = analytics.get("total_usage", [{}])[0]\n                \n                stats_text = f"""\n📊 *Your Learning Stats*\n\n*This Month:*\n• Doubts solved: {total_usage.get('total_requests', 0)}\n• Success rate: {(total_usage.get('successful_requests', 0) / max(total_usage.get('total_requests', 1), 1) * 100):.1f}%\n• Cost saved: ₹{(0.50 * total_usage.get('total_requests', 0)):.2f}\n\n*Today:*\n• Questions asked: {session.get('doubt_count_today', 0)}\n• Plan: {session.get('plan', 'basic').title()}\n\n*Keep learning! 🚀*\n                """\n            else:\n                stats_text = f"""\n📊 *Your Learning Stats*\n\n*Today:*\n• Questions asked: {session.get('doubt_count_today', 0)}/5\n• Plan: {session.get('plan', 'basic').title()}\n\n*Upgrade for detailed analytics! 📈*\n                """\n            \n            return WhatsAppResponse(\n                to_number=phone_number,\n                message_type="text",\n                content=stats_text.strip()\n            )\n            \n        except Exception as e:\n            return WhatsAppResponse(\n                to_number=phone_number,\n                message_type="text",\n                content="📊 Stats temporarily unavailable. Try again later!"\n            )
    \n    async def send_message(self, response: WhatsAppResponse) -> bool:\n        """Send message via WhatsApp Business API or Twilio"""
        \n        # Try WhatsApp Business API first\n        if self.whatsapp_token and self.phone_number_id:\n            success = await self._send_via_business_api(response)\n            if success:\n                return True\n        \n        # Fallback to Twilio WhatsApp API\n        if self.twilio_client and self.twilio_whatsapp_number:\n            return await self._send_via_twilio(response)\n        \n        print(f"❌ Failed to send message: No valid WhatsApp API configured")\n        return False
    \n    async def _send_via_business_api(self, response: WhatsAppResponse) -> bool:\n        """Send message via Meta WhatsApp Business API"""
        \n        try:\n            url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"\n            headers = {\n                "Authorization": f"Bearer {self.whatsapp_token}",\n                "Content-Type": "application/json"\n            }\n            \n            payload = {\n                "messaging_product": "whatsapp",\n                "to": response.to_number,\n                "type": response.message_type,\n                "text": {\n                    "body": response.content\n                }\n            }\n            \n            async with aiohttp.ClientSession() as session:\n                async with session.post(url, headers=headers, json=payload) as resp:\n                    if resp.status == 200:\n                        print(f"✅ Message sent successfully via Business API")\n                        return True\n                    else:\n                        print(f"❌ Business API error: {resp.status}")\n                        return False\n                        \n        except Exception as e:\n            print(f"❌ Business API send error: {e}")\n            return False
    \n    async def _send_via_twilio(self, response: WhatsAppResponse) -> bool:\n        """Send message via Twilio WhatsApp API"""
        \n        try:\n            message = self.twilio_client.messages.create(\n                body=response.content,\n                from_=self.twilio_whatsapp_number,\n                to=f"whatsapp:{response.to_number}"\n            )\n            \n            print(f"✅ Message sent successfully via Twilio: {message.sid}")\n            return True\n            \n        except Exception as e:\n            print(f"❌ Twilio send error: {e}")\n            return False

# ================================================================================
# 🔧 WhatsApp Integration Utilities
# ================================================================================

class WhatsAppFormatter:
    """Format doubt solutions for WhatsApp"""
    
    @staticmethod
    def format_solution(solution) -> str:\n        """Format solution for WhatsApp with emojis and structure"""
        \n        formatted_parts = []\n        \n        # Header with question\n        formatted_parts.append(f"🤓 *Solution:*\\n")\n        formatted_parts.append(f"📝 _{solution.question[:100]}{'...' if len(solution.question) > 100 else ''}_\\n")\n        \n        # Main answer\n        formatted_parts.append(f"✅ *Answer:* {solution.final_answer}\\n")\n        \n        # Steps (limited for WhatsApp)\n        if solution.steps and len(solution.steps) > 0:\n            formatted_parts.append("📋 *Steps:*")\n            \n            for i, step in enumerate(solution.steps[:3], 1):  # Limit to 3 steps\n                title = step.get('title', f'Step {i}')\n                explanation = step.get('explanation', '').strip()\n                \n                if explanation:\n                    # Truncate long explanations\n                    if len(explanation) > 150:\n                        explanation = explanation[:147] + "..."\n                    \n                    formatted_parts.append(f"{i}. *{title}*")\n                    formatted_parts.append(f"   {explanation}\\n")\n            \n            if len(solution.steps) > 3:\n                formatted_parts.append("   _...and more steps in our app!_\\n")\n        \n        # Method and confidence\n        method_emojis = {\n            "textbook": "📚",\n            "wolfram": "🔬", \n            "gpt35": "🤖",\n            "gpt4": "🧠"\n        }\n        \n        method_emoji = method_emojis.get(solution.solution_method, "🤖")\n        formatted_parts.append(f"{method_emoji} Method: {solution.solution_method.upper()}")\n        formatted_parts.append(f"🎯 Confidence: {solution.confidence_score:.1%}\\n")\n        \n        # Call to action\n        formatted_parts.append("💡 *Need more help?*")\n        formatted_parts.append("📱 Download our Android app for detailed solutions!")\n        \n        return "\\n".join(formatted_parts)\n    \n    @staticmethod\n    def format_error_message(error_type: str) -> str:\n        """Format error messages for WhatsApp"""
        \n        error_messages = {\n            "quota_exceeded": "🚫 *Daily limit reached!*\\n\\nUpgrade to Premium for unlimited doubts.\\nReply *UPGRADE* for details.",\n            "invalid_image": "📸 *Image unclear!*\\n\\nPlease send a clearer photo with:\\n• Good lighting\\n• Clear text\\n• Minimal background",\n            "api_error": "⚠️ *Technical issue!*\\n\\nI'm having trouble right now. Please try again in a few minutes.",\n            "unsupported": "❓ *Can't solve this!*\\n\\nI specialize in math problems. For other subjects, try our Android app!"
        }\n        \n        return error_messages.get(error_type, "❌ Something went wrong. Please try again!")\n\n# ================================================================================\n# 🚀 WhatsApp Integration Setup\n# ================================================================================\n\ndef create_whatsapp_bot(config: Dict[str, Any]) -> WhatsAppBot:\n    """Create and configure WhatsApp bot"""
    \n    # Default configuration\n    default_config = {\n        "whatsapp_access_token": os.getenv("WHATSAPP_ACCESS_TOKEN"),\n        "whatsapp_phone_number_id": os.getenv("WHATSAPP_PHONE_NUMBER_ID"),\n        "whatsapp_verify_token": os.getenv("WHATSAPP_VERIFY_TOKEN"),\n        "twilio_account_sid": os.getenv("TWILIO_ACCOUNT_SID"),\n        "twilio_auth_token": os.getenv("TWILIO_AUTH_TOKEN"),\n        "twilio_whatsapp_number": os.getenv("TWILIO_WHATSAPP_NUMBER"),\n    }\n    \n    # Merge with provided config\n    final_config = {**default_config, **config}\n    \n    return WhatsAppBot(final_config)\n\n# ================================================================================\n# 🧪 WhatsApp Integration Testing\n# ================================================================================\n\nasync def test_whatsapp_integration():\n    """Test WhatsApp bot functionality"""
    \n    # Mock configuration for testing\n    config = {\n        "whatsapp_access_token": "test_token",\n        "whatsapp_phone_number_id": "test_phone_id",\n        "whatsapp_verify_token": "test_verify_token"\n    }\n    \n    # Create bot\n    bot = create_whatsapp_bot(config)\n    \n    # Mock doubt engine\n    engine_config = {\n        "openai_api_key": "test_key",\n        "wolfram_api_key": "test_key",\n        "mathpix_api_key": "test_key",\n        "mathpix_api_secret": "test_secret"\n    }\n    \n    engine = ProductionDoubtSolvingEngine(engine_config)\n    await bot.initialize(engine)\n    \n    # Test message processing\n    test_webhook = {\n        "entry": [{\n            "changes": [{\n                "value": {\n                    "messages": [{\n                        "from": "+919876543210",\n                        "id": "test_msg_123",\n                        "type": "text",\n                        "text": {"body": "What is 2 + 2?"},\n                        "timestamp": str(int(datetime.now().timestamp()))\n                    }]\n                }\n            }]\n        }]\n    }\n    \n    responses = await bot.process_webhook(test_webhook)\n    print(f"✅ WhatsApp integration test: {len(responses)} responses generated")\n    \n    return bot\n\nif __name__ == "__main__":\n    # Test WhatsApp integration\n    asyncio.run(test_whatsapp_integration())
