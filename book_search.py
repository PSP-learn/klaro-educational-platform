#!/usr/bin/env python3
"""
PDF Book Search System

This script extracts text from PDF books, creates embeddings using sentence-transformers,
and provides semantic search capabilities using FAISS vector database.

Features:
- Extract text from PDF files using multiple methods (PyMuPDF, pdfplumber)
- Generate embeddings using sentence-transformers
- Store embeddings in FAISS vector database
- Semantic search across your book collection
- Metadata tracking (book title, author, page numbers, file path)
"""

import os
import json
import pickle
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

import fitz  # PyMuPDF
import pdfplumber
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class BookMetadata:
    """Metadata for a book and its text chunks"""
    file_path: str
    title: str
    author: str = ""
    page_count: int = 0
    file_size: int = 0
    last_modified: str = ""
    chunks_count: int = 0

@dataclass
class TextChunk:
    """A chunk of text with its metadata"""
    text: str
    book_title: str
    page_number: int
    file_path: str
    chunk_id: str
    chunk_index: int

class PDFTextExtractor:
    """Extract text from PDF files using multiple methods"""
    
    def __init__(self):
        self.methods = ['pymupdf', 'pdfplumber']
    
    def extract_with_pymupdf(self, pdf_path: str) -> List[Tuple[str, int]]:
        """Extract text using PyMuPDF (fitz)"""
        text_pages = []
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                if text.strip():  # Only add non-empty pages
                    text_pages.append((text, page_num + 1))
            doc.close()
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed for {pdf_path}: {e}")
        return text_pages
    
    def extract_with_pdfplumber(self, pdf_path: str) -> List[Tuple[str, int]]:
        """Extract text using pdfplumber"""
        text_pages = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text and text.strip():  # Only add non-empty pages
                        text_pages.append((text, page_num + 1))
        except Exception as e:
            logger.error(f"pdfplumber extraction failed for {pdf_path}: {e}")
        return text_pages
    
    def extract_text(self, pdf_path: str, method: str = 'pymupdf') -> List[Tuple[str, int]]:
        """Extract text from PDF using specified method"""
        if method == 'pymupdf':
            return self.extract_with_pymupdf(pdf_path)
        elif method == 'pdfplumber':
            return self.extract_with_pdfplumber(pdf_path)
        else:
            raise ValueError(f"Unknown extraction method: {method}")

class TextChunker:
    """Split text into chunks for embedding"""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, book_title: str, page_number: int, file_path: str) -> List[TextChunk]:
        """Split text into overlapping chunks"""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if chunk_text.strip():  # Only add non-empty chunks
                chunk_id = f"{Path(file_path).stem}_page{page_number}_chunk{len(chunks)}"
                chunk = TextChunk(
                    text=chunk_text,
                    book_title=book_title,
                    page_number=page_number,
                    file_path=file_path,
                    chunk_id=chunk_id,
                    chunk_index=len(chunks)
                )
                chunks.append(chunk)
        
        return chunks

