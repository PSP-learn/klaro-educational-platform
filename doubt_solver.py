#!/usr/bin/env python3
"""
Compatibility wrapper for doubt solving engine
"""

# Import the production doubt solving engine with fallback
import os

try:
    from doubt_solving_engine_production import ProductionDoubtSolvingEngine
    DOUBT_SOLVER_AVAILABLE = True
except ImportError:
    print("⚠️ Advanced doubt solver not available - using mock mode")
    DOUBT_SOLVER_AVAILABLE = False

class DoubtSolverEngine:
    """Wrapper class for the production doubt solving engine"""
    
    def __init__(self):
        """Initialize the doubt solver with environment configuration"""
        if DOUBT_SOLVER_AVAILABLE:
            config = {
                "openai_api_key": os.environ.get("OPENAI_API_KEY"),
                "wolfram_api_key": os.environ.get("WOLFRAM_API_KEY"),
                "mathpix_api_key": os.environ.get("MATHPIX_API_KEY"),
                "mathpix_api_secret": os.environ.get("MATHPIX_API_SECRET"),
                "openai_timeout": 30.0,
                "wolfram_timeout": 15.0,
                "mathpix_timeout": 20.0,
            }
            self.engine = ProductionDoubtSolvingEngine(config)
        else:
            self.engine = None
    
    async def solve_doubt(self, request):
        """Solve a doubt using the production engine"""
        return await self.engine.solve_doubt(request)
    
    def get_usage_stats(self, user_id: str):
        """Get usage statistics for a user"""
        return self.engine.get_usage_stats(user_id)
