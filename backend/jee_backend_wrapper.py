#!/usr/bin/env python3
"""
JEE Test System Backend Integration
Wrapper for the main JEE test system to be used by the FastAPI backend.
"""

import sys
import os
from typing import Dict, List, Optional
from dataclasses import asdict

# Add parent directory to path to import the main JEE system
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    # Import with a different name to avoid circular import
    import jee_test_system as jee_main
    JEETestConfig = jee_main.JEETestConfig
    JEETestCustomizer = jee_main.JEETestCustomizer
    JEETestGenerator = jee_main.JEETestGenerator
    Subject = jee_main.Subject
    QuestionType = jee_main.QuestionType
    Difficulty = jee_main.Difficulty
    JEETopics = jee_main.JEETopics
    JEE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: JEE system import failed: {e}")
    JEE_AVAILABLE = False
    
    # Mock classes for when import fails
    class Subject:
        PHYSICS = "Physics"
        CHEMISTRY = "Chemistry"
        MATHEMATICS = "Mathematics"
    
    class JEETestConfig:
        def __init__(self, **kwargs):
            self.test_type = kwargs.get('test_type', 'full_mock')
            
    class JEETestGenerator:
        def __init__(self):
            pass
            
        def generate_jee_test(self, config):
            return {
                "test_id": "mock_test",
                "questions": [],
                "metadata": {"message": "JEE system not available"}
            }

