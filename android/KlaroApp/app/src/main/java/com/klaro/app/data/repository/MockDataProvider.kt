package com.klaro.app.data.repository

import com.klaro.app.data.models.*

/**
 * 🎭 Mock Data Provider
 * Provides sample data for development when backend is not available
 */
object MockDataProvider {

    fun getQuizPresets(): Map<String, QuizPreset> = mapOf(
        "jee_main_math" to QuizPreset(
            presetId = "jee_main_math",
            name = "JEE Main Mathematics",
            description = "Complete JEE Main Math practice",
            topics = listOf("Algebra", "Calculus", "Trigonometry"),
            questions = 30,
            duration = 90,
            difficulty = listOf("medium", "hard")
        ),
        "neet_physics" to QuizPreset(
            presetId = "neet_physics",
            name = "NEET Physics",
            description = "NEET Physics preparation",
            topics = listOf("Mechanics", "Thermodynamics", "Optics"),
            questions = 45,
            duration = 120,
            difficulty = listOf("easy", "medium")
        )
    )

    fun mockJEETestResponse(subjects: List<String>, topics: List<String>, duration: Int): JEETestResponse {
        val qs = (1..10).map { idx ->
            JEEQuestion(
                questionId = "jee_q_$idx",
                questionText = "Sample JEE Question $idx" + (if (topics.isNotEmpty()) " on ${topics[idx % topics.size]}" else ""),
                options = listOf("A", "B", "C", "D"),
                questionType = "mcq",
                subject = subjects.getOrElse(0) { "Mathematics" },
                topic = topics.getOrElse(0) { "Algebra" },
                difficulty = listOf("easy","medium","hard")[idx % 3],
                marks = 4,
                negativeMarks = -1.0
            )
        }
        return JEETestResponse(
            testId = "mock_test_${System.currentTimeMillis()}",
            title = "Mock ${subjects.joinToString(", ")}",
            questions = qs,
            totalQuestions = qs.size,
            duration = duration,
            subjects = subjects,
            createdAt = "2025-09-03T00:00:00Z"
        )
    }

    fun mockPYQs(subject: String?, year: Int?, limit: Int): List<JEEQuestion> {
        val subj = subject ?: "Mathematics"
        val topics = topicOptions[subj] ?: listOf("Algebra", "Calculus")
        return (1..limit).map { idx ->
            JEEQuestion(
                questionId = "pyq_${year ?: 2024}_$idx",
                questionText = "PYQ ${year ?: 2024} - $subj Question $idx on ${topics[idx % topics.size]}",
                options = listOf("A","B","C","D"),
                questionType = "mcq",
                subject = subj,
                topic = topics[idx % topics.size],
                difficulty = listOf("easy","medium","hard")[idx % 3],
                marks = 4,
                negativeMarks = -1.0
            )
        }
    }

    fun mockQuizResponse(): QuizResponse = QuizResponse(
        quizId = "mock_quiz_${System.currentTimeMillis()}",
        title = "Sample Quiz",
        questionsFile = null,
        answersFile = null,
        pdfQuestionsFile = null,
        pdfAnswersFile = null,
        pdfMarkingSchemeFile = null,
        metadata = mapOf(
            "total_questions" to 10,
            "total_points" to 100
        ),
        createdAt = "2025-09-01T19:15:00Z"
    )

    fun mockDoubtSolution(question: String): DoubtSolution = DoubtSolution(
        question = question,
        answer = "This is a sample solution for: $question\n\nStep-by-step approach:\n1. Identify the problem type\n2. Apply relevant formulas\n3. Calculate the result",
        steps = listOf(
            SolutionStep(1, "Problem Analysis", "Break down the given information", 0.9),
            SolutionStep(2, "Formula Application", "Apply the relevant mathematical formula", 0.85),
            SolutionStep(3, "Final Calculation", "Compute the final answer", 0.92)
        ),
        metadata = DoubtMetadata(
            topic = "Mathematics",
            difficulty = "medium",
            confidence = 0.89,
            method = "analytical",
            cost = 0.0,
            timeTaken = 2.5,
            retryAttempts = 0
        ),
        mobileFormat = MobileFormat(
            shortAnswer = "Sample answer for mobile view",
            keySteps = listOf("Step 1: Analyze", "Step 2: Apply", "Step 3: Calculate"),
            visualAids = listOf("Graph visualization", "Formula diagram"),
            practiceProblems = listOf("Similar problem 1", "Similar problem 2")
        ),
        whatsappFormat = "📚 Solution: $question\n\n✅ Answer: Sample solution\n\n📝 Steps:\n1. Analyze\n2. Apply\n3. Calculate"
    )

    // Quiz Generation Options
    val streamOptions = listOf("All", "Science", "Commerce", "Arts")
    val classOptions = listOf("All", "Class 9", "Class 10", "Class 11", "Class 12")
    val subjectOptions = listOf("All", "Mathematics", "Physics", "Chemistry", "Biology", "English", "Hindi")
    val topicOptions = mapOf(
        "Mathematics" to listOf("All", "Algebra", "Geometry", "Calculus", "Trigonometry", "Statistics"),
        "Physics" to listOf("All", "Mechanics", "Thermodynamics", "Optics", "Electricity", "Magnetism"),
        "Chemistry" to listOf("All", "Organic", "Inorganic", "Physical", "Biochemistry")
    )
    val subtopicOptions = mapOf(
        "Algebra" to listOf("All", "Linear Equations", "Quadratic Equations", "Polynomials"),
        "Calculus" to listOf("All", "Derivatives", "Integrals", "Limits", "Applications")
    )
    val questionTypeOptions = listOf("All", "MCQ", "Short Answer", "Long Answer", "Numerical")
    val levelOptions = listOf("All", "Easy", "Medium", "Hard", "Expert")
    val sourceMaterialOptions = listOf("All", "NCERT", "Previous Year Papers", "Reference Books", "Mock Tests")
    val languageOptions = listOf("All", "English", "Hindi", "Tamil", "Telugu", "Bengali")
    val centerOptions = listOf("All", "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Pune")
}
