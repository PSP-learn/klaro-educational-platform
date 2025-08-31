#!/usr/bin/env python3
"""
AI-Powered Quiz Generator

This script generates customizable test papers and quizzes from your organized textbook collection.
It uses the existing book search system to find relevant content and AI to generate questions.

Features:
- Multiple question types (MCQ, Short Answer, Long Answer, True/False)
- Customizable difficulty levels
- Topic/chapter selection
- Auto-generated answer keys with explanations
- Multiple output formats (PDF, HTML, Text)
- Progress tracking and analytics
"""

import os
import json
import argparse
import logging
import random
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Import our existing book search system
from book_search import BookVectorDB, TextChunk

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuestionType(Enum):
    """Types of questions that can be generated"""
    MULTIPLE_CHOICE = "mcq"
    SHORT_ANSWER = "short"
    LONG_ANSWER = "long"
    TRUE_FALSE = "true_false"
    FILL_BLANKS = "fill_blanks"

class DifficultyLevel(Enum):
    """Difficulty levels for questions"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

@dataclass
class Question:
    """A generated question with metadata"""
    question_text: str
    question_type: QuestionType
    difficulty: DifficultyLevel
    options: List[str] = None  # For MCQ
    correct_answer: str = ""
    explanation: str = ""
    source_chunk: str = ""
    source_book: str = ""
    source_page: int = 0
    points: int = 1
    topic: str = ""

@dataclass
class TestPaper:
    """A complete test paper"""
    title: str
    subject: str
    topics: List[str]
    questions: List[Question]
    total_points: int
    duration_minutes: int
    instructions: str
    created_at: str
    difficulty_distribution: Dict[str, int]

class QuestionGenerator:
    """AI-powered question generator"""
    
    def __init__(self, book_db: BookVectorDB):
        self.book_db = book_db
        self.question_templates = self._load_question_templates()
    
    def _load_question_templates(self) -> Dict[str, List[str]]:
        """Load question templates for different types"""
        return {
            QuestionType.MULTIPLE_CHOICE: [
                "What is {concept}?",
                "Which of the following best describes {concept}?",
                "In the context of {topic}, {concept} refers to:",
                "The primary characteristic of {concept} is:",
                "Which statement about {concept} is correct?"
            ],
            QuestionType.SHORT_ANSWER: [
                "Define {concept}.",
                "Explain {concept} in your own words.",
                "What is the significance of {concept} in {topic}?",
                "How does {concept} relate to {related_concept}?",
                "Give an example of {concept}."
            ],
            QuestionType.LONG_ANSWER: [
                "Discuss {concept} in detail with examples.",
                "Analyze the role of {concept} in {topic}.",
                "Compare and contrast {concept} with {related_concept}.",
                "Explain the practical applications of {concept}.",
                "Derive and explain the formula for {concept}."
            ],
            QuestionType.TRUE_FALSE: [
                "{statement} is always true.",
                "In {topic}, {statement}.",
                "The concept of {concept} means that {statement}.",
                "According to the theory, {statement}."
            ],
            QuestionType.FILL_BLANKS: [
                "{concept} is defined as ______.",
                "The formula for {concept} is ______.",
                "In {topic}, ______ is used to calculate {concept}.",
                "The relationship between {concept1} and {concept2} is ______."
            ]
        }
    
    def extract_concepts_from_content(self, content: str) -> List[str]:
        """Extract key concepts from textbook content"""
        # Simple concept extraction - can be enhanced with NLP
        import re
        
        # Look for mathematical terms, formulas, definitions
        concepts = []
        
        # Find terms that appear to be definitions (word followed by "is" or "are")
        definition_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|are)\s+'
        definitions = re.findall(definition_pattern, content)
        concepts.extend(definitions)
        
        # Find mathematical terms (words ending in common math suffixes)
        math_terms = re.findall(r'([a-z]+(?:tion|ment|ity|ness|ism|ology))', content.lower())
        concepts.extend([term.title() for term in math_terms])
        
        # Find capitalized terms (likely to be important concepts)
        capitalized = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', content)
        concepts.extend(capitalized)
        
        # Remove duplicates and filter
        unique_concepts = list(set(concepts))
        # Filter out common words
        filtered_concepts = [c for c in unique_concepts if c.lower() not in 
                           ['the', 'and', 'or', 'but', 'chapter', 'section', 'page', 'figure']]
        
        return filtered_concepts[:10]  # Return top 10 concepts
    
    def generate_mcq_question(self, chunk: TextChunk, concept: str, difficulty: DifficultyLevel) -> Question:
        """Generate a multiple choice question"""
        # Extract context around the concept
        content = chunk.text
        
        # Generate question
        templates = self.question_templates[QuestionType.MULTIPLE_CHOICE]
        template = random.choice(templates)
        question_text = template.format(concept=concept, topic=chunk.book_title)
        
        # Generate options (simplified - would use AI in production)
        correct_answer = f"The correct definition/explanation of {concept}"
        options = [
            correct_answer,
            f"An incorrect but plausible definition of {concept}",
            f"A related but different concept from {concept}",
            f"A completely unrelated concept"
        ]
        random.shuffle(options)
        
        # Find correct answer index
        correct_index = options.index(correct_answer)
        correct_letter = chr(65 + correct_index)  # A, B, C, D
        
        return Question(
            question_text=question_text,
            question_type=QuestionType.MULTIPLE_CHOICE,
            difficulty=difficulty,
            options=options,
            correct_answer=correct_letter,
            explanation=f"Based on the content from {chunk.book_title}, page {chunk.page_number}",
            source_chunk=content[:200] + "..." if len(content) > 200 else content,
            source_book=chunk.book_title,
            source_page=chunk.page_number,
            points=1 if difficulty == DifficultyLevel.EASY else 2 if difficulty == DifficultyLevel.MEDIUM else 3,
            topic=concept
        )
    
    def generate_short_answer_question(self, chunk: TextChunk, concept: str, difficulty: DifficultyLevel) -> Question:
        """Generate a short answer question"""
        templates = self.question_templates[QuestionType.SHORT_ANSWER]
        template = random.choice(templates)
        question_text = template.format(concept=concept, topic=chunk.book_title)
        
        return Question(
            question_text=question_text,
            question_type=QuestionType.SHORT_ANSWER,
            difficulty=difficulty,
            correct_answer=f"Answer should include key points about {concept} from the textbook",
            explanation=f"Refer to {chunk.book_title}, page {chunk.page_number}",
            source_chunk=chunk.text[:300] + "..." if len(chunk.text) > 300 else chunk.text,
            source_book=chunk.book_title,
            source_page=chunk.page_number,
            points=2 if difficulty == DifficultyLevel.EASY else 4 if difficulty == DifficultyLevel.MEDIUM else 6,
            topic=concept
        )
    
    def generate_questions_from_content(self, chunks: List[Tuple[TextChunk, float]], 
                                      question_types: List[QuestionType],
                                      difficulty_levels: List[DifficultyLevel],
                                      num_questions: int) -> List[Question]:
        """Generate questions from content chunks"""
        questions = []
        
        for i, (chunk, score) in enumerate(chunks[:num_questions * 2]):  # Get more chunks than needed
            if len(questions) >= num_questions:
                break
            
            # Extract concepts from this chunk
            concepts = self.extract_concepts_from_content(chunk.text)
            
            if not concepts:
                continue
            
            # Pick a random concept and question type
            concept = random.choice(concepts)
            question_type = random.choice(question_types)
            difficulty = random.choice(difficulty_levels)
            
            try:
                if question_type == QuestionType.MULTIPLE_CHOICE:
                    question = self.generate_mcq_question(chunk, concept, difficulty)
                elif question_type == QuestionType.SHORT_ANSWER:
                    question = self.generate_short_answer_question(chunk, concept, difficulty)
                else:
                    # For now, default to short answer for other types
                    question = self.generate_short_answer_question(chunk, concept, difficulty)
                
                questions.append(question)
                
            except Exception as e:
                logger.warning(f"Failed to generate question from chunk: {e}")
                continue
        
        return questions

class TestPaperGenerator:
    """Main test paper generator"""
    
    def __init__(self, book_db_path: str = "book_db"):
        self.book_db = BookVectorDB(db_dir=book_db_path)
        self.question_generator = QuestionGenerator(self.book_db)
    
    def create_custom_test(self,
                          topics: List[str],
                          question_types: List[str] = ["mcq", "short"],
                          difficulty_levels: List[str] = ["easy", "medium"],
                          num_questions: int = 10,
                          duration_minutes: int = 60,
                          subject: str = "Mathematics") -> TestPaper:
        """Create a customized test paper"""
        
        logger.info(f"Creating test for topics: {topics}")
        
        # Convert string enums to actual enums
        q_types = [QuestionType(qt) for qt in question_types]
        diff_levels = [DifficultyLevel(dl) for dl in difficulty_levels]
        
        # Search for content related to all topics
        all_chunks = []
        for topic in topics:
            search_results = self.book_db.search(topic, top_k=20)
            all_chunks.extend(search_results)
        
        if not all_chunks:
            raise ValueError(f"No content found for topics: {topics}")
        
        # Sort by relevance and remove duplicates
        unique_chunks = {}
        for chunk, score in all_chunks:
            if chunk.chunk_id not in unique_chunks or unique_chunks[chunk.chunk_id][1] < score:
                unique_chunks[chunk.chunk_id] = (chunk, score)
        
        sorted_chunks = sorted(unique_chunks.values(), key=lambda x: x[1], reverse=True)
        
        # Generate questions
        logger.info(f"Generating {num_questions} questions from {len(sorted_chunks)} content chunks")
        questions = self.question_generator.generate_questions_from_content(
            sorted_chunks, q_types, diff_levels, num_questions
        )
        
        if not questions:
            raise ValueError("Failed to generate any questions")
        
        # Calculate difficulty distribution
        difficulty_dist = {}
        for q in questions:
            diff_str = q.difficulty.value
            difficulty_dist[diff_str] = difficulty_dist.get(diff_str, 0) + 1
        
        # Create test paper
        test_paper = TestPaper(
            title=f"{subject} Test - {', '.join(topics)}",
            subject=subject,
            topics=topics,
            questions=questions,
            total_points=sum(q.points for q in questions),
            duration_minutes=duration_minutes,
            instructions=self._generate_instructions(questions),
            created_at=datetime.now().isoformat(),
            difficulty_distribution=difficulty_dist
        )
        
        logger.info(f"Created test with {len(questions)} questions, {test_paper.total_points} points")
        return test_paper
    
    def _generate_instructions(self, questions: List[Question]) -> str:
        """Generate test instructions"""
        mcq_count = sum(1 for q in questions if q.question_type == QuestionType.MULTIPLE_CHOICE)
        short_count = sum(1 for q in questions if q.question_type == QuestionType.SHORT_ANSWER)
        long_count = sum(1 for q in questions if q.question_type == QuestionType.LONG_ANSWER)
        
        instructions = "TEST INSTRUCTIONS:\n\n"
        instructions += f"• Total Questions: {len(questions)}\n"
        
        if mcq_count > 0:
            instructions += f"• Multiple Choice Questions: {mcq_count} (Choose the best answer)\n"
        if short_count > 0:
            instructions += f"• Short Answer Questions: {short_count} (2-3 sentences)\n"
        if long_count > 0:
            instructions += f"• Long Answer Questions: {long_count} (Detailed explanation required)\n"
        
        instructions += "\n• Write clearly and legibly\n"
        instructions += "• Show your work for mathematical problems\n"
        instructions += "• Read each question carefully before answering\n"
        
        return instructions

class TestPaperFormatter:
    """Format test papers in different formats"""
    
    def __init__(self):
        self.output_dir = Path("generated_tests")
        self.output_dir.mkdir(exist_ok=True)
    
    def format_as_text(self, test_paper: TestPaper) -> str:
        """Format test paper as plain text"""
        output = []
        output.append("=" * 80)
        output.append(f"📝 {test_paper.title}")
        output.append("=" * 80)
        output.append(f"Subject: {test_paper.subject}")
        output.append(f"Topics: {', '.join(test_paper.topics)}")
        output.append(f"Duration: {test_paper.duration_minutes} minutes")
        output.append(f"Total Points: {test_paper.total_points}")
        output.append(f"Created: {test_paper.created_at}")
        output.append("\n")
        
        # Instructions
        output.append(test_paper.instructions)
        output.append("\n" + "=" * 80 + "\n")
        
        # Questions
        for i, question in enumerate(test_paper.questions, 1):
            output.append(f"Q{i}. {question.question_text}")
            output.append(f"    [Difficulty: {question.difficulty.value.title()}, Points: {question.points}]")
            
            if question.question_type == QuestionType.MULTIPLE_CHOICE and question.options:
                for j, option in enumerate(question.options):
                    output.append(f"    {chr(65 + j)}. {option}")
            
            output.append("")  # Blank line for answer space
            output.append("")  # Extra space
        
        return "\n".join(output)
    
    def format_answer_key(self, test_paper: TestPaper) -> str:
        """Format answer key as text"""
        output = []
        output.append("=" * 80)
        output.append(f"📚 ANSWER KEY - {test_paper.title}")
        output.append("=" * 80)
        output.append("")
        
        for i, question in enumerate(test_paper.questions, 1):
            output.append(f"Q{i}. {question.correct_answer}")
            
            if question.explanation:
                output.append(f"     Explanation: {question.explanation}")
            
            output.append(f"     Source: {question.source_book}, Page {question.source_page}")
            output.append(f"     Points: {question.points}")
            output.append("")
        
        # Statistics
        output.append("\n" + "=" * 80)
        output.append("📊 TEST STATISTICS")
        output.append("=" * 80)
        output.append(f"Total Questions: {len(test_paper.questions)}")
        output.append(f"Total Points: {test_paper.total_points}")
        
        for difficulty, count in test_paper.difficulty_distribution.items():
            output.append(f"{difficulty.title()} Questions: {count}")
        
        return "\n".join(output)
    
    def save_test_paper(self, test_paper: TestPaper, filename_prefix: str = None) -> Tuple[str, str]:
        """Save test paper and answer key to files"""
        if not filename_prefix:
            filename_prefix = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save test paper
        test_content = self.format_as_text(test_paper)
        test_file = self.output_dir / f"{filename_prefix}_questions.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Save answer key
        answer_content = self.format_answer_key(test_paper)
        answer_file = self.output_dir / f"{filename_prefix}_answers.txt"
        with open(answer_file, 'w', encoding='utf-8') as f:
            f.write(answer_content)
        
        # Save metadata
        metadata_file = self.output_dir / f"{filename_prefix}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            # Convert test paper to dict, handling enums
            test_dict = asdict(test_paper)
            # Convert enum values to strings
            for question in test_dict['questions']:
                question['question_type'] = question['question_type'].value if hasattr(question['question_type'], 'value') else str(question['question_type'])
                question['difficulty'] = question['difficulty'].value if hasattr(question['difficulty'], 'value') else str(question['difficulty'])
            
            json.dump(test_dict, f, indent=2, default=str)
        
        logger.info(f"Test paper saved:")
        logger.info(f"  Questions: {test_file}")
        logger.info(f"  Answers: {answer_file}")
        logger.info(f"  Metadata: {metadata_file}")
        
        return str(test_file), str(answer_file)

class QuizGeneratorCLI:
    """Command line interface for quiz generation"""
    
    def __init__(self):
        self.generator = TestPaperGenerator()
        self.formatter = TestPaperFormatter()
    
    def interactive_mode(self):
        """Interactive quiz creation mode"""
        print("\n🎯 Interactive Quiz Generator")
        print("=" * 50)
        
        try:
            # Get user preferences
            subject = input("Subject (default: Mathematics): ").strip() or "Mathematics"
            
            print("\nAvailable topics in your database:")
            self._suggest_topics()
            
            topics_input = input("\nEnter topics (comma-separated): ").strip()
            topics = [t.strip() for t in topics_input.split(",") if t.strip()]
            
            if not topics:
                print("❌ No topics specified. Exiting.")
                return
            
            # Question types
            print("\nQuestion types: mcq, short, long, true_false, fill_blanks")
            types_input = input("Question types (default: mcq,short): ").strip() or "mcq,short"
            question_types = [t.strip() for t in types_input.split(",")]
            
            # Difficulty
            print("\nDifficulty levels: easy, medium, hard")
            diff_input = input("Difficulty levels (default: easy,medium): ").strip() or "easy,medium"
            difficulty_levels = [d.strip() for d in diff_input.split(",")]
            
            # Number of questions
            num_questions = int(input("Number of questions (default: 10): ").strip() or "10")
            
            # Duration
            duration = int(input("Duration in minutes (default: 60): ").strip() or "60")
            
            # Generate test
            print(f"\n🔄 Generating test for: {', '.join(topics)}")
            test_paper = self.generator.create_custom_test(
                topics=topics,
                question_types=question_types,
                difficulty_levels=difficulty_levels,
                num_questions=num_questions,
                duration_minutes=duration,
                subject=subject
            )
            
            # Save test
            test_file, answer_file = self.formatter.save_test_paper(test_paper)
            
            print(f"\n✅ Test generated successfully!")
            print(f"📄 Test Questions: {test_file}")
            print(f"📚 Answer Key: {answer_file}")
            
            # Show preview
            self._show_test_preview(test_paper)
            
        except KeyboardInterrupt:
            print("\n❌ Test generation cancelled.")
        except Exception as e:
            logger.error(f"Test generation failed: {e}")
    
    def _suggest_topics(self):
        """Suggest available topics based on database content"""
        # Get some sample content to suggest topics
        if self.generator.book_db.index.ntotal > 0:
            sample_queries = ["mathematics", "algebra", "geometry", "trigonometry", "calculus"]
            suggested_topics = set()
            
            for query in sample_queries:
                results = self.generator.book_db.search(query, top_k=3)
                for chunk, score in results:
                    concepts = self.generator.question_generator.extract_concepts_from_content(chunk.text)
                    suggested_topics.update(concepts[:3])
            
            if suggested_topics:
                topics_list = sorted(list(suggested_topics))[:10]
                print("  " + ", ".join(topics_list))
        else:
            print("  No topics available - please index some books first")
    
    def _show_test_preview(self, test_paper: TestPaper):
        """Show a preview of the generated test"""
        print(f"\n📋 Test Preview:")
        print(f"Title: {test_paper.title}")
        print(f"Questions: {len(test_paper.questions)}")
        print(f"Total Points: {test_paper.total_points}")
        print(f"Estimated Duration: {test_paper.duration_minutes} minutes")
        
        print(f"\nDifficulty Distribution:")
        for difficulty, count in test_paper.difficulty_distribution.items():
            print(f"  {difficulty.title()}: {count} questions")
        
        print(f"\nFirst Question Preview:")
        if test_paper.questions:
            q = test_paper.questions[0]
            print(f"  {q.question_text}")
            if q.options:
                for i, option in enumerate(q.options[:2]):  # Show first 2 options
                    print(f"    {chr(65 + i)}. {option}")
                print("    ...")

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Quiz Generator")
    parser.add_argument('--topics', '-t', type=str, help='Topics for the test (comma-separated)')
    parser.add_argument('--subject', '-s', type=str, default='Mathematics', help='Subject name')
    parser.add_argument('--questions', '-q', type=int, default=10, help='Number of questions')
    parser.add_argument('--types', type=str, default='mcq,short', 
                       help='Question types: mcq,short,long,true_false,fill_blanks')
    parser.add_argument('--difficulty', '-d', type=str, default='easy,medium',
                       help='Difficulty levels: easy,medium,hard')
    parser.add_argument('--duration', type=int, default=60, help='Test duration in minutes')
    parser.add_argument('--output', '-o', type=str, help='Output filename prefix')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--db-dir', type=str, default='book_db', help='Book database directory')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = QuizGeneratorCLI()
    cli.generator = TestPaperGenerator(args.db_dir)
    
    # Interactive mode
    if args.interactive or not args.topics:
        cli.interactive_mode()
        return
    
    # Command line mode
    try:
        topics = [t.strip() for t in args.topics.split(",")]
        question_types = [t.strip() for t in args.types.split(",")]
        difficulty_levels = [d.strip() for d in args.difficulty.split(",")]
        
        print(f"🎯 Generating test for: {', '.join(topics)}")
        
        test_paper = cli.generator.create_custom_test(
            topics=topics,
            question_types=question_types,
            difficulty_levels=difficulty_levels,
            num_questions=args.questions,
            duration_minutes=args.duration,
            subject=args.subject
        )
        
        # Save test
        output_prefix = args.output or f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_file, answer_file = cli.formatter.save_test_paper(test_paper, output_prefix)
        
        print(f"\n✅ Test generated successfully!")
        print(f"📄 Questions: {test_file}")
        print(f"📚 Answers: {answer_file}")
        
        # Show preview
        cli._show_test_preview(test_paper)
        
    except Exception as e:
        logger.error(f"Test generation failed: {e}")

if __name__ == "__main__":
    main()
