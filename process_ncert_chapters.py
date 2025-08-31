#!/usr/bin/env python3
"""
📚 NCERT Chapter Processor
=========================

Processes your NCERT chapter files and organizes them properly.
Handles the chapter-wise PDFs you have in grade folders.
"""

import re
import os
from pathlib import Path
from typing import Dict, List

def process_ncert_chapters():
    """Process all NCERT chapter files."""
    
    print("📚 NCERT Chapter Processor")
    print("==========================")
    print()
    
    raw_dir = Path("/Users/sushantnandwana/Educational_Books_Raw/Core_Curriculum/CBSE")
    target_dir = Path("/Users/sushantnandwana/klaro-unified/textbooks")
    target_dir.mkdir(exist_ok=True)
    
    # Process textbook chapters
    textbook_folders = {
        "Grade_9_Mathematics_Chapters": ("class_9", "textbook"),
        "Grade_10_Mathematics_Chapters": ("class_10", "textbook"), 
        "Grade_11_Mathematics_Chapters": ("class_11", "textbook"),
        "Grade_12_Mathematics_Part1_Chapters": ("class_12", "textbook_part1"),
        "Grade_12_Mathematics_Part2_Chapters": ("class_12", "textbook_part2")
    }
    
    print("📖 Processing NCERT Textbook Chapters...")
    
    for folder_name, (class_grade, book_type) in textbook_folders.items():
        folder_path = raw_dir / "Textbooks" / folder_name
        
        if folder_path.exists():
            target_class_dir = target_dir / "ncert" / "mathematics" / class_grade
            target_class_dir.mkdir(parents=True, exist_ok=True)
            
            pdf_files = list(folder_path.glob("*.pdf"))
            print(f"  📁 {folder_name}: {len(pdf_files)} files")
            
            for pdf_file in pdf_files:
                # Create descriptive filename
                new_name = f"NCERT_Mathematics_{class_grade.title()}_{book_type.title()}_{pdf_file.name}"
                target_file = target_class_dir / new_name
                
                if not target_file.exists():
                    # Copy (not move) to preserve original structure
                    import shutil
                    shutil.copy2(pdf_file, target_file)
                    print(f"    ✅ {pdf_file.name} → {new_name}")
    
    # Process exemplar chapters
    exemplar_folders = {
        "Grade_9_Mathematics_Exemplar_Chapters": "class_9",
        "Grade_11_Mathematics_Exemplar_Chapters": "class_11",
        "Grade_12_Mathematics_Exemplar_Chapters": "class_12"
    }
    
    print("\\n📘 Processing NCERT Exemplar Chapters...")
    
    for folder_name, class_grade in exemplar_folders.items():
        folder_path = raw_dir / "Exemplar" / folder_name
        
        if folder_path.exists():
            target_class_dir = target_dir / "ncert" / "mathematics" / class_grade
            target_class_dir.mkdir(parents=True, exist_ok=True)
            
            pdf_files = list(folder_path.glob("*.pdf"))
            print(f"  📁 {folder_name}: {len(pdf_files)} files")
            
            for pdf_file in pdf_files:
                new_name = f"NCERT_Mathematics_{class_grade.title()}_Exemplar_{pdf_file.name}"
                target_file = target_class_dir / new_name
                
                if not target_file.exists():
                    import shutil
                    shutil.copy2(pdf_file, target_file)
                    print(f"    ✅ {pdf_file.name} → {new_name}")
    
    # Process the Class 10 complete exemplar book
    class_10_exemplar = raw_dir / "Exemplar" / "NCERT_Mathematics_Class_10_Exemplar_2023.pdf"
    if class_10_exemplar.exists():
        target_class_dir = target_dir / "ncert" / "mathematics" / "class_10"
        target_class_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_class_dir / "NCERT_Mathematics_Class_10_Exemplar_Complete_2023.pdf"
        
        if not target_file.exists():
            import shutil
            shutil.copy2(class_10_exemplar, target_file)
            print(f"    ✅ Complete Class 10 Exemplar moved")
    
    print("\\n📊 Summary:")
    
    # Count files by class
    for class_grade in ["class_9", "class_10", "class_11", "class_12"]:
        class_dir = target_dir / "ncert" / "mathematics" / class_grade
        if class_dir.exists():
            pdf_count = len(list(class_dir.glob("*.pdf")))
            print(f"  📚 {class_grade.replace('_', ' ').title()}: {pdf_count} files")
    
    print("\\n✅ All NCERT Mathematics books processed!")
    
    # Show final structure
    print("\\n📁 Final Structure:")
    show_directory_tree(target_dir / "ncert")

def show_directory_tree(directory: Path, prefix="", max_depth=4, current_depth=0):
    """Show directory structure."""
    
    if current_depth >= max_depth or not directory.exists():
        return
    
    items = sorted([item for item in directory.iterdir()])
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        
        if item.is_file():
            print(f"{prefix}{current_prefix}{item.name}")
        else:
            file_count = len([f for f in item.rglob("*.pdf")]) if item.is_dir() else 0
            print(f"{prefix}{current_prefix}{item.name}/ ({file_count} PDFs)")
            
            if current_depth < max_depth - 1:
                next_prefix = prefix + ("    " if is_last else "│   ")
                show_directory_tree(item, next_prefix, max_depth, current_depth + 1)

def preview_processing():
    """Preview what would be processed without actually moving files."""
    
    print("👀 PREVIEW: What would be processed...")
    
    raw_dir = Path("/Users/sushantnandwana/Educational_Books_Raw/Core_Curriculum/CBSE")
    
    # Check textbook folders
    textbook_dir = raw_dir / "Textbooks"
    if textbook_dir.exists():
        for folder in textbook_dir.iterdir():
            if folder.is_dir():
                pdf_count = len(list(folder.glob("*.pdf")))
                print(f"📖 {folder.name}: {pdf_count} PDF files")
    
    # Check exemplar folders  
    exemplar_dir = raw_dir / "Exemplar"
    if exemplar_dir.exists():
        for folder in exemplar_dir.iterdir():
            if folder.is_dir():
                pdf_count = len(list(folder.glob("*.pdf")))
                print(f"📘 {folder.name}: {pdf_count} PDF files")
            elif folder.is_file() and folder.suffix == '.pdf':
                print(f"📘 {folder.name}: Individual file")

if __name__ == "__main__":
    
    print("🎯 NCERT Chapter Processing Options:")
    print("1. Process all NCERT chapters")
    print("2. Preview what would be processed")
    print("3. Exit")
    
    choice = input("\\nChoose (1-3): ").strip()
    
    if choice == "1":
        process_ncert_chapters()
    elif choice == "2":
        preview_processing()
    else:
        print("👋 Goodbye!")
