package com.klaro.app.data.models

import com.google.gson.annotations.SerializedName

/**
 * 📊 API Data Models
 * 
 * Data classes for communication with Klaro FastAPI backend
 */

// ================================================================================
// 📄 Quiz/PDF Generation Models
// ================================================================================

data class BlueprintConfig(
    @SerializedName("total_questions") val totalQuestions: Int? = null,
    @SerializedName("by_type") val byType: Map<String, Int>? = null,
    @SerializedName("by_difficulty") val byDifficulty: Map<String, Int>? = null,
    @SerializedName("duration_minutes") val durationMinutes: Int? = null
)

data class SectionConfig(
    val name: String,
    val types: List<String>,
    val count: Int,
    val difficulty: Map<String, Int>? = null,
    @SerializedName("negative_marking") val negativeMarking: Double? = 0.0
)

data class QuizRequest(
    val topics: List<String>,
    @SerializedName("num_questions") val numQuestions: Int = 10,
    @SerializedName("question_types") val questionTypes: List<String> = listOf("mcq", "short"),
    @SerializedName("difficulty_levels") val difficultyLevels: List<String> = listOf("easy", "medium"),
    val subject: String = "Mathematics",
    val duration: Int? = null,
    val title: String? = null,
    // New customization fields
    val domain: String? = null, // CBSE | JEE | NEET
    val grade: String? = null,
    val subjects: List<String>? = null,
    val header: String? = null,
    val instructions: List<String>? = null,
    val mode: String? = "mixed",
    @SerializedName("scope_filter") val scopeFilter: String? = null,
    val render: String? = "auto",
    @SerializedName("books_dir") val booksDir: String? = null,
    @SerializedName("output_engine") val outputEngine: String? = "reportlab",
    @SerializedName("include_solutions") val includeSolutions: Boolean? = false,
    val blueprint: BlueprintConfig? = null,
    val sections: List<SectionConfig>? = null,
    val marks: Map<String, Int>? = null,
    // UI metadata only
    val streams: List<String>? = null,
    @SerializedName("class_filter") val classFilter: List<String>? = null,
    @SerializedName("topic_tags") val topicTags: List<String>? = null,
    val subtopics: List<String>? = null,
    val levels: List<String>? = null,
    @SerializedName("source_material") val sourceMaterial: List<String>? = null,
    val language: String? = null,
    val centers: List<String>? = null
)

data class QuizResponse(
    @SerializedName("quiz_id") val quizId: String,
    val title: String,
    @SerializedName("questions_file") val questionsFile: String?,
    @SerializedName("answers_file") val answersFile: String?,
    @SerializedName("pdf_questions_file") val pdfQuestionsFile: String?,
    @SerializedName("pdf_answers_file") val pdfAnswersFile: String?,
    @SerializedName("pdf_marking_scheme_file") val pdfMarkingSchemeFile: String?,
    val metadata: Map<String, Any>?,
    @SerializedName("created_at") val createdAt: String
)

data class PreviewResponse(
    val valid: Boolean,
    val totals: Map<String, Int>,
    @SerializedName("duration_estimate") val durationEstimate: Int,
    val warnings: List<String> = emptyList(),
    @SerializedName("normalized_blueprint") val normalizedBlueprint: BlueprintConfig?
)

// ================================================================================
// 📚 Catalog Models
// ================================================================================

data class ChaptersResponse(
    val success: Boolean,
    val count: Int,
    val chapters: List<String>
)

data class SubtopicsResponse(
    val success: Boolean,
    val count: Int,
    val subtopics: List<String>
)

// ================================================================================
// 🎯 JEE Test Models
// ================================================================================

data class JEETestRequest(
    val testType: String = "full_mock",
    val subjects: List<String> = listOf("Mathematics", "Physics", "Chemistry"),
    val topics: List<String> = emptyList(),
    val duration: Int = 180,
    val difficulty: String = "mixed"
)

data class JEEQuestion(
    val questionId: String,
    val questionText: String,
    val options: List<String>? = null,
    val questionType: String,
    val subject: String,
    val topic: String,
    val difficulty: String,
    val marks: Int,
    val negativeMarks: Double
)

data class JEETestResponse(
    val testId: String,
    val title: String,
    val questions: List<JEEQuestion>,
    val totalQuestions: Int,
    val duration: Int,
    val subjects: List<String>,
    val createdAt: String
)

// ================================================================================
// 🤔 Doubt Solving Models
// ================================================================================

