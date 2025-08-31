#!/bin/bash
# PDF Book Management Helper Script
#
# This script provides easy commands for common book management operations.

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORGANIZER_SCRIPT="$SCRIPT_DIR/book_organizer.py"
SEARCH_SCRIPT="$SCRIPT_DIR/book_search.py"
TEST_SCRIPT="$SCRIPT_DIR/test_system.py"
QUIZ_SCRIPT="$SCRIPT_DIR/quiz_manager.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo -e "${BLUE}PDF Book Management System${NC}"
    echo "=========================="
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  organize <source> <target> [strategy]  - Organize books"
    echo "  preview <source> <target> [strategy]   - Preview organization"
    echo "  index <directory>                      - Build search index"
    echo "  search <query>                         - Search books"
    echo "  interactive                            - Interactive search mode"
    echo "  stats                                  - Show database statistics"
    echo "  quiz-presets                           - List available quiz presets"
    echo "  quiz-create <preset_name>              - Create quiz from preset"
    echo "  quiz-custom                            - Create custom quiz (interactive)"
    echo "  quiz-quick <topics>                    - Quick quiz from topics"
    echo "  test                                   - Run system test"
    echo "  help                                   - Show this help"
    echo ""
    echo "Strategies: subject (default), purpose, publisher, mixed"
    echo ""
    echo "Examples:"
    echo "  $0 preview ~/Downloads/books ~/organized_books"
    echo "  $0 organize ~/Downloads/books ~/organized_books subject"
    echo "  $0 index ~/organized_books"
    echo "  $0 search 'machine learning'"
    echo "  $0 interactive"
}

check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 not found${NC}"
        exit 1
    fi
    
    # Check if required Python packages are available
    python3 -c "import fitz, pdfplumber, sentence_transformers, faiss" 2>/dev/null || {
        echo -e "${YELLOW}⚠️  Missing dependencies. Installing...${NC}"
        pip3 install PyMuPDF pdfplumber sentence-transformers faiss-cpu
    }
    
    echo -e "${GREEN}✅ Dependencies OK${NC}"
}

organize_books() {
    local source_dir="$1"
    local target_dir="$2"
    local strategy="${3:-subject}"
    
    if [[ ! -d "$source_dir" ]]; then
        echo -e "${RED}❌ Source directory not found: $source_dir${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}📚 Organizing books...${NC}"
    echo "Source: $source_dir"
    echo "Target: $target_dir"
    echo "Strategy: $strategy"
    echo ""
    
    python3 "$ORGANIZER_SCRIPT" "$source_dir" "$target_dir" --strategy "$strategy"
}

preview_organization() {
    local source_dir="$1"
    local target_dir="$2"
    local strategy="${3:-subject}"
    
    if [[ ! -d "$source_dir" ]]; then
        echo -e "${RED}❌ Source directory not found: $source_dir${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}👀 Previewing organization...${NC}"
    python3 "$ORGANIZER_SCRIPT" "$source_dir" "$target_dir" --strategy "$strategy" --preview
}

build_index() {
    local books_dir="$1"
    
    if [[ ! -d "$books_dir" ]]; then
        echo -e "${RED}❌ Books directory not found: $books_dir${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🔍 Building search index...${NC}"
    python3 "$SEARCH_SCRIPT" --directory "$books_dir"
}

search_books() {
    local query="$1"
    
    if [[ -z "$query" ]]; then
        echo -e "${RED}❌ Search query is required${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🔎 Searching for: '$query'${NC}"
    python3 "$SEARCH_SCRIPT" --search "$query"
}

interactive_search() {
    echo -e "${BLUE}🔍 Starting interactive search mode...${NC}"
    python3 "$SEARCH_SCRIPT"
}

show_stats() {
    echo -e "${BLUE}📊 Database Statistics${NC}"
    python3 "$SEARCH_SCRIPT" --stats
}

run_test() {
    echo -e "${BLUE}🧪 Running system test...${NC}"
    python3 "$TEST_SCRIPT"
}

quiz_presets() {
    echo -e "${BLUE}📚 Available Quiz Presets${NC}"
    python3 "$QUIZ_SCRIPT" --list-presets
}

quiz_create() {
    local preset_name="$1"
    
    if [[ -z "$preset_name" ]]; then
        echo -e "${RED}❌ Preset name is required${NC}"
        echo -e "${YELLOW}Use: $0 quiz-presets to see available presets${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🎯 Creating quiz from preset: $preset_name${NC}"
    python3 "$QUIZ_SCRIPT" --preset "$preset_name"
}

quiz_custom() {
    echo -e "${BLUE}🎨 Creating custom quiz...${NC}"
    python3 "$QUIZ_SCRIPT" --custom
}

quiz_quick() {
    local topics="$1"
    local num_questions="${2:-10}"
    
    if [[ -z "$topics" ]]; then
        echo -e "${RED}❌ Topics are required${NC}"
        echo -e "${YELLOW}Example: $0 quiz-quick 'quadratic equations,trigonometry'${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🚀 Creating quick quiz for: $topics${NC}"
    python3 "$QUIZ_SCRIPT" --topics "$topics" --questions "$num_questions"
}

# Main script logic
case "${1:-help}" in
    "organize")
        check_dependencies
        if [[ $# -lt 3 ]]; then
            echo -e "${RED}❌ Usage: $0 organize <source_dir> <target_dir> [strategy]${NC}"
            exit 1
        fi
        organize_books "$2" "$3" "$4"
        ;;
    
    "preview")
        check_dependencies
        if [[ $# -lt 3 ]]; then
            echo -e "${RED}❌ Usage: $0 preview <source_dir> <target_dir> [strategy]${NC}"
            exit 1
        fi
        preview_organization "$2" "$3" "$4"
        ;;
    
    "index")
        check_dependencies
        if [[ $# -lt 2 ]]; then
            echo -e "${RED}❌ Usage: $0 index <books_directory>${NC}"
            exit 1
        fi
        build_index "$2"
        ;;
    
    "search")
        check_dependencies
        if [[ $# -lt 2 ]]; then
            echo -e "${RED}❌ Usage: $0 search <query>${NC}"
            exit 1
        fi
        search_books "$2"
        ;;
    
    "interactive")
        check_dependencies
        interactive_search
        ;;
    
    "stats")
        check_dependencies
        show_stats
        ;;
    
    "test")
        check_dependencies
        run_test
        ;;
    
    "quiz-presets")
        check_dependencies
        quiz_presets
        ;;
    
    "quiz-create")
        check_dependencies
        if [[ $# -lt 2 ]]; then
            echo -e "${RED}❌ Usage: $0 quiz-create <preset_name>${NC}"
            exit 1
        fi
        quiz_create "$2"
        ;;
    
    "quiz-custom")
        check_dependencies
        quiz_custom
        ;;
    
    "quiz-quick")
        check_dependencies
        if [[ $# -lt 2 ]]; then
            echo -e "${RED}❌ Usage: $0 quiz-quick <topics> [num_questions]${NC}"
            exit 1
        fi
        quiz_quick "$2" "$3"
        ;;
    
    "help"|*)
        print_usage
        ;;
esac
