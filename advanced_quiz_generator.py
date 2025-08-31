#!/usr/bin/env python3
"""
Advanced AI-Powered Quiz Generator

Enhanced version with smarter question generation, better content analysis,
and more sophisticated quiz creation capabilities.
"""

import os
import json
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

from quiz_generator import (
    QuestionType, DifficultyLevel, Question, TestPaper, 
    TestPaperGenerator, TestPaperFormatter
)
from book_search import TextChunk

class SmartQuestionGenerator:
    """Enhanced question generator with better content analysis"""
    
    def __init__(self, book_db):
        self.book_db = book_db
        self.math_keywords = self._load_math_keywords()
        self.question_patterns = self._load_question_patterns()
    
    def _load_math_keywords(self) -> Dict[str, List[str]]:
        """Load mathematical keywords and concepts"""
        return {
            'algebra': ['equation', 'variable', 'coefficient', 'polynomial', 'factorization', 'quadratic'],
            'geometry': ['triangle', 'circle', 'angle', 'parallel', 'perpendicular', 'area', 'perimeter'],
            'trigonometry': ['sine', 'cosine', 'tangent', 'angle', 'hypotenuse', 'adjacent', 'opposite'],
            'coordinate_geometry': ['coordinate', 'axis', 'origin', 'distance', 'midpoint', 'slope'],
            'statistics': ['mean', 'median', 'mode', 'frequency', 'data', 'distribution'],
            'calculus': ['derivative', 'integral', 'limit', 'function', 'differentiation'],
            'arithmetic': ['number', 'addition', 'multiplication', 'division', 'progression'],
            'probability': ['probability', 'outcome', 'event', 'sample', 'favorable']
        }
    
    def _load_question_patterns(self) -> Dict[QuestionType, Dict[str, List[str]]]:
        """Load sophisticated question patterns"""
        return {
            QuestionType.MULTIPLE_CHOICE: {
                'definition': [
                    "What is the definition of {concept}?",
                    "Which of the following best defines {concept}?",
                    "{concept} is:",
                    "In mathematics, {concept} refers to:"
                ],
                'calculation': [
                    "What is the value of {expression}?",
                    "Calculate {expression}:",
                    "The result of {expression} is:",
                    "Find the value of {expression}:"
                ],
                'property': [
                    "Which property is true for {concept}?",
                    "What is a characteristic of {concept}?",
                    "Which statement about {concept} is correct?",
                    "The property of {concept} is:"
                ],
                'application': [
                    "When is {concept} used?",
                    "In which situation would you apply {concept}?",
                    "The practical application of {concept} is:",
                    "{concept} is most useful when:"
                ]
            },
            QuestionType.SHORT_ANSWER: {
                'explain': [
                    "Explain {concept}.",
                    "What is {concept}? Explain briefly.",
                    "Describe {concept} in your own words.",
                    "Give a brief explanation of {concept}."
                ],
                'example': [
                    "Give an example of {concept}.",
                    "Provide a real-life example of {concept}.",
                    "Illustrate {concept} with an example.",
                    "Show how {concept} is used with an example."
                ],
                'method': [
                    "How do you calculate {concept}?",
                    "What is the method to find {concept}?",
                    "Describe the steps to solve for {concept}.",
                    "What is the procedure for {concept}?"
                ]
            },
            QuestionType.LONG_ANSWER: {
                'derive': [
                    "Derive the formula for {concept}.",
                    "Show the derivation of {formula}.",
                    "Prove that {statement}.",
                    "Derive and explain {concept}."
                ],
                'compare': [
                    "Compare {concept1} and {concept2}.",
                    "What are the differences between {concept1} and {concept2}?",
                    "Contrast {concept1} with {concept2}.",
                    "How do {concept1} and {concept2} differ?"
                ],
                'analyze': [
                    "Analyze the importance of {concept} in {topic}.",
                    "Discuss the role of {concept} in mathematics.",
                    "Explain the significance of {concept}.",
                    "Why is {concept} important in {topic}?"
                ]
            }
        }
    
    def extract_mathematical_concepts(self, content: str) -> Dict[str, List[str]]:
        """Extract mathematical concepts categorized by topic"""
        content_lower = content.lower()
        found_concepts = {}
        
        for category, keywords in self.math_keywords.items():
            category_concepts = []
            for keyword in keywords:
                if keyword in content_lower:
                    # Find the context around the keyword
                    pattern = rf'\b\w*{re.escape(keyword)}\w*\b'
                    matches = re.findall(pattern, content_lower)
                    category_concepts.extend([m.title() for m in matches])
            
            if category_concepts:
                found_concepts[category] = list(set(category_concepts))
        
        return found_concepts
    
    def generate_contextual_mcq(self, chunk: TextChunk, concept: str, difficulty: DifficultyLevel) -> Question:
        """Generate MCQ with proper context and realistic distractors"""
        content = chunk.text
        
        # Determine question pattern based on content
        if 'formula' in content.lower() or '=' in content:
            pattern_type = 'calculation'
        elif 'definition' in content.lower() or 'is defined as' in content.lower():
            pattern_type = 'definition'
        elif 'property' in content.lower() or 'theorem' in content.lower():
            pattern_type = 'property'
        else:
            pattern_type = 'application'
        
        # Get question template
        templates = self.question_patterns[QuestionType.MULTIPLE_CHOICE][pattern_type]
        template = templates[0]  # Use first template for now
        
        # Generate contextual question
        question_text = template.format(concept=concept)
        
        # Generate realistic options based on content
        options = self._generate_realistic_options(content, concept, pattern_type)
        
        # Shuffle options and find correct answer
        correct_answer = options[0]  # First option is correct
        random.shuffle(options)
        correct_index = options.index(correct_answer)
        correct_letter = chr(65 + correct_index)
        
        return Question(
            question_text=question_text,
            question_type=QuestionType.MULTIPLE_CHOICE,
            difficulty=difficulty,
            options=options,
            correct_answer=correct_letter,
            explanation=f"From {chunk.book_title}, page {chunk.page_number}: {content[:100]}...",
            source_chunk=content,
            source_book=chunk.book_title,
            source_page=chunk.page_number,
            points=self._calculate_points(difficulty, QuestionType.MULTIPLE_CHOICE),
            topic=concept
        )
    
    def _generate_realistic_options(self, content: str, concept: str, pattern_type: str) -> List[str]:
        """Generate realistic MCQ options based on content"""
        # Extract key information from content
        sentences = content.split('.')
        key_sentence = ""
        
        for sentence in sentences:
            if concept.lower() in sentence.lower():
                key_sentence = sentence.strip()
                break
        
        if pattern_type == 'definition':
            correct = f"A mathematical concept that {key_sentence.split('is')[-1].strip() if 'is' in key_sentence else 'relates to the given content'}"
            options = [
                correct,
                f"A concept unrelated to {concept}",
                f"A different mathematical term",
                f"An advanced topic not covered in this chapter"
            ]
        elif pattern_type == 'calculation':
            correct = "The correct calculated value"
            options = [
                correct,
                "An incorrect calculation result",
                "A value from a different formula",
                "An approximation that's not accurate"
            ]
        else:
            correct = f"The correct property or application of {concept}"
            options = [
                correct,
                f"A common misconception about {concept}",
                f"A property of a different concept",
                f"An unrelated mathematical statement"
            ]
        
        return options
    
    def _calculate_points(self, difficulty: DifficultyLevel, question_type: QuestionType) -> int:
        """Calculate points based on difficulty and type"""
        base_points = {
            QuestionType.MULTIPLE_CHOICE: 1,
            QuestionType.SHORT_ANSWER: 3,
            QuestionType.LONG_ANSWER: 5,
            QuestionType.TRUE_FALSE: 1,
            QuestionType.FILL_BLANKS: 2
        }
        
        multiplier = {
            DifficultyLevel.EASY: 1,
            DifficultyLevel.MEDIUM: 1.5,
            DifficultyLevel.HARD: 2
        }
        
        return int(base_points[question_type] * multiplier[difficulty])

