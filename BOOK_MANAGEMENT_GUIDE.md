# PDF Book Management System

A comprehensive system for organizing and searching through your PDF book collection using AI-powered semantic search.

## Features

### 📚 Book Organization (`book_organizer.py`)
- **Multiple Organization Strategies**: Subject-first, purpose-first, publisher-first, or mixed approaches
- **Smart Categorization**: Automatic categorization based on PDF metadata and content analysis
- **Duplicate Detection**: Identifies potential duplicate books
- **Safe Operations**: Dry-run mode and comprehensive error handling
- **Customizable**: Custom subject mappings and folder structures

### 🔍 Semantic Search (`book_search.py`)
- **AI-Powered Search**: Uses sentence-transformers for semantic understanding
- **Fast Retrieval**: FAISS vector database for efficient similarity search
- **Rich Metadata**: Tracks book titles, authors, page numbers, and file paths
- **Multiple PDF Readers**: PyMuPDF and pdfplumber support for robust text extraction
- **Incremental Updates**: Only processes new or modified books

## Quick Start

### 1. Install Dependencies
```bash
pip3 install PyMuPDF pdfplumber sentence-transformers faiss-cpu
```

### 2. Organize Your Books
```bash
# Preview organization (recommended first step)
python3 book_organizer.py /path/to/messy/books /path/to/organized/books --strategy subject --preview

# Dry run to see what would happen
python3 book_organizer.py /path/to/messy/books /path/to/organized/books --strategy subject --dry-run

# Actually organize the books
python3 book_organizer.py /path/to/messy/books /path/to/organized/books --strategy subject
```

### 3. Build Search Index
```bash
# Process all books in organized directory
python3 book_search.py --directory /path/to/organized/books

# Check database statistics
python3 book_search.py --stats
```

### 4. Search Your Books
```bash
# Command line search
python3 book_search.py --search "machine learning algorithms"

# Interactive search mode
python3 book_search.py
```

## Organization Strategies

### Subject-First Strategy (Default)
Organizes books by topic/subject matter:
```
organized_books/
├── programming/
│   ├── Martin_Fowler/
│   │   └── Refactoring_Improving_the_Design_of_Existing_Code.pdf
│   └── Robert_Martin/
│       └── Clean_Code.pdf
├── data_science/
│   └── Hands_On_Machine_Learning.pdf
└── business/
    └── The_Lean_Startup.pdf
```

### Purpose-First Strategy
Organizes by how you use the books:
```
organized_books/
├── reference/
│   └── programming/
│       └── Python_Reference_Manual.pdf
├── learning/
│   └── data_science/
│       └── Introduction_to_Machine_Learning.pdf
└── project_books/
    └── Build_Your_Own_Neural_Network.pdf
```

### Publisher-First Strategy
Organizes by publisher/source:
```
organized_books/
├── oreilly/
│   └── programming/
│       └── Learning_Python.pdf
├── manning/
│   └── data_science/
│       └── Data_Science_Bookcamp.pdf
└── academic/
    └── Machine_Learning_Research_Papers.pdf
```

### Mixed Strategy
Combines subject and purpose:
```
organized_books/
├── programming/
│   ├── reference/
│   │   └── Python_Documentation.pdf
│   └── learning/
│       └── Learn_Python_the_Hard_Way.pdf
└── data_science/
    ├── research/
    │   └── Deep_Learning_Papers.pdf
    └── project_books/
        └── Practical_Machine_Learning.pdf
```

## Advanced Usage

### Custom Subject Mapping
Create a JSON file with custom subject categories:

```json
{
  "web_development": ["html", "css", "javascript", "react", "vue", "angular"],
  "mobile_development": ["ios", "android", "swift", "kotlin", "react native"],
  "devops": ["docker", "kubernetes", "aws", "azure", "devops", "ci/cd"]
}
```

Use it with:
```bash
python3 book_organizer.py source target --strategy subject --subject-mapping custom_subjects.json
```

### Different PDF Extraction Methods
If one method fails, try another:
```bash
# Use pdfplumber instead of PyMuPDF
python3 book_search.py --directory /path/to/books --extraction-method pdfplumber
```

### Advanced Search Options
```bash
# Use different embedding model
python3 book_search.py --model all-mpnet-base-v2 --search "neural networks"

# Get more results
python3 book_search.py --search "python programming" --top-k 20

# Store database in custom location
python3 book_search.py --db-dir /path/to/custom/db --directory /path/to/books
```

## Example Workflows

