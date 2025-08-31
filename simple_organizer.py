#!/usr/bin/env python3
"""
📚 Simple Book Organizer (No External Dependencies)
==================================================

Organizes your books based on filenames only - no PDF processing needed.
Perfect for getting started quickly!
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Any

def parse_filename(filename: str) -> Dict[str, str]:
    """Parse metadata from filename using smart patterns."""
    
    metadata = {
        'publisher': 'unknown',
        'subject': 'unknown', 
        'class_grade': 'unknown',
        'book_type': 'textbook',
        'edition': '2023'
    }
    
    filename_clean = filename.replace('_', ' ').replace('-', ' ').lower()
    print(f"🔍 Analyzing: {filename_clean}")
    
    # Publisher detection
    if re.search(r'\\bncert\\b', filename_clean):
        metadata['publisher'] = 'ncert'
    elif re.search(r'\\b(?:rd\\s*sharma|r\\.d\\s*sharma)\\b', filename_clean):
        metadata['publisher'] = 'rd_sharma'
    elif re.search(r'\\bcengage\\b', filename_clean):
        metadata['publisher'] = 'cengage'
    elif re.search(r'\\barihant\\b', filename_clean):
        metadata['publisher'] = 'arihant'
    elif re.search(r'\\bfiitjee\\b', filename_clean):
        metadata['publisher'] = 'fiitjee'
    
    # Subject detection
    if re.search(r'\\b(?:math|mathematics|maths)\\b', filename_clean):
        metadata['subject'] = 'mathematics'
    elif re.search(r'\\b(?:physics|phy)\\b', filename_clean):
        metadata['subject'] = 'physics'
    elif re.search(r'\\b(?:chemistry|chem)\\b', filename_clean):
        metadata['subject'] = 'chemistry'
    elif re.search(r'\\b(?:biology|bio)\\b', filename_clean):
        metadata['subject'] = 'biology'
    
    # Class detection
    class_match = re.search(r'\\bclass\\s*([0-9]{1,2})\\b', filename_clean)
    if class_match:
        metadata['class_grade'] = f'class_{class_match.group(1)}'
    elif re.search(r'\\b10\\b', filename_clean):
        metadata['class_grade'] = 'class_10'
    elif re.search(r'\\b11\\b', filename_clean):
        metadata['class_grade'] = 'class_11'
    elif re.search(r'\\b12\\b', filename_clean):
        metadata['class_grade'] = 'class_12'
    elif re.search(r'\\bjee\\b', filename_clean):
        metadata['class_grade'] = 'jee'
    elif re.search(r'\\bneet\\b', filename_clean):
        metadata['class_grade'] = 'neet'
    
    # Book type detection
    if re.search(r'\\b(?:solutions|sol|answer|solved)\\b', filename_clean):
        metadata['book_type'] = 'solutions'
    elif re.search(r'\\b(?:practice|exercise|problems)\\b', filename_clean):
        metadata['book_type'] = 'practice'
    elif re.search(r'\\b(?:exemplar)\\b', filename_clean):
        metadata['book_type'] = 'exemplar'
    elif re.search(r'\\b(?:question|bank|qb)\\b', filename_clean):
        metadata['book_type'] = 'question_bank'
    
    # Year detection
    year_match = re.search(r'\\b(20[0-9]{2})\\b', filename_clean)
    if year_match:
        metadata['edition'] = year_match.group(1)
    
    return metadata

def organize_single_book(pdf_path: Path, textbooks_dir: Path, auto_rename: bool = True) -> Dict[str, Any]:
    """Organize a single book."""
    
    # Parse metadata from filename
    metadata = parse_filename(pdf_path.stem)
    
    print(f"   📖 Detected: {metadata['publisher']} {metadata['subject']} {metadata['class_grade']}")
    
    # Create target directory structure
    target_dir = textbooks_dir / metadata['publisher'] / metadata['subject'] / metadata['class_grade']
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate new filename if auto-renaming
    if auto_rename:
        new_filename = f"{metadata['publisher'].title()}_{metadata['subject'].title()}_{metadata['class_grade'].title()}_{metadata['book_type'].title()}_{metadata['edition']}.pdf"
    else:
        new_filename = pdf_path.name
    
    target_path = target_dir / new_filename
    
    # Move file
    if pdf_path != target_path:
        if not target_path.exists():
            pdf_path.rename(target_path)
            print(f"   ✅ Moved to: {target_path}")
        else:
            print(f"   ⚠️  Already exists: {target_path}")
    
    metadata['new_path'] = str(target_path)
    metadata['organized'] = True
    
    return metadata

def main():
    """Main organization function."""
    
    print("📚 Simple Book Organizer")
    print("========================")
    print("(No external libraries needed!)\\n")
    
    # Setup directories
    current_dir = Path.cwd()
    textbooks_dir = current_dir / 'textbooks'
    textbooks_dir.mkdir(exist_ok=True)
    
    print(f"📂 Books will be organized in: {textbooks_dir}\\n")
    
    # Get source directory
    while True:
        source_input = input("📥 Where are your PDF files? (path or 'Downloads'): ").strip()
        
        if source_input.lower() == 'downloads':
            source_dir = Path.home() / 'Downloads'
        else:
            source_dir = Path(source_input)
        
        if source_dir.exists():
            pdf_files = list(source_dir.glob('*.pdf'))
            print(f"✅ Found {len(pdf_files)} PDF files")
            break
        else:
            print(f"❌ Directory not found: {source_dir}")
    
    if not pdf_files:
        print("No PDF files found!")
        return
    
    print("\\n📖 Files found:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf_file.name}")
    
    print("\\n🔧 Organization mode:")
    print("1. Auto-organize all files")
    print("2. Ask me about each file") 
    print("3. Show me what you detected first")
    
    choice = input("\\nChoose (1/2/3): ").strip()
    
    if choice == "1":
        print("\\n🤖 Auto-organizing all files...")
        for pdf_file in pdf_files:
            try:
                result = organize_single_book(pdf_file, textbooks_dir, auto_rename=True)
                print(f"✅ {pdf_file.name}")
            except Exception as e:
                print(f"❌ {pdf_file.name}: {e}")
    
    elif choice == "2":
        print("\\n🤔 Interactive organization...")
        for pdf_file in pdf_files:
            print(f"\\n📖 {pdf_file.name}")
            
            # Show auto-detection
            detected = parse_filename(pdf_file.stem)
            print(f"   🤖 I think: {detected['publisher']} | {detected['subject']} | {detected['class_grade']}")
            
            action = input("   ✅ Correct? (y/n/edit/skip): ").lower()
            
            if action == 'y':
                organize_single_book(pdf_file, textbooks_dir)
            elif action == 'edit':
                print("\\n📝 Correct the details:")
                detected['publisher'] = input(f"   Publisher [{detected['publisher']}]: ").strip() or detected['publisher']
                detected['subject'] = input(f"   Subject [{detected['subject']}]: ").strip() or detected['subject']
                detected['class_grade'] = input(f"   Class [{detected['class_grade']}]: ").strip() or detected['class_grade']
                detected['book_type'] = input(f"   Type [{detected['book_type']}]: ").strip() or detected['book_type']
                
                organize_single_book(pdf_file, textbooks_dir)
            elif action == 'skip':
                print("   ⏭️  Skipped")
            else:
                organize_single_book(pdf_file, textbooks_dir)
    
    elif choice == "3":
        print("\\n🔍 Detection preview:")
        for pdf_file in pdf_files:
            detected = parse_filename(pdf_file.stem)
            print(f"📖 {pdf_file.name}")
            print(f"   → {detected['publisher']} | {detected['subject']} | {detected['class_grade']} | {detected['book_type']}")
        
        if input("\\n🚀 Proceed with auto-organization? (y/n): ").lower() == 'y':
            for pdf_file in pdf_files:
                organize_single_book(pdf_file, textbooks_dir, auto_rename=True)
    
    # Show final structure
    print("\\n✅ Organization complete!")
    print("\\n📁 Final directory structure:")
    show_tree(textbooks_dir)

def show_tree(directory: Path, prefix="", max_depth=3, current_depth=0):
    """Show directory tree."""
    
    if current_depth >= max_depth or not directory.exists():
        return
    
    items = sorted([item for item in directory.iterdir()])
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        
        if item.is_file():
            size_mb = round(item.stat().st_size / 1024 / 1024, 1)
            print(f"{prefix}{current_prefix}{item.name} ({size_mb}MB)")
        else:
            print(f"{prefix}{current_prefix}{item.name}/")
            next_prefix = prefix + ("    " if is_last else "│   ")
            show_tree(item, next_prefix, max_depth, current_depth + 1)

if __name__ == "__main__":
    main()
