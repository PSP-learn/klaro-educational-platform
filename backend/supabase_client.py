#!/usr/bin/env python3
"""
🟢 Supabase Integration Client

Handles all database operations through Supabase
while keeping our FastAPI backend for AI processing
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
try:
    from supabase import create_client, Client
except ImportError:
    # Fallback for older versions
    from supabase_py import create_client, Client
import asyncio
from dataclasses import asdict

class SupabaseClient:
    """Async wrapper for Supabase operations"""
    
    def __init__(self):
        # Initialize Supabase client
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        self.service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not all([self.supabase_url, self.supabase_key]):
            raise ValueError("Supabase credentials not found in environment")
        
        # Client for user operations (with RLS)
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Admin client for service operations (bypasses RLS) - optional
        if self.service_role_key:
            self.admin_client: Client = create_client(self.supabase_url, self.service_role_key)
            print("🟢 Supabase client initialized with admin access")
        else:
            self.admin_client = None
            print("🟡 Supabase client initialized without admin access (service role key not provided)")
        
        print("🟢 Supabase client initialized successfully")
    
    # ================================================================================
    # 👤 User Management
    # ================================================================================
    
    async def create_user(self, email: str, password: str, name: str, metadata: Dict = None) -> Dict:
        """Create new user with Supabase Auth"""
        try:
            # Create auth user
            auth_response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "name": name,
                        **(metadata or {})
                    }
                }
            })
            
            if auth_response.user:
                # Create user profile
                user_data = {
                    "id": auth_response.user.id,
                    "email": email,
                    "name": name,
                    "created_at": datetime.now().isoformat()
                }
                
                self.client.table('users').insert(user_data).execute()
                
                return {
                    "success": True,
                    "user": auth_response.user,
                    "message": "User created successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to create user"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def authenticate_user(self, email: str, password: str) -> Dict:
        """Authenticate user and return session"""
        try:
            auth_response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                # Update last active
                self.client.table('users').update({
                    "last_active": datetime.now().isoformat()
                }).eq('id', auth_response.user.id).execute()
                
                return {
                    "success": True,
                    "user": auth_response.user,
                    "session": auth_response.session,
                    "access_token": auth_response.session.access_token
                }
            else:
                return {
                    "success": False,
                    "error": "Invalid credentials"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile data"""
        try:
            response = self.client.table('users').select('*').eq('id', user_id).execute()
            
            if response.data:
                return response.data[0]
            return None
            
        except Exception as e:
            print(f"❌ Error getting user profile: {e}")
            return None
    
    # ================================================================================
    # 🤔 Doubt Management
    # ================================================================================
    
    async def save_doubt(self, user_id: str, doubt_data: Dict) -> bool:
        """Save solved doubt to database"""
        try:
            doubt_record = {
                "user_id": user_id,
                "question_text": doubt_data.get("question", ""),
                "solution_data": doubt_data.get("solution", {}),
                "subject": doubt_data.get("subject", "Mathematics"),
                "method_used": doubt_data.get("method", "unknown"),
                "cost_incurred": doubt_data.get("cost", 0.0),
                "time_taken": doubt_data.get("time_taken", 0.0),
                "confidence_score": doubt_data.get("confidence", 0.0),
                "route": doubt_data.get("route", "doubts")
            }
            
            response = self.client.table('doubts').insert(doubt_record).execute()
            
            if response.data:
                # Update user's total doubts solved
                self.client.table('users').update({
                    "total_doubts_solved": self.client.table('users').select('total_doubts_solved').eq('id', user_id).execute().data[0]['total_doubts_solved'] + 1
                }).eq('id', user_id).execute()
                
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error saving doubt: {e}")
            return False
    
    async def get_user_doubts(self, user_id: str, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Get user's doubt history"""
        try:
            response = self.client.table('doubts').select('*').eq('user_id', user_id).order('created_at', desc=True).range(offset, offset + limit - 1).execute()
            
            return response.data or []
            
        except Exception as e:
            print(f"❌ Error getting doubts: {e}")
            return []
    
    # ================================================================================
    # 📄 Quiz Management
    # ================================================================================
    
    async def save_quiz(self, user_id: str, quiz_data: Dict) -> bool:
        """Save generated quiz to history"""
        try:
            quiz_record = {
                "user_id": user_id,
                "quiz_title": quiz_data.get("title", "Untitled Quiz"),
                "topics": quiz_data.get("topics", []),
                "questions_count": quiz_data.get("questions_count", 0),
                "difficulty_levels": quiz_data.get("difficulty_levels", []),
                "quiz_file_url": quiz_data.get("file_url", "")
            }
            
            response = self.client.table('quiz_history').insert(quiz_record).execute()
            return bool(response.data)
            
        except Exception as e:
            print(f"❌ Error saving quiz: {e}")
            return False
    
    async def get_user_quizzes(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user's quiz history"""
        try:
            response = self.client.table('quiz_history').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
            
            return response.data or []
            
        except Exception as e:
            print(f"❌ Error getting quizzes: {e}")
            return []
    
    # ================================================================================
    # 🎯 JEE Test Management
    # ================================================================================
    
    async def save_jee_result(self, user_id: str, test_result: Dict) -> bool:
        """Save JEE test result"""
        try:
            result_record = {
                "user_id": user_id,
                "test_id": test_result.get("test_id", ""),
                "test_type": test_result.get("test_type", "full_mock"),
                "total_score": test_result.get("total_score", 0),
                "max_score": test_result.get("max_score", 300),
                "subject_scores": test_result.get("subject_scores", {}),
                "time_taken": test_result.get("time_taken", 0)
            }
            
            response = self.client.table('jee_test_results').insert(result_record).execute()
            return bool(response.data)
            
        except Exception as e:
            print(f"❌ Error saving JEE result: {e}")
            return False
    
    async def get_user_jee_results(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's JEE test results"""
        try:
            response = self.client.table('jee_test_results').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
            
            return response.data or []
            
        except Exception as e:
            print(f"❌ Error getting JEE results: {e}")
            return []
    
    # ================================================================================
    # 📊 Analytics
    # ================================================================================
    
    async def record_usage(self, user_id: str, route: str, method: str, cost: float, success: bool = True) -> bool:
        """Record API usage for analytics"""
        try:
            usage_record = {
                "user_id": user_id,
                "route": route,
                "method": method,
                "cost": cost,
                "success": success
            }
            
            response = self.client.table('usage_analytics').insert(usage_record).execute()
            return bool(response.data)
            
        except Exception as e:
            print(f"❌ Error recording usage: {e}")
            return False
    
    async def get_user_analytics(self, user_id: str, days: int = 30) -> Dict:
        """Get user analytics for specified period"""
        try:
            since_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            # Get usage data
            usage_response = self.client.table('usage_analytics').select('*').eq('user_id', user_id).gte('created_at', since_date).execute()
            
            # Get doubts data
            doubts_response = self.client.table('doubts').select('*').eq('user_id', user_id).gte('created_at', since_date).execute()
            
            usage_data = usage_response.data or []
            doubts_data = doubts_response.data or []
            
            # Calculate analytics
            total_requests = len(usage_data)
            total_cost = sum(float(item.get('cost', 0)) for item in usage_data)
            success_rate = (sum(1 for item in usage_data if item.get('success', True)) / max(total_requests, 1)) * 100
            
            return {
                "total_requests": total_requests,
                "total_cost": total_cost,
                "success_rate": success_rate,
                "doubts_solved": len(doubts_data),
                "favorite_methods": self._get_method_breakdown(usage_data)
            }
            
        except Exception as e:
            print(f"❌ Error getting analytics: {e}")
            return {}
    
    def _get_method_breakdown(self, usage_data: List[Dict]) -> Dict[str, int]:
        """Get breakdown of methods used"""
        method_counts = {}
        for item in usage_data:
            method = item.get('method', 'unknown')
            method_counts[method] = method_counts.get(method, 0) + 1
        return method_counts

# Global Supabase client instance
supabase_client: Optional[SupabaseClient] = None

def get_supabase_client() -> SupabaseClient:
    """Get global Supabase client instance"""
    global supabase_client
    if not supabase_client:
        supabase_client = SupabaseClient()
    return supabase_client
