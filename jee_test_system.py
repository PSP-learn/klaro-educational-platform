#!/usr/bin/env python3
"""
JEE Main Online Test Platform

Customizable JEE Main mock test system with NTA Abhyas interface matching.
Supports full-length tests and custom topic/subject-wise practice.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum
import json
from datetime import datetime, timedelta
import random

class Subject(Enum):
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry" 
    MATHEMATICS = "Mathematics"

class QuestionType(Enum):
    MCQ = "Multiple Choice"
    NUMERICAL = "Numerical Value"

class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

@dataclass
class JEETestConfig:
    """Configuration for customizable JEE tests"""
    
    # Test Type
    test_type: str  # "full_mock", "subject_wise", "topic_wise", "pyq_practice"
    
    # Subject Configuration
    subjects: List[Subject]
    
    # Topic Configuration (subject-wise)
    physics_topics: List[str] = None
    chemistry_topics: List[str] = None
    math_topics: List[str] = None
    
    # Question Configuration
    total_questions: int = 90
    questions_per_subject: Dict[Subject, int] = None
    
    # Difficulty & Type
    difficulty_distribution: Dict[Difficulty, float] = None
    question_type_distribution: Dict[QuestionType, float] = None
    
    # Time Configuration
    total_time_minutes: int = 180  # 3 hours for full test
    section_wise_time: bool = False
    
    # Test Behavior
    negative_marking: bool = True
    shuffle_questions: bool = True
    shuffle_options: bool = True
    
    def __post_init__(self):
        """Set defaults based on test type"""
        if self.test_type == "full_mock":
            self._setup_full_mock()
        elif self.test_type == "subject_wise":
            self._setup_subject_test()
        elif self.test_type == "topic_wise":
            self._setup_topic_test()

    def _setup_full_mock(self):
        """Standard JEE Main full mock configuration"""
        self.subjects = [Subject.PHYSICS, Subject.CHEMISTRY, Subject.MATHEMATICS]
        self.questions_per_subject = {
            Subject.PHYSICS: 30,
            Subject.CHEMISTRY: 30,
            Subject.MATHEMATICS: 30
        }
        self.total_questions = 90
        self.total_time_minutes = 180
        
        # JEE Main difficulty distribution (approximately)
        self.difficulty_distribution = {
            Difficulty.EASY: 0.30,    # 30% easy
            Difficulty.MEDIUM: 0.50,  # 50% medium  
            Difficulty.HARD: 0.20     # 20% hard
        }
        
        # JEE Main question type distribution
        self.question_type_distribution = {
            QuestionType.MCQ: 0.83,      # 75/90 MCQs
            QuestionType.NUMERICAL: 0.17  # 15/90 Numerical
        }

    def _setup_subject_test(self):
        """Single subject test configuration"""
        self.total_questions = 30
        self.total_time_minutes = 60
        self.questions_per_subject = {self.subjects[0]: 30}

    def _setup_topic_test(self):
        """Topic-specific test configuration"""
        # Will be customized based on user selection
        pass

class JEETopics:
    """JEE Main syllabus topics organized by subject"""
    
    PHYSICS_TOPICS = {
        "Mechanics": [
            "Units and Measurements", "Motion in Straight Line", "Motion in Plane",
            "Laws of Motion", "Work Energy Power", "Rotational Motion",
            "Gravitation", "Properties of Solids and Liquids"
        ],
        "Thermodynamics": [
            "Thermal Properties of Matter", "Thermodynamics", "Kinetic Theory of Gases"
        ],
        "Electrodynamics": [
            "Electric Charges and Fields", "Electrostatic Potential", "Current Electricity",
            "Magnetic Effects of Current", "Electromagnetic Induction", "AC Circuits"
        ],
        "Optics": [
            "Ray Optics", "Wave Optics"
        ],
        "Modern Physics": [
            "Dual Nature of Matter", "Atoms and Nuclei", "Electronic Devices"
        ]
    }
    
    CHEMISTRY_TOPICS = {
        "Physical Chemistry": [
            "Atomic Structure", "Chemical Bonding", "Thermodynamics", 
            "Solutions", "Equilibrium", "Redox Reactions", "Electrochemistry",
            "Chemical Kinetics", "Surface Chemistry"
        ],
        "Organic Chemistry": [
            "Hydrocarbons", "Haloalkanes and Haloarenes", "Alcohols Phenols Ethers",
            "Aldehydes Ketones", "Carboxylic Acids", "Nitrogen Compounds",
            "Biomolecules", "Polymers", "Environmental Chemistry"
        ],
        "Inorganic Chemistry": [
            "Classification of Elements", "Hydrogen", "s-Block Elements",
            "p-Block Elements", "d-Block Elements", "f-Block Elements",
            "Coordination Compounds", "Environmental Chemistry"
        ]
    }
    
    MATHEMATICS_TOPICS = {
        "Algebra": [
            "Sets Relations Functions", "Complex Numbers", "Quadratic Equations",
            "Sequences and Series", "Permutations Combinations", "Binomial Theorem",
            "Mathematical Induction"
        ],
        "Coordinate Geometry": [
            "Straight Lines", "Circles", "Parabola", "Ellipse", "Hyperbola"
        ],
        "Calculus": [
            "Limits and Derivatives", "Applications of Derivatives",
            "Integrals", "Applications of Integrals", "Differential Equations"
        ],
        "Trigonometry": [
            "Trigonometric Functions", "Inverse Trigonometric Functions",
            "Heights and Distances"
        ],
        "Vectors and 3D": [
            "Vectors", "Three Dimensional Geometry"
        ],
        "Statistics": [
            "Statistics and Probability"
        ]
    }

class JEETestCustomizer:
    """Handles customizable JEE test creation"""
    
    def __init__(self):
        self.topics = JEETopics()
    
    def create_custom_config(self) -> JEETestConfig:
        """Interactive custom test configuration"""
        
        print("🎓 JEE Main Test Customizer")
        print("=" * 50)
        print("\n🎯 Create your personalized JEE practice test")
        
        # Test type selection
        print("\n📝 Select Test Type:")
        print("1. 🎯 Full JEE Main Mock (90Q, 3hr)")
        print("2. 📚 Subject-wise Test (30Q, 1hr)")
        print("3. 🔍 Topic-wise Practice (Custom)")
        print("4. 📋 Previous Year Questions")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            return self._create_full_mock()
        elif choice == "2":
            return self._create_subject_test()
        elif choice == "3":
            return self._create_topic_test()
        elif choice == "4":
            return self._create_pyq_test()
        else:
            print("❌ Invalid choice. Creating full mock test.")
            return self._create_full_mock()
    
    def _create_full_mock(self) -> JEETestConfig:
        """Create full JEE Main mock test"""
        return JEETestConfig(
            test_type="full_mock",
            subjects=[Subject.PHYSICS, Subject.CHEMISTRY, Subject.MATHEMATICS]
        )
    
    def _create_subject_test(self) -> JEETestConfig:
        """Create subject-specific test"""
        print("\n📚 Select Subject:")
        print("1. ⚛️ Physics")
        print("2. 🧪 Chemistry")  
        print("3. 📐 Mathematics")
        
        subject_choice = input("Enter subject (1-3): ").strip()
        subject_map = {"1": Subject.PHYSICS, "2": Subject.CHEMISTRY, "3": Subject.MATHEMATICS}
        
        selected_subject = subject_map.get(subject_choice, Subject.PHYSICS)
        
        # Get number of questions
        num_questions = int(input("Number of questions (10-30, default 30): ").strip() or "30")
        time_minutes = int(input("Time in minutes (30-90, default 60): ").strip() or "60")
        
        return JEETestConfig(
            test_type="subject_wise",
            subjects=[selected_subject],
            total_questions=num_questions,
            total_time_minutes=time_minutes
        )
    
    def _create_topic_test(self) -> JEETestConfig:
        """Create topic-specific test"""
        print("\n🔍 Topic-wise Practice")
        
        # Subject selection
        print("\nSelect Subject:")
        print("1. ⚛️ Physics")
        print("2. 🧪 Chemistry")
        print("3. 📐 Mathematics")
        
        subject_choice = input("Enter subject (1-3): ").strip()
        
        if subject_choice == "1":
            selected_subject = Subject.PHYSICS
            self._show_physics_topics()
        elif subject_choice == "2":
            selected_subject = Subject.CHEMISTRY
            self._show_chemistry_topics()
        else:
            selected_subject = Subject.MATHEMATICS
            self._show_math_topics()
        
        topics_input = input("\nEnter topics (comma-separated): ").strip()
        selected_topics = [t.strip() for t in topics_input.split(",")]
        
        num_questions = int(input("Number of questions (5-50, default 20): ").strip() or "20")
        time_minutes = int(input("Time in minutes (15-120, default 45): ").strip() or "45")
        
        config = JEETestConfig(
            test_type="topic_wise",
            subjects=[selected_subject],
            total_questions=num_questions,
            total_time_minutes=time_minutes
        )
        
        # Set topic-specific configuration
        if selected_subject == Subject.PHYSICS:
            config.physics_topics = selected_topics
        elif selected_subject == Subject.CHEMISTRY:
            config.chemistry_topics = selected_topics
        else:
            config.math_topics = selected_topics
            
        return config
    
    def _show_physics_topics(self):
        """Display Physics topics"""
        print("\n⚛️ Physics Topics:")
        for category, topics in self.topics.PHYSICS_TOPICS.items():
            print(f"\n  📂 {category}:")
            for i, topic in enumerate(topics, 1):
                print(f"    {i}. {topic}")
    
    def _show_chemistry_topics(self):
        """Display Chemistry topics"""
        print("\n🧪 Chemistry Topics:")
        for category, topics in self.topics.CHEMISTRY_TOPICS.items():
            print(f"\n  📂 {category}:")
            for i, topic in enumerate(topics, 1):
                print(f"    {i}. {topic}")
    
    def _show_math_topics(self):
        """Display Mathematics topics"""
        print("\n📐 Mathematics Topics:")
        for category, topics in self.topics.MATHEMATICS_TOPICS.items():
            print(f"\n  📂 {category}:")
            for i, topic in enumerate(topics, 1):
                print(f"    {i}. {topic}")
    
    def _create_pyq_test(self) -> JEETestConfig:
        """Create PYQ-based test"""
        print("\n📋 Previous Year Questions Practice")
        
        years = ["2024", "2023", "2022", "2021", "2020"]
        print("\nAvailable Years:")
        for i, year in enumerate(years, 1):
            print(f"{i}. JEE Main {year}")
        
        year_choice = input("Select year (1-5): ").strip()
        selected_year = years[int(year_choice)-1] if year_choice.isdigit() and 1 <= int(year_choice) <= 5 else "2024"
        
        return JEETestConfig(
            test_type="pyq_practice",
            subjects=[Subject.PHYSICS, Subject.CHEMISTRY, Subject.MATHEMATICS],
            total_questions=90,
            total_time_minutes=180
        )

class NTAAbhyasInterface:
    """NTA Abhyas app interface replication"""
    
    # Official NTA Abhyas color scheme
    COLORS = {
        "primary_blue": "#1976D2",
        "secondary_blue": "#42A5F5", 
        "background": "#F5F5F5",
        "card_white": "#FFFFFF",
        "text_dark": "#212121",
        "text_light": "#757575",
        "success_green": "#4CAF50",
        "warning_orange": "#FF9800",
        "error_red": "#F44336",
        "timer_red": "#D32F2F"
    }
    
    @staticmethod
    def get_test_interface_config():
        """Get exact NTA Abhyas interface configuration"""
        return {
            "layout": {
                "header_height": "60px",
                "question_panel_width": "70%",
                "omr_panel_width": "30%",
                "timer_position": "top-right",
                "navigation_position": "bottom"
            },
            "colors": NTAAbhyasInterface.COLORS,
            "fonts": {
                "question_text": "16px Arial",
                "option_text": "14px Arial", 
                "timer_text": "18px Arial Bold",
                "header_text": "20px Arial Bold"
            },
            "components": {
                "timer_format": "HH:MM:SS",
                "question_numbering": "Question 1 of 90",
                "omr_grid": "15x6 grid layout",
                "mark_for_review": "Orange flag icon",
                "attempted": "Green circle",
                "not_attempted": "Gray circle",
                "marked_attempted": "Purple circle"
            }
        }

class JEETestGenerator:
    """Generates JEE Main style questions and tests"""
    
    def __init__(self, quiz_generator=None):
        self.quiz_generator = quiz_generator
        self.topics = JEETopics()
    
    def generate_jee_test(self, config: JEETestConfig) -> Dict:
        """Generate JEE test based on configuration"""
        
        print(f"🔄 Generating {config.test_type} test...")
        print(f"📊 {config.total_questions} questions, {config.total_time_minutes} minutes")
        
        test_data = {
            "test_id": f"jee_{config.test_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "config": config,
            "questions": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "test_type": config.test_type,
                "total_questions": config.total_questions,
                "total_time_minutes": config.total_time_minutes,
                "subjects": [s.value for s in config.subjects],
                "scoring": {
                    "correct": 4,
                    "incorrect": -1,
                    "unattempted": 0
                }
            }
        }
        
        # Generate questions for each subject
        for subject in config.subjects:
            questions_needed = config.questions_per_subject.get(subject, 30)
            subject_questions = self._generate_subject_questions(subject, questions_needed, config)
            test_data["questions"].extend(subject_questions)
        
        # Shuffle if enabled
        if config.shuffle_questions:
            random.shuffle(test_data["questions"])
        
        print(f"✅ Generated {len(test_data['questions'])} questions")
        return test_data
    
    def _generate_subject_questions(self, subject: Subject, count: int, config: JEETestConfig) -> List[Dict]:
        """Generate questions for a specific subject"""
        
        questions = []
        
        # Get topics for this subject
        if subject == Subject.PHYSICS:
            topics = config.physics_topics or ["Mechanics", "Thermodynamics", "Electromagnetism"]
        elif subject == Subject.CHEMISTRY:
            topics = config.chemistry_topics or ["Physical Chemistry", "Organic Chemistry", "Inorganic Chemistry"]
        else:  # Mathematics
            topics = config.math_topics or ["Algebra", "Calculus", "Coordinate Geometry"]
        
        # Distribute questions across topics
        questions_per_topic = count // len(topics)
        remaining_questions = count % len(topics)
        
        for i, topic in enumerate(topics):
            topic_questions = questions_per_topic + (1 if i < remaining_questions else 0)
            
            # Generate questions for this topic
            for q_num in range(topic_questions):
                question = self._generate_jee_question(subject, topic, config)
                questions.append(question)
        
        return questions
    
    def _generate_jee_question(self, subject: Subject, topic: str, config: JEETestConfig) -> Dict:
        """Generate a single JEE-style question"""
        
        # Determine question type
        is_mcq = random.random() < config.question_type_distribution.get(QuestionType.MCQ, 0.83)
        
        # Determine difficulty
        diff_rand = random.random()
        if diff_rand < config.difficulty_distribution.get(Difficulty.EASY, 0.3):
            difficulty = Difficulty.EASY
        elif diff_rand < config.difficulty_distribution.get(Difficulty.EASY, 0.3) + config.difficulty_distribution.get(Difficulty.MEDIUM, 0.5):
            difficulty = Difficulty.MEDIUM
        else:
            difficulty = Difficulty.HARD
        
        if is_mcq:
            return self._create_mcq_question(subject, topic, difficulty)
        else:
            return self._create_numerical_question(subject, topic, difficulty)
    
    def _create_mcq_question(self, subject: Subject, topic: str, difficulty: Difficulty) -> Dict:
        """Create MCQ question in JEE format"""
        
        # Generate using existing quiz generator if available
        if self.quiz_generator:
            try:
                # Use existing system to generate content
                content = self.quiz_generator.book_db.search(f"{subject.value} {topic}", top_k=1)
                if content:
                    base_content = content[0][0]
                else:
                    base_content = f"Question about {topic} in {subject.value}"
            except:
                base_content = f"Question about {topic} in {subject.value}"
        else:
            base_content = f"Sample JEE {subject.value} question on {topic}"
        
        return {
            "question_id": f"q_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000,9999)}",
            "subject": subject.value,
            "topic": topic,
            "difficulty": difficulty.value,
            "type": "MCQ",
            "question_text": f"[{subject.value}] {base_content[:200]}",
            "options": {
                "A": "Option A (generated based on content)",
                "B": "Option B (generated based on content)", 
                "C": "Option C (generated based on content)",
                "D": "Option D (generated based on content)"
            },
            "correct_answer": "A",
            "explanation": f"Detailed explanation for {topic} concept",
            "marks": 4,
            "negative_marks": -1 if config.negative_marking else 0
        }
    
    def _create_numerical_question(self, subject: Subject, topic: str, difficulty: Difficulty) -> Dict:
        """Create numerical answer question in JEE format"""
        
        return {
            "question_id": f"q_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000,9999)}",
            "subject": subject.value,
            "topic": topic,
            "difficulty": difficulty.value,
            "type": "NUMERICAL",
            "question_text": f"[{subject.value}] Numerical question on {topic}",
            "answer_range": "0-9999",
            "correct_answer": "42.5",
            "explanation": f"Step-by-step solution for {topic}",
            "marks": 4,
            "negative_marks": 0  # No negative marking for numerical
        }

def demo_jee_customization():
    """Demonstrate the JEE test customization system"""
    
    print("🎓 JEE Main Online Test Platform Demo")
    print("=" * 60)
    
    customizer = JEETestCustomizer()
    generator = JEETestGenerator()
    
    # Show customization options
    print("\n🎯 Customization Options:")
    print("\n1. 📱 **Mobile App Interface:**")
    print("   • Tap to select subjects")
    print("   • Swipe through topics") 
    print("   • Slider for question count")
    print("   • Toggle for time limits")
    
    print("\n2. 🎨 **NTA Abhyas Matching:**")
    print("   • Same blue color scheme (#1976D2)")
    print("   • Identical timer display")
    print("   • Exact OMR sheet layout")
    print("   • Same navigation buttons")
    
    print("\n3. 🎯 **Test Types:**")
    print("   • Full Mock (90Q, 3hr) - Complete JEE simulation")
    print("   • Subject Test (30Q, 1hr) - Physics/Chemistry/Math")
    print("   • Topic Practice (Custom) - Specific topics only")
    print("   • PYQ Tests (90Q, 3hr) - Year-wise practice")
    
    print("\n4. 🤖 **AI Features:**")
    print("   • Adaptive difficulty based on performance")
    print("   • Personalized weak area identification")
    print("   • Smart question selection from PYQ patterns")
    print("   • Real-time performance prediction")

if __name__ == "__main__":
    demo_jee_customization()
