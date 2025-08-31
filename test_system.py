#!/usr/bin/env python3
"""
Test script for the PDF Book Management System

This script creates a simple test PDF and verifies that both the organizer
and search system work correctly.
"""

import os
import tempfile
import shutil
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf(file_path: str, title: str, content: str, author: str = "Test Author"):
    """Create a simple test PDF with metadata"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        c = canvas.Canvas(file_path, pagesize=letter)
        
        # Set metadata
        c.setTitle(title)
        c.setAuthor(author)
        c.setSubject("Test Subject")
        c.setKeywords("test, pdf, sample")
        
        # Add content
        width, height = letter
        y = height - 100
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, y, title)
        y -= 40
        
        # Author
        c.setFont("Helvetica", 12)
        c.drawString(100, y, f"By: {author}")
        y -= 40
        
        # Content
        c.setFont("Helvetica", 10)
        words = content.split()
        line = ""
        
        for word in words:
            if len(line + word) < 80:  # Simple line wrapping
                line += word + " "
            else:
                c.drawString(100, y, line.strip())
                y -= 15
                line = word + " "
                
                if y < 100:  # New page if needed
                    c.showPage()
                    y = height - 100
        
        if line.strip():
            c.drawString(100, y, line.strip())
        
        c.save()
        print(f"✅ Created test PDF: {file_path}")
        return True
        
    except ImportError:
        print("❌ reportlab not installed. Installing...")
        os.system("pip3 install reportlab")
        return create_test_pdf(file_path, title, content, author)
    except Exception as e:
        print(f"❌ Failed to create test PDF: {e}")
        return False

def run_system_test():
    """Run a complete system test"""
    print("🧪 Running PDF Book Management System Test")
    print("=" * 50)
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        source_dir = temp_path / "source_books"
        target_dir = temp_path / "organized_books"
        source_dir.mkdir()
        
        print(f"📁 Test directories created in: {temp_dir}")
        
        # Create test PDFs
        test_books = [
            {
                "title": "Introduction to Machine Learning",
                "author": "Jane Smith",
                "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models. This book covers supervised learning, unsupervised learning, and reinforcement learning. We will explore decision trees, neural networks, and deep learning concepts."
            },
            {
                "title": "Python Programming Guide",
                "author": "John Doe",
                "content": "Python is a versatile programming language used for web development, data science, and automation. This guide covers Python syntax, object-oriented programming, libraries like pandas and numpy, and best practices for writing clean code."
            },
            {
                "title": "Business Strategy in Digital Age",
                "author": "Sarah Johnson",
                "content": "Digital transformation is changing how businesses operate. This book explores strategic planning, digital marketing, customer experience, and innovation management in the modern business environment."
            }
        ]
        
        print("\n📖 Creating test PDFs...")
        created_pdfs = []
        for book in test_books:
            pdf_path = source_dir / f"{book['title'].replace(' ', '_')}.pdf"
            if create_test_pdf(str(pdf_path), book['title'], book['content'], book['author']):
                created_pdfs.append(str(pdf_path))
        
        if not created_pdfs:
            print("❌ Failed to create test PDFs")
            return False
        
        print(f"✅ Created {len(created_pdfs)} test PDFs")
        
        # Test organizer
        print("\n🗂️  Testing book organizer...")
        organizer_cmd = f"python3 book_organizer.py {source_dir} {target_dir} --strategy subject --dry-run"
        print(f"Running: {organizer_cmd}")
        
        import subprocess
        try:
            result = subprocess.run(organizer_cmd.split(), capture_output=True, text=True, cwd="/Users/sushantnandwana/klaro-unified")
            if result.returncode == 0:
                print("✅ Book organizer test passed")
                print("Preview output:", result.stdout[-200:] if len(result.stdout) > 200 else result.stdout)
            else:
                print(f"❌ Book organizer test failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Failed to run organizer test: {e}")
            return False
        
        # Actually organize the books for search test
        print("\n📁 Organizing books for search test...")
        organizer_cmd_real = f"python3 book_organizer.py {source_dir} {target_dir} --strategy subject"
        try:
            result = subprocess.run(organizer_cmd_real.split(), capture_output=True, text=True, cwd="/Users/sushantnandwana/klaro-unified")
            if result.returncode == 0:
                print("✅ Books organized successfully")
            else:
                print(f"❌ Book organization failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Failed to organize books: {e}")
            return False
        
        # Test search system
        print("\n🔍 Testing search system...")
        
        # Build index
        search_cmd = f"python3 book_search.py --directory {target_dir}"
        print(f"Building search index...")
        try:
            result = subprocess.run(search_cmd.split(), capture_output=True, text=True, cwd="/Users/sushantnandwana/klaro-unified")
            if result.returncode == 0:
                print("✅ Search index built successfully")
            else:
                print(f"❌ Search index build failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Failed to build search index: {e}")
            return False
        
        # Test search
        print("\n🔎 Testing search functionality...")
        search_query_cmd = ["python3", "book_search.py", "--search", "machine learning algorithms", "--top-k", "3"]
        try:
            result = subprocess.run(search_query_cmd, capture_output=True, text=True, cwd="/Users/sushantnandwana/klaro-unified")
            if result.returncode == 0:
                print("✅ Search test passed")
                print("Search results preview:", result.stdout[-300:] if len(result.stdout) > 300 else result.stdout)
            else:
                print(f"❌ Search test failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Failed to run search test: {e}")
            return False
        
        print("\n🎉 All tests passed! The system is working correctly.")
        return True

if __name__ == "__main__":
    run_system_test()