class MathematicsQuizPresets:
    """Predefined quiz templates for mathematics topics"""
    
    @staticmethod
    def get_available_presets() -> Dict[str, Dict]:
        """Get available quiz presets"""
        return {
            'class_10_algebra': {
                'name': 'Class 10 - Algebra',
                'topics': ['quadratic equations', 'polynomials', 'linear equations'],
                'types': ['mcq', 'short'],
                'difficulty': ['easy', 'medium'],
                'questions': 15,
                'duration': 60
            },
            'class_10_geometry': {
                'name': 'Class 10 - Geometry',
                'topics': ['triangles', 'circles', 'coordinate geometry'],
                'types': ['mcq', 'short', 'long'],
                'difficulty': ['easy', 'medium'],
                'questions': 12,
                'duration': 90
            },
            'class_10_trigonometry': {
                'name': 'Class 10 - Trigonometry',
                'topics': ['trigonometry', 'angles', 'ratios'],
                'types': ['mcq', 'short'],
                'difficulty': ['medium', 'hard'],
                'questions': 10,
                'duration': 45
            },
            'comprehensive_test': {
                'name': 'Comprehensive Test',
                'topics': ['algebra', 'geometry', 'trigonometry', 'statistics'],
                'types': ['mcq', 'short', 'long'],
                'difficulty': ['easy', 'medium', 'hard'],
                'questions': 20,
                'duration': 120
            }
        }

