"""
🎓 Unified Klaro System
=======================

Core system that integrates:
- Quiz-bot's textbook database and content retrieval
- Klaro's AI processing and handwriting generation
- Multi-source validation for accurate solutions
- Cross-referenced educational content
"""

from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import time
import json
from pathlib import Path

# Quiz-bot imports (textbook database and content retrieval)
from .quiz_content_manager import QuizContentManager
from .textbook_search import TextbookSearchEngine
from .book_registry import BookRegistryManager

# Klaro imports (AI processing and handwriting)
from .question_processor import UnifiedQuestionProcessor
from .solution_generator import MultiSourceSolutionGenerator
from .teaching_guidance import TeachingGuidanceGenerator

# Rendering and output
from ..rendering.handwriting_generator import HandwritingGenerator
from ..rendering.export_manager import ExportManager

# Knowledge base integration
from ..knowledge_base.unified_rag_system import UnifiedRAGSystem
from ..knowledge_base.cross_reference_engine import CrossReferenceEngine

# Voice processing
from ..interfaces.voice_processor import VoiceProcessor

# Utilities
from ..utils.config import KlaroConfig
from ..utils.logging_system import get_logger

logger = get_logger(__name__)


@dataclass
class QuestionSource:
    """Information about where a question or solution comes from."""
    source_type: str  # 'textbook', 'pyq', 'user', 'generated'
    book_name: str
    chapter: Optional[str] = None
    page_number: Optional[int] = None
    confidence_score: float = 0.0


@dataclass
class CrossReferencedSolution:
    """Solution with multiple source validation."""
    primary_solution: Dict[str, Any]
    supporting_sources: List[QuestionSource]
    alternative_approaches: List[Dict[str, Any]]
    confidence_score: float
    handwritten_image_path: Optional[str] = None
    textbook_references: List[str] = None
    similar_pyq_questions: List[str] = None


@dataclass
class UnifiedKlaroResponse:
    """Complete response from unified Klaro system."""
    question: str
    processed_question: Dict[str, Any]
    solution: CrossReferencedSolution
    teaching_guidance: Optional[Dict[str, Any]] = None
    quiz_suggestions: Optional[List[Dict[str, Any]]] = None
    response_time: float = 0.0
    session_id: Optional[str] = None


