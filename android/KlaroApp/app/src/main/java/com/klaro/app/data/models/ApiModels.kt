package com.klaro.app.data.models

/**
 * 📊 API Data Models
 * 
 * Data classes for communication with Klaro FastAPI backend
 */

// ================================================================================
// 📄 Quiz/PDF Generation Models
// ================================================================================

data class QuizRequest(
    val topics: List<String>,
    val numQuestions: Int = 10,
    val questionTypes: List<String> = listOf("mcq", "short"),
    val difficultyLevels: List<String> = listOf("easy", "medium"),
    val subject: String = "Mathematics",
    val title: String? = null,
    val source: String? = null
)

data class QuizResponse(
    val quizId: String,
    val title: String,
    val totalQuestions: Int,
    val totalPoints: Int,
    val createdAt: String,
    val downloadUrl: String
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
    val userId: String,
    val userPlan: String = "basic",
    val context: String? = null,
    val imageData: String? = null
)

data class DoubtSolution(
    val question: String,
    val answer: String,
    val steps: List<SolutionStep>,
    val metadata: DoubtMetadata,
    val mobileFormat: MobileFormat,
    val whatsappFormat: String
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