def create_quiz_from_preset(preset_name: str, db_dir: str = "book_db") -> Optional[TestPaper]:
    """Create a quiz from a predefined preset"""
    presets = MathematicsQuizPresets.get_available_presets()
    
    if preset_name not in presets:
        print(f"❌ Preset '{preset_name}' not found.")
        print(f"Available presets: {', '.join(presets.keys())}")
        return None
    
    preset = presets[preset_name]
    generator = TestPaperGenerator(db_dir)
    
    print(f"🎯 Creating quiz from preset: {preset['name']}")
    
    test_paper = generator.create_custom_test(
        topics=preset['topics'],
        question_types=preset['types'],
        difficulty_levels=preset['difficulty'],
        num_questions=preset['questions'],
        duration_minutes=preset['duration'],
        subject="Mathematics"
    )
    
    return test_paper

def main_with_presets():
    """Enhanced main function with preset support"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Quiz Generator with Presets")
    parser.add_argument('--preset', '-p', type=str, help='Use a predefined quiz preset')
    parser.add_argument('--list-presets', action='store_true', help='List available presets')
    parser.add_argument('--topics', '-t', type=str, help='Custom topics (comma-separated)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--output', '-o', type=str, help='Output filename prefix')
    
    args = parser.parse_args()
    
    if args.list_presets:
        presets = MathematicsQuizPresets.get_available_presets()
        print("\n📚 Available Quiz Presets:")
        print("=" * 50)
        for key, preset in presets.items():
            print(f"\n🎯 {key}")
            print(f"   Name: {preset['name']}")
            print(f"   Topics: {', '.join(preset['topics'])}")
            print(f"   Questions: {preset['questions']}")
            print(f"   Duration: {preset['duration']} minutes")
        return
    
    if args.preset:
        # Use preset
        test_paper = create_quiz_from_preset(args.preset)
        if test_paper:
            formatter = TestPaperFormatter()
            output_prefix = args.output or f"preset_{args.preset}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            test_file, answer_file = formatter.save_test_paper(test_paper, output_prefix)
            
            print(f"\n✅ Preset quiz generated!")
            print(f"📄 Questions: {test_file}")
            print(f"📚 Answers: {answer_file}")
        return
    
    # Fall back to regular interactive or custom mode
    from quiz_generator import main
    main()

if __name__ == "__main__":
    main_with_presets()