### 1. New Book Collection Setup
```bash
# 1. Preview organization
python3 book_organizer.py ~/Downloads/books ~/organized_books --strategy subject --preview

# 2. Organize books
python3 book_organizer.py ~/Downloads/books ~/organized_books --strategy subject

# 3. Build search index
python3 book_search.py --directory ~/organized_books

# 4. Test search
python3 book_search.py --search "design patterns"
```

### 2. Adding New Books
```bash
# 1. Organize new books
python3 book_organizer.py ~/Downloads/new_books ~/organized_books --strategy subject

# 2. Update search index (only processes new/changed files)
python3 book_search.py --directory ~/organized_books
```

### 3. Rebuilding Everything
```bash
# Force rebuild of search database
python3 book_search.py --directory ~/organized_books --rebuild

# Force reorganization of books
python3 book_organizer.py ~/organized_books ~/organized_books_new --strategy mixed
```

## Command Reference

### Book Organizer Commands
```bash
# Basic organization
python3 book_organizer.py <source_dir> <target_dir>

# With specific strategy
python3 book_organizer.py source target --strategy [subject|purpose|publisher|mixed]

# Safe preview mode
python3 book_organizer.py source target --preview

# Dry run mode
python3 book_organizer.py source target --dry-run

# Custom subject mapping
python3 book_organizer.py source target --subject-mapping mapping.json

# Custom report file
python3 book_organizer.py source target --report my_report.json
```

### Book Search Commands
```bash
# Build/update index
python3 book_search.py --directory <books_directory>

# Search books
python3 book_search.py --search "your query here"

# Interactive search
python3 book_search.py

# Show database statistics
python3 book_search.py --stats

# Custom settings
python3 book_search.py --model all-mpnet-base-v2 --db-dir custom_db --top-k 15

# Force rebuild
python3 book_search.py --directory <books_directory> --rebuild
```

## Configuration Examples

### Custom Subject Mapping (`custom_subjects.json`)
```json
{
  "artificial_intelligence": [
    "ai", "artificial intelligence", "machine learning", "deep learning", 
    "neural networks", "nlp", "computer vision"
  ],
  "web_technologies": [
    "html", "css", "javascript", "typescript", "react", "vue", "angular", 
    "node", "express", "web development"
  ],
  "databases": [
    "sql", "nosql", "mongodb", "postgresql", "mysql", "database", 
    "data modeling", "redis"
  ],
  "cloud_computing": [
    "aws", "azure", "gcp", "cloud", "serverless", "microservices", 
    "containers", "docker", "kubernetes"
  ]
}
```

## Search Examples

### Programming Concepts
```bash
python3 book_search.py --search "design patterns singleton factory"
python3 book_search.py --search "algorithm complexity big O notation"
python3 book_search.py --search "functional programming monads"
```

### Specific Technologies
```bash
python3 book_search.py --search "React hooks useEffect useState"
python3 book_search.py --search "Docker containers orchestration"
python3 book_search.py --search "PostgreSQL query optimization"
```

### Conceptual Searches
```bash
python3 book_search.py --search "how to handle user authentication"
python3 book_search.py --search "best practices for API design"
python3 book_search.py --search "debugging techniques for distributed systems"
```

## Tips for Best Results

### Organization Tips
1. **Start Small**: Test with a small subset of books first
2. **Use Preview**: Always preview before organizing
3. **Backup**: Keep original files safe
4. **Custom Mapping**: Create subject mappings that match your interests
5. **Consistent Naming**: Clean up file names before organizing

### Search Tips
1. **Be Specific**: More specific queries yield better results
2. **Use Context**: Include context words in your search
3. **Try Variations**: If first search doesn't work, try different phrasing
4. **Check Stats**: Monitor database statistics to ensure all books are indexed
5. **Update Regularly**: Re-run indexing when you add new books

## Troubleshooting

### Common Issues

1. **No text extracted**: Some PDFs are image-based. Consider OCR tools.
2. **Memory issues**: Process books in smaller batches
3. **Encoding errors**: Some PDF metadata may have encoding issues
4. **Permission errors**: Ensure read/write access to directories

### Performance Optimization

1. **Use PyMuPDF**: Generally faster than pdfplumber
2. **Adjust chunk size**: Balance between context and processing speed
3. **Better hardware**: More RAM and CPU cores help with embedding generation
4. **SSD storage**: Faster disk I/O improves database operations

## File Locations

After running the scripts, you'll have:
- **Organized books**: In your specified target directory
- **Search database**: In `book_db/` directory (or custom location)
- **Organization report**: `organization_report.json`
- **Log files**: Console output with detailed logging

This system grows with your collection and provides powerful search capabilities across all your technical books!
