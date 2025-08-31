#!/usr/bin/env python3
"""
PDF Quiz Generator - Wrapper for advanced quiz generation
"""

# Import the advanced quiz generator with fallback
import os

try:
    from advanced_quiz_generator import AdvancedQuizGenerator
    QUIZ_GENERATOR_AVAILABLE = True
except ImportError:
    print("⚠️ Advanced quiz generator not available - using mock mode")
    QUIZ_GENERATOR_AVAILABLE = False

class PDFQuizGenerator:
    """Wrapper class for the advanced quiz generator with PDF output"""
    
    def __init__(self):
        """Initialize the PDF quiz generator"""
        if QUIZ_GENERATOR_AVAILABLE:
            self.generator = AdvancedQuizGenerator()
        else:
            self.generator = None
    
    async def generate_quiz(self, topic: str, difficulty: str = "medium", num_questions: int = 10):
        """Generate a quiz and return PDF"""
        return await self.generator.generate_quiz(
            topic=topic,
            difficulty=difficulty,
            num_questions=num_questions
        )
    
    async def generate_pdf(self, quiz_data: dict) -> bytes:
        """Convert quiz data to PDF format"""
        return await self.generator.create_pdf(quiz_data)
    
    def get_supported_topics(self) -> list:
        """Get list of supported topics"""
        return self.generator.get_topics()