class UnifiedKlaroSystem:
    """
    Main Klaro system that integrates quiz-bot and teaching assistant capabilities.
    
    This system combines:
    - Textbook database and organized content (from quiz-bot)
    - AI-powered question processing and solution generation (from Klaro)
    - Handwritten output generation
    - Multi-source validation and cross-referencing
    - Voice input and interactive interfaces
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the unified Klaro system."""
        logger.info("🎓 Initializing Unified Klaro Educational System...")
        
        # Load configuration
        self.config = KlaroConfig(config_path)
        
        # Initialize textbook and content management (from quiz-bot)
        self._init_content_systems()
        
        # Initialize AI processing (from Klaro)
        self._init_ai_systems()
        
        # Initialize rendering and output (from Klaro)
        self._init_rendering_systems()
        
        # Initialize voice processing (from Klaro)
        self._init_voice_systems()
        
        # Session management
        self.session_history = []
        self.current_session_id = None
        
        logger.info("✅ Unified Klaro system initialized successfully!")
        print("🎓 Klaro is ready - Ask questions, generate quizzes, get handwritten solutions!")
    
    def _init_content_systems(self):
        """Initialize content management systems from quiz-bot."""
        logger.info("📚 Initializing content management systems...")
        
        # Book registry and management
        self.book_registry = BookRegistryManager(
            registry_path=self.config.BOOK_REGISTRY_PATH
        )
        
        # Textbook search engine
        self.textbook_search = TextbookSearchEngine(
            textbook_path=self.config.TEXTBOOKS_PATH,
            faiss_index_path=self.config.FAISS_INDEX_PATH
        )
        
        # Quiz content manager
        self.quiz_content_manager = QuizContentManager(
            book_registry=self.book_registry,
            search_engine=self.textbook_search
        )
        
        logger.info("✅ Content systems initialized")
    
    def _init_ai_systems(self):
        """Initialize AI processing systems from Klaro."""
        logger.info("🧠 Initializing AI processing systems...")
        
        # Question processor (enhanced with textbook context)
        self.question_processor = UnifiedQuestionProcessor(
            textbook_search=self.textbook_search
        )
        
        # Solution generator (with multi-source validation)
        self.solution_generator = MultiSourceSolutionGenerator(
            openai_api_key=self.config.OPENAI_API_KEY,
            model=self.config.OPENAI_MODEL
        )
        
        # Teaching guidance generator
        self.teaching_guidance_generator = TeachingGuidanceGenerator()
        
        # Unified RAG system
        self.rag_system = UnifiedRAGSystem(
            textbook_search=self.textbook_search,
            knowledge_base_path=self.config.KNOWLEDGE_BASE_PATH
        )
        
        # Cross-reference engine for multi-source validation
        self.cross_reference_engine = CrossReferenceEngine(
            book_registry=self.book_registry,
            rag_system=self.rag_system
        )
        
        logger.info("✅ AI systems initialized")
    
    def _init_rendering_systems(self):
        """Initialize rendering and output systems from Klaro."""
        logger.info("✍️ Initializing rendering systems...")
        
        # Handwriting generator
        self.handwriting_generator = HandwritingGenerator(
            style_config=self.config.HANDWRITING_CONFIG
        )
        
        # Export manager for multiple formats
        self.export_manager = ExportManager(
            output_dir=self.config.OUTPUT_DIR
        )
        
        logger.info("✅ Rendering systems initialized")
    
    def _init_voice_systems(self):
        """Initialize voice processing systems from Klaro."""
        try:
            logger.info("🎤 Initializing voice processing...")
            self.voice_processor = VoiceProcessor()
            logger.info("✅ Voice processing available")
        except Exception as e:
            logger.warning(f"⚠️ Voice processing not available: {e}")
            self.voice_processor = None
    
    def process_question(self, question_text: str, 
                        generate_handwriting: bool = True,
                        cross_validate: bool = True) -> UnifiedKlaroResponse:
        """
        Process a question using the unified system.
        
        This combines:
        1. Question analysis and classification
        2. Multi-source content retrieval
        3. AI-powered solution generation
        4. Cross-validation across sources
        5. Handwritten output generation
        """
        start_time = time.time()
        logger.info(f"🤔 Processing question: {question_text[:50]}...")
        
        try:
            # Step 1: Process and classify the question
            print("🔍 Analyzing question...")
            processed_question = self.question_processor.process_question(question_text)
            
            # Step 2: Search across all content sources
            print("📚 Searching textbooks and knowledge base...")
            content_results = self.rag_system.comprehensive_search(
                question=question_text,
                processed_question=processed_question
            )
            
            # Step 3: Generate solution with multi-source context
            print("🧠 Generating solution with AI...")
            solution = self.solution_generator.generate_multi_source_solution(
                processed_question=processed_question,
                content_context=content_results
            )
            
            # Step 4: Cross-validate solution (if enabled)
            if cross_validate:
                print("🔗 Cross-validating with multiple sources...")
                validated_solution = self.cross_reference_engine.validate_solution(
                    solution=solution,
                    content_results=content_results
                )
            else:
                validated_solution = solution
            
            # Step 5: Generate handwritten output (if requested)
            handwritten_path = None
            if generate_handwriting:
                print("✍️ Creating handwritten-style solution...")
                handwritten_path = self.handwriting_generator.generate_solution(
                    solution=validated_solution
                )
            
            # Step 6: Generate teaching guidance
            teaching_guidance = None
            if processed_question.get('question_type') == 'teaching':
                print("👩‍🏫 Generating teaching guidance...")
                teaching_guidance = self.teaching_guidance_generator.generate_guidance(
                    solution=validated_solution
                )
            
            # Step 7: Generate quiz suggestions for practice
            print("📝 Finding related practice questions...")
            quiz_suggestions = self.quiz_content_manager.get_related_questions(
                processed_question=processed_question,
                limit=5
            )
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Create unified response
            response = UnifiedKlaroResponse(
                question=question_text,
                processed_question=processed_question,
                solution=validated_solution,
                teaching_guidance=teaching_guidance,
                quiz_suggestions=quiz_suggestions,
                response_time=response_time,
                session_id=self._get_session_id()
            )
            
            # Add to session history
            self.session_history.append(response)
            
            logger.info(f"✅ Question processed successfully in {response_time:.2f}s")
            print(f"🎉 Solution generated with {len(validated_solution.supporting_sources)} source references!")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing question: {e}")
            raise
    
    def generate_quiz(self, subject: str, grade: str, topic: Optional[str] = None,
                     difficulty: str = "medium", num_questions: int = 5) -> Dict[str, Any]:
        """Generate a quiz using the enhanced content database."""
        logger.info(f"📝 Generating quiz: {subject} Grade {grade}")
        
        return self.quiz_content_manager.generate_enhanced_quiz(
            subject=subject,
            grade=grade,
            topic=topic,
            difficulty=difficulty,
            num_questions=num_questions
        )
    
    def process_voice_input(self) -> Optional[UnifiedKlaroResponse]:
        """Process voice input from user."""
        if not self.voice_processor:
            print("❌ Voice processing not available")
            return None
        
        print("🎤 Listening for your question...")
        voice_result = self.voice_processor.get_voice_input()
        
        if voice_result and voice_result.get('text'):
            print(f"🗣️ Heard: {voice_result['text']}")
            return self.process_question(voice_result['text'])
        else:
            print("❌ No clear voice input detected")
            return None
    
    def start_voice_mode(self):
        """Start continuous voice listening mode."""
        if not self.voice_processor:
            print("❌ Voice processing not available")
            return
        
        print("🎤 Voice mode activated - say 'Hey Klaro' followed by your question")
        print("Press Ctrl+C to stop")
        
        def voice_callback(voice_input):
            if voice_input and voice_input.get('text'):
                print(f"\n🗣️ Processing: {voice_input['text']}")
                response = self.process_question(voice_input['text'])
                self.display_response_summary(response)
                print("\n🎤 Listening for next question...")
        
        self.voice_processor.start_continuous_listening(voice_callback)
    
    def display_response(self, response: UnifiedKlaroResponse):
        """Display a complete response to the user."""
        print("\n" + "="*80)
        print(f"📋 SOLUTION FOR: {response.question}")
        print("="*80)
        
        # Display main solution
        solution = response.solution
        print(f"\n💡 SOLUTION (Confidence: {solution.confidence_score:.1%}):")
        print("-" * 50)
        
        if hasattr(solution.primary_solution, 'steps'):
            for i, step in enumerate(solution.primary_solution.steps, 1):
                print(f"\nStep {i}: {step.title}")
                print(f"   {step.explanation}")
                if hasattr(step, 'mathematical_expression') and step.mathematical_expression:
                    print(f"   📐 {step.mathematical_expression}")
        
        # Display sources
        if solution.supporting_sources:
            print(f"\n📚 SOURCES ({len(solution.supporting_sources)} references):")
            print("-" * 50)
            for source in solution.supporting_sources[:3]:  # Show top 3
                print(f"   📖 {source.book_name}")
                if source.chapter:
                    print(f"      Chapter: {source.chapter}")
                if source.confidence_score > 0:
                    print(f"      Relevance: {source.confidence_score:.1%}")
        
        # Display handwritten solution path
        if solution.handwritten_image_path:
            print(f"\n✍️ HANDWRITTEN SOLUTION:")
            print(f"   📁 {solution.handwritten_image_path}")
        
        # Display teaching guidance (if available)
        if response.teaching_guidance:
            print(f"\n👩‍🏫 TEACHING GUIDANCE:")
            print("-" * 50)
            guidance = response.teaching_guidance
            if guidance.get('strategies'):
                print("   📋 Teaching Strategies:")
                for strategy in guidance['strategies'][:2]:
                    print(f"      • {strategy}")
        
        # Display related questions
        if response.quiz_suggestions:
            print(f"\n📝 PRACTICE QUESTIONS:")
            print("-" * 50)
            for i, quiz in enumerate(response.quiz_suggestions[:3], 1):
                print(f"   {i}. {quiz.get('question', 'Question available')[:60]}...")
        
        print(f"\n⏱️ Generated in {response.response_time:.2f} seconds")
        print("="*80)
    
    def display_response_summary(self, response: UnifiedKlaroResponse):
        """Display a brief summary of the response."""
        solution = response.solution
        print(f"\n✅ Solution generated (Confidence: {solution.confidence_score:.1%})")
        print(f"📚 Referenced {len(solution.supporting_sources)} sources")
        if solution.handwritten_image_path:
            print(f"✍️ Handwritten solution: {solution.handwritten_image_path}")
        print(f"⏱️ {response.response_time:.2f}s")
    
    def get_subject_statistics(self) -> Dict[str, Any]:
        """Get statistics about available content."""
        return {
            'textbooks': self.book_registry.get_statistics(),
            'faiss_index': self.textbook_search.get_index_statistics(),
            'knowledge_base': self.rag_system.get_statistics()
        }
    
    def search_content(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search across all content sources."""
        return self.rag_system.comprehensive_search(query, filters)
    
    def add_textbook(self, book_path: str, metadata: Dict[str, Any]):
        """Add a new textbook to the system."""
        # Add to book registry
        self.book_registry.add_book(book_path, metadata)
        
        # Update search indexes
        self.textbook_search.index_new_book(book_path)
        
        # Update RAG system
        self.rag_system.ingest_new_content(book_path, metadata)
        
        logger.info(f"✅ Added textbook: {metadata.get('title', 'Unknown')}")
    
    def _get_session_id(self) -> str:
        """Get or create session ID."""
        if not self.current_session_id:
            self.current_session_id = f"session_{int(time.time())}"
        return self.current_session_id
    
    def export_solution(self, response: UnifiedKlaroResponse, 
                       formats: List[str] = None) -> Dict[str, str]:
        """Export solution in multiple formats."""
        if formats is None:
            formats = ['pdf', 'html', 'png']
        
        return self.export_manager.export_solution(
            solution=response.solution,
            formats=formats,
            include_sources=True
        )
    
    def get_available_books(self) -> Dict[str, List[str]]:
        """Get list of available books organized by subject and grade."""
        return self.book_registry.get_available_books()
    
    def validate_setup(self) -> Dict[str, bool]:
        """Validate that all systems are properly configured."""
        validation_results = {
            'openai_api_key': bool(self.config.OPENAI_API_KEY),
            'textbook_database': self.book_registry.validate(),
            'faiss_index': self.textbook_search.validate(),
            'knowledge_base': self.rag_system.validate(),
            'handwriting_system': self.handwriting_generator.validate(),
            'voice_processing': self.voice_processor is not None
        }
        
        logger.info(f"🔍 System validation: {sum(validation_results.values())}/{len(validation_results)} systems ready")
        return validation_results


# Convenience function for quick testing
def quick_test():
    """Quick test of the unified system."""
    klaro = UnifiedKlaroSystem()
    
    test_questions = [
        "Solve x² + 5x + 6 = 0",
        "Explain photosynthesis process",
        "What is Newton's second law of motion?",
        "How do I solve integration by parts?"
    ]
    
    for question in test_questions:
        print(f"\n🧪 Testing: {question}")
        try:
            response = klaro.process_question(question)
            print(f"✅ Success - Confidence: {response.solution.confidence_score:.1%}")
        except Exception as e:
            print(f"❌ Failed: {e}")


if __name__ == "__main__":
    quick_test()
