#!/usr/bin/env python3
"""
📚 Quick Book Organization Script
================================

Run this to organize your downloaded books into the proper structure.
Use this RIGHT NOW to organize whatever books you have.
"""

import sys
from pathlib import Path
from core.book_detector import BookOrganizer, InteractiveBookSetup

def main():
    """Organize books with user guidance."""
    
    print("📚 Klaro Book Organizer")
    print("======================")
    print()
    
    # Setup paths
    textbooks_dir = Path.cwd() / 'textbooks'
    textbooks_dir.mkdir(exist_ok=True)
    
    print(f"📂 Textbooks will be organized in: {textbooks_dir}")
    print()
    
    # Get source directory
    while True:
        source_dir = input("📥 Where are your PDF files? (full path or 'Downloads'): ").strip()
        
        if source_dir.lower() == 'downloads':
            source_dir = str(Path.home() / 'Downloads')
        
        source_path = Path(source_dir)
        if source_path.exists():
            pdf_count = len(list(source_path.glob('*.pdf')))
            print(f"✅ Found {pdf_count} PDF files in {source_dir}")
            break
        else:
            print(f"❌ Directory not found: {source_dir}")
    
    print()
    
    # Choose organization method
    print("🔧 Organization Options:")
    print("1. Automatic (I'll try to detect everything)")
    print("2. Interactive (I'll ask when unsure)")
    print("3. Manual (you tell me about each book)")
    
    choice = input("\\nChoose method (1/2/3): ").strip()
    
    organizer = BookOrganizer(str(textbooks_dir))
    
    if choice == "1":
        print("\\n🤖 Starting automatic organization...")
        results = organizer.organize_bulk_books(source_dir)
        
        successful = [r for r in results if r.get('organized')]
        failed = [r for r in results if not r.get('organized')]
        
        print(f"\\n📊 Results: {len(successful)} organized, {len(failed)} failed")
        
        if failed:
            print("\\n❌ Failed files:")
            for f in failed:
                print(f"   {Path(f['file_path']).name}: {f.get('error')}")
            print("\\n💡 Try interactive mode for failed files")
    
    elif choice == "2":
        print("\\n🤔 Starting interactive organization...")
        interactive = InteractiveBookSetup(str(textbooks_dir))
        interactive.setup_books_interactively(source_dir)
        
    elif choice == "3":
        print("\\n📝 Manual organization mode:")
        pdf_files = list(Path(source_dir).glob('*.pdf'))
        
        for pdf_file in pdf_files:
            print(f"\\n📖 Book: {pdf_file.name}")
            print("Please provide details:")
            
            publisher = input("Publisher (NCERT/RD_Sharma/etc): ").strip() or 'unknown'
            subject = input("Subject (Mathematics/Physics/etc): ").strip() or 'unknown' 
            class_grade = input("Class (Class_10/JEE/etc): ").strip() or 'unknown'
            book_type = input("Type (Textbook/Solutions/etc): ").strip() or 'textbook'
            
            # Create target directory
            target_dir = textbooks_dir / publisher.lower() / subject.lower() / class_grade.lower()
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Move file
            new_filename = f"{publisher}_{subject}_{class_grade}_{book_type}_2023.pdf"
            target_path = target_dir / new_filename
            
            if not target_path.exists():
                pdf_file.rename(target_path)
                print(f"✅ Organized: {target_path}")
            else:
                print(f"⚠️  Already exists: {target_path}")
    
    else:
        print("❌ Invalid choice")
        return
    
    print("\\n✅ Book organization complete!")
    print(f"📂 Check your organized books in: {textbooks_dir}")
    
    # Show final directory structure
    print("\\n📁 Directory Structure:")
    show_directory_tree(textbooks_dir)


def show_directory_tree(directory: Path, prefix="", max_depth=3, current_depth=0):
    """Show directory tree structure."""
    
    if current_depth >= max_depth:
        return
    
    items = []
    if directory.exists():
        items = sorted([item for item in directory.iterdir() 
                       if item.is_dir() or item.suffix == '.pdf'])
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        
        if item.is_file():
            print(f"{prefix}{current_prefix}{item.name} ({item.stat().st_size // 1024 // 1024}MB)")
        else:
            print(f"{prefix}{current_prefix}{item.name}/")
            
            next_prefix = prefix + ("    " if is_last else "│   ")
            show_directory_tree(item, next_prefix, max_depth, current_depth + 1)


if __name__ == "__main__":
    main()


# QUICK START GUIDE:
"""
🚀 QUICK START - Organize Your Books RIGHT NOW:

STEP 1: Download some NCERT PDFs
- Go to ncert.nic.in
- Download Class 10-12 Math, Physics, Chemistry PDFs
- Save them with clear names like "NCERT Mathematics Class 10.pdf"

STEP 2: Run the organizer
```bash
cd /Users/sushantnandwana/klaro-unified
python organize_books.py
```

STEP 3: Follow the prompts
- Choose "Interactive" mode for best results
- I'll detect what I can and ask for help when unsure
- Books will be organized into textbooks/publisher/subject/class/

STEP 4: Verify organization  
```bash
ls -la textbooks/
# Should see: ncert/ rd_sharma/ etc.

ls -la textbooks/ncert/mathematics/
# Should see: class_10/ class_11/ class_12/
```

THAT'S IT! 
Your books are now properly organized and ready for processing.

NEXT: We'll process these organized books into our vector database.
"""
