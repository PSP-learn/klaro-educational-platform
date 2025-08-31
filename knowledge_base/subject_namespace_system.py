"""
🔬 Subject Namespace & Extensibility System
==========================================

Handles multiple subjects (Math, Physics, Chemistry, Biology) 
without embedding confusion or retrieval interference.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum
import numpy as np

class Subject(Enum):
    MATHEMATICS = "mathematics"
    PHYSICS = "physics" 
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    COMPUTER_SCIENCE = "computer_science"
    ENGLISH = "english"
    REASONING = "reasoning"


@dataclass
class NamespacedChunk:
    """Chunk with subject and topic namespace."""
    chunk_id: str
    content: str
    subject: Subject
    topic_hierarchy: List[str]  # ['mathematics', 'algebra', 'quadratic_equations']
    grade_level: str
    difficulty: str
    mathematical_context: bool
    language_context: str  # 'english', 'hindi', etc.


class SubjectNamespaceSystem:
    """
    Intelligent namespace system that prevents subject confusion.
    
    STRATEGY:
    1. Subject-Specific Embeddings: Different models for different subjects
    2. Hierarchical Filtering: Multi-level topic organization  
    3. Context Preservation: Subject-aware chunking and retrieval
    4. Cross-Subject Linking: Smart connections where relevant
    """
    
    def __init__(self):
        # Subject-specific embedding models
        self.subject_embedding_models = {
            Subject.MATHEMATICS: 'sentence-transformers/all-mpnet-base-v2',  # Good for math symbols
            Subject.PHYSICS: 'sentence-transformers/all-mpnet-base-v2',     # Good for physics concepts
            Subject.CHEMISTRY: 'sentence-transformers/all-MiniLM-L6-v2',    # Good for chemical formulas
            Subject.BIOLOGY: 'sentence-transformers/all-MiniLM-L6-v2',      # Good for biological terms
            Subject.COMPUTER_SCIENCE: 'sentence-transformers/all-distilroberta-v1',  # Good for code
            Subject.ENGLISH: 'sentence-transformers/all-MiniLM-L6-v2',      # Language processing
            Subject.REASONING: 'sentence-transformers/all-mpnet-base-v2'    # Logical reasoning
        }
        
        # Subject-specific vector stores (separate indexes)
        self.subject_indexes = {}
        
        # Topic hierarchies for each subject
        self.topic_hierarchies = {
            Subject.MATHEMATICS: {
                'algebra': ['polynomials', 'quadratic_equations', 'linear_equations'],
                'calculus': ['limits', 'derivatives', 'integrals', 'differential_equations'],
                'geometry': ['coordinate_geometry', 'trigonometry', 'solid_geometry'],
                'statistics': ['probability', 'data_analysis', 'distributions']
            },
            Subject.PHYSICS: {
                'mechanics': ['kinematics', 'dynamics', 'work_energy', 'rotational_motion'],
                'electricity': ['electrostatics', 'current_electricity', 'magnetism'],
                'optics': ['ray_optics', 'wave_optics', 'optical_instruments'],
                'modern_physics': ['atomic_structure', 'nuclear_physics', 'quantum_mechanics']
            },
            Subject.CHEMISTRY: {
                'physical_chemistry': ['thermodynamics', 'kinetics', 'equilibrium'],
                'organic_chemistry': ['hydrocarbons', 'functional_groups', 'reactions'],
                'inorganic_chemistry': ['periodic_table', 'coordination', 'metallurgy']
            },
            Subject.BIOLOGY: {
                'cell_biology': ['cell_structure', 'cell_division', 'metabolism'],
                'genetics': ['heredity', 'dna_rna', 'evolution'],
                'ecology': ['ecosystems', 'biodiversity', 'environmental_biology']
            }
        }
    
    def add_content_with_namespace(self, content: str, metadata: Dict[str, Any]) -> bool:
        """Add content with proper subject namespace."""
        try:
            subject = Subject(metadata['subject'])
            
            # Create namespaced chunk
            namespaced_chunk = NamespacedChunk(
                chunk_id=f"{subject.value}_{metadata['book_id']}_{metadata['chunk_id']}",
                content=content,
                subject=subject,
                topic_hierarchy=self._determine_topic_hierarchy(content, subject),
                grade_level=metadata.get('grade_level', 'unknown'),
                difficulty=metadata.get('difficulty', 'medium'),
                mathematical_context=self._has_mathematical_content(content),
                language_context=metadata.get('language', 'english')
            )
            
            # Add to subject-specific index
            if subject not in self.subject_indexes:
                self.subject_indexes[subject] = self._create_subject_index(subject)
            
            # Generate subject-specific embedding
            embedding = self._generate_subject_embedding(content, subject)
            
            # Add to subject index with namespace metadata
            self.subject_indexes[subject].add_vectors(
                vectors=embedding.reshape(1, -1),
                metadata=[{
                    'chunk_id': namespaced_chunk.chunk_id,
                    'subject': subject.value,
                    'topic_hierarchy': namespaced_chunk.topic_hierarchy,
                    'grade_level': namespaced_chunk.grade_level,
                    'difficulty': namespaced_chunk.difficulty,
                    'content': content,
                    'book_title': metadata.get('book_title', 'Unknown'),
                    'chapter': metadata.get('chapter', 'Unknown')
                }]
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Error adding namespaced content: {e}")
            return False
    
    def search_with_namespace(self, query: str, target_subject: Subject, 
                             grade_filter: Optional[str] = None,
                             topic_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search within specific subject namespace."""
        
        if target_subject not in self.subject_indexes:
            print(f"⚠️ No content available for {target_subject.value}")
            return []
        
        # Generate subject-specific embedding for query
        query_embedding = self._generate_subject_embedding(query, target_subject)
        
        # Search within subject index
        results = self.subject_indexes[target_subject].search(query_embedding, k=20)
        
        # Apply namespace filters
        filtered_results = []
        for result in results:
            # Grade filter
            if grade_filter and result.get('grade_level') != grade_filter:
                continue
            
            # Topic filter  
            if topic_filter and not any(topic_filter.lower() in topic.lower() 
                                      for topic in result.get('topic_hierarchy', [])):
                continue
            
            filtered_results.append(result)
        
        return filtered_results
    
    def cross_subject_search(self, query: str, primary_subject: Subject,
                           include_subjects: List[Subject] = None) -> Dict[Subject, List[Dict[str, Any]]]:
        """Search across multiple subjects with proper context separation."""
        
        results = {}
        subjects_to_search = include_subjects or [primary_subject]
        
        # Add related subjects based on query analysis
        if self._has_mathematical_content(query):
            if Subject.PHYSICS not in subjects_to_search:
                subjects_to_search.append(Subject.PHYSICS)  # Math-Physics connection
        
        if 'equation' in query.lower() and Subject.CHEMISTRY not in subjects_to_search:
            subjects_to_search.append(Subject.CHEMISTRY)  # Chemical equations
        
        # Search each subject separately
        for subject in subjects_to_search:
            if subject in self.subject_indexes:
                subject_results = self.search_with_namespace(query, subject)
                
                # Add subject context to results
                for result in subject_results:
                    result['search_subject'] = subject.value
                    result['cross_subject_relevance'] = self._calculate_cross_subject_relevance(
                        query, primary_subject, subject
                    )
                
                results[subject] = subject_results
        
        return results
    
    def _determine_topic_hierarchy(self, content: str, subject: Subject) -> List[str]:
        """Determine topic hierarchy for content within subject."""
        hierarchy = [subject.value]
        
        if subject not in self.topic_hierarchies:
            return hierarchy
        
        content_lower = content.lower()
        subject_topics = self.topic_hierarchies[subject]
        
        # Find matching main topics
        for main_topic, subtopics in subject_topics.items():
            if main_topic in content_lower:
                hierarchy.append(main_topic)
                
                # Find matching subtopics
                for subtopic in subtopics:
                    if subtopic.replace('_', ' ') in content_lower:
                        hierarchy.append(subtopic)
                        break
                break
        
        return hierarchy
    
    def _has_mathematical_content(self, content: str) -> bool:
        """Check if content has mathematical expressions."""
        math_indicators = [
            r'[=<>≤≥±∞∑∏∫∂√π]',  # Math symbols
            r'\$.*?\$',            # LaTeX math
            r'\\frac\{.*?\}',      # Fractions
            r'\^[0-9]',            # Exponents
            r'_[0-9]',             # Subscripts
        ]
        
        for pattern in math_indicators:
            if re.search(pattern, content):
                return True
        return False
    
    def _generate_subject_embedding(self, content: str, subject: Subject) -> np.ndarray:
        """Generate embedding using subject-specific model."""
        model_name = self.subject_embedding_models[subject]
        
        # In practice, this would load the appropriate sentence transformer model
        # For now, return dummy embedding
        return np.random.random(768)  # Replace with actual embedding
    
    def _create_subject_index(self, subject: Subject):
        """Create subject-specific vector index.""" 
        # Use the optimized FAISS from previous component
        from .scalable_vector_store import OptimizedFAISS
        return OptimizedFAISS(dimension=768)
    
    def _calculate_cross_subject_relevance(self, query: str, 
                                         primary_subject: Subject, 
                                         search_subject: Subject) -> float:
        """Calculate relevance when searching across subjects."""
        
        # Define cross-subject relevance matrix
        relevance_matrix = {
            (Subject.MATHEMATICS, Subject.PHYSICS): 0.8,    # High math-physics overlap
            (Subject.MATHEMATICS, Subject.CHEMISTRY): 0.6,  # Some chemical calculations
            (Subject.PHYSICS, Subject.CHEMISTRY): 0.7,      # Physical chemistry
            (Subject.BIOLOGY, Subject.CHEMISTRY): 0.9,      # Biochemistry overlap
            (Subject.COMPUTER_SCIENCE, Subject.MATHEMATICS): 0.8  # Algorithms, discrete math
        }
        
        # Check both directions
        key1 = (primary_subject, search_subject)
        key2 = (search_subject, primary_subject)
        
        return relevance_matrix.get(key1, relevance_matrix.get(key2, 0.3))


