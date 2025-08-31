#!/usr/bin/env python3
"""
🧪 Production Unit Tests for Doubt Solving Engine

Tests the 4 critical real-world failure scenarios:
1. Missing API key
2. Invalid API key  
3. Exceeded quota
4. API downtime

Plus concurrency, retry logic, and analytics validation.
"""

import pytest
import asyncio
import threading
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
import json

# Import the production engine
from doubt_solving_engine_production import (
    ProductionDoubtSolvingEngine, 
    DoubtRequest, 
    DoubtSolution,
    EnhancedDoubtAnalytics,
    APIRoute
)

class TestProductionDoubtEngine:
    """Production test suite for critical failure scenarios"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing"""
        return {
            "openai_api_key": "sk-test-key",
            "wolfram_api_key": "test-wolfram-key",
            "mathpix_api_key": "test-mathpix-key",
            "mathpix_api_secret": "test-mathpix-secret",
            "openai_timeout": 10.0,
            "wolfram_timeout": 5.0,
            "mathpix_timeout": 8.0
        }
    
    @pytest.fixture
    def test_request(self):
        """Standard test request"""
        return DoubtRequest(
            question_text="Solve x² + 5x + 6 = 0",
            user_id="test_user_123",
            user_plan="basic",
            subject="Mathematics",
            route="tests"
        )
    
    # ================================================================================
    # 🔑 Test Scenario 1: Missing API Key
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_missing_openai_key(self, mock_config, test_request):
        """Test behavior when OpenAI API key is missing"""
        
        # Remove OpenAI key
        config = mock_config.copy()
        config["openai_api_key"] = None
        
        engine = ProductionDoubtSolvingEngine(config)
        
        # Should handle gracefully without crashing
        solution = await engine.solve_doubt(test_request)
        
        assert solution is not None
        assert solution.solution_method == "fallback"
        assert solution.cost_incurred == 0.0
        assert "trouble solving" in solution.final_answer.lower()
        
        print("✅ Missing API key handled gracefully")
    
    @pytest.mark.asyncio 
    async def test_missing_wolfram_key(self, mock_config, test_request):
        """Test computational problems when Wolfram key is missing"""
        
        config = mock_config.copy()
        config["wolfram_api_key"] = None
        
        engine = ProductionDoubtSolvingEngine(config)
        
        # Computational question should fallback to OpenAI
        computational_request = DoubtRequest(
            question_text="Calculate derivative of x²",
            user_id="test_user",
            user_plan="basic",
            route="doubts"
        )
        
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            mock_openai.return_value = "STEP 1: Solution - Test answer\nFINAL ANSWER: Test result"
            
            solution = await engine.solve_doubt(computational_request)
            
            assert solution.solution_method == "gpt35"  # Should fallback to GPT
            assert mock_openai.called
        
        print("✅ Missing Wolfram key - graceful fallback to OpenAI")
    
    # ================================================================================
    # 🚫 Test Scenario 2: Invalid API Key  
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_invalid_openai_key(self, mock_config, test_request):
        """Test behavior with invalid OpenAI API key"""
        
        config = mock_config.copy()
        config["openai_api_key"] = "sk-invalid-12345"
        
        engine = ProductionDoubtSolvingEngine(config)
        
        # Mock OpenAI to raise authentication error
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            from openai import AuthenticationError
            mock_openai.side_effect = AuthenticationError("Invalid API key")
            
            solution = await engine.solve_doubt(test_request)
            
            assert solution.solution_method == "fallback"
            assert solution.cost_incurred == 0.0
            assert solution.retry_attempts >= 0
        
        print("✅ Invalid API key - proper error handling")
    
    @pytest.mark.asyncio
    async def test_invalid_wolfram_key(self, mock_config, test_request):
        """Test Wolfram Alpha with invalid key"""
        
        config = mock_config.copy()
        config["wolfram_api_key"] = "invalid-wolfram-key"
        
        engine = ProductionDoubtSolvingEngine(config)
        
        # Mock Wolfram to return error response
        with patch.object(engine, '_wolfram_request_with_retry') as mock_wolfram:
            mock_wolfram.return_value = {
                "queryresult": {
                    "success": False,
                    "error": "Invalid appid"
                }
            }
            
            # Mock the GPT fallback
            with patch.object(engine, '_openai_request_with_retry') as mock_openai:
                mock_openai.return_value = "STEP 1: Solution\nFINAL ANSWER: Fallback result"
                
                solution = await engine.solve_doubt(test_request)
                
                # Should fallback to GPT when Wolfram fails
                assert solution.solution_method == "gpt35"
                assert mock_wolfram.called
                assert mock_openai.called
        
        print("✅ Invalid Wolfram key - proper fallback to OpenAI")
    
    # ================================================================================
    # 📊 Test Scenario 3: Exceeded Quota
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_basic_plan_quota_exceeded(self, mock_config):
        """Test quota limits for basic plan users"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        # Simulate user who has used 20 doubts (limit reached)
        user_id = "quota_test_user"
        current_month = datetime.now().strftime("%Y-%m")
        user_key = f"{user_id}_{current_month}"
        
        engine.usage_db[user_key] = {
            "doubts_used": 20,  # At limit
            "plan": "basic",
            "total_cost": 0.08,
            "methods_used": {"gpt35": 20},
            "routes_used": {"doubts": 20}
        }
        
        request = DoubtRequest(
            question_text="New question after limit",
            user_id=user_id,
            user_plan="basic"
        )
        
        solution = await engine.solve_doubt(request)
        
        assert solution.solution_method == "upgrade_prompt"
        assert "reached your monthly doubt limit" in solution.final_answer
        assert "Upgrade to Premium" in solution.steps[0].explanation
        
        print("✅ Quota exceeded - proper upgrade prompt shown")
    
    @pytest.mark.asyncio
    async def test_premium_plan_unlimited(self, mock_config):
        """Test that premium users have unlimited access"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        # Simulate premium user with high usage
        user_id = "premium_test_user"
        current_month = datetime.now().strftime("%Y-%m")
        user_key = f"{user_id}_{current_month}"
        
        engine.usage_db[user_key] = {
            "doubts_used": 100,  # Way over basic limit
            "plan": "premium",
            "total_cost": 9.0,
            "methods_used": {"gpt4": 100},
            "routes_used": {"doubts": 100}
        }
        
        request = DoubtRequest(
            question_text="Premium user question",
            user_id=user_id,
            user_plan="premium"
        )
        
        # Mock successful GPT-4 response
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            mock_openai.return_value = "STEP 1: Premium solution\nFINAL ANSWER: Premium result"
            
            solution = await engine.solve_doubt(request)
            
            assert solution.solution_method == "gpt4"
            assert solution.cost_incurred == 0.09
        
        print("✅ Premium plan - unlimited access confirmed")
    
    @pytest.mark.asyncio
    async def test_openai_rate_limit_handling(self, mock_config, test_request):
        """Test OpenAI rate limit error handling"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            from openai import RateLimitError
            
            # First call raises rate limit, second succeeds
            mock_openai.side_effect = [
                RateLimitError("Rate limit exceeded"),
                "STEP 1: Solution after retry\nFINAL ANSWER: Success"
            ]
            
            solution = await engine.solve_doubt(test_request)
            
            # Should eventually succeed with retries
            assert solution.solution_method == "gpt35"
            assert mock_openai.call_count >= 1
        
        print("✅ Rate limit handling - proper retry logic")
    
    # ================================================================================
    # 🌐 Test Scenario 4: API Downtime
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_openai_api_downtime(self, mock_config, test_request):
        """Test complete OpenAI API downtime"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            from openai import APIError
            mock_openai.side_effect = APIError("Service temporarily unavailable")
            
            solution = await engine.solve_doubt(test_request)
            
            assert solution.solution_method == "fallback"
            assert "temporarily unavailable" in solution.steps[0].explanation
            assert solution.cost_incurred == 0.0
        
        print("✅ API downtime - graceful fallback handling")
    
    @pytest.mark.asyncio
    async def test_wolfram_api_downtime(self, mock_config, test_request):
        """Test Wolfram Alpha API downtime"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        # Computational question
        computational_request = DoubtRequest(
            question_text="Solve equation x² = 4",
            user_id="test_user",
            user_plan="basic"
        )
        
        with patch.object(engine, '_wolfram_request_with_retry') as mock_wolfram:
            with patch.object(engine, '_openai_request_with_retry') as mock_openai:
                # Wolfram fails, OpenAI succeeds
                import aiohttp
                mock_wolfram.side_effect = aiohttp.ServerTimeoutError("Wolfram timeout")
                mock_openai.return_value = "STEP 1: Fallback solution\nFINAL ANSWER: x = ±2"
                
                solution = await engine.solve_doubt(computational_request)
                
                assert solution.solution_method == "gpt35"  # Fallback from Wolfram
                assert mock_wolfram.called
                assert mock_openai.called
        
        print("✅ Wolfram downtime - proper fallback to OpenAI")
    
    # ================================================================================
    # 🧵 Test Concurrency Safety
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, mock_config):
        """Test thread safety with concurrent requests"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        # Create multiple concurrent requests
        requests = [
            DoubtRequest(
                question_text=f"Question {i}: solve x + {i} = 10",
                user_id=f"user_{i}",
                user_plan="basic",
                route="tests"
            )
            for i in range(5)
        ]
        
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            mock_openai.return_value = "STEP 1: Concurrent solution\nFINAL ANSWER: x = result"
            
            # Execute all requests concurrently
            solutions = await asyncio.gather(*[
                engine.solve_doubt(req) for req in requests
            ])
            
            # All should succeed
            assert len(solutions) == 5
            assert all(sol.solution_method == "gpt35" for sol in solutions)
            assert mock_openai.call_count == 5
            
            # Check usage tracking worked for all
            for i in range(5):
                user_key = f"user_{i}_{datetime.now().strftime('%Y-%m')}"
                assert user_key in engine.usage_db
                assert engine.usage_db[user_key]["doubts_used"] == 1
        
        print("✅ Concurrency - thread-safe operation confirmed")
    
    # ================================================================================
    # 🔄 Test Retry Logic
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_retry_logic_eventual_success(self, mock_config, test_request):
        """Test retry logic eventually succeeds"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            from openai import APITimeoutError
            
            # Fail twice, then succeed
            mock_openai.side_effect = [
                APITimeoutError("Timeout 1"),
                APITimeoutError("Timeout 2"),
                "STEP 1: Final success\nFINAL ANSWER: Retry worked"
            ]
            
            solution = await engine.solve_doubt(test_request)
            
            assert solution.solution_method == "gpt35"
            assert solution.retry_attempts >= 2
            assert mock_openai.call_count == 3
        
        print("✅ Retry logic - eventual success after failures")
    
    @pytest.mark.asyncio
    async def test_retry_logic_max_attempts(self, mock_config, test_request):
        """Test retry logic gives up after max attempts"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            from openai import APIError
            
            # Always fail
            mock_openai.side_effect = APIError("Persistent failure")
            
            solution = await engine.solve_doubt(test_request)
            
            assert solution.solution_method == "fallback"
            assert solution.retry_attempts == 3  # Max retries
            assert "temporarily unavailable" in solution.steps[0].explanation
        
        print("✅ Retry logic - proper fallback after max attempts")
    
    # ================================================================================
    # 📊 Test Enhanced Analytics
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_route_analytics_tracking(self, mock_config):
        """Test granular route-level analytics"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        # Different routes
        test_requests = [
            DoubtRequest(question_text="Q1", user_id="user1", route="doubts"),
            DoubtRequest(question_text="Q2", user_id="user1", route="tests"),
            DoubtRequest(question_text="Q3", user_id="user1", route="papers"),
            DoubtRequest(question_text="Q4", user_id="user1", route="doubts"),
        ]
        
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            mock_openai.return_value = "STEP 1: Solution\nFINAL ANSWER: Result"
            
            # Process all requests
            for req in test_requests:
                await engine.solve_doubt(req)
            
            # Check route analytics
            route_analytics = engine.get_route_analytics()
            
            assert "doubts" in route_analytics["current_month_routes"]
            assert "tests" in route_analytics["current_month_routes"]
            assert "papers" in route_analytics["current_month_routes"]
            
            # Doubts should have 2 requests
            doubts_data = route_analytics["current_month_routes"]["doubts"]
            assert doubts_data["total_requests"] == 2
            
            # Tests and papers should have 1 each
            tests_data = route_analytics["current_month_routes"]["tests"]
            papers_data = route_analytics["current_month_routes"]["papers"]
            assert tests_data["total_requests"] == 1
            assert papers_data["total_requests"] == 1
        
        print("✅ Route analytics - granular tracking working")
    
    @pytest.mark.asyncio
    async def test_cost_efficiency_analytics(self, mock_config):
        """Test cost efficiency analysis"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        analytics = EnhancedDoubtAnalytics(engine.usage_db, engine.route_analytics)
        
        # Simulate mixed usage pattern
        user_id = "efficiency_user"
        current_month = datetime.now().strftime("%Y-%m")
        user_key = f"{user_id}_{current_month}"
        
        engine.usage_db[user_key] = {
            "doubts_used": 10,
            "total_cost": 0.025,  # Mix of free and paid
            "methods_used": {
                "textbook": 5,  # Free
                "gpt35": 3,     # $0.012
                "wolfram": 2    # $0.005
            },
            "routes_used": {"doubts": 10},
            "plan": "basic"
        }
        
        analytics_result = analytics.get_comprehensive_analytics(user_id)
        
        # Check cost efficiency calculation
        efficiency = analytics_result["cost_efficiency"]
        assert efficiency["efficiency_score"] == 50.0  # 5/10 free queries
        assert efficiency["savings_from_textbook"] == 5 * 0.004  # Saved costs
        
        print("✅ Cost efficiency analytics - accurate calculations")
    
    # ================================================================================
    # ⚡ Test Performance and Timeouts
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self, mock_config, test_request):
        """Test timeout handling doesn't hang the system"""
        
        config = mock_config.copy()
        config["openai_timeout"] = 1.0  # Very short timeout
        
        engine = ProductionDoubtSolvingEngine(config)
        
        with patch.object(engine, '_openai_request_with_retry') as mock_openai:
            from openai import APITimeoutError
            mock_openai.side_effect = APITimeoutError("Request timeout")
            
            start_time = time.time()
            solution = await engine.solve_doubt(test_request)
            end_time = time.time()
            
            # Should fail fast and not hang
            assert end_time - start_time < 10.0  # Should not take too long
            assert solution.solution_method == "fallback"
        
        print("✅ Timeout handling - no system hangs")
    
    # ================================================================================
    # 🖼️ Test OCR Failure Scenarios
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_mathpix_ocr_failure(self, mock_config):
        """Test OCR failure handling"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        request = DoubtRequest(
            image_data=b"fake_image_data",
            user_id="ocr_user",
            route="ocr"
        )
        
        with patch.object(engine, '_mathpix_request_with_retry') as mock_mathpix:
            mock_mathpix.side_effect = Exception("Mathpix API error")
            
            solution = await engine.solve_doubt(request)
            
            # Should handle OCR failure gracefully
            assert "OCR extraction failed" in solution.question or "Unable to extract" in solution.question
            assert solution.solution_method == "fallback"
        
        print("✅ OCR failure - graceful error handling")
    
    # ================================================================================
    # 📈 Test Analytics Edge Cases
    # ================================================================================
    
    def test_analytics_with_empty_data(self, mock_config):
        """Test analytics with no usage data"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        analytics = EnhancedDoubtAnalytics(engine.usage_db, engine.route_analytics)
        
        # User with no usage
        result = analytics.get_comprehensive_analytics("new_user")
        
        assert result["user_metrics"]["doubts_used"] == 0
        assert result["insights"]["most_used_method"] == "none"
        assert result["cost_efficiency"]["efficiency_score"] == 100.0
        
        print("✅ Analytics edge cases - empty data handled")
    
    def test_route_analytics_calculation(self, mock_config):
        """Test route analytics success rate calculation"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        # Mock route data
        current_month = datetime.now().strftime("%Y-%m")
        engine.route_analytics = {
            f"doubts_{current_month}": {
                "total_requests": 10,
                "successful_requests": 8,
                "total_cost": 0.04
            },
            f"tests_{current_month}": {
                "total_requests": 5,
                "successful_requests": 5,
                "total_cost": 0.02
            }
        }
        
        analytics = engine.get_route_analytics()
        
        assert analytics["total_requests"] == 15
        assert analytics["overall_success_rate"] == (13/15) * 100  # 86.67%
        
        print("✅ Route analytics - accurate success rate calculation")
    
    # ================================================================================
    # 🔄 Test Multi-Service Fallback Chain
    # ================================================================================
    
    @pytest.mark.asyncio
    async def test_complete_fallback_chain(self, mock_config):
        """Test complete fallback chain: Textbook → Wolfram → GPT-3.5 → Fallback"""
        
        engine = ProductionDoubtSolvingEngine(mock_config)
        
        # Mock textbook database to return no results
        with patch.object(engine, '_search_textbook_database') as mock_textbook:
            mock_textbook.return_value = None
            
            # Mock Wolfram to fail
            with patch.object(engine, '_wolfram_request_with_retry') as mock_wolfram:
                mock_wolfram.side_effect = Exception("Wolfram failed")
                
                # Mock OpenAI to fail
                with patch.object(engine, '_openai_request_with_retry') as mock_openai:
                    from openai import APIError
                    mock_openai.side_effect = APIError("OpenAI failed")
                    
                    request = DoubtRequest(
                        question_text="Solve x + 1 = 5",
                        user_id="fallback_user",
                        user_plan="basic"
                    )
                    
                    solution = await engine.solve_doubt(request)
                    
                    # Should reach final fallback
                    assert solution.solution_method == "fallback"
                    assert mock_textbook.called
                    assert mock_wolfram.called
                    assert mock_openai.called
        
        print("✅ Complete fallback chain - all services failing handled gracefully")

# ================================================================================
# 🚀 Test Runner and Reporting
# ================================================================================

async def run_all_production_tests():
    """Run comprehensive production test suite"""
    
    print("🧪 PRODUCTION DOUBT ENGINE TEST SUITE")
    print("=" * 80)
    print("Testing critical real-world failure scenarios...\n")
    
    # Mock config for all tests
    mock_config = {
        "openai_api_key": "sk-test-key",
        "wolfram_api_key": "test-wolfram-key",
        "mathpix_api_key": "test-mathpix-key",
        "mathpix_api_secret": "test-mathpix-secret",
        "openai_timeout": 10.0,
        "wolfram_timeout": 5.0,
        "mathpix_timeout": 8.0
    }
    
    test_request = DoubtRequest(
        question_text="Test: solve x² + 5x + 6 = 0",
        user_id="test_user_123",
        user_plan="basic",
        subject="Mathematics",
        route="tests"
    )
    
    test_suite = TestProductionDoubtEngine()
    
    # Run all tests
    tests = [
        ("Missing OpenAI Key", test_suite.test_missing_openai_key(mock_config, test_request)),
        ("Missing Wolfram Key", test_suite.test_missing_wolfram_key(mock_config, test_request)),
        ("Invalid OpenAI Key", test_suite.test_invalid_openai_key(mock_config, test_request)),
        ("Invalid Wolfram Key", test_suite.test_invalid_wolfram_key(mock_config, test_request)),
        ("Basic Plan Quota", test_suite.test_basic_plan_quota_exceeded(mock_config)),
        ("Premium Unlimited", test_suite.test_premium_plan_unlimited(mock_config)),
        ("Rate Limit Handling", test_suite.test_openai_rate_limit_handling(mock_config, test_request)),
        ("OpenAI Downtime", test_suite.test_openai_api_downtime(mock_config, test_request)),
        ("Wolfram Downtime", test_suite.test_wolfram_api_downtime(mock_config, test_request)),
        ("Concurrent Requests", test_suite.test_concurrent_requests(mock_config)),
        ("Retry Logic Success", test_suite.test_retry_logic_eventual_success(mock_config, test_request)),
        ("Retry Logic Failure", test_suite.test_retry_logic_max_attempts(mock_config, test_request)),
        ("Route Analytics", test_suite.test_route_analytics_tracking(mock_config)),
        ("Cost Efficiency", test_suite.test_cost_efficiency_analytics(mock_config)),
        ("Timeout Handling", test_suite.test_timeout_handling(mock_config, test_request)),
        ("OCR Failure", test_suite.test_mathpix_ocr_failure(mock_config)),
        ("Complete Fallback", test_suite.test_complete_fallback_chain(mock_config))
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_coro in tests:
        try:
            print(f"🔍 Running: {test_name}")
            await test_coro
            passed += 1
            
        except Exception as e:
            print(f"❌ FAILED: {test_name} - {e}")
            failed += 1
    
    print(f"\n📊 TEST RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed))*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED - ENGINE IS PRODUCTION READY!")
    else:
        print(f"\n⚠️ {failed} tests failed - review before production deployment")

# ================================================================================
# 🎯 Mock Test Data and Helpers
# ================================================================================

class MockOpenAIResponse:
    """Mock OpenAI response structure"""
    def __init__(self, content: str):
        self.choices = [MockChoice(content)]

class MockChoice:
    """Mock OpenAI choice structure"""
    def __init__(self, content: str):
        self.message = MockMessage(content)

class MockMessage:
    """Mock OpenAI message structure"""
    def __init__(self, content: str):
        self.content = content

# ================================================================================
# 🧪 Integration Test Helpers
# ================================================================================

async def test_real_api_integration():
    """
    Integration test with real APIs (requires real keys)
    ⚠️ Only run this with valid API keys and expect costs!
    """
    
    print("🔥 REAL API INTEGRATION TEST")
    print("⚠️ This will incur actual API costs!")
    print("=" * 50)
    
    # Use environment variables for real keys
    import os
    
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "wolfram_api_key": os.getenv("WOLFRAM_API_KEY"),
        "mathpix_api_key": os.getenv("MATHPIX_API_KEY"),
        "mathpix_api_secret": os.getenv("MATHPIX_API_SECRET")
    }
    
    if not config["openai_api_key"]:
        print("⚠️ No real API keys found - skipping integration test")
        return
    
    engine = ProductionDoubtSolvingEngine(config)
    
    request = DoubtRequest(
        question_text="What is the derivative of x³?",
        user_id="integration_test_user",
        user_plan="basic",
        route="tests"
    )
    
    try:
        solution = await engine.solve_doubt(request)
        
        print(f"✅ Real API test successful!")
        print(f"   Method: {solution.solution_method}")
        print(f"   Cost: ${solution.cost_incurred:.4f}")
        print(f"   Answer: {solution.final_answer[:50]}...")
        
    except Exception as e:
        print(f"❌ Real API test failed: {e}")

if __name__ == "__main__":
    print("🧪 Starting Production Test Suite...")
    asyncio.run(run_all_production_tests())
    
    # Uncomment to test with real APIs (costs money!)
    # print("\n" + "="*50)
    # asyncio.run(test_real_api_integration())
