#!/usr/bin/env python3
"""
Demo: User Input Workflow

This script demonstrates exactly where and how users provide input to customize their quizzes.
"""

def demo_interactive_workflow():
    """Show the interactive workflow with simulated user inputs"""
    
    print("🎯 DEMO: Interactive Quiz Creation Workflow")
    print("=" * 60)
    print("\nThis shows exactly where users provide input:\n")
    
    # Simulate the interactive prompts
    print("🎨 Custom Quiz Creator")
    print("=" * 50)
    print()
    
    # Example user inputs (what the user would type)
    demo_inputs = {
        "Quiz title": "My Algebra Practice Test",
        "Subject": "Mathematics", 
        "Topics": "quadratic equations, polynomials, factorization",
        "Question types": "mcq, short",
        "Difficulty levels": "easy, medium", 
        "Number of questions": "8",
        "Duration in minutes": "45"
    }
    
    for prompt, user_input in demo_inputs.items():
        print(f"💬 System asks: {prompt}")
        print(f"👤 User types: '{user_input}'")
        print()
    
    print("🔄 System then generates quiz based on these inputs...")
    print()
    print("📄 OUTPUT: Custom quiz with:")
    print("   • 8 questions about quadratic equations and polynomials")  
    print("   • Mix of MCQ and short answer questions")
    print("   • Easy and medium difficulty levels")
    print("   • 45-minute duration")
    print("   • Professional formatting with answer key")

def demo_command_line_workflow():
    """Show command line input options"""
    
    print("\n🖥️  DEMO: Command Line Input Options")
    print("=" * 60)
    print()
    
    examples = [
        {
            "description": "Search your textbooks",
            "command": "./manage_books.sh search 'quadratic equations'",
            "user_input": "The search term in quotes"
        },
        {
            "description": "Quick quiz generation", 
            "command": "./manage_books.sh quiz-quick 'algebra,geometry' 10",
            "user_input": "Topics in quotes + number of questions"
        },
        {
            "description": "Use preset quiz",
            "command": "./manage_books.sh quiz-create class_10_algebra_basic", 
            "user_input": "Just the preset name"
        },
        {
            "description": "Advanced quiz with all options",
            "command": "python3 smart_quiz_generator.py --topics 'trigonometry' --questions 5 --types mcq,short --difficulty medium",
            "user_input": "Multiple parameters: topics, question count, types, difficulty"
        }
    ]
    
    for example in examples:
        print(f"📝 {example['description']}:")
        print(f"   Command: {example['command']}")
        print(f"   👤 User Input: {example['user_input']}")
        print()

def demo_customization_files():
    """Show file-based customization"""
    
    print("\n📁 DEMO: File-Based Customization")
    print("=" * 60)
    print()
    print("Users can create custom configuration files:")
    print()
    print("📄 example_subject_mapping.json")
    print("   👤 User defines: Custom subject categories")
    print("   📝 Contains: Topic keywords and categorization rules")
    print()
    print("📄 Custom quiz templates (future)")
    print("   👤 User defines: Question templates and difficulty rules")
    print("   📝 Contains: Question patterns and scoring rubrics")

if __name__ == "__main__":
    demo_interactive_workflow()
    demo_command_line_workflow() 
    demo_customization_files()
    
    print("\n🎯 SUMMARY: User Input Locations")
    print("=" * 60)
    print("1. 💬 Interactive prompts (--custom mode)")
    print("2. 🖥️  Command line arguments (--topics, --questions, etc.)")
    print("3. 📋 Preset selection (choosing from predefined options)")
    print("4. 📁 Configuration files (JSON files for advanced customization)")
    print("\nThe system is designed to be flexible - users can provide input")
    print("in whatever way is most convenient for them!")