class JEETestSystem:
    """Main JEE Test System class for backend integration"""
    
    def __init__(self, quiz_generator=None):
        """Initialize JEE test system"""
        self.available = JEE_AVAILABLE
        self.quiz_generator = quiz_generator
        
        if self.available:
            self.generator = JEETestGenerator(quiz_generator)
            self.customizer = JEETestCustomizer()
            self.topics = JEETopics()
        else:
            self.generator = JEETestGenerator()
            self.customizer = None
            self.topics = None
    
    def create_full_mock_test(self) -> Dict:
        """Create a full JEE Main mock test (90 questions, 3 hours)"""
        if not self.available:
            return self._mock_response("Full Mock Test")
            
        config = JEETestConfig(
            test_type="full_mock",
            subjects=[Subject.PHYSICS, Subject.CHEMISTRY, Subject.MATHEMATICS],
            total_questions=90,
            total_time_minutes=180
        )
        
        return self.generator.generate_jee_test(config)
    
    def create_subject_test(self, subject: str, questions: int = 30) -> Dict:
        """Create a subject-specific test"""
        if not self.available:
            return self._mock_response(f"{subject} Test")
            
        # Map string to Subject enum
        subject_map = {
            "physics": Subject.PHYSICS,
            "chemistry": Subject.CHEMISTRY,
            "mathematics": Subject.MATHEMATICS,
            "math": Subject.MATHEMATICS
        }
        
        subject_enum = subject_map.get(subject.lower())
        if not subject_enum:
            raise ValueError(f"Invalid subject: {subject}")
        
        config = JEETestConfig(
            test_type="subject_wise",
            subjects=[subject_enum],
            total_questions=questions,
            total_time_minutes=60
        )
        
        return self.generator.generate_jee_test(config)
    
    def create_topic_test(self, subject: str, topics: List[str], questions: int = 15) -> Dict:
        """Create a topic-specific test"""
        if not self.available:
            return self._mock_response(f"{subject} - {', '.join(topics)} Test")
            
        subject_map = {
            "physics": Subject.PHYSICS,
            "chemistry": Subject.CHEMISTRY,
            "mathematics": Subject.MATHEMATICS,
            "math": Subject.MATHEMATICS
        }
        
        subject_enum = subject_map.get(subject.lower())
        if not subject_enum:
            raise ValueError(f"Invalid subject: {subject}")
        
        config = JEETestConfig(
            test_type="topic_wise",
            subjects=[subject_enum],
            total_questions=questions,
            total_time_minutes=30
        )
        
        # Set topic-specific configuration
        if subject_enum == Subject.PHYSICS:
            config.physics_topics = topics
        elif subject_enum == Subject.CHEMISTRY:
            config.chemistry_topics = topics
        else:
            config.math_topics = topics
        
        return self.generator.generate_jee_test(config)
    
    def get_available_topics(self, subject: str) -> Dict[str, List[str]]:
        """Get available topics for a subject"""
        if not self.available:
            return {"General": ["Sample Topic 1", "Sample Topic 2"]}
            
        subject_topics = {
            "physics": self.topics.PHYSICS_TOPICS,
            "chemistry": self.topics.CHEMISTRY_TOPICS,
            "mathematics": self.topics.MATHEMATICS_TOPICS,
            "math": self.topics.MATHEMATICS_TOPICS
        }
        
        return subject_topics.get(subject.lower(), {})
    
    def validate_test_config(self, config_data: Dict) -> bool:
        """Validate test configuration"""
        required_fields = ["test_type", "subjects", "total_questions"]
        return all(field in config_data for field in required_fields)
    
    def get_test_presets(self) -> Dict[str, Dict]:
        """Get predefined test presets"""
        return {
            "jee_full_mock": {
                "name": "JEE Main Full Mock Test",
                "description": "Complete JEE Main simulation - 90 questions, 3 hours",
                "subjects": ["Physics", "Chemistry", "Mathematics"],
                "questions": 90,
                "time_minutes": 180,
                "type": "full_mock"
            },
            "physics_practice": {
                "name": "Physics Practice Test",
                "description": "30 Physics questions, 1 hour",
                "subjects": ["Physics"],
                "questions": 30,
                "time_minutes": 60,
                "type": "subject_wise"
            },
            "chemistry_practice": {
                "name": "Chemistry Practice Test", 
                "description": "30 Chemistry questions, 1 hour",
                "subjects": ["Chemistry"],
                "questions": 30,
                "time_minutes": 60,
                "type": "subject_wise"
            },
            "math_practice": {
                "name": "Mathematics Practice Test",
                "description": "30 Mathematics questions, 1 hour", 
                "subjects": ["Mathematics"],
                "questions": 30,
                "time_minutes": 60,
                "type": "subject_wise"
            }
        }
    
    def _mock_response(self, test_name: str) -> Dict:
        """Generate mock response when JEE system is not available"""
        return {
            "test_id": f"mock_{test_name.lower().replace(' ', '_')}",
            "questions": [
                {
                    "question_id": "mock_q1",
                    "subject": "Physics",
                    "topic": "Sample Topic",
                    "difficulty": "Medium",
                    "type": "MCQ",
                    "question_text": "This is a sample question (JEE system not fully loaded)",
                    "options": {
                        "A": "Option A",
                        "B": "Option B", 
                        "C": "Option C",
                        "D": "Option D"
                    },
                    "correct_answer": "A",
                    "explanation": "Sample explanation",
                    "marks": 4,
                    "negative_marks": -1
                }
            ],
            "metadata": {
                "test_name": test_name,
                "total_questions": 1,
                "total_time_minutes": 30,
                "message": "This is a mock test. Full JEE system not available.",
                "available": False
            }
        }

# Backward compatibility
def create_jee_test_system(quiz_generator=None):
    """Factory function to create JEE test system"""
    return JEETestSystem(quiz_generator)

# For direct testing
if __name__ == "__main__":
    print("Testing JEE Test System Backend Integration...")
    
    jee_system = JEETestSystem()
    print(f"JEE System Available: {jee_system.available}")
    
    # Test full mock
    full_test = jee_system.create_full_mock_test()
    print(f"\nFull Mock Test: {full_test['test_id']}")
    print(f"Questions: {len(full_test['questions'])}")
    
    # Test presets
    presets = jee_system.get_test_presets()
    print(f"\nAvailable Presets: {list(presets.keys())}")
    
    # Test topics
    physics_topics = jee_system.get_available_topics("physics")
    print(f"\nPhysics Topic Categories: {list(physics_topics.keys())}")
