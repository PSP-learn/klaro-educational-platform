#!/usr/bin/env python3
"""
📚 Custom Book Organizer for Your Structure
==========================================

Organizes books from your Educational_Books_Raw structure into 
the final klaro-unified/textbooks/ structure for processing.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

class CustomBookOrganizer:
    """Organizer that understands your specific folder structure."""
    
    def __init__(self):
        self.raw_books_dir = Path("/Users/sushantnandwana/Educational_Books_Raw")
        self.target_dir = Path("/Users/sushantnandwana/klaro-unified/textbooks")
        self.target_dir.mkdir(exist_ok=True)
        
    def organize_all_books(self):
        """Process all books from your raw structure."""
        
        print("📚 Custom Book Organizer")
        print("========================")
        print(f"📂 Source: {self.raw_books_dir}")
        print(f"🎯 Target: {self.target_dir}")
        print()
        
        # Process each category
        self.process_core_curriculum()
        self.process_entrance_prep() 
        self.process_reference_materials()
        self.process_competitive_publishers()
        
        print("\\n✅ All books organized!")
        self.show_final_structure()
    
    def process_core_curriculum(self):
        """Process Core_Curriculum books."""
        
        print("🎓 Processing Core Curriculum...")
        
        # CBSE (NCERT) books
        cbse_dir = self.raw_books_dir / "Core_Curriculum" / "CBSE"
        
        if (cbse_dir / "Textbooks").exists():
            self._process_ncert_textbooks(cbse_dir / "Textbooks")
        
        if (cbse_dir / "Exemplar").exists():
            self._process_ncert_exemplar(cbse_dir / "Exemplar")
            
        if (cbse_dir / "Lab_Manuals").exists():
            self._process_lab_manuals(cbse_dir / "Lab_Manuals")
        
        # State boards
        state_board_dir = cbse_dir.parent / "State_Board"
        for state_folder in ["Maharashtra", "ICSE", "IB"]:
            state_path = state_board_dir / state_folder
            if state_path.exists():
                self._process_state_board_books(state_path, state_folder.lower())
    
    def process_entrance_prep(self):
        """Process Entrance_Prep books."""
        
        print("📝 Processing Entrance Prep...")
        
        entrance_dir = self.raw_books_dir / "Entrance_Prep"
        
        # JEE books
        jee_dir = entrance_dir / "JEE"
        for jee_type in ["Main", "Advanced", "PYQ"]:
            jee_path = jee_dir / jee_type
            if jee_path.exists():
                self._process_jee_books(jee_path, jee_type.lower())
        
        # NEET books  
        neet_dir = entrance_dir / "NEET"
        for subject in ["Physics", "Chemistry", "Biology"]:
            neet_path = neet_dir / subject
            if neet_path.exists():
                self._process_neet_books(neet_path, subject.lower())
    
    def process_reference_materials(self):
        """Process Reference_Materials books."""
        
        print("📖 Processing Reference Materials...")
        
        ref_dir = self.raw_books_dir / "Reference_Materials"
        
        ref_types = {
            "Solutions_Manuals": "solutions",
            "Practice_Books": "practice", 
            "Quick_Guides": "guide",
            "Revision_Notes": "notes"
        }
        
        for folder_name, book_type in ref_types.items():
            folder_path = ref_dir / folder_name
            if folder_path.exists():
                self._process_reference_books(folder_path, book_type)
    
    def process_competitive_publishers(self):
        """Process Competitive_Publishers books."""
        
        print("🏢 Processing Competitive Publishers...")
        
        pub_dir = self.raw_books_dir / "Competitive_Publishers"
        
        publishers = ["Arihant", "Cengage", "MTG", "RD_Sharma", "HC_Verma", "Disha"]
        
        for publisher in publishers:
            pub_path = pub_dir / publisher
            if pub_path.exists():
                self._process_publisher_books(pub_path, publisher.lower().replace(" ", "_"))
    
    def _process_ncert_textbooks(self, textbooks_dir: Path):
        """Process NCERT textbooks."""
        
        for pdf_file in textbooks_dir.glob("*.pdf"):
            metadata = self._parse_ncert_textbook(pdf_file.name)
            target_path = self._get_target_path(metadata)
            self._move_book(pdf_file, target_path, metadata)
    
    def _parse_ncert_textbook(self, filename: str) -> Dict[str, str]:
        """Parse NCERT textbook filename."""
        
        metadata = {
            'publisher': 'ncert',
            'book_type': 'textbook',
            'curriculum': 'cbse'
        }
        
        filename_clean = filename.lower().replace('_', ' ').replace('-', ' ')
        
        # Subject detection
        if re.search(r'\\b(?:math|mathematics)\\b', filename_clean):
            metadata['subject'] = 'mathematics'
        elif re.search(r'\\b(?:physics|phy)\\b', filename_clean):
            metadata['subject'] = 'physics'
        elif re.search(r'\\b(?:chemistry|chem)\\b', filename_clean):
            metadata['subject'] = 'chemistry'
        elif re.search(r'\\b(?:biology|bio)\\b', filename_clean):
            metadata['subject'] = 'biology'
        else:
            metadata['subject'] = 'unknown'
        
        # Class detection
        class_match = re.search(r'\\bclass[\\s_-]*([0-9]{1,2})\\b', filename_clean)
        if class_match:
            metadata['class_grade'] = f'class_{class_match.group(1)}'
        elif re.search(r'\\b([0-9]{1,2})th\\b', filename_clean):
            class_num = re.search(r'\\b([0-9]{1,2})th\\b', filename_clean).group(1)
            metadata['class_grade'] = f'class_{class_num}'
        else:
            # Try to extract just numbers
            numbers = re.findall(r'\\b([0-9]{1,2})\\b', filename_clean)
            valid_classes = [n for n in numbers if int(n) >= 9 and int(n) <= 12]
            if valid_classes:
                metadata['class_grade'] = f'class_{valid_classes[0]}'
            else:
                metadata['class_grade'] = 'unknown'
        
        # Part detection (for multi-part books)
        if 'part' in filename_clean:
            part_match = re.search(r'part[\\s_-]*([0-9]+)', filename_clean)
            if part_match:
                metadata['part'] = f'part_{part_match.group(1)}'
        
        return metadata
    
    def _process_jee_books(self, jee_dir: Path, jee_type: str):
        """Process JEE preparation books."""
        
        for pdf_file in jee_dir.glob("*.pdf"):
            metadata = self._parse_jee_book(pdf_file.name, jee_type)
            target_path = self._get_target_path(metadata)
            self._move_book(pdf_file, target_path, metadata)
    
    def _parse_jee_book(self, filename: str, jee_type: str) -> Dict[str, str]:
        """Parse JEE book filename."""
        
        metadata = {
            'class_grade': 'jee',
            'curriculum': 'entrance_exam',
            'book_type': 'practice',
            'exam_type': jee_type  # main, advanced, pyq
        }
        
        filename_clean = filename.lower()
        
        # Publisher detection
        if 'arihant' in filename_clean:
            metadata['publisher'] = 'arihant'
        elif 'cengage' in filename_clean:
            metadata['publisher'] = 'cengage'
        elif 'mtg' in filename_clean:
            metadata['publisher'] = 'mtg'
        else:
            metadata['publisher'] = 'unknown'
        
        # Subject detection
        if re.search(r'\\b(?:math|mathematics)\\b', filename_clean):
            metadata['subject'] = 'mathematics'
        elif re.search(r'\\b(?:physics|phy)\\b', filename_clean):
            metadata['subject'] = 'physics'
        elif re.search(r'\\b(?:chemistry|chem)\\b', filename_clean):
            metadata['subject'] = 'chemistry'
        else:
            metadata['subject'] = 'unknown'
        
        return metadata
    
    def _process_neet_books(self, neet_dir: Path, subject: str):
        """Process NEET books by subject."""
        
        for pdf_file in neet_dir.glob("*.pdf"):
            metadata = {
                'class_grade': 'neet',
                'subject': subject,
                'curriculum': 'entrance_exam',
                'book_type': 'practice',
                'publisher': self._detect_publisher_from_filename(pdf_file.name)
            }
            
            target_path = self._get_target_path(metadata)
            self._move_book(pdf_file, target_path, metadata)
    
    def _process_publisher_books(self, pub_dir: Path, publisher: str):
        """Process books from competitive publishers."""
        
        for pdf_file in pub_dir.glob("*.pdf"):
            metadata = self._parse_publisher_book(pdf_file.name, publisher)
            target_path = self._get_target_path(metadata)
            self._move_book(pdf_file, target_path, metadata)
    
    def _parse_publisher_book(self, filename: str, publisher: str) -> Dict[str, str]:
        """Parse competitive publisher book."""
        
        metadata = {
            'publisher': publisher,
            'book_type': 'reference'
        }
        
        filename_clean = filename.lower()
        
        # Subject detection
        if re.search(r'\\b(?:math|mathematics)\\b', filename_clean):
            metadata['subject'] = 'mathematics'
        elif re.search(r'\\b(?:physics|phy)\\b', filename_clean):
            metadata['subject'] = 'physics'
        elif re.search(r'\\b(?:chemistry|chem)\\b', filename_clean):
            metadata['subject'] = 'chemistry'
        elif re.search(r'\\b(?:biology|bio)\\b', filename_clean):
            metadata['subject'] = 'biology'
        else:
            metadata['subject'] = 'unknown'
        
        # Class/Exam detection
        if 'jee' in filename_clean:
            metadata['class_grade'] = 'jee'
        elif 'neet' in filename_clean:
            metadata['class_grade'] = 'neet'
        else:
            # Try to find class number
            class_match = re.search(r'\\bclass[\\s_-]*([0-9]{1,2})\\b', filename_clean)
            if class_match:
                metadata['class_grade'] = f'class_{class_match.group(1)}'
            else:
                numbers = re.findall(r'\\b([0-9]{1,2})\\b', filename_clean)
                valid_classes = [n for n in numbers if int(n) >= 9 and int(n) <= 12]
                if valid_classes:
                    metadata['class_grade'] = f'class_{valid_classes[0]}'
                else:
                    metadata['class_grade'] = 'unknown'
        
        return metadata
    
    def _get_target_path(self, metadata: Dict[str, str]) -> Path:
        """Get target path in final textbooks structure."""
        
        publisher = metadata.get('publisher', 'unknown')
        subject = metadata.get('subject', 'unknown')  
        class_grade = metadata.get('class_grade', 'unknown')
        
        return self.target_dir / publisher / subject / class_grade
    
    def _move_book(self, source_file: Path, target_dir: Path, metadata: Dict[str, str]):
        """Move book to target location with proper naming."""
        
        # Create target directory
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate clean filename
        clean_filename = self._generate_clean_filename(source_file.name, metadata)
        target_file = target_dir / clean_filename
        
        # Move file
        if not target_file.exists():
            source_file.rename(target_file)
            print(f"✅ {source_file.name}")
            print(f"   → {target_file.relative_to(self.target_dir)}")
        else:
            print(f"⚠️  Already exists: {target_file.name}")
    
    def _generate_clean_filename(self, original_name: str, metadata: Dict[str, str]) -> str:
        """Generate clean, standardized filename."""
        
        components = []
        
        # Publisher
        publisher = metadata.get('publisher', 'Unknown').title()
        components.append(publisher)
        
        # Subject  
        subject = metadata.get('subject', 'Unknown').title()
        components.append(subject)
        
        # Class
        class_grade = metadata.get('class_grade', 'Unknown')
        if class_grade.startswith('class_'):
            components.append(f"Class_{class_grade.split('_')[1]}")
        else:
            components.append(class_grade.upper())
        
        # Book type
        book_type = metadata.get('book_type', 'Book').title()
        components.append(book_type)
        
        # Year (try to extract from original, default to 2023)
        year_match = re.search(r'\\b(20[0-9]{2})\\b', original_name)
        year = year_match.group(1) if year_match else '2023'
        components.append(year)
        
        return '_'.join(components) + '.pdf'
    
    def _detect_publisher_from_filename(self, filename: str) -> str:
        """Detect publisher from filename."""
        
        filename_lower = filename.lower()
        
        publishers = {
            'ncert': r'\\bncert\\b',
            'rd_sharma': r'\\b(?:rd\\s*sharma|r\\.d\\s*sharma)\\b',
            'arihant': r'\\barihant\\b',
            'cengage': r'\\bcengage\\b',
            'mtg': r'\\bmtg\\b',
            'hc_verma': r'\\b(?:hc\\s*verma|h\\.c\\s*verma)\\b',
            'disha': r'\\bdisha\\b'
        }
        
        for publisher, pattern in publishers.items():
            if re.search(pattern, filename_lower):
                return publisher
        
        return 'unknown'
    
    def show_source_structure(self):
        """Show your current raw books structure."""
        
        print("📁 Your Current Raw Structure:")
        self._show_tree(self.raw_books_dir, max_depth=3)
    
    def show_final_structure(self):
        """Show final organized structure."""
        
        print("\\n📁 Final Organized Structure:")
        self._show_tree(self.target_dir, max_depth=3)
    
    def _show_tree(self, directory: Path, prefix="", max_depth=3, current_depth=0):
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
                self._show_tree(item, next_prefix, max_depth, current_depth + 1)
    
    def process_single_folder(self, folder_path: str):
        """Process books from a single folder (for testing)."""
        
        folder = Path(folder_path)
        if not folder.exists():
            print(f"❌ Folder not found: {folder_path}")
            return
        
        pdf_files = list(folder.glob("*.pdf"))
        if not pdf_files:
            print(f"📂 No PDF files found in {folder.name}")
            return
        
        print(f"📚 Processing {len(pdf_files)} books from {folder.name}...")
        
        # Determine folder type and process accordingly
        folder_name = folder.name
        
        if "CBSE/Textbooks" in str(folder):
            for pdf_file in pdf_files:
                metadata = self._parse_ncert_textbook(pdf_file.name)
                target_path = self._get_target_path(metadata)
                self._move_book(pdf_file, target_path, metadata)
        
        elif "JEE" in str(folder):
            jee_type = folder.name.lower()
            for pdf_file in pdf_files:
                metadata = self._parse_jee_book(pdf_file.name, jee_type)
                target_path = self._get_target_path(metadata)
                self._move_book(pdf_file, target_path, metadata)
        
        else:
            # Generic processing
            for pdf_file in pdf_files:
                metadata = {
                    'publisher': self._detect_publisher_from_filename(pdf_file.name),
                    'subject': self._detect_subject_from_filename(pdf_file.name),
                    'class_grade': self._detect_class_from_filename(pdf_file.name),
                    'book_type': 'reference'
                }
                target_path = self._get_target_path(metadata)
                self._move_book(pdf_file, target_path, metadata)
    
    def _detect_subject_from_filename(self, filename: str) -> str:
        """Detect subject from filename."""
        filename_lower = filename.lower()
        
        if re.search(r'\\b(?:math|mathematics)\\b', filename_lower):
            return 'mathematics'
        elif re.search(r'\\b(?:physics|phy)\\b', filename_lower):
            return 'physics'
        elif re.search(r'\\b(?:chemistry|chem)\\b', filename_lower):
            return 'chemistry'
        elif re.search(r'\\b(?:biology|bio)\\b', filename_lower):
            return 'biology'
        
        return 'unknown'
    
    def _detect_class_from_filename(self, filename: str) -> str:
        """Detect class from filename."""
        filename_lower = filename.lower()
        
        # Try class pattern first
        class_match = re.search(r'\\bclass[\\s_-]*([0-9]{1,2})\\b', filename_lower)
        if class_match:
            return f'class_{class_match.group(1)}'
        
        # Try exam patterns
        if 'jee' in filename_lower:
            return 'jee'
        elif 'neet' in filename_lower:
            return 'neet'
        
        # Try standalone numbers
        numbers = re.findall(r'\\b([0-9]{1,2})\\b', filename_lower)
        valid_classes = [n for n in numbers if int(n) >= 9 and int(n) <= 12]
        if valid_classes:
            return f'class_{valid_classes[0]}'
        
        return 'unknown'


def main():
    """Main function with user-friendly interface."""
    
    organizer = CustomBookOrganizer()
    
    print("📚 Welcome to Your Custom Book Organizer!")
    print("=========================================")
    print()
    
    # Check if raw books directory exists
    if not organizer.raw_books_dir.exists():
        print(f"❌ Raw books directory not found: {organizer.raw_books_dir}")
        print("Please create it first and add some books!")
        return
    
    # Show current structure
    organizer.show_source_structure()
    
    print("\\n🔧 Organization Options:")
    print("1. Organize ALL books from all folders")
    print("2. Organize books from a specific folder")
    print("3. Just show me what would happen (preview)")
    print("4. Exit")
    
    choice = input("\\nChoose option (1-4): ").strip()
    
    if choice == "1":
        print("\\n🚀 Organizing all books...")
        organizer.organize_all_books()
        
    elif choice == "2":
        print("\\n📂 Available folders:")
        folders = []
        import os
        for root, dirs, files in os.walk(organizer.raw_books_dir):
            if any(f.endswith('.pdf') for f in files):
                folders.append(str(root))
        
        for i, folder in enumerate(folders, 1):
            rel_path = Path(folder).relative_to(organizer.raw_books_dir)
            pdf_count = len(list(Path(folder).glob('*.pdf')))
            print(f"   {i}. {rel_path} ({pdf_count} PDFs)")
        
        try:
            folder_choice = int(input("\\nChoose folder number: ")) - 1
            if 0 <= folder_choice < len(folders):
                organizer.process_single_folder(folders[folder_choice])
            else:
                print("❌ Invalid choice")
        except (ValueError, IndexError):
            print("❌ Invalid input")
    
    elif choice == "3":
        print("\\n👀 Preview mode - showing what would happen...")
        # Just show detection without moving files
        
    else:
        print("👋 Goodbye!")


if __name__ == "__main__":
    main()


# QUICK USAGE GUIDE:
"""
🚀 HOW TO USE YOUR CUSTOM ORGANIZER:

1. DOWNLOAD BOOKS into the appropriate raw folders:
   📚 NCERT Math Class 10 → Core_Curriculum/CBSE/Textbooks/
   📚 Arihant JEE Physics → Entrance_Prep/JEE/Main/
   📚 RD Sharma Solutions → Competitive_Publishers/RD_Sharma/

2. RUN THE ORGANIZER:
   ```bash
   cd /Users/sushantnandwana/klaro-unified
   python3 organize_my_books.py
   ```

3. CHOOSE OPTION:
   - Option 1: Organize everything at once
   - Option 2: Organize one folder at a time (recommended for testing)

4. VERIFY RESULTS:
   Books get organized into textbooks/publisher/subject/class/

NAMING TIP: 
Even with folders, good names help:
✅ "NCERT Mathematics Class 10 Textbook 2023.pdf"
✅ "Arihant JEE Physics Practice Book.pdf"  
✅ "RD Sharma Class 11 Solutions Manual.pdf"
"""
