"""
📚 Enhanced Book Registry Manager
================================

Multi-dimensional book organization system that supports:
- Class-based learning (Grade 9-12)
- Entrance exam preparation (JEE, NEET, SSC, etc.)
- Publisher-based organization
- Cross-referencing and smart recommendations
"""

from typing import Dict, List, Optional, Any, Set, Tuple
import json
from pathlib import Path
from datetime import datetime
import re
from dataclasses import dataclass

from ..utils.config import get_config


@dataclass
class BookMetadata:
    """Enhanced metadata for educational books."""
    id: str
    title: str
    publisher: str
    subject: str
    path: str
    primary_classification: Dict[str, Any]
    exam_relevance: List[Dict[str, Any]]
    chapters: Dict[str, Any] = None
    status: str = "active"
    complements: List[str] = None
    covers_topics: List[str] = None


@dataclass
class ExamProfile:
    """Profile for entrance exams with book recommendations."""
    name: str
    full_name: str
    subjects: List[str]
    grade_levels: List[str]
    book_recommendations: Dict[str, Dict[str, List[str]]]
    topic_priorities: Dict[str, Dict[str, List[str]]]


class EnhancedBookManager:
    """Enhanced book manager with multi-dimensional organization."""
    
    def __init__(self, registry_path: Optional[str] = None):
        """Initialize enhanced book manager."""
        self.config = get_config()
        self.registry_path = registry_path or self.config.BOOK_REGISTRY_PATH.replace('.json', '_enhanced.json')
        self.textbooks_path = Path(self.config.TEXTBOOKS_PATH)
        
        # Load or create enhanced registry
        self.registry = self._load_enhanced_registry()
        
        # Cache for quick lookups
        self._book_cache = {}
        self._exam_cache = {}
        self._topic_cache = {}
        self._rebuild_caches()
    
    def _load_enhanced_registry(self) -> Dict[str, Any]:
        """Load the enhanced registry structure."""
        try:
            with open(self.registry_path, 'r') as f:
                registry = json.load(f)
            print(f"✅ Loaded enhanced registry with {len(registry.get('books', {}))} books")
            return registry
        except FileNotFoundError:
            print(f"⚠️ Enhanced registry not found, creating new one...")
            return self._create_enhanced_registry()
    
    def _create_enhanced_registry(self) -> Dict[str, Any]:
        """Create a new enhanced registry structure."""
        registry = {
            "version": "3.0.0",
            "last_updated": datetime.now().isoformat(),
            "organization_strategy": "multi_dimensional",
            "metadata": {
                "total_books": 0,
                "total_chapters": 0,
                "supported_exams": ["jee_main", "jee_advanced", "neet", "board_exams", "ssc", "nda"],
                "supported_subjects": ["mathematics", "physics", "chemistry", "biology", "reasoning", "english"]
            },
            "books": {},
            "exam_profiles": {},
            "topic_taxonomy": {},
            "content_cross_references": {},
            "smart_recommendations": {}
        }
        
        self._save_registry(registry)
        return registry
    
    def add_book(self, book_metadata: Dict[str, Any]) -> bool:
        """
        Add a book with enhanced metadata.
        
        Expected metadata structure:
        {
            "title": "Book Title",
            "publisher": "Publisher Name",
            "subject": "mathematics",
            "grade": "11",  # or grade_range for advanced books
            "book_type": "textbook|practice|advanced",
            "chapters": [...],
            "exam_relevance": [{"exam": "jee_main", "priority": "high"}],
            "path": "physical/path/to/book"
        }
        """
        try:
            # Generate book ID
            book_id = self._generate_book_id(book_metadata)
            
            # Validate required fields
            required_fields = ['title', 'publisher', 'subject']
            for field in required_fields:
                if field not in book_metadata:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create book entry
            book_entry = {
                "id": book_id,
                "title": book_metadata['title'],
                "publisher": book_metadata['publisher'],
                "subject": book_metadata['subject'].lower(),
                "path": book_metadata.get('path', ''),
                "primary_classification": {
                    "type": book_metadata.get('book_type', 'textbook'),
                    "grade": str(book_metadata.get('grade', '')),
                    "curriculum": book_metadata.get('curriculum', 'cbse')
                },
                "exam_relevance": book_metadata.get('exam_relevance', []),
                "chapters": book_metadata.get('chapters', {}),
                "status": book_metadata.get('status', 'active'),
                "added_date": datetime.now().isoformat()
            }
            
            # Add optional fields
            optional_fields = ['complements', 'covers_topics', 'difficulty_level', 'author', 'edition']
            for field in optional_fields:
                if field in book_metadata:
                    book_entry[field] = book_metadata[field]
            
            # Add to registry
            self.registry['books'][book_id] = book_entry
            self.registry['metadata']['total_books'] = len(self.registry['books'])
            
            # Update caches
            self._rebuild_caches()
            
            # Save registry
            self._save_registry()
            
            print(f"✅ Added book: {book_metadata['title']} (ID: {book_id})")
            return True
            
        except Exception as e:
            print(f"❌ Error adding book: {e}")
            return False
    
    def get_books_for_class(self, grade: str, subject: str, 
                           book_type: Optional[str] = None) -> List[BookMetadata]:
        """Get books for specific class and subject."""
        books = []
        
        for book_id, book in self.registry['books'].items():
            # Check grade match
            if book['primary_classification'].get('grade') == str(grade):
                # Check subject match
                if book['subject'] == subject.lower():
                    # Check book type if specified
                    if not book_type or book['primary_classification'].get('type') == book_type:
                        books.append(self._dict_to_metadata(book))
        
        return sorted(books, key=lambda x: x.primary_classification.get('type', ''))
    
    def get_books_for_exam(self, exam: str, subject: Optional[str] = None,
                          priority: Optional[str] = None) -> List[BookMetadata]:
        """Get recommended books for specific entrance exam."""
        books = []
        
        # Check if exam profile exists
        if exam not in self.registry.get('exam_profiles', {}):
            return books
        
        exam_profile = self.registry['exam_profiles'][exam]
        
        # Get books from exam recommendations
        recommendations = exam_profile.get('book_recommendations', {})
        
        for priority_level, subjects_books in recommendations.items():
            # Filter by priority if specified
            if priority and priority_level != priority:
                continue
            
            for subj, book_ids in subjects_books.items():
                # Filter by subject if specified
                if subject and subj != subject.lower():
                    continue
                
                for book_id in book_ids:
                    if book_id in self.registry['books']:
                        book = self.registry['books'][book_id]
                        book_metadata = self._dict_to_metadata(book)
                        book_metadata.priority = priority_level
                        books.append(book_metadata)
        
        return books
    
    def get_books_for_topic(self, topic: str, difficulty: Optional[str] = None,
                           exam_context: Optional[str] = None) -> List[BookMetadata]:
        """Get books that cover a specific topic."""
        books = []
        
        # Search through book chapters and topics
        for book_id, book in self.registry['books'].items():
            book_covers_topic = False
            
            # Check chapters
            if 'chapters' in book:
                for chapter_key, chapter in book['chapters'].items():
                    if topic.lower() in chapter.get('topics', []):
                        book_covers_topic = True
                        break
            
            # Check covers_topics
            if 'covers_topics' in book:
                if topic.lower() in [t.lower() for t in book['covers_topics']]:
                    book_covers_topic = True
            
            # Check exam relevance if exam context provided
            if book_covers_topic and exam_context:
                exam_relevant = any(
                    rel['exam'] == exam_context 
                    for rel in book.get('exam_relevance', [])
                )
                if not exam_relevant:
                    continue
            
            if book_covers_topic:
                books.append(self._dict_to_metadata(book))
        
        return books
    
    def get_learning_pathway(self, exam: str, subject: str) -> Dict[str, List[str]]:
        """Get recommended learning pathway for exam preparation."""
        if exam in self.registry.get('smart_recommendations', {}).get('learning_pathways', {}):
            pathway_key = f"{exam}_{subject}"
            if pathway_key in self.registry['smart_recommendations']['learning_pathways']:
                return self.registry['smart_recommendations']['learning_pathways'][pathway_key]
        
        # Fallback: create basic pathway from exam profile
        if exam in self.registry.get('exam_profiles', {}):
            recommendations = self.registry['exam_profiles'][exam].get('book_recommendations', {})
            return {
                level: recommendations.get(level, {}).get(subject, [])
                for level in ['essential', 'practice', 'advanced']
            }
        
        return {}
    
    def get_cross_references(self, topic: str) -> Dict[str, Any]:
        """Get cross-references for a topic."""
        topic_key = topic.lower().replace(' ', '_')
        return self.registry.get('content_cross_references', {}).get(topic_key, {})
    
    def add_exam_profile(self, exam_data: Dict[str, Any]) -> bool:
        """Add or update an exam profile."""
        try:
            exam_id = exam_data['exam_id']
            self.registry.setdefault('exam_profiles', {})[exam_id] = exam_data
            self._save_registry()
            print(f"✅ Added exam profile: {exam_data.get('name', exam_id)}")
            return True
        except Exception as e:
            print(f"❌ Error adding exam profile: {e}")
            return False
    
    def search_books(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[BookMetadata]:
        """Search books with optional filters."""
        results = []
        query_lower = query.lower()
        
        for book_id, book in self.registry['books'].items():
            # Check if query matches title, publisher, or topics
            matches_query = (
                query_lower in book['title'].lower() or
                query_lower in book['publisher'].lower() or
                any(query_lower in topic for topic in book.get('covers_topics', []))
            )
            
            if not matches_query:
                continue
            
            # Apply filters if provided
            if filters:
                # Filter by subject
                if 'subject' in filters and book['subject'] != filters['subject'].lower():
                    continue
                
                # Filter by grade
                if 'grade' in filters and book['primary_classification'].get('grade') != str(filters['grade']):
                    continue
                
                # Filter by exam relevance
                if 'exam' in filters:
                    exam_relevant = any(
                        rel['exam'] == filters['exam']
                        for rel in book.get('exam_relevance', [])
                    )
                    if not exam_relevant:
                        continue
                
                # Filter by book type
                if 'book_type' in filters and book['primary_classification'].get('type') != filters['book_type']:
                    continue
            
            results.append(self._dict_to_metadata(book))
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the book collection."""
        stats = {
            'total_books': len(self.registry['books']),
            'by_subject': {},
            'by_grade': {},
            'by_publisher': {},
            'by_book_type': {},
            'by_exam': {},
            'topics_coverage': {}
        }
        
        for book_id, book in self.registry['books'].items():
            # Count by subject
            subject = book['subject']
            stats['by_subject'][subject] = stats['by_subject'].get(subject, 0) + 1
            
            # Count by grade
            grade = book['primary_classification'].get('grade', 'unknown')
            stats['by_grade'][grade] = stats['by_grade'].get(grade, 0) + 1
            
            # Count by publisher
            publisher = book['publisher']
            stats['by_publisher'][publisher] = stats['by_publisher'].get(publisher, 0) + 1
            
            # Count by book type
            book_type = book['primary_classification'].get('type', 'unknown')
            stats['by_book_type'][book_type] = stats['by_book_type'].get(book_type, 0) + 1
            
            # Count by exam relevance
            for exam_rel in book.get('exam_relevance', []):
                exam = exam_rel['exam']
                stats['by_exam'][exam] = stats['by_exam'].get(exam, 0) + 1
        
        return stats
    
    def recommend_books_for_student(self, student_profile: Dict[str, Any]) -> Dict[str, List[BookMetadata]]:
        """
        Recommend books based on student profile.
        
        Student profile example:
        {
            "grade": "11",
            "target_exam": "jee_main", 
            "subjects": ["mathematics", "physics"],
            "current_level": "intermediate",
            "weak_topics": ["calculus", "mechanics"]
        }
        """
        recommendations = {
            "essential": [],
            "practice": [],
            "advanced": [],
            "weak_topics": []
        }
        
        grade = student_profile.get('grade')
        target_exam = student_profile.get('target_exam')
        subjects = student_profile.get('subjects', [])
        weak_topics = student_profile.get('weak_topics', [])
        
        # Get books for target exam
        if target_exam:
            for subject in subjects:
                exam_books = self.get_books_for_exam(target_exam, subject)
                for book in exam_books:
                    priority = getattr(book, 'priority', 'essential')
                    if priority in recommendations:
                        recommendations[priority].append(book)
        
        # Get books for weak topics
        for topic in weak_topics:
            topic_books = self.get_books_for_topic(topic, exam_context=target_exam)
            recommendations['weak_topics'].extend(topic_books)
        
        # Remove duplicates
        for category in recommendations:
            seen_ids = set()
            unique_books = []
            for book in recommendations[category]:
                if book.id not in seen_ids:
                    seen_ids.add(book.id)
                    unique_books.append(book)
            recommendations[category] = unique_books
        
        return recommendations
    
    def get_study_plan(self, exam: str, subject: str, 
                      time_available: int = 12) -> Dict[str, Any]:
        """
        Generate a study plan based on exam and time available (in months).
        """
        if exam not in self.registry.get('exam_profiles', {}):
            return {}
        
        exam_profile = self.registry['exam_profiles'][exam]
        topic_priorities = exam_profile.get('topic_priorities', {}).get(subject, {})
        
        # Distribute time based on priority
        time_distribution = {
            'high': time_available * 0.5,
            'medium': time_available * 0.3,
            'low': time_available * 0.2
        }
        
        study_plan = {}
        for priority, topics in topic_priorities.items():
            months_for_priority = time_distribution.get(priority, 0)
            months_per_topic = months_for_priority / len(topics) if topics else 0
            
            for topic in topics:
                # Get books for this topic
                topic_books = self.get_books_for_topic(topic, exam_context=exam)
                
                study_plan[topic] = {
                    'priority': priority,
                    'time_allocation_months': round(months_per_topic, 1),
                    'recommended_books': [book.title for book in topic_books[:3]],  # Top 3 books
                    'exam_weightage': self._get_topic_weightage(topic, exam)
                }
        
        return study_plan
    
    def migrate_from_old_registry(self, old_registry_path: str) -> bool:
        """Migrate from old registry format to enhanced format."""
        try:
            with open(old_registry_path, 'r') as f:
                old_registry = json.load(f)
            
            print("🔄 Migrating from old registry format...")
            migrated_count = 0
            
            # Process old format: subjects -> levels -> books
            for subject, subject_info in old_registry.get('subjects', {}).items():
                for grade, grade_info in subject_info.get('levels', {}).items():
                    for book_key, book_info in grade_info.get('books', {}).items():
                        
                        # Convert to new format
                        book_metadata = {
                            'title': book_info['title'],
                            'publisher': book_info['publisher'],
                            'subject': subject,
                            'grade': grade,
                            'book_type': book_info.get('type', 'textbook'),
                            'path': book_info.get('path', ''),
                            'chapters': self._convert_chapters_to_enhanced_format(
                                book_info.get('chapters', [])
                            ),
                            'exam_relevance': self._infer_exam_relevance(subject, grade, book_info['publisher'])
                        }
                        
                        if self.add_book(book_metadata):
                            migrated_count += 1
            
            print(f"✅ Migrated {migrated_count} books to enhanced format")
            return True
            
        except Exception as e:
            print(f"❌ Error migrating registry: {e}")
            return False
    
    def _convert_chapters_to_enhanced_format(self, chapters: List[str]) -> Dict[str, Any]:
        """Convert simple chapter list to enhanced chapter format."""
        enhanced_chapters = {}
        
        for i, chapter in enumerate(chapters, 1):
            chapter_key = chapter.lower().replace(' ', '_').replace(',', '').replace(':', '')
            chapter_key = re.sub(r'[^a-z0-9_]', '', chapter_key)
            
            enhanced_chapters[chapter_key] = {
                'number': i,
                'title': chapter,
                'exam_tags': ['board_exams'],  # Default
                'difficulty': 'foundation',
                'topics': self._extract_topics_from_chapter_name(chapter)
            }
        
        return enhanced_chapters
    
    def _extract_topics_from_chapter_name(self, chapter_name: str) -> List[str]:
        """Extract likely topic keywords from chapter name."""
        # Simple topic extraction based on common patterns
        topic_mappings = {
            'polynomial': ['polynomials', 'factorization'],
            'quadratic': ['quadratic_equations', 'discriminant'],
            'trigonometr': ['trigonometric_functions', 'identities'],
            'coordinate': ['coordinate_geometry', 'distance_formula'],
            'calculus': ['limits', 'derivatives', 'integrals'],
            'limit': ['limits', 'continuity'],
            'derivative': ['derivatives', 'applications'],
            'integral': ['integrals', 'applications'],
            'probability': ['probability', 'statistics'],
            'statistic': ['statistics', 'data_analysis']
        }
        
        chapter_lower = chapter_name.lower()
        topics = []
        
        for keyword, topic_list in topic_mappings.items():
            if keyword in chapter_lower:
                topics.extend(topic_list)
        
        return topics if topics else [chapter_name.lower().replace(' ', '_')]
    
    def _infer_exam_relevance(self, subject: str, grade: str, publisher: str) -> List[Dict[str, Any]]:
        """Infer exam relevance based on subject, grade, and publisher."""
        relevance = []
        
        # Board exams always relevant
        relevance.append({"exam": "board_exams", "relevance": 1.0, "priority": "essential"})
        
        # JEE relevance for math/physics/chemistry grades 11-12
        if subject in ['mathematics', 'physics', 'chemistry'] and grade in ['11', '12']:
            if publisher == 'NCERT':
                relevance.extend([
                    {"exam": "jee_main", "relevance": 0.95, "priority": "essential"},
                    {"exam": "jee_advanced", "relevance": 0.80, "priority": "foundation"}
                ])
            elif publisher in ['RD Sharma', 'HC Verma']:
                relevance.extend([
                    {"exam": "jee_main", "relevance": 0.90, "priority": "high"},
                    {"exam": "jee_advanced", "relevance": 0.85, "priority": "high"}
                ])
        
        # NEET relevance for physics/chemistry/biology
        if subject in ['physics', 'chemistry', 'biology'] and grade in ['11', '12']:
            relevance.append({"exam": "neet", "relevance": 0.85, "priority": "high"})
        
        return relevance
    
    def _get_topic_weightage(self, topic: str, exam: str) -> int:
        """Get topic weightage for specific exam."""
        topic_taxonomy = self.registry.get('topic_taxonomy', {})
        
        for subject, subjects_topics in topic_taxonomy.items():
            if topic in subjects_topics:
                return subjects_topics[topic].get('exam_weightage', {}).get(exam, 0)
        
        return 0
    
    def _dict_to_metadata(self, book_dict: Dict[str, Any]) -> BookMetadata:
        """Convert book dictionary to BookMetadata object."""
        return BookMetadata(
            id=book_dict['id'],
            title=book_dict['title'],
            publisher=book_dict['publisher'],
            subject=book_dict['subject'],
            path=book_dict['path'],
            primary_classification=book_dict['primary_classification'],
            exam_relevance=book_dict['exam_relevance'],
            chapters=book_dict.get('chapters'),
            status=book_dict.get('status', 'active'),
            complements=book_dict.get('complements'),
            covers_topics=book_dict.get('covers_topics')
        )
    
    def _generate_book_id(self, metadata: Dict[str, Any]) -> str:
        """Generate unique book ID."""
        # Create readable ID: publisher_subject_grade
        publisher = metadata['publisher'].lower().replace(' ', '_')
        subject = metadata['subject'].lower()
        grade = str(metadata.get('grade', 'general'))
        
        return f"{publisher}_{subject}_{grade}"
    
    def _rebuild_caches(self):
        """Rebuild internal caches for quick lookups."""
        self._book_cache = {book['id']: book for book in self.registry['books'].values()}
        self._exam_cache = self.registry.get('exam_profiles', {})
        self._topic_cache = self.registry.get('topic_taxonomy', {})
    
    def _save_registry(self, registry: Optional[Dict[str, Any]] = None):
        """Save registry to file."""
        registry = registry or self.registry
        registry['last_updated'] = datetime.now().isoformat()
        
        with open(self.registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def validate(self) -> bool:
        """Validate the enhanced registry structure."""
        try:
            # Check required top-level keys
            required_keys = ['books', 'exam_profiles', 'topic_taxonomy']
            for key in required_keys:
                if key not in self.registry:
                    print(f"❌ Missing key: {key}")
                    return False
            
            # Validate book entries
            for book_id, book in self.registry['books'].items():
                # Check required book fields
                required_book_fields = ['title', 'publisher', 'subject', 'primary_classification']
                for field in required_book_fields:
                    if field not in book:
                        print(f"❌ Book {book_id} missing field: {field}")
                        return False
                
                # Check if book path exists
                book_path = Path(self.config.TEXTBOOKS_PATH) / book.get('path', '')
                if book.get('status') == 'active' and not book_path.exists():
                    print(f"⚠️ Book content not found: {book['title']} at {book_path}")
            
            print("✅ Enhanced registry validation successful")
            return True
            
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