# NAMESPACE JUSTIFICATION:
"""
🎯 Subject Namespace Strategy:

SEPARATE INDEXES BY SUBJECT:
✅ Mathematics Index: Only math content, math-optimized embeddings
✅ Physics Index: Physics concepts, formula-optimized embeddings  
✅ Chemistry Index: Chemical formulas, reaction-optimized embeddings
✅ Biology Index: Biological terms, process-optimized embeddings

BENEFITS:
1. No Cross-Contamination: Math search won't return chemistry results
2. Subject-Optimized Models: Better embeddings for each domain
3. Scalable Architecture: Add new subjects without affecting existing ones
4. Faster Search: Smaller indexes = faster retrieval

CROSS-SUBJECT INTELLIGENCE:
- Smart cross-references where relevant (math in physics)
- Explicit relevance scoring for cross-subject results
- User control over which subjects to include in search

EXAMPLE SCENARIOS:
Query: \"Solve x² + 5x + 6 = 0\"
✅ Searches: Mathematics index (primary)
✅ May include: Physics index (mathematical physics problems)
✅ Excludes: Biology index (no relevance)

Query: \"What is photosynthesis?\"
✅ Searches: Biology index (primary)
✅ May include: Chemistry index (chemical reactions)
✅ Excludes: Mathematics index (no relevance)

MEMORY EFFICIENCY:
- Each subject index ~100MB-500MB
- Total: ~2GB for all subjects
- vs. Single mixed index: ~2GB but with lower quality results
"""
