#!/usr/bin/env python3
"""
Live Demo: User Interface Experience

This shows exactly what users see when they interact with the quiz generator.
"""

def show_main_menu():
    """Show the main menu interface"""
    print("🎯 Quiz Manager - Your Test Creation Assistant")
    print("=" * 60)
    print("\nWhat would you like to do?")
    print("\n1. 📚 Use a preset quiz (--preset or --list-presets)")
    print("2. 🎨 Create custom quiz (--custom)")
    print("3. 🚀 Quick quiz from topics (--topics 'topic1,topic2')")
    print("4. 📋 View recent quizzes (--recent)")
    print("\nExamples:")
    print("  python3 quiz_manager.py --list-presets")
    print("  python3 quiz_manager.py --preset class_10_algebra_basic")
    print("  python3 quiz_manager.py --custom")
    print("  python3 quiz_manager.py --topics 'quadratic equations,trigonometry' --questions 8")
    print("\nFor detailed help: python3 quiz_manager.py --help")

def show_interactive_prompts():
    """Show what the interactive custom quiz interface looks like"""
    print("\n" + "="*80)
    print("🎨 INTERACTIVE MODE - What users see when they run --custom:")
    print("="*80)
    
    print("\n🎨 Custom Quiz Creator")
    print("=" * 50)
    
    # Show the actual prompts users see
    prompts_and_responses = [
        ("Quiz title (optional): ", "My Algebra Practice Test"),
        ("Subject (default: Mathematics): ", "Mathematics"),
        ("", "\nSuggested topics from your textbooks:"),
        ("", "  quadratic equations, polynomials, trigonometry, geometry"),
        ("", ""),
        ("Enter topics (comma-separated): ", "quadratic equations, polynomials"),
        ("", "\n📋 Question Configuration:"),
        ("", "Available types: mcq, short, long"),
        ("Question types (default: mcq,short): ", "mcq, short"),
        ("", "\nDifficulty levels: easy, medium, hard"),
        ("Difficulty levels (default: easy,medium): ", "easy, medium"),
        ("Number of questions (default: 10): ", "8"),
        ("Duration in minutes (default: auto-calculate): ", "45"),
    ]
    
    for prompt, response in prompts_and_responses:
        if prompt:
            print(f"{prompt}", end="")
            if response and not response.startswith(("\n", " ")):
                print(f"{response}")
            else:
                print()
        else:
            print(response)
    
    print("\n🔄 Generating custom quiz...")
    print("✅ Custom quiz created!")
    print("📄 Questions: generated_tests/my_algebra_practice_test_20250830_110000_questions.txt")
    print("📚 Answers: generated_tests/my_algebra_practice_test_20250830_110000_answers.txt")

def show_preset_interface():
    """Show preset selection interface"""
    print("\n" + "="*80)
    print("📚 PRESET MODE - Available quiz templates:")
    print("="*80)
    
    presets = [
        {
            "id": "class_10_algebra_basic",
            "name": "Class 10 - Algebra Basics",
            "desc": "Fundamental algebraic concepts",
            "topics": "polynomials, linear equations, quadratic equations",
            "questions": "15 (45 min)",
            "types": "mcq, short",
            "difficulty": "easy, medium"
        },
        {
            "id": "class_10_trigonometry", 
            "name": "Class 10 - Trigonometry",
            "desc": "Trigonometric ratios and applications",
            "topics": "trigonometry, trigonometric ratios, applications",
            "questions": "10 (60 min)",
            "types": "mcq, short",
            "difficulty": "medium, hard"
        },
        {
            "id": "quick_revision",
            "name": "Quick Revision Test", 
            "desc": "Fast review of key concepts",
            "topics": "quadratic equations, triangles, trigonometry",
            "questions": "20 (30 min)",
            "types": "mcq",
            "difficulty": "easy"
        }
    ]
    
    for preset in presets:
        print(f"\n🎯 {preset['id']}")
        print(f"   📖 {preset['name']}")
        print(f"   📝 {preset['desc']}")
        print(f"   📋 Topics: {preset['topics']}")
        print(f"   ❓ Questions: {preset['questions']}")
        print(f"   📊 Types: {preset['types']}")
        print(f"   ⚡ Difficulty: {preset['difficulty']}")
    
    print(f"\n💡 To use: python3 quiz_manager.py --preset class_10_algebra_basic")

def show_command_line_examples():
    """Show command line interface examples"""
    print("\n" + "="*80)
    print("🖥️ COMMAND LINE MODE - Direct parameter input:")
    print("="*80)
    
    examples = [
        ("Quick quiz generation:", "python3 quiz_manager.py --topics 'algebra,geometry' --questions 10"),
        ("Using shell script:", "./manage_books.sh quiz-quick 'trigonometry' 5"),
        ("Advanced options:", "python3 smart_quiz_generator.py --topics 'calculus' --questions 8 --types mcq,short --difficulty medium"),
        ("With output file:", "python3 quiz_manager.py --topics 'statistics' --questions 12 --output my_stats_test")
    ]
    
    for desc, cmd in examples:
        print(f"\n📝 {desc}")
        print(f"   $ {cmd}")
        print(f"   👤 User types this entire command and presses Enter")

if __name__ == "__main__":
    print("🔍 USER INTERFACE DEMONSTRATION")
    print("How users interact with your quiz generator system")
    print("="*80)
    
    show_main_menu()
    show_interactive_prompts()
    show_preset_interface()
    show_command_line_examples()
    
    print("\n" + "="*80)
    print("🎯 SUMMARY: What Users See")
    print("="*80)
    print("1. 📋 Main menu with clear options and examples")
    print("2. 💬 Step-by-step prompts in interactive mode") 
    print("3. 📚 Beautiful preset listings with all details")
    print("4. 🖥️ Simple command line options for power users")
    print("\n✨ The interface is designed to be user-friendly and intuitive!")
