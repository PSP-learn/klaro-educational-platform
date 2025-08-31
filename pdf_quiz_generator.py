#!/usr/bin/env python3
"""
PDF Quiz Generator - Wrapper for advanced quiz generation
"""

# Import the advanced quiz generator
from advanced_quiz_generator import AdvancedQuizGenerator
import os

class PDFQuizGenerator:
    """Wrapper class for the advanced quiz generator with PDF output"""
    
    def __init__(self):
        """Initialize the PDF quiz generator"""
        self.generator = AdvancedQuizGenerator()
    
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