data class DoubtRequest(
    val question: String,
    val subject: String = "Mathematics",
    @SerializedName(value = "user_id", alternate = ["userId"]) val userId: String,
    @SerializedName(value = "user_plan", alternate = ["userPlan"]) val userPlan: String = "basic",
    val context: String? = null,
    @SerializedName(value = "image_data", alternate = ["imageData"]) val imageData: String? = null
)

data class DoubtSolution(
    val question: String,
    val answer: String,
    val steps: List<SolutionStep>,
    val metadata: DoubtMetadata,
    val mobileFormat: MobileFormat,
    val whatsappFormat: String,
    val handwrittenImages: List<String>? = null,
    val handwrittenPdfUrl: String? = null
)

data class SolutionStep(
    val stepNumber: Int,
    val title: String,
    val explanation: String,
    val confidence: Double
)

data class DoubtMetadata(
    val topic: String,
    val difficulty: String,
    val confidence: Double,
    val method: String,
    val cost: Double,
    val timeTaken: Double,
    val retryAttempts: Int
)

data class MobileFormat(
    val shortAnswer: String,
    val keySteps: List<String>,
    val visualAids: List<String>,
    val practiceProblems: List<String>
)

// ================================================================================
// 👤 User Management Models
// ================================================================================

data class User(
    val userId: String,
    val name: String,
    val email: String,
    val gradeLevel: String? = null,
    val subjects: List<String> = emptyList(),
    val plan: String = "basic",
    val joinedDate: String,
    val totalDoubtsAsked: Int = 0,
    val favoriteSubjects: List<String> = emptyList()
)

data class UserStats(
    val totalQuizzes: Int,
    val totalTests: Int,
    val totalDoubts: Int,
    val averageScore: Double,
    val studyStreak: Int,
    val hoursStudied: Double
)

data class UserAnalytics(
    val totalDoubts: Int,
    val doubtsThisWeek: Int,
    val averageResponseTime: Double,
    val topSubjects: List<String>,
    val accuracyRate: Double
)

data class Achievement(
    val id: String,
    val name: String,
    val description: String,
    val icon: String,
    val unlockedAt: String?
)

data class SubscriptionInfo(
    val plan: String,
    val status: String,
    val expiresAt: String?,
    val features: List<String>
)

// ================================================================================
// 🔄 API Response Wrappers
// ================================================================================

data class ApiResponse<T>(
    val data: T,
    val message: String,
    val status: String
)

data class PaginatedResponse<T>(
    val items: List<T>,
    val total: Int,
    val page: Int,
    val limit: Int,
    val hasNext: Boolean
)

data class DoubtsResponse(
    val question: String,
    val answer: String,
    val steps: List<SolutionStep>,
    val metadata: DoubtMetadata,
    val createdAt: String
)

// ================================================================================
// ⚠️ Error Models
// ================================================================================

data class ApiError(
    val code: String,
    val message: String,
    val details: Map<String, Any>? = null
)

enum class ErrorType {
    NETWORK_ERROR,
    TIMEOUT_ERROR,
    AUTHENTICATION_ERROR,
    QUOTA_EXCEEDED,
    INVALID_INPUT,
    SERVER_ERROR,
    UNKNOWN_ERROR
}

// ================================================================================
// 📄 Missing Models
// ================================================================================

data class QuizPreset(
    val presetId: String,
    val name: String,
    val description: String,
    val topics: List<String>,
    val questions: Int,
    val duration: Int,
    val difficulty: List<String>
)

data class JEEAnswer(
    val questionId: String,
    val selectedOption: String? = null,
    val numericalValue: Double? = null,
    val timeTaken: Long,
    val isMarkedForReview: Boolean = false
)

data class JEETestResult(
    val testId: String,
    val totalScore: Double,
    val maxScore: Int,
    val percentile: Double,
    val subjectWiseScores: Map<String, Double>,
    val correctAnswers: Int,
    val incorrectAnswers: Int,
    val unattempted: Int,
    val timeTaken: Long,
    val analysis: TestAnalysis
)

data class TestAnalysis(
    val strongTopics: List<String>,
    val weakTopics: List<String>,
    val recommendations: List<String>,
    val timeManagement: String,
    val accuracyRate: Double
)

data class UserProfile(
    val user: User,
    val stats: UserStats,
    val achievements: List<Achievement>,
    val subscription: SubscriptionInfo
)
