"""
Book Registry Manager for Klaro
================================

Manages registration and organization of textbooks and educational content.
"""

from typing import Dict, List, Optional, Any
import json
from pathlib import Path
import shutil
import hashlib
from datetime import datetime

from ..utils.config import get_config


class BookRegistryManager:
    """Manages the registration and organization of educational content."""
    
    def __init__(self, registry_path: Optional[str] = None):
        """Initialize book registry manager."""
        self.config = get_config()
        self.registry_path = registry_path or self.config.BOOK_REGISTRY_PATH
        self.textbooks_path = Path(self.config.TEXTBOOKS_PATH)
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load the book registry from file."""
        try:
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Registry file not found at {self.registry_path}")
            print("Creating new registry...")
            return self._create_default_registry()
    
    def _create_default_registry(self) -> Dict[str, Any]:
        """Create a default registry structure."""
        default_registry = {
            "version": "2.0.0",
            "last_updated": datetime.now().isoformat(),
            "subjects": {},
            "categories": {
                "textbook": {"name": "Core Textbook", "description": "Standard curriculum textbooks"},
                "practice": {"name": "Practice Book", "description": "Additional practice problems"},
                "advanced": {"name": "Advanced Level", "description": "Competitive exam preparation"}
            },
            "exam_mappings": {}
        }
        
        # Save default registry
        with open(self.registry_path, 'w') as f:
            json.dump(default_registry, f, indent=2)
        
        return default_registry
    
    def add_book(self, book_path: str, metadata: Dict[str, Any]) -> bool:
        """
        Add a new book to the registry.
        
        Args:
            book_path: Path to the book file/directory
            metadata: Book metadata including:
                - subject: Subject name
                - grade: Grade/class level
                - title: Book title
                - publisher: Publisher name
                - type: Book type (textbook/practice/advanced)
                - chapters: List of chapters
        """
        try:
            # Validate metadata
            required_fields = ['subject', 'grade', 'title', 'publisher', 'type']
            for field in required_fields:
                if field not in metadata:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create subject if not exists
            subject = metadata['subject'].lower()
            if subject not in self.registry['subjects']:
                self.registry['subjects'][subject] = {
                    "name": metadata['subject'],
                    "levels": {}
                }
            
            # Create grade level if not exists
            grade = str(metadata['grade'])
            if grade not in self.registry['subjects'][subject]['levels']:
                self.registry['subjects'][subject]['levels'][grade] = {
                    "name": f"Class {grade}",
                    "books": {}
                }
            
            # Generate book ID
            book_id = self._generate_book_id(metadata)
            
            # Calculate target path
            rel_path = f"textbooks/{metadata['publisher'].lower()}/{subject}/class_{grade:02d}"
            target_path = self.textbooks_path / rel_path
            
            # Create book entry
            book_entry = {
                "title": metadata['title'],
                "publisher": metadata['publisher'],
                "type": metadata['type'],
                "path": str(rel_path),
                "chapters": metadata.get('chapters', []),
                "status": "active"
            }
            
            # Optional metadata fields
            optional_fields = ['description', 'author', 'edition', 'year', 'isbn']
            for field in optional_fields:
                if field in metadata:
                    book_entry[field] = metadata[field]
            
            # Add to registry
            self.registry['subjects'][subject]['levels'][grade]['books'][book_id] = book_entry
            
            # Create directory structure
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Copy/move book content if path provided
            if Path(book_path).exists():
                if Path(book_path).is_file():
                    shutil.copy2(book_path, target_path)
                else:
                    shutil.copytree(book_path, target_path, dirs_exist_ok=True)
            
            # Update registry file
            self._save_registry()
            
            print(f"✅ Added book: {metadata['title']}")
            print(f"📁 Content location: {target_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding book: {e}")
            return False
    
    def get_book_info(self, subject: str, grade: str, book_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific book."""
        try:
            return self.registry['subjects'][subject.lower()]['levels'][str(grade)]['books'][book_id]
        except KeyError:
            return None
    
    def get_subject_books(self, subject: str, grade: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all books for a subject and optional grade level."""
        books = []
        subject = subject.lower()
        
        if subject not in self.registry['subjects']:
            return books
        
        levels = self.registry['subjects'][subject]['levels']
        
        if grade:
            grade = str(grade)
            if grade in levels:
                return [
                    {**info, 'id': book_id, 'grade': grade}
                    for book_id, info in levels[grade]['books'].items()
                ]
        else:
            for grade, grade_info in levels.items():
                books.extend([
                    {**info, 'id': book_id, 'grade': grade}
                    for book_id, info in grade_info['books'].items()
                ])
        
        return books
    
    def get_exam_books(self, exam: str) -> List[Dict[str, Any]]:
        """Get recommended books for a specific exam."""
        if exam not in self.registry['exam_mappings']:
            return []
        
        exam_info = self.registry['exam_mappings'][exam]
        books = []
        
        for book_path in exam_info['recommended_books']:
            parts = book_path.split('/')
            if len(parts) >= 4:  # publisher/subject/class_XX
                publisher = parts[1]
                subject = parts[2]
                grade = parts[3].replace('class_', '')
                
                # Find matching books
                subject_books = self.get_subject_books(subject, grade)
                for book in subject_books:
                    if book['publisher'].lower() == publisher:
                        books.append(book)
        
        return books
    
    def update_book_status(self, subject: str, grade: str, book_id: str, 
                          status: str, message: Optional[str] = None) -> bool:
        """Update a book's status (active/pending/archived)."""
        try:
            book = self.registry['subjects'][subject.lower()]['levels'][str(grade)]['books'][book_id]
            book['status'] = status
            if message:
                book['status_message'] = message
            book['last_updated'] = datetime.now().isoformat()
            
            self._save_registry()
            return True
        except KeyError:
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about registered books."""
        stats = {
            'total_books': 0,
            'subjects': {},
            'publishers': set(),
            'book_types': {
                'textbook': 0,
                'practice': 0,
                'advanced': 0
            }
        }
        
        for subject, subject_info in self.registry['subjects'].items():
            subject_books = 0
            subject_stats = {'total': 0, 'by_grade': {}}
            
            for grade, grade_info in subject_info['levels'].items():
                grade_books = len(grade_info['books'])
                subject_books += grade_books
                subject_stats['by_grade'][grade] = grade_books
                
                for book_id, book in grade_info['books'].items():
                    stats['publishers'].add(book['publisher'])
                    stats['book_types'][book['type']] += 1
            
            subject_stats['total'] = subject_books
            stats['subjects'][subject] = subject_stats
            stats['total_books'] += subject_books
        
        stats['publishers'] = list(stats['publishers'])
        return stats
    
    def validate(self) -> bool:
        """Validate the registry and book organization."""
        try:
            # Check registry file exists
            if not Path(self.registry_path).exists():
                print("❌ Registry file not found")
                return False
            
            # Check registry structure
            required_keys = ['version', 'subjects', 'categories', 'exam_mappings']
            for key in required_keys:
                if key not in self.registry:
                    print(f"❌ Missing required key in registry: {key}")
                    return False
            
            # Check textbook directories
            for subject in self.registry['subjects']:
                for grade, grade_info in self.registry['subjects'][subject]['levels'].items():
                    for book_id, book in grade_info['books'].items():
                        book_path = self.textbooks_path / book['path']
                        if not book_path.exists():
                            print(f"❌ Missing book content: {book['title']} at {book_path}")
                            return False
            
            print("✅ Registry validation successful")
            return True
            
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
    
    def _generate_book_id(self, metadata: Dict[str, Any]) -> str:
        """Generate a unique book ID based on metadata."""
        id_string = f"{metadata['publisher']}_{metadata['subject']}_{metadata['grade']}_{metadata['title']}"
        return hashlib.md5(id_string.lower().encode()).hexdigest()[:8]
    
    def _save_registry(self):
        """Save the current registry to file."""
        self.registry['last_updated'] = datetime.now().isoformat()
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def get_available_books(self) -> Dict[str, List[str]]:
        """Get a list of available books organized by subject and grade."""
        available_books = {}
        
        for subject, subject_info in self.registry['subjects'].items():
            available_books[subject] = []
            
            for grade, grade_info in subject_info['levels'].items():
                for book_id, book in grade_info['books'].items():
                    if book['status'] == 'active':
                        available_books[subject].append(
                            f"{book['title']} (Class {grade})"
                        )
        
        return available_books
