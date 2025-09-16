#!/usr/bin/env python3
"""
JEE Main Online Test Module

Additional feature for Klaro Educational Platform.
Provides live online JEE Main mock tests with NTA Abhyas interface matching.

This works alongside:
- Existing PDF quiz generator 
- Textbook library system
- Future doubt solving assistant
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from enum import Enum
import json
import random
from datetime import datetime, timedelta

class JEESubject(Enum):
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    MATHEMATICS = "Mathematics"

class JEEQuestionType(Enum):
    MCQ = "MCQ"
    NUMERICAL = "Numerical"

@dataclass
class JEETestConfig:
    """Customizable JEE test configuration"""
    
    # Test Customization
    test_name: str
    test_type: str  # "full_mock", "subject_practice", "topic_practice", "pyq_test"
    
    # Subject & Topic Selection
    subjects: List[str]
    selected_topics: Dict[str, List[str]] = None
    
    # Question Distribution (JEE Main 2024 Format)
    total_questions: int = 75  # Updated to current format
    questions_per_subject: Dict[str, int] = None
    
    # Time Configuration  
    total_time_minutes: int = 180  # Still 3 hours
    section_wise_timing: bool = False
    
    # JEE Specific Settings (Current Format)
    negative_marking: bool = True
    mcq_questions_per_subject: int = 20  # 20 MCQs per subject
    numerical_questions_per_subject: int = 5  # 5 numerical per subject
    total_mcq_questions: int = 60  # 20 × 3 subjects
    total_numerical_questions: int = 15  # 5 × 3 subjects
    
    # Interface Settings
    nta_abhyas_mode: bool = True
    show_calculator: bool = True
    allow_review_marking: bool = True

class JEESyllabus:
    """Complete JEE Main syllabus with topics"""
    
    SUBJECTS = {
        "Physics": {
            "Mechanics": [
                "Units and Measurements", "Motion in Straight Line", "Motion in Plane",
                "Laws of Motion", "Work Energy Power", "Rotational Motion", 
                "Gravitation", "Properties of Matter"
            ],
            "Heat & Thermodynamics": [
                "Thermal Properties", "Thermodynamics", "Kinetic Theory"
            ],
            "Waves & Oscillations": [
                "Oscillations", "Waves", "Sound"
            ],
            "Electricity & Magnetism": [
                "Electric Charges", "Electric Potential", "Current Electricity",
                "Magnetic Effects", "Electromagnetic Induction", "AC Circuits"
            ],
            "Optics": [
                "Ray Optics", "Wave Optics"
            ],
            "Modern Physics": [
                "Dual Nature", "Atoms", "Nuclei", "Electronic Devices"
            ]
        },
        
        "Chemistry": {
            "Physical Chemistry": [
                "Atomic Structure", "Chemical Bonding", "States of Matter",
                "Thermodynamics", "Equilibrium", "Redox Reactions", 
                "Hydrogen", "Solutions", "Electrochemistry", "Chemical Kinetics"
            ],
            "Inorganic Chemistry": [
                "Classification of Elements", "s-Block Elements", "p-Block Elements",
                "d-Block Elements", "f-Block Elements", "Coordination Compounds",
                "Environmental Chemistry"
            ],
            "Organic Chemistry": [
                "Basic Principles", "Hydrocarbons", "Haloalkanes", 
                "Alcohols Phenols Ethers", "Aldehydes Ketones", "Carboxylic Acids",
                "Nitrogen Compounds", "Biomolecules", "Polymers"
            ]
        },
        
        "Mathematics": {
            "Algebra": [
                "Sets Relations Functions", "Complex Numbers", "Quadratic Equations",
                "Sequences Series", "Permutations Combinations", "Binomial Theorem",
                "Mathematical Induction", "Matrices Determinants"
            ],
            "Coordinate Geometry": [
                "Straight Lines", "Circles", "Parabola", "Ellipse", "Hyperbola"
            ],
            "Calculus": [
                "Limits Continuity", "Differentiation", "Applications of Derivatives",
                "Integration", "Applications of Integrals", "Differential Equations"
            ],
            "Trigonometry": [
                "Trigonometric Functions", "Inverse Trigonometric Functions",
                "Solutions of Triangles"
            ],
            "Vector & 3D Geometry": [
                "Vectors", "Three Dimensional Geometry"
            ],
            "Statistics & Probability": [
                "Statistics", "Probability"
            ]
        }
    }

class JEEOnlineTest:
    """JEE Main online test system with NTA Abhyas interface"""
    
    def __init__(self, quiz_generator=None):
        """Initialize with optional connection to existing quiz generator"""
        self.quiz_generator = quiz_generator
        self.syllabus = JEESyllabus()
        
    def create_test_interface_config(self, config: JEETestConfig) -> Dict:
        """Create NTA Abhyas matching interface configuration"""
        
        return {
            "test_info": {
                "test_id": f"jee_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "test_name": config.test_name,
                "total_questions": config.total_questions,
                "total_time": config.total_time_minutes,
                "subjects": config.subjects,
                "marking_scheme": {
                    "correct": "+4",
                    "incorrect": "-1" if config.negative_marking else "0",
                    "unattempted": "0"
                },
                "instructions": [
                    "Each subject (Physics, Chemistry, Mathematics) contains 20 MCQ (+4/−1) and 5 Numerical (+4/0).",
                    "Numerical answers are evaluated with appropriate rounding based on the specified format.",
                    "Mark for review is available; ensure you submit before time ends."
                ]
            },
            
            "nta_abhyas_interface": {
                "colors": {
                    "primary": "#1976D2",        # NTA Blue
                    "secondary": "#42A5F5",      # Light Blue
                    "background": "#F5F5F5",     # Light Gray
                    "paper": "#FFFFFF",          # White
                    "timer": "#D32F2F",          # Red
                    "success": "#4CAF50",        # Green
                    "warning": "#FF9800",        # Orange
                    "text": "#212121"            # Dark Gray
                },
                
                "layout": {
                    "header_height": "64px",
                    "question_area": "65%",
                    "omr_area": "35%",
                    "timer_position": "top-right",
                    "subject_tabs": "top-center",
                    "navigation": "bottom"
                },
                
                "components": {
                    "timer_format": "02:59:45",
                    "question_counter": "Question 15 of 90",
                    "omr_status": {
                        "answered": "🟢 Green circle",
                        "marked": "🟠 Orange flag", 
                        "marked_answered": "🟣 Purple circle",
                        "not_answered": "⚪ Gray circle"
                    },
                    "calculator": config.show_calculator,
                    "mark_for_review": config.allow_review_marking
                }
            },
            
            "test_sections": self._create_test_sections(config),
            "navigation_rules": {
                "can_skip": True,
                "can_go_back": True,
                "auto_submit": True,
                "warn_before_submit": True
            }
        }
    
    def _create_test_sections(self, config: JEETestConfig) -> List[Dict]:
        """Create test sections based on configuration"""
        
        sections = []
        
        if config.test_type == "full_mock":
            # JEE Main 2024 Format: 75 questions total
            sections = [
                {
                    "section_id": "physics",
                    "name": "Physics",
                    "questions": 25,  # 20 MCQ + 5 Numerical
                    "mcq_questions": 20,
                    "numerical_questions": 5,
                    "time_minutes": 60,
                    "color": "#E3F2FD"
                },
                {
                    "section_id": "chemistry", 
                    "name": "Chemistry",
                    "questions": 25,  # 20 MCQ + 5 Numerical
                    "mcq_questions": 20,
                    "numerical_questions": 5,
                    "time_minutes": 60,
                    "color": "#E8F5E8"
                },
                {
                    "section_id": "mathematics",
                    "name": "Mathematics", 
                    "questions": 25,  # 20 MCQ + 5 Numerical
                    "mcq_questions": 20,
                    "numerical_questions": 5,
                    "time_minutes": 60,
                    "color": "#FFF3E0"
                }
            ]
        
        elif config.test_type == "subject_practice":
            # Single subject practice
            subject = config.subjects[0]
            sections = [{
                "section_id": subject.lower(),
                "name": subject,
                "questions": config.total_questions,
                "time_minutes": config.total_time_minutes,
                "color": "#E3F2FD"
            }]
        
        elif config.test_type == "topic_practice":
            # Topic-specific practice
            sections = [{
                "section_id": "practice",
                "name": f"{config.subjects[0]} Practice",
                "questions": config.total_questions,
                "time_minutes": config.total_time_minutes,
                "topics": config.selected_topics,
                "color": "#F3E5F5"
            }]
        
        return sections
    
    def generate_jee_questions(self, config: JEETestConfig) -> List[Dict]:
        """Generate JEE-style questions based on configuration"""
        
        print(f"🎯 Generating JEE {config.test_type} test...")
        print(f"📊 {config.total_questions} questions, {config.total_time_minutes} minutes")
        
        questions = []
        
        for subject in config.subjects:
            if config.test_type == "full_mock":
                # JEE Main 2024: 25 questions per subject (20 MCQ + 5 Numerical)
                subject_questions = 25
                mcq_count = 20
                numerical_count = 5
            else:
                subject_questions = config.questions_per_subject.get(subject, 25)
                # For custom tests, maintain 4:1 ratio approximately
                mcq_count = int(subject_questions * 0.8)
                numerical_count = subject_questions - mcq_count
            
            print(f"  📚 {subject}: {mcq_count} MCQ + {numerical_count} Numerical")
            
            # Get topics for this subject
            if config.selected_topics and subject in config.selected_topics:
                topics = config.selected_topics[subject]
            else:
                topics = self._get_default_topics(subject)
            
            # Generate MCQ questions
            mcq_per_topic = mcq_count // len(topics)
            mcq_remaining = mcq_count % len(topics)
            
            for i, topic in enumerate(topics):
                topic_mcqs = mcq_per_topic + (1 if i < mcq_remaining else 0)
                
                for q_num in range(topic_mcqs):
                    question = self._generate_jee_question(subject, topic, config, force_type="MCQ")
                    questions.append(question)
            
            # Generate Numerical questions
            numerical_per_topic = numerical_count // len(topics)
            numerical_remaining = numerical_count % len(topics)
            
            for i, topic in enumerate(topics):
                topic_numericals = numerical_per_topic + (1 if i < numerical_remaining else 0)
                
                for q_num in range(topic_numericals):
                    question = self._generate_jee_question(subject, topic, config, force_type="NUMERICAL")
                    questions.append(question)
        
        # For full mock, keep subject-wise grouping (don't shuffle)
        if config.test_type != "full_mock":
            random.shuffle(questions)
        
        # Number questions sequentially
        for i, question in enumerate(questions, 1):
            question['question_number'] = i
        
        print(f"✅ Generated {len(questions)} JEE-style questions")
        print(f"   📊 MCQs: {len([q for q in questions if q['type'] == 'MCQ'])}")
        print(f"   📊 Numerical: {len([q for q in questions if q['type'] == 'NUMERICAL'])}")
        return questions
    
    def _get_default_topics(self, subject: str) -> List[str]:
        """Get default topics for a subject"""
        subject_topics = self.syllabus.SUBJECTS.get(subject, {})
        all_topics = []
        for category_topics in subject_topics.values():
            all_topics.extend(category_topics[:2])  # Take first 2 from each category
        return all_topics[:5]  # Limit to 5 topics
    
    def _generate_jee_question(self, subject: str, topic: str, config: JEETestConfig, force_type: str = None) -> Dict:
        """Generate single JEE-style question"""
        
        # Determine question type (MCQ vs Numerical)
        if force_type:
            is_mcq = force_type == "MCQ"
        else:
            is_mcq = random.random() < 0.8  # Default 80% MCQ, 20% Numerical
        
        # Determine difficulty based on JEE pattern
        difficulty_rand = random.random()
        if difficulty_rand < 0.30:
            difficulty = "Easy"
        elif difficulty_rand < 0.80:
            difficulty = "Medium" 
        else:
            difficulty = "Hard"
        
        question_id = f"jee_{subject.lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000,9999)}"
        
        if is_mcq:
            return {
                "question_id": question_id,
                "subject": subject,
                "topic": topic,
                "type": "MCQ",
                "difficulty": difficulty,
                "question_text": f"[{subject}] {self._generate_question_text(subject, topic)}",
                "options": {
                    "A": f"Option A for {topic}",
                    "B": f"Option B for {topic}",
                    "C": f"Option C for {topic}", 
                    "D": f"Option D for {topic}"
                },
                "correct_answer": "A",
                "explanation": f"Detailed solution explaining {topic} concept",
                "marks": 4,
                "negative_marks": -1 if config.negative_marking else 0,
                "time_expected": 90  # seconds
            }
        else:
            return {
                "question_id": question_id,
                "subject": subject,
                "topic": topic,
                "type": "NUMERICAL",
                "difficulty": difficulty,
                "question_text": f"[{subject}] Numerical question on {topic}",
                "answer_format": "0000.00",
                "correct_answer": "42.50",
                "explanation": f"Step-by-step numerical solution for {topic}",
                "marks": 4,
                "negative_marks": 0,  # No negative marking for numerical
                "time_expected": 120  # seconds
            }
    
    def _generate_question_text(self, subject: str, topic: str) -> str:
        """Generate realistic JEE question text"""
        
        # If connected to existing quiz generator, use it
        if self.quiz_generator:
            try:
                # Search for content in textbook database
                results = self.quiz_generator.book_db.search(f"{subject} {topic}", top_k=1)
                if results and results[0][1] > 0.4:
                    content = results[0][0]
                    return f"Based on {topic}: {content[:150]}..."
            except:
                pass
        
        # Fallback to template-based generation
        templates = {
            "Physics": [
                f"A particle undergoes motion related to {topic}. Calculate the required parameter.",
                f"In the context of {topic}, find the value of the physical quantity.",
                f"Given the scenario involving {topic}, determine the correct relationship."
            ],
            "Chemistry": [
                f"In the chemical process involving {topic}, calculate the required value.",
                f"For the reaction related to {topic}, find the correct answer.",
                f"Based on the principles of {topic}, determine the outcome."
            ],
            "Mathematics": [
                f"Solve the problem based on {topic} concepts.",
                f"Find the value using {topic} methods.",
                f"Calculate the required parameter using {topic} principles."
            ]
        }
        
        return random.choice(templates.get(subject, templates["Mathematics"]))

class JEETestInterface:
    """NTA Abhyas matching test interface generator"""
    
    def create_test_session(self, config: JEETestConfig, questions: List[Dict]) -> Dict:
        """Create complete test session data for frontend"""
        
        session = {
            "session_id": f"jee_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "test_config": asdict(config),
            "questions": questions,
            "interface_config": self._get_nta_interface_config(),
            "test_state": {
                "current_question": 1,
                "time_remaining": config.total_time_minutes * 60,  # Convert to seconds
                "answers": {},
                "marked_for_review": set(),
                "section_timings": {},
                "start_time": datetime.now().isoformat()
            },
            "omr_sheet": self._create_omr_sheet(questions)
        }
        
        return session
    
    def _get_nta_interface_config(self) -> Dict:
        """NTA Abhyas exact interface configuration"""
        
        return {
            "design": {
                "primary_color": "#1976D2",
                "background_color": "#F5F5F5",
                "paper_color": "#FFFFFF",
                "timer_color": "#D32F2F",
                "success_color": "#4CAF50",
                "warning_color": "#FF9800"
            },
            
            "layout": {
                "split_screen": True,
                "question_panel_width": "70%",
                "omr_panel_width": "30%",
                "header_elements": ["timer", "question_counter", "subject_tabs"],
                "footer_elements": ["previous", "mark_review", "clear", "next", "submit"]
            },
            
            "timer": {
                "format": "HH:MM:SS",
                "warning_at": 300,  # 5 minutes
                "critical_at": 60,  # 1 minute
                "auto_submit": True
            },
            
            "omr_visualization": {
                "grid_layout": "15x5",  # 15 rows, 5 columns for 75 questions
                "status_colors": {
                    "answered": "#4CAF50",
                    "marked": "#FF9800", 
                    "marked_answered": "#9C27B0",
                    "not_answered": "#E0E0E0"
                }
            },
            
            "question_navigation": {
                "show_question_palette": True,
                "click_to_navigate": True,
                "keyboard_shortcuts": {
                    "next": "→",
                    "previous": "←", 
                    "mark": "M",
                    "clear": "C"
                }
            }
        }
    
    def _create_omr_sheet(self, questions: List[Dict]) -> Dict:
        """Create OMR sheet structure for visualization"""
        
        omr_data = {}
        
        for i, question in enumerate(questions, 1):
            omr_data[str(i)] = {
                "question_number": i,
                "subject": question["subject"],
                "type": question["type"],
                "status": "not_answered",
                "selected_answer": None,
                "marked_for_review": False,
                "time_spent": 0
            }
        
        return omr_data

class JEEScoring:
    """JEE Main scoring and analysis system"""
    
    @staticmethod
    def calculate_score(answers: Dict, questions: List[Dict], config: JEETestConfig) -> Dict:
        """Calculate JEE score with detailed analysis
        - MCQ: strict option match (A/B/C/D), apply negative marking if enabled
        - Numerical: numeric normalization with tolerance and rounding based on answer_format when provided
        """
        
        def _decimals_from_format(fmt: str) -> int:
            if not fmt or "." not in fmt:
                return 0
            return len(fmt.split(".")[-1])
        
        def _try_float(s: str) -> Optional[float]:
            try:
                return float(str(s).strip())
            except Exception:
                return None
        
        def _numeric_equal(user: str, correct: str, fmt: Optional[str]) -> bool:
            # Determine decimals from format if available
            decimals = _decimals_from_format(fmt) if fmt else None
            uf = _try_float(user)
            cf = _try_float(correct)
            if uf is None or cf is None:
                # Fallback to exact string match if not parseable
                return (str(user).strip() == str(correct).strip())
            # If decimals specified, round both to that many decimals
            if decimals is not None and decimals > 0:
                uf_rounded = round(uf, decimals)
                cf_rounded = round(cf, decimals)
                return uf_rounded == cf_rounded
            # Else use a small absolute tolerance
            tol = 1e-3
            return abs(uf - cf) <= tol
        
        results = {
            "overall": {"correct": 0, "incorrect": 0, "unattempted": 0, "score": 0},
            "subject_wise": {},
            "difficulty_wise": {"Easy": {"correct": 0, "total": 0}, "Medium": {"correct": 0, "total": 0}, "Hard": {"correct": 0, "total": 0}},
            "time_analysis": {},
            "percentile": 0.0,
            "rank": 0
        }
        
        # Initialize subject-wise results
        for subject in config.subjects:
            results["subject_wise"][subject] = {
                "correct": 0, "incorrect": 0, "unattempted": 0, "score": 0, "total": 0
            }
        
        # Calculate scores
        for question in questions:
            q_id = question["question_id"]
            subject = question["subject"]
            difficulty = question["difficulty"]
            correct_ans = question["correct_answer"]
            
            # Update totals
            results["subject_wise"][subject]["total"] += 1
            results["difficulty_wise"][difficulty]["total"] += 1
            
            if q_id in answers:
                user_answer = answers[q_id]
                is_correct = False
                if question.get("type") == "NUMERICAL":
                    fmt = question.get("answer_format") or question.get("answer_range")
                    is_correct = _numeric_equal(user_answer, correct_ans, fmt)
                else:
                    is_correct = (str(user_answer).strip().upper() == str(correct_ans).strip().upper())
                
                if is_correct:
                    # Correct answer
                    results["overall"]["correct"] += 1
                    results["subject_wise"][subject]["correct"] += 1
                    results["difficulty_wise"][difficulty]["correct"] += 1
                    
                    score_points = question.get("marks", 4)
                    results["overall"]["score"] += score_points
                    results["subject_wise"][subject]["score"] += score_points
                else:
                    # Incorrect answer
                    results["overall"]["incorrect"] += 1
                    results["subject_wise"][subject]["incorrect"] += 1
                    
                    negative_points = question.get("negative_marks", -1 if question.get("type") == "MCQ" else 0)
                    results["overall"]["score"] += negative_points
                    results["subject_wise"][subject]["score"] += negative_points
            else:
                # Unattempted
                results["overall"]["unattempted"] += 1
                results["subject_wise"][subject]["unattempted"] += 1
        
        # Calculate percentile (mock calculation)
        total_possible = len(questions) * 4
        percentage = (results["overall"]["score"] / total_possible) * 100 if total_possible else 0
        results["percentile"] = max(0, min(100, percentage + random.uniform(-5, 5)))
        results["rank"] = random.randint(1000, 50000)  # Mock rank
        
        return results

# ================================================================================
# 🎯 Integration with Existing Platform
# ================================================================================

def integrate_jee_with_existing_platform():
    """Show how JEE online tests integrate with existing features"""
    
    print("🔗 JEE Online Tests Integration")
    print("=" * 50)
    print()
    print("📱 Android App Menu:")
    print("├── 🏠 Home Dashboard")
    print("├── 📝 PDF Quiz Generator (EXISTING)")
    print("├── 🎯 JEE Online Tests (NEW)")
    print("├── 📚 Textbook Library (EXISTING)")
    print("├── 📊 Progress Analytics (ENHANCED)")
    print("└── ⚙️ Settings")
    print()
    print("🔄 Shared Components:")
    print("├── 📚 Same textbook database")
    print("├── 🤖 Same AI content generation")
    print("├── 👤 Same user accounts and progress")
    print("├── 📊 Combined analytics dashboard")
    print("└── 🔧 Same CLI for testing and management")
    print()
    print("💡 Users can:")
    print("├── Create PDF tests for offline practice")
    print("├── Take live JEE mocks for exam prep")
    print("├── Track progress across both formats")
    print("└── Use same textbook library for everything")

def demo_customization_options():
    """Demo the JEE test customization options"""
    
    print("\n🎯 JEE Test Customization Demo")
    print("=" * 50)
    
    print("\n📱 Mobile App Interface:")
    print("┌─────────────────────────────┐")
    print("│  🎓 Create JEE Test         │")
    print("├─────────────────────────────┤")
    print("│                             │")
    print("│  📚 Select Type:            │")
    print("│  ○ Full Mock (90Q, 3hr)     │")
    print("│  ● Subject Practice         │")
    print("│  ○ Topic Practice           │")
    print("│  ○ PYQ Test                 │")
    print("│                             │")
    print("│  ⚛️ Subject: Physics        │")
    print("│                             │")
    print("│  🔍 Topics:                 │")
    print("│  ✓ Mechanics               │")
    print("│  ✓ Thermodynamics          │")
    print("│  ○ Optics                  │")
    print("│                             │")
    print("│  ❓ Questions: [20] ━━━━○━━  │")
    print("│  ⏱️ Time: [45 min] ━━━○━━━  │")
    print("│                             │")
    print("│  [Generate Test] 🚀         │")
    print("└─────────────────────────────┘")

if __name__ == "__main__":
    integrate_jee_with_existing_platform()
    demo_customization_options()
    
    print("\n🎉 JEE Online Tests = Perfect Addition!")
    print("✅ Keeps all existing features")
    print("✅ Adds competitive exam preparation") 
    print("✅ Serves wider student market")
    print("✅ Multiple revenue opportunities")
