#!/usr/bin/env python3
"""
PDF Book Organizer

This script helps organize PDF books into structured directories based on different
organizational strategies: subject-first, purpose-first, publisher-first, or mixed.

Features:
- Extract metadata from PDF files (title, author, subject, etc.)
- Multiple organization strategies
- Safe file operations with backup options
- Duplicate detection and handling
- Customizable folder structures
"""

import os
import shutil
import json
import argparse
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

import fitz  # PyMuPDF

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class BookInfo:
    """Book information extracted from PDF"""
    file_path: str
    title: str
    author: str = ""
    subject: str = ""
    creator: str = ""
    producer: str = ""
    creation_date: str = ""
    modification_date: str = ""
    keywords: str = ""
    file_size: int = 0
    page_count: int = 0

class OrganizationStrategy:
    """Base class for organization strategies"""
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def get_target_path(self, book: BookInfo) -> Path:
        """Get target path for the book based on organization strategy"""
        raise NotImplementedError
    
    def sanitize_name(self, name: str) -> str:
        """Sanitize name for use as directory/file name"""
        # Remove invalid characters and replace with underscores
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
        # Remove multiple consecutive underscores/spaces
        sanitized = re.sub(r'[_\s]+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        # Limit length
        return sanitized[:100] if sanitized else "Unknown"

class SubjectFirstStrategy(OrganizationStrategy):
    """Subject/Topic-based organization"""
    
    def __init__(self, base_dir: str, subject_mapping: Optional[Dict[str, str]] = None):
        super().__init__(base_dir)
        self.subject_mapping = subject_mapping or self._default_subject_mapping()
    
    def _default_subject_mapping(self) -> Dict[str, str]:
        """Default subject mapping based on keywords"""
        return {
            'programming': ['python', 'java', 'javascript', 'programming', 'coding', 'software', 'development'],
            'data_science': ['data', 'science', 'machine learning', 'ai', 'artificial intelligence', 'statistics'],
            'business': ['business', 'management', 'marketing', 'finance', 'economics', 'entrepreneurship'],
            'design': ['design', 'ui', 'ux', 'user experience', 'interface', 'graphics'],
            'mathematics': ['math', 'mathematics', 'calculus', 'algebra', 'geometry', 'statistics'],
            'science': ['physics', 'chemistry', 'biology', 'science', 'research'],
            'technology': ['technology', 'tech', 'computer', 'digital', 'internet', 'web'],
            'personal_development': ['self help', 'personal', 'development', 'productivity', 'habits'],
            'fiction': ['novel', 'fiction', 'story', 'fantasy', 'sci-fi', 'romance'],
            'reference': ['reference', 'manual', 'guide', 'handbook', 'documentation']
        }
    
    def _categorize_by_subject(self, book: BookInfo) -> str:
        """Categorize book by subject"""
        text_to_check = f"{book.title} {book.subject} {book.keywords}".lower()
        
        for category, keywords in self.subject_mapping.items():
            if any(keyword.lower() in text_to_check for keyword in keywords):
                return category
        
        return 'miscellaneous'
    
    def get_target_path(self, book: BookInfo) -> Path:
        """Get target path: base_dir/subject/author/title.pdf"""
        subject = self._categorize_by_subject(book)
        author = self.sanitize_name(book.author) if book.author else "Unknown_Author"
        title = self.sanitize_name(book.title)
        
        return self.base_dir / subject / author / f"{title}.pdf"

class PurposeFirstStrategy(OrganizationStrategy):
    """Purpose-based organization (Reference, Learning, Research, etc.)"""
    
    def __init__(self, base_dir: str):
        super().__init__(base_dir)
        self.purpose_keywords = {
            'reference': ['reference', 'manual', 'guide', 'handbook', 'documentation', 'cookbook'],
            'learning': ['tutorial', 'course', 'beginner', 'introduction', 'learn', 'teach'],
            'research': ['research', 'study', 'analysis', 'academic', 'journal', 'paper'],
            'project_books': ['project', 'practical', 'hands-on', 'workshop', 'build'],
            'quick_ref': ['quick', 'cheat sheet', 'summary', 'brief', 'pocket']
        }
    
    def _categorize_by_purpose(self, book: BookInfo) -> str:
        """Categorize book by purpose"""
        text_to_check = f"{book.title} {book.subject} {book.keywords}".lower()
        
        for purpose, keywords in self.purpose_keywords.items():
            if any(keyword.lower() in text_to_check for keyword in keywords):
                return purpose
        
        return 'general'
    
    def get_target_path(self, book: BookInfo) -> Path:
        """Get target path: base_dir/purpose/subject/title.pdf"""
        purpose = self._categorize_by_purpose(book)
        # Use SubjectFirstStrategy for secondary categorization
        subject_strategy = SubjectFirstStrategy("")
        subject = subject_strategy._categorize_by_subject(book)
        title = self.sanitize_name(book.title)
        
        return self.base_dir / purpose / subject / f"{title}.pdf"

class PublisherFirstStrategy(OrganizationStrategy):
    """Publisher/Source-based organization"""
    
    def __init__(self, base_dir: str):
        super().__init__(base_dir)
        self.publisher_mapping = {
            'oreilly': ['o\'reilly', 'oreilly'],
            'manning': ['manning'],
            'packt': ['packt'],
            'apress': ['apress'],
            'wiley': ['wiley'],
            'pearson': ['pearson', 'addison-wesley'],
            'springer': ['springer'],
            'mit_press': ['mit press'],
            'academic': ['academic', 'university', 'press']
        }
    
    def _categorize_by_publisher(self, book: BookInfo) -> str:
        """Categorize book by publisher"""
        text_to_check = f"{book.producer} {book.creator}".lower()
        
        for publisher, keywords in self.publisher_mapping.items():
            if any(keyword.lower() in text_to_check for keyword in keywords):
                return publisher
        
        return 'other_publishers'
    
    def get_target_path(self, book: BookInfo) -> Path:
        """Get target path: base_dir/publisher/subject/title.pdf"""
        publisher = self._categorize_by_publisher(book)
        # Use SubjectFirstStrategy for secondary categorization
        subject_strategy = SubjectFirstStrategy("")
        subject = subject_strategy._categorize_by_subject(book)
        title = self.sanitize_name(book.title)
        
        return self.base_dir / publisher / subject / f"{title}.pdf"

class MixedStrategy(OrganizationStrategy):
    """Mixed organization strategy combining multiple approaches"""
    
    def __init__(self, base_dir: str):
        super().__init__(base_dir)
        self.subject_strategy = SubjectFirstStrategy("")
        self.purpose_strategy = PurposeFirstStrategy("")
    
    def get_target_path(self, book: BookInfo) -> Path:
        """Get target path: base_dir/subject/purpose/author/title.pdf"""
        subject = self.subject_strategy._categorize_by_subject(book)
        purpose = self.purpose_strategy._categorize_by_purpose(book)
        author = self.sanitize_name(book.author) if book.author else "Unknown_Author"
        title = self.sanitize_name(book.title)
        
        return self.base_dir / subject / purpose / author / f"{title}.pdf"

class BookOrganizer:
    """Main organizer class"""
    
    def __init__(self, strategy: OrganizationStrategy, dry_run: bool = False):
        self.strategy = strategy
        self.dry_run = dry_run
        self.processed_books: List[BookInfo] = []
        self.errors: List[str] = []
        self.duplicates: List[Tuple[str, str]] = []
    
    def extract_metadata(self, pdf_path: str) -> Optional[BookInfo]:
        """Extract metadata from PDF file"""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            page_count = len(doc)
            doc.close()
            
            file_stat = os.stat(pdf_path)
            
            # Clean up title
            title = metadata.get('title', '') or Path(pdf_path).stem
            title = title.replace('_', ' ').replace('-', ' ').strip()
            
            book_info = BookInfo(
                file_path=pdf_path,
                title=title,
                author=metadata.get('author', '').strip(),
                subject=metadata.get('subject', '').strip(),
                creator=metadata.get('creator', '').strip(),
                producer=metadata.get('producer', '').strip(),
                creation_date=metadata.get('creationDate', ''),
                modification_date=metadata.get('modDate', ''),
                keywords=metadata.get('keywords', '').strip(),
                file_size=file_stat.st_size,
                page_count=page_count
            )
            
            return book_info
            
        except Exception as e:
            logger.error(f"Failed to extract metadata from {pdf_path}: {e}")
            return None
    
    def find_duplicates(self, books: List[BookInfo]) -> List[Tuple[BookInfo, BookInfo]]:
        """Find potential duplicate books based on title similarity"""
        duplicates = []
        
        for i, book1 in enumerate(books):
            for book2 in books[i+1:]:
                # Simple duplicate detection based on title similarity
                title1 = book1.title.lower().strip()
                title2 = book2.title.lower().strip()
                
                # Check if titles are very similar (after removing common words)
                if self._titles_similar(title1, title2):
                    duplicates.append((book1, book2))
        
        return duplicates
    
    def _titles_similar(self, title1: str, title2: str, threshold: float = 0.8) -> bool:
        """Check if two titles are similar"""
        # Simple similarity check
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if not words1 or not words2:
            return False
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union) if union else 0
        return similarity >= threshold
    
    def organize_file(self, book: BookInfo) -> bool:
        """Organize a single file"""
        source_path = Path(book.file_path)
        target_path = self.strategy.get_target_path(book)
        
        # Skip if source and target are the same
        if source_path.resolve() == target_path.resolve():
            logger.info(f"File already in correct location: {source_path}")
            return True
        
        # Check if target already exists
        if target_path.exists():
            if target_path.stat().st_size == source_path.stat().st_size:
                logger.warning(f"Duplicate found: {target_path} (skipping)")
                self.duplicates.append((str(source_path), str(target_path)))
                return False
        
        if self.dry_run:
            print(f"DRY RUN: Would move {source_path} -> {target_path}")
            return True
        
        try:
            # Create target directory
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            shutil.move(str(source_path), str(target_path))
            logger.info(f"Moved: {source_path} -> {target_path}")
            
            # Update book info with new path
            book.file_path = str(target_path)
            return True
            
        except Exception as e:
            error_msg = f"Failed to move {source_path} -> {target_path}: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False
    
    def organize_directory(self, directory: str) -> Dict:
        """Organize all PDF files in directory"""
        directory = Path(directory)
        
        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        
        # Find all PDF files
        pdf_files = list(directory.rglob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files to organize")
        
        if not pdf_files:
            logger.warning("No PDF files found")
            return {"processed": 0, "errors": [], "duplicates": []}
        
        # Extract metadata from all files
        books = []
        for pdf_path in pdf_files:
            book_info = self.extract_metadata(str(pdf_path))
            if book_info:
                books.append(book_info)
        
        logger.info(f"Successfully extracted metadata from {len(books)} books")
        
        # Find duplicates
        duplicates = self.find_duplicates(books)
        if duplicates:
            logger.warning(f"Found {len(duplicates)} potential duplicate pairs")
            for book1, book2 in duplicates:
                logger.warning(f"  Duplicate: '{book1.title}' vs '{book2.title}'")
        
        # Organize files
        successful = 0
        for book in books:
            if self.organize_file(book):
                successful += 1
                self.processed_books.append(book)
        
        return {
            "processed": successful,
            "total_found": len(pdf_files),
            "metadata_extracted": len(books),
            "errors": self.errors,
            "duplicates": self.duplicates
        }
    
    def generate_report(self, output_file: str = "organization_report.json"):
        """Generate organization report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "strategy": self.strategy.__class__.__name__,
            "total_processed": len(self.processed_books),
            "errors_count": len(self.errors),
            "duplicates_count": len(self.duplicates),
            "books": [asdict(book) for book in self.processed_books],
            "errors": self.errors,
            "duplicates": self.duplicates
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to {output_file}")

def create_strategy(strategy_name: str, base_dir: str, **kwargs) -> OrganizationStrategy:
    """Factory function to create organization strategy"""
    strategies = {
        'subject': SubjectFirstStrategy,
        'purpose': PurposeFirstStrategy,
        'publisher': PublisherFirstStrategy,
        'mixed': MixedStrategy
    }
    
    if strategy_name not in strategies:
        raise ValueError(f"Unknown strategy: {strategy_name}. Available: {list(strategies.keys())}")
    
    return strategies[strategy_name](base_dir, **kwargs)

def preview_organization(directory: str, strategy: OrganizationStrategy, max_preview: int = 20):
    """Preview how files would be organized"""
    directory = Path(directory)
    pdf_files = list(directory.rglob("*.pdf"))[:max_preview]
    
    if not pdf_files:
        print("No PDF files found for preview")
        return
    
    print(f"\n📋 Organization Preview (showing first {len(pdf_files)} files):")
    print("=" * 80)
    
    organizer = BookOrganizer(strategy, dry_run=True)
    
    for pdf_path in pdf_files:
        book_info = organizer.extract_metadata(str(pdf_path))
        if book_info:
            target_path = strategy.get_target_path(book_info)
            relative_target = target_path.relative_to(strategy.base_dir)
            
            print(f"\n📖 {Path(pdf_path).name}")
            print(f"   Title: {book_info.title}")
            print(f"   Author: {book_info.author or 'Unknown'}")
            print(f"   Target: {relative_target}")

def main():
    parser = argparse.ArgumentParser(description="PDF Book Organizer")
    parser.add_argument('source_dir', help='Source directory containing PDF books')
    parser.add_argument('target_dir', help='Target directory for organized books')
    parser.add_argument('--strategy', '-s', choices=['subject', 'purpose', 'publisher', 'mixed'],
                       default='subject', help='Organization strategy')
    parser.add_argument('--dry-run', action='store_true', help='Preview organization without moving files')
    parser.add_argument('--preview', action='store_true', help='Show organization preview')
    parser.add_argument('--report', type=str, default='organization_report.json',
                       help='Output file for organization report')
    parser.add_argument('--subject-mapping', type=str, help='JSON file with custom subject mapping')
    
    args = parser.parse_args()
    
    # Validate directories
    if not os.path.exists(args.source_dir):
        logger.error(f"Source directory does not exist: {args.source_dir}")
        return
    
    # Load custom subject mapping if provided
    subject_mapping = None
    if args.subject_mapping and os.path.exists(args.subject_mapping):
        with open(args.subject_mapping, 'r') as f:
            subject_mapping = json.load(f)
        logger.info(f"Loaded custom subject mapping from {args.subject_mapping}")
    
    # Create strategy
    strategy_kwargs = {}
    if args.strategy == 'subject' and subject_mapping:
        strategy_kwargs['subject_mapping'] = subject_mapping
    
    strategy = create_strategy(args.strategy, args.target_dir, **strategy_kwargs)
    
    # Preview mode
    if args.preview:
        preview_organization(args.source_dir, strategy)
        return
    
    # Initialize organizer
    organizer = BookOrganizer(strategy, dry_run=args.dry_run)
    
    print(f"🚀 Starting organization with {args.strategy} strategy")
    print(f"Source: {args.source_dir}")
    print(f"Target: {args.target_dir}")
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be moved")
    
    # Organize files
    try:
        result = organizer.organize_directory(args.source_dir)
        
        # Print summary
        print(f"\n📊 Organization Summary:")
        print("=" * 50)
        print(f"Files found: {result['total_found']}")
        print(f"Metadata extracted: {result['metadata_extracted']}")
        print(f"Successfully processed: {result['processed']}")
        print(f"Errors: {len(result['errors'])}")
        print(f"Duplicates found: {len(result['duplicates'])}")
        
        if result['errors']:
            print(f"\n❌ Errors:")
            for error in result['errors']:
                print(f"  • {error}")
        
        if result['duplicates']:
            print(f"\n🔄 Duplicates:")
            for src, dst in result['duplicates']:
                print(f"  • {Path(src).name} -> {Path(dst).name}")
        
        # Generate report
        if not args.dry_run:
            organizer.generate_report(args.report)
            print(f"\n📄 Full report saved to: {args.report}")
        
    except KeyboardInterrupt:
        print("\n❌ Organization cancelled by user")
    except Exception as e:
        logger.error(f"Organization failed: {e}")

if __name__ == "__main__":
    main()