class BookVectorDB:
    """Vector database for book content using FAISS"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', db_dir: str = 'book_db'):
        self.model_name = model_name
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(exist_ok=True)
        
        # Initialize sentence transformer
        logger.info(f"Loading sentence transformer model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product (cosine similarity)
        
        # Storage for metadata
        self.chunks: List[TextChunk] = []
        self.books: Dict[str, BookMetadata] = {}
        
        # Load existing database if available
        self.load_database()
    
    def extract_book_info(self, pdf_path: str) -> Tuple[str, str]:
        """Extract book title and author from PDF metadata or filename"""
        title = Path(pdf_path).stem.replace('_', ' ').replace('-', ' ')
        author = ""
        
        try:
            # Try to get metadata from PDF
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            if metadata.get('title'):
                title = metadata['title']
            if metadata.get('author'):
                author = metadata['author']
            doc.close()
        except Exception as e:
            logger.warning(f"Could not extract metadata from {pdf_path}: {e}")
        
        return title, author
    
    def process_book(self, pdf_path: str, extraction_method: str = 'pymupdf') -> Optional[BookMetadata]:
        """Process a single PDF book"""
        logger.info(f"Processing book: {pdf_path}")
        
        # Extract book info
        title, author = self.extract_book_info(pdf_path)
        
        # Extract text
        extractor = PDFTextExtractor()
        text_pages = extractor.extract_text(pdf_path, extraction_method)
        
        if not text_pages:
            logger.warning(f"No text extracted from {pdf_path}")
            return None
        
        # Create chunks
        chunker = TextChunker()
        all_chunks = []
        
        for text, page_num in text_pages:
            page_chunks = chunker.chunk_text(text, title, page_num, pdf_path)
            all_chunks.extend(page_chunks)
        
        if not all_chunks:
            logger.warning(f"No chunks created from {pdf_path}")
            return None
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(all_chunks)} chunks from {title}")
        chunk_texts = [chunk.text for chunk in all_chunks]
        embeddings = self.model.encode(chunk_texts, show_progress_bar=True)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add to index
        start_idx = len(self.chunks)
        self.index.add(embeddings)
        self.chunks.extend(all_chunks)
        
        # Create book metadata
        file_stat = os.stat(pdf_path)
        book_metadata = BookMetadata(
            file_path=pdf_path,
            title=title,
            author=author,
            page_count=len(text_pages),
            file_size=file_stat.st_size,
            last_modified=datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
            chunks_count=len(all_chunks)
        )
        
        self.books[pdf_path] = book_metadata
        logger.info(f"Successfully processed {title}: {len(all_chunks)} chunks")
        
        return book_metadata
    
    def process_directory(self, directory: str, extraction_method: str = 'pymupdf') -> List[BookMetadata]:
        """Process all PDF files in a directory"""
        directory = Path(directory)
        pdf_files = list(directory.rglob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {directory}")
            return []
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        processed_books = []
        
        for pdf_path in tqdm(pdf_files, desc="Processing books"):
            try:
                # Skip if already processed and file hasn't changed
                if self.is_book_current(str(pdf_path)):
                    logger.info(f"Skipping {pdf_path} (already up to date)")
                    continue
                
                metadata = self.process_book(str(pdf_path), extraction_method)
                if metadata:
                    processed_books.append(metadata)
                    
            except Exception as e:
                logger.error(f"Failed to process {pdf_path}: {e}")
                continue
        
        # Save database after processing
        self.save_database()
        return processed_books
    
    def is_book_current(self, pdf_path: str) -> bool:
        """Check if book is already processed and up to date"""
        if pdf_path not in self.books:
            return False
        
        try:
            file_stat = os.stat(pdf_path)
            stored_modified = self.books[pdf_path].last_modified
            current_modified = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
            return stored_modified == current_modified
        except (OSError, KeyError):
            return False
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[TextChunk, float]]:
        """Search for similar text chunks"""
        if self.index.ntotal == 0:
            logger.warning("No books in database. Please process some PDFs first.")
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
        
        # Return results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.chunks) and score > 0:  # Filter out invalid indices and negative scores
                results.append((self.chunks[idx], float(score)))
        
        return results
    
    def save_database(self):
        """Save the vector database and metadata"""
        logger.info("Saving database...")
        
        # Save FAISS index
        faiss.write_index(self.index, str(self.db_dir / "index.faiss"))
        
        # Save chunks
        with open(self.db_dir / "chunks.pkl", 'wb') as f:
            pickle.dump(self.chunks, f)
        
        # Save book metadata
        books_dict = {path: asdict(metadata) for path, metadata in self.books.items()}
        with open(self.db_dir / "books.json", 'w') as f:
            json.dump(books_dict, f, indent=2)
        
        # Save config
        config = {
            'model_name': self.model_name,
            'embedding_dim': self.embedding_dim,
            'total_chunks': len(self.chunks),
            'total_books': len(self.books),
            'last_updated': datetime.now().isoformat()
        }
        with open(self.db_dir / "config.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Database saved with {len(self.chunks)} chunks from {len(self.books)} books")
    
    def load_database(self):
        """Load existing database if available"""
        index_path = self.db_dir / "index.faiss"
        chunks_path = self.db_dir / "chunks.pkl"
        books_path = self.db_dir / "books.json"
        config_path = self.db_dir / "config.json"
        
        if not all(p.exists() for p in [index_path, chunks_path, books_path, config_path]):
            logger.info("No existing database found. Starting fresh.")
            return
        
        try:
            # Load config
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Verify model compatibility
            if config['model_name'] != self.model_name:
                logger.warning(f"Model mismatch. Stored: {config['model_name']}, Current: {self.model_name}")
                logger.warning("Starting fresh database.")
                return
            
            # Load FAISS index
            self.index = faiss.read_index(str(index_path))
            
            # Load chunks
            with open(chunks_path, 'rb') as f:
                self.chunks = pickle.load(f)
            
            # Load book metadata
            with open(books_path, 'r') as f:
                books_dict = json.load(f)
                self.books = {path: BookMetadata(**metadata) for path, metadata in books_dict.items()}
            
            logger.info(f"Loaded database with {len(self.chunks)} chunks from {len(self.books)} books")
            
        except Exception as e:
            logger.error(f"Failed to load database: {e}")
            logger.info("Starting fresh database.")
            self.index = faiss.IndexFlatIP(self.embedding_dim)
            self.chunks = []
            self.books = {}
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        return {
            'total_books': len(self.books),
            'total_chunks': len(self.chunks),
            'total_pages': sum(book.page_count for book in self.books.values()),
            'books_by_author': self._group_books_by_author(),
            'database_size_mb': sum(
                os.path.getsize(self.db_dir / f) 
                for f in os.listdir(self.db_dir) 
                if os.path.isfile(self.db_dir / f)
            ) / (1024 * 1024)
        }
    
    def _group_books_by_author(self) -> Dict[str, int]:
        """Group books by author"""
        authors = {}
        for book in self.books.values():
            author = book.author or "Unknown"
            authors[author] = authors.get(author, 0) + 1
        return authors

def print_search_results(results: List[Tuple[TextChunk, float]], max_results: int = 10):
    """Pretty print search results"""
    if not results:
        print("No results found.")
        return
    
    print(f"\nFound {len(results)} results:\n")
    print("=" * 80)
    
    for i, (chunk, score) in enumerate(results[:max_results], 1):
        print(f"\n{i}. {chunk.book_title} (Page {chunk.page_number}) - Score: {score:.3f}")
        print(f"   File: {Path(chunk.file_path).name}")
        print("-" * 80)
        
        # Display text preview (first 300 characters)
        text_preview = chunk.text[:300].strip()
        if len(chunk.text) > 300:
            text_preview += "..."
        
        print(text_preview)
        print("-" * 80)

def print_database_stats(db: BookVectorDB):
    """Print database statistics"""
    stats = db.get_stats()
    
    print("\n📚 Database Statistics")
    print("=" * 50)
    print(f"Total Books: {stats['total_books']}")
    print(f"Total Text Chunks: {stats['total_chunks']}")
    print(f"Total Pages: {stats['total_pages']}")
    print(f"Database Size: {stats['database_size_mb']:.2f} MB")
    
    print(f"\n📖 Books by Author:")
    for author, count in sorted(stats['books_by_author'].items()):
        print(f"  {author}: {count} book(s)")
    
    print(f"\n📚 Books in Database:")
    for book in db.books.values():
        print(f"  • {book.title}")
        if book.author:
            print(f"    Author: {book.author}")
        print(f"    Pages: {book.page_count}, Chunks: {book.chunks_count}")

def main():
    parser = argparse.ArgumentParser(description="PDF Book Search System")
    parser.add_argument('--directory', '-d', type=str, help='Directory containing PDF books')
    parser.add_argument('--search', '-s', type=str, help='Search query')
    parser.add_argument('--model', '-m', type=str, default='all-MiniLM-L6-v2', 
                       help='Sentence transformer model name')
    parser.add_argument('--db-dir', type=str, default='book_db', 
                       help='Directory to store vector database')
    parser.add_argument('--extraction-method', type=str, default='pymupdf', 
                       choices=['pymupdf', 'pdfplumber'], help='PDF text extraction method')
    parser.add_argument('--top-k', type=int, default=10, help='Number of search results to return')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--rebuild', action='store_true', help='Force rebuild of database')
    
    args = parser.parse_args()
    
    # Initialize database
    if args.rebuild and os.path.exists(args.db_dir):
        import shutil
        logger.info("Rebuilding database from scratch...")
        shutil.rmtree(args.db_dir)
    
    db = BookVectorDB(model_name=args.model, db_dir=args.db_dir)
    
    # Process directory if provided
    if args.directory:
        if not os.path.exists(args.directory):
            logger.error(f"Directory not found: {args.directory}")
            return
        
        processed = db.process_directory(args.directory, args.extraction_method)
        if processed:
            print(f"\n✅ Successfully processed {len(processed)} books!")
            for book in processed:
                print(f"  • {book.title} ({book.chunks_count} chunks)")
    
    # Show stats if requested
    if args.stats:
        print_database_stats(db)
    
    # Perform search if query provided
    if args.search:
        print(f"\n🔍 Searching for: '{args.search}'")
        results = db.search(args.search, args.top_k)
        print_search_results(results, args.top_k)
    
    # Interactive search mode if no search query provided
    if not args.search and not args.stats and not args.directory:
        print("\n🔍 Interactive Search Mode")
        print("Enter search queries (or 'quit' to exit):")
        
        while True:
            try:
                query = input("\nSearch: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                
                if query:
                    results = db.search(query, args.top_k)
                    print_search_results(results, args.top_k)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    main()
