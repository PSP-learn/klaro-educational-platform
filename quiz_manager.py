#!/usr/bin/env python3
"""
Comprehensive Quiz Manager

Master interface for creating, managing, and customizing test papers from your textbook collection.
Combines all quiz generation capabilities with an easy-to-use interface.
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from book_search import BookVectorDB
from smart_quiz_generator import SmartTestGenerator

class QuizPresets:
    """Predefined quiz templates for different subjects and levels"""
    
    @staticmethod
    def get_mathematics_presets() -> Dict[str, Dict]:
        """Mathematics quiz presets based on NCERT curriculum"""
        return {
            'class_10_algebra_basic': {
                'name': 'Class 10 - Algebra Basics',
                'description': 'Fundamental algebraic concepts',
                'topics': ['polynomials', 'linear equations', 'quadratic equations'],
                'types': ['mcq', 'short'],
                'difficulty': ['easy', 'medium'],
                'questions': 15,
                'duration': 45
            },
            'class_10_algebra_advanced': {
                'name': 'Class 10 - Advanced Algebra',
                'description': 'Complex algebraic problems and applications',
                'topics': ['quadratic equations', 'arithmetic progressions', 'factorization'],
                'types': ['short', 'long'],
                'difficulty': ['medium', 'hard'],
                'questions': 12,
                'duration': 90
            },
            'class_10_geometry': {
                'name': 'Class 10 - Geometry',
                'description': 'Triangles, circles, and coordinate geometry',
                'topics': ['triangles', 'circles', 'coordinate geometry', 'areas'],
                'types': ['mcq', 'short', 'long'],
                'difficulty': ['easy', 'medium'],
                'questions': 15,
                'duration': 75
            },
            'class_10_trigonometry': {
                'name': 'Class 10 - Trigonometry',
                'description': 'Trigonometric ratios and applications',
                'topics': ['trigonometry', 'trigonometric ratios', 'applications of trigonometry'],
                'types': ['mcq', 'short'],
                'difficulty': ['medium', 'hard'],
                'questions': 10,
                'duration': 60
            },
            'class_10_statistics': {
                'name': 'Class 10 - Statistics',
                'description': 'Data handling and statistical measures',
                'topics': ['statistics', 'mean', 'median', 'mode', 'probability'],
                'types': ['mcq', 'short'],
                'difficulty': ['easy', 'medium'],
                'questions': 12,
                'duration': 45
            },
            'class_10_comprehensive': {
                'name': 'Class 10 - Comprehensive Test',
                'description': 'Complete syllabus coverage',
                'topics': ['algebra', 'geometry', 'trigonometry', 'statistics', 'coordinate geometry'],
                'types': ['mcq', 'short', 'long'],
                'difficulty': ['easy', 'medium', 'hard'],
                'questions': 25,
                'duration': 180
            },
            'quick_revision': {
                'name': 'Quick Revision Test',
                'description': 'Fast review of key concepts',
                'topics': ['quadratic equations', 'triangles', 'trigonometry'],
                'types': ['mcq'],
                'difficulty': ['easy'],
                'questions': 20,
                'duration': 30
            },
            'problem_solving': {
                'name': 'Problem Solving Practice',
                'description': 'Focus on application and problem-solving',
                'topics': ['word problems', 'applications', 'real life mathematics'],
                'types': ['short', 'long'],
                'difficulty': ['medium', 'hard'],
                'questions': 8,
                'duration': 120
            }
        }

class QuizManager:
    """Main quiz management interface"""
    
    def __init__(self, db_dir: str = "book_db"):
        self.db_dir = db_dir
        self.generator = SmartTestGenerator(db_dir)
        self.presets = QuizPresets.get_mathematics_presets()
        self.output_dir = Path("generated_tests")
        self.output_dir.mkdir(exist_ok=True)
    
    def list_presets(self):
        """List available quiz presets"""
        print("\\n📚 Available Quiz Presets:")
        print("=" * 60)
        
        for key, preset in self.presets.items():
            print(f"\\n🎯 {key}")
            print(f"   📖 {preset['name']}")
            print(f"   📝 {preset['description']}")
            print(f"   📋 Topics: {', '.join(preset['topics'])}")
            print(f"   ❓ Questions: {preset['questions']} ({preset['duration']} min)")
            print(f"   📊 Types: {', '.join(preset['types'])}")
            print(f"   ⚡ Difficulty: {', '.join(preset['difficulty'])}")
    
    def create_from_preset(self, preset_name: str, output_prefix: str = None, generate_pdf: bool = False) -> Optional[Tuple[str, str]]:
        """Create quiz from preset"""
        if preset_name not in self.presets:
            print(f"❌ Preset '{preset_name}' not found!")
            print(f"Available presets: {', '.join(self.presets.keys())}")
            return None
        
        preset = self.presets[preset_name]
        
        print(f"🎯 Creating quiz: {preset['name']}")
        print(f"📝 {preset['description']}")
        
        try:
            test_data = self.generator.create_test(
                topics=preset['topics'],
                num_questions=preset['questions'],
                question_types=preset['types'],
                difficulty_levels=preset['difficulty'],
                subject="Mathematics",
                mode='mixed',
                render='auto'
            )
            
            output_prefix = output_prefix or f"preset_{preset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            test_file, answer_file = self.generator.save_test(test_data, output_prefix)
            
            print(f"\n✅ Quiz created successfully!")
            print(f"📄 Questions: {test_file}")
            print(f"📚 Answers: {answer_file}")
            
            if generate_pdf:
                qpdf, apdf = self.generator.save_test_pdf(test_data, output_prefix)
                print(f"📄 PDF Questions: {qpdf}")
                print(f"📚 PDF Answers: {apdf}")
            
            return test_file, answer_file
            
        except Exception as e:
            print(f"❌ Failed to create quiz: {e}")
            return None
    
    def create_custom_quiz(self, generate_pdf: bool = False):
        """Interactive custom quiz creation"""
        print("\n🎨 Custom Quiz Creator")
        print("=" * 50)
        
        try:
            # Get basic info
            title = input("Quiz title (optional): ").strip()
            subject = input("Subject (default: Mathematics): ").strip() or "Mathematics"
            
            # Suggest topics based on database
            print("\nSuggested topics from your textbooks:")
            self._suggest_topics_from_db()
            
            topics_input = input("\nEnter topics (comma-separated): ").strip()
            if not topics_input:
                print("❌ No topics specified!")
                return None
            
            topics = [t.strip() for t in topics_input.split(",")]
            
            # Question configuration
            print("\n📋 Question Configuration:")
            print("Available types: mcq, short, long")
            types_input = input("Question types (default: mcq,short): ").strip() or "mcq,short"
            question_types = [t.strip() for t in types_input.split(",")]
            
            print("\nDifficulty levels: easy, medium, hard")
            diff_input = input("Difficulty levels (default: easy,medium): ").strip() or "easy,medium"
            difficulty_levels = [d.strip() for d in diff_input.split(",")]
            
            num_questions = int(input("Number of questions (default: 10): ").strip() or "10")
            duration = int(input("Duration in minutes (default: auto-calculate): ").strip() or str(num_questions * 3))
            
            # Generate quiz
            print(f"\n🔄 Generating custom quiz...")
            test_data = self.generator.create_test(
                topics=topics,
                num_questions=num_questions,
                question_types=question_types,
                difficulty_levels=difficulty_levels,
                subject=subject,
                mode=args.mode if hasattr(args, 'mode') else 'mixed',
                scope_filter=args.scope if hasattr(args, 'scope') else None,
                render=args.render if hasattr(args, 'render') else 'auto',
                books_dir=args.books_dir if hasattr(args, 'books_dir') else None
            )
            
            # Save quiz
            safe_title = title.replace(' ', '_').lower() if title else 'custom_quiz'
            output_prefix = f"{safe_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            test_file, answer_file = self.generator.save_test(test_data, output_prefix)
            
            print(f"\n🎉 Custom quiz created!")
            print(f"📄 Questions: {test_file}")
            print(f"📚 Answers: {answer_file}")
            
            if generate_pdf:
                qpdf, apdf = self.generator.save_test_pdf(test_data, output_prefix)
                print(f"📄 PDF Questions: {qpdf}")
                print(f"📚 PDF Answers: {apdf}")
            
            return test_file, answer_file
            
        except KeyboardInterrupt:
            print("\\n❌ Quiz creation cancelled")
            return None
        except Exception as e:
            print(f"❌ Quiz creation failed: {e}")
            return None
    
    def _suggest_topics_from_db(self):
        """Suggest topics based on database content"""
        common_topics = [
            "quadratic equations", "polynomials", "trigonometry", "geometry", 
            "coordinate geometry", "statistics", "probability", "circles", 
            "triangles", "linear equations", "arithmetic progressions"
        ]
        
        available_topics = []
        for topic in common_topics:
            results = self.generator.book_db.search(topic, top_k=1)
            if results and results[0][1] > 0.4:  # Good relevance score
                available_topics.append(topic)
        
        if available_topics:
            print("  " + ", ".join(available_topics))
        else:
            print("  No specific topics found - try general terms")
    
    def list_recent_quizzes(self, limit: int = 10):
        """List recently generated quizzes"""
        if not self.output_dir.exists():
            print("No quizzes generated yet.")
            return
        
        # Find all quiz files
        question_files = list(self.output_dir.glob("*_questions.txt"))
        
        if not question_files:
            print("No quizzes found.")
            return
        
        # Sort by creation time
        question_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        print(f"\\n📚 Recent Quizzes (last {min(limit, len(question_files))}):")
        print("=" * 60)
        
        for i, quiz_file in enumerate(question_files[:limit], 1):
            quiz_name = quiz_file.stem.replace('_questions', '')
            metadata_file = quiz_file.parent / f"{quiz_name}_metadata.json"
            
            # Try to load metadata
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    print(f"\\n{i}. {metadata.get('title', quiz_name)}")
                    print(f"   📅 Created: {metadata.get('created_at', 'Unknown')[:16]}")
                    print(f"   📋 Questions: {metadata.get('total_questions', 'Unknown')}")
                    print(f"   💯 Points: {metadata.get('total_points', 'Unknown')}")
                    print(f"   📂 File: {quiz_file.name}")
                    
                except Exception:
                    print(f"\\n{i}. {quiz_name}")
                    print(f"   📂 File: {quiz_file.name}")
            else:
                print(f"\\n{i}. {quiz_name}")
                print(f"   📂 File: {quiz_file.name}")

def main():
    parser = argparse.ArgumentParser(description="Comprehensive Quiz Manager")
    parser.add_argument('--preset', '-p', type=str, help='Create quiz from preset')
    parser.add_argument('--list-presets', action='store_true', help='List available presets')
    parser.add_argument('--custom', '-c', action='store_true', help='Create custom quiz (interactive)')
    parser.add_argument('--topics', '-t', type=str, help='Quick custom topics (comma-separated)')
    parser.add_argument('--recent', '-r', action='store_true', help='Show recent quizzes')
    parser.add_argument('--output', '-o', type=str, help='Output filename prefix')
    parser.add_argument('--questions', '-q', type=int, default=10, help='Number of questions (for quick mode)')
    parser.add_argument('--pdf', action='store_true', help='Also generate PDF outputs')
    parser.add_argument('--mode', type=str, default='mixed', choices=['mixed','source'], help='Question generation mode')
    parser.add_argument('--scope', type=str, default=None, help='Restrict to files whose path contains this substring (e.g., class_10)')
    parser.add_argument('--render', type=str, default='auto', choices=['auto','image','text'], help='Rendering for source mode questions')
    parser.add_argument('--books-dir', type=str, default=None, help='Base directory to locate source PDFs for image rendering')
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = QuizManager()
    
    if args.list_presets:
        manager.list_presets()
        return
    
    if args.recent:
        manager.list_recent_quizzes()
        return
    
    if args.preset:
        manager.create_from_preset(args.preset, args.output, generate_pdf=args.pdf)
        return
    
    if args.custom:
        manager.create_custom_quiz(generate_pdf=args.pdf)
        return
    
    if args.topics:
        # Quick mode - generate quiz directly from topics
        print(f"🚀 Quick Quiz Generation")
        topics = [t.strip() for t in args.topics.split(',')]
        
        try:
            test_data = manager.generator.create_test(
                topics=topics,
                num_questions=args.questions
            )
            
            output_prefix = args.output or f"quick_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            test_file, answer_file = manager.generator.save_test(test_data, output_prefix)
            
            if args.pdf:
                qpdf, apdf = manager.generator.save_test_pdf(test_data, output_prefix)
                print(f"📄 PDF Questions: {qpdf}")
                print(f"📚 PDF Answers: {apdf}")
            
            print(f"\n✅ Quick quiz created!")
            print(f"📄 Questions: {test_file}")
            print(f"📚 Answers: {answer_file}")
            
        except Exception as e:
            print(f"❌ Quick quiz failed: {e}")
        return
    
    # Default: show help and options
    print("\\n🎯 Quiz Manager - Your Test Creation Assistant")
    print("=" * 60)
    print("\\nWhat would you like to do?")
    print("\\n1. 📚 Use a preset quiz (--preset or --list-presets)")
    print("2. 🎨 Create custom quiz (--custom)")
    print("3. 🚀 Quick quiz from topics (--topics 'topic1,topic2')")
    print("4. 📋 View recent quizzes (--recent)")
    print("\\nExamples:")
    print("  python3 quiz_manager.py --list-presets")
    print("  python3 quiz_manager.py --preset class_10_algebra_basic")
    print("  python3 quiz_manager.py --custom")
    print("  python3 quiz_manager.py --topics 'quadratic equations,trigonometry' --questions 8")
    print("\\nFor detailed help: python3 quiz_manager.py --help")

if __name__ == "__main__":
    main()
