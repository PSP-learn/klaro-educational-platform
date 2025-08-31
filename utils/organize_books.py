#!/usr/bin/env python3
"""
🎓 Book Organization Helper
==========================

Helps organize books by publisher, subject, and grade level.
Creates proper directory structure and updates book registry.

Usage:
    python organize_books.py organize --source <source_dir> --publisher <publisher> --subject <subject>
    python organize_books.py validate
    python organize_books.py stats

Example:
    python organize_books.py organize --source ~/Downloads/rd_sharma --publisher "RD Sharma" --subject mathematics
"""

import argparse
import sys
from pathlib import Path
import shutil
import re
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.book_registry import BookRegistryManager
from utils.config import get_config


class BookOrganizer:
    """Helper for organizing educational books."""
    
    def __init__(self):
        """Initialize book organizer."""
        self.config = get_config()
        self.book_registry = BookRegistryManager()
        
        # Known publishers and their common names
        self.publisher_aliases = {
            'ncert': 'NCERT',
            'rd sharma': 'RD Sharma',
            'rd_sharma': 'RD Sharma',
            'cengage': 'Cengage Learning',
            'hc verma': 'HC Verma',
            'hc_verma': 'HC Verma'
        }
    
    def organize_books(self, source_dir: str, publisher: str, subject: str) -> bool:
        """
        Organize books from source directory into proper structure.
        
        Args:
            source_dir: Source directory containing books
            publisher: Publisher name
            subject: Subject name
        """
        try:
            source_path = Path(source_dir)
            if not source_path.exists():
                print(f"❌ Source directory not found: {source_dir}")
                return False
            
            # Normalize publisher and subject names
            publisher = self._normalize_publisher(publisher)
            subject = subject.lower()
            
            print(f"🔍 Scanning {source_dir} for {publisher} {subject} books...")
            
            # Find grade-specific directories or files
            grade_pattern = re.compile(r'(?:class|grade)[_\s-]*(\d{1,2})', re.IGNORECASE)
            
            organized_count = 0
            
            for item in source_path.glob('**/*'):
                if item.is_dir() and not item.name.startswith('.'):
                    # Try to extract grade from directory name
                    grade_match = grade_pattern.search(item.name)
                    if grade_match:
                        grade = int(grade_match.group(1))
                        print(f"\n📚 Found Grade {grade} content in: {item.name}")
                        
                        # Create metadata for this book
                        metadata = {
                            'subject': subject,
                            'grade': grade,
                            'publisher': publisher,
                            'title': f"{publisher} {subject.title()} Class {grade}",
                            'type': self._detect_book_type(publisher),
                            'chapters': self._detect_chapters(item)
                        }
                        
                        # Add to registry and organize
                        if self.book_registry.add_book(str(item), metadata):
                            organized_count += 1
                
                elif item.is_file() and item.suffix.lower() in ['.pdf', '.epub']:
                    # Try to extract grade from filename
                    grade_match = grade_pattern.search(item.name)
                    if grade_match:
                        grade = int(grade_match.group(1))
                        print(f"\n📖 Found Grade {grade} book: {item.name}")
                        
                        metadata = {
                            'subject': subject,
                            'grade': grade,
                            'publisher': publisher,
                            'title': item.stem,
                            'type': self._detect_book_type(publisher)
                        }
                        
                        if self.book_registry.add_book(str(item), metadata):
                            organized_count += 1
            
            print(f"\n✅ Organized {organized_count} books from {publisher}")
            return True
            
        except Exception as e:
            print(f"❌ Error organizing books: {e}")
            return False
    
    def validate_organization(self) -> bool:
        """Validate the book organization."""
        print("🔍 Validating book organization...")
        
        # Check basic registry validation
        if not self.book_registry.validate():
            return False
        
        # Get statistics
        stats = self.book_registry.get_statistics()
        
        print("\n📊 Current Status:")
        print(f"Total Books: {stats['total_books']}")
        print("\nBy Subject:")
        for subject, subject_stats in stats['subjects'].items():
            print(f"  {subject.title()}: {subject_stats['total']} books")
            for grade, count in subject_stats['by_grade'].items():
                print(f"    Grade {grade}: {count} books")
        
        print("\nBy Type:")
        for book_type, count in stats['book_types'].items():
            print(f"  {book_type.title()}: {count} books")
        
        print("\nPublishers:")
        for publisher in stats['publishers']:
            print(f"  • {publisher}")
        
        return True
    
    def show_statistics(self):
        """Show detailed statistics about organized books."""
        stats = self.book_registry.get_statistics()
        
        print("\n📚 Book Collection Statistics")
        print("=" * 40)
        
        # Overall stats
        print(f"\n📊 Overall Statistics:")
        print(f"Total Books: {stats['total_books']}")
        print(f"Total Publishers: {len(stats['publishers'])}")
        print(f"Active Subjects: {len(stats['subjects'])}")
        
        # Book types
        print(f"\n📑 By Book Type:")
        for book_type, count in stats['book_types'].items():
            percentage = (count / stats['total_books']) * 100 if stats['total_books'] > 0 else 0
            print(f"  {book_type.title()}: {count} ({percentage:.1f}%)")
        
        # Subject breakdown
        print(f"\n📗 By Subject:")
        for subject, subject_stats in stats['subjects'].items():
            print(f"\n{subject.title()}:")
            print(f"  Total: {subject_stats['total']} books")
            print("  Grade distribution:")
            for grade, count in subject_stats['by_grade'].items():
                print(f"    Grade {grade}: {count} books")
        
        # Publisher details
        print(f"\n📖 Publishers:")
        for publisher in sorted(stats['publishers']):
            print(f"  • {publisher}")
        
        print("\n" + "=" * 40)
    
    def _normalize_publisher(self, publisher: str) -> str:
        """Normalize publisher name using known aliases."""
        lookup = publisher.lower().replace(' ', '_')
        return self.publisher_aliases.get(lookup, publisher)
    
    def _detect_book_type(self, publisher: str) -> str:
        """Detect book type based on publisher."""
        publisher_types = {
            'NCERT': 'textbook',
            'RD Sharma': 'practice',
            'Cengage Learning': 'advanced',
            'HC Verma': 'advanced'
        }
        return publisher_types.get(publisher, 'textbook')
    
    def _detect_chapters(self, directory: Path) -> List[str]:
        """Try to detect chapter names from directory structure."""
        chapters = []
        chapter_pattern = re.compile(r'chapter[_\s-]*(\d+)', re.IGNORECASE)
        
        for item in sorted(directory.glob('*')):
            if item.is_dir():
                # Try to match chapter directory
                if chapter_match := chapter_pattern.search(item.name):
                    chapter_num = int(chapter_match.group(1))
                    # Clean up chapter name
                    chapter_name = item.name.split('_')[-1].replace('-', ' ').title()
                    chapters.append(f"Chapter {chapter_num}: {chapter_name}")
                
                # Or check if directory name looks like a chapter name
                elif not any(x in item.name.lower() for x in ['assignment', 'exercise', 'solution']):
                    chapters.append(item.name.replace('_', ' ').title())
        
        return chapters


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="🎓 Klaro Book Organization Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Organize RD Sharma books:
    python organize_books.py organize --source ~/Downloads/rd_sharma --publisher "RD Sharma" --subject mathematics
  
  Validate organization:
    python organize_books.py validate
  
  Show statistics:
    python organize_books.py stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Organize command
    organize_parser = subparsers.add_parser('organize', help='Organize books into proper structure')
    organize_parser.add_argument('--source', required=True, help='Source directory containing books')
    organize_parser.add_argument('--publisher', required=True, help='Publisher name')
    organize_parser.add_argument('--subject', required=True, help='Subject name')
    
    # Validate command
    subparsers.add_parser('validate', help='Validate current organization')
    
    # Stats command
    subparsers.add_parser('stats', help='Show detailed statistics')
    
    args = parser.parse_args()
    
    # Create organizer
    organizer = BookOrganizer()
    
    if args.command == 'organize':
        success = organizer.organize_books(
            source_dir=args.source,
            publisher=args.publisher,
            subject=args.subject
        )
        if success:
            print("\n✅ Books organized successfully!")
            print("Run 'validate' command to verify organization")
        sys.exit(0 if success else 1)
    
    elif args.command == 'validate':
        success = organizer.validate_organization()
        sys.exit(0 if success else 1)
    
    elif args.command == 'stats':
        organizer.show_statistics()
        sys.exit(0)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
