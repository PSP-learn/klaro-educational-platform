package com.klaro.app.data.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

/**
 * 📊 API Data Models
 * 
 * Data classes for communication with Klaro FastAPI backend
 */

// ================================================================================
// 📄 Quiz/PDF Generation Models
// ================================================================================

@Parcelize
data class QuizRequest(
    val topics: List<String>,
    val numQuestions: Int = 10,
    val questionTypes: List<String> = listOf("mcq", "short"),
    val difficultyLevels: List<String> = listOf("easy", "medium"),
    val subject: String = "Mathematics",
    val title: String? = null
) : Parcelable

@Parcelize
data class QuizResponse(
    val quizId: String,
    val title: String,
    val totalQuestions: Int,
    val totalPoints: Int,
    val createdAt: String,
    val downloadUrl: String
) : Parcelable

@Parcelize
data class QuizPreset(
    val presetId: String,
    val name: String,
    val description: String,
    val topics: List<String>,
    val questions: Int,
    val duration: Int,
    val difficulty: List<String>
) : Parcelable

// ================================================================================
// 🎯 JEE Test Models
// ================================================================================

@Parcelize
data class JEETestRequest(
    val testType: String = "full_mock", // "full_mock", "subject_practice", "topic_practice"
    val subjects: List<String> = listOf("Mathematics", "Physics", "Chemistry"),
    val topics: List<String> = emptyList(),
    val duration: Int = 180, // minutes
    val difficulty: String = "mixed"
) : Parcelable

@Parcelize
data class JEEQuestion(
    val questionId: String,
    val questionText: String,
    val options: List<String>? = null, // null for numerical questions
    val questionType: String, // "mcq" or "numerical"
    val subject: String,
    val topic: String,
    val difficulty: String,
    val marks: Int,
    val negativeMarks: Double
) : Parcelable

@Parcelize
data class JEETestResponse(
    val testId: String,
    val title: String,
    val questions: List<JEEQuestion>,
    val totalQuestions: Int,
    val duration: Int,
    val subjects: List<String>,
    val createdAt: String
) : Parcelable

@Parcelize
data class JEEAnswer(
    val questionId: String,
    val selectedOption: String? = null, // for MCQ
    val numericalValue: Double? = null, // for numerical
    val timeTaken: Long, // milliseconds
    val isMarkedForReview: Boolean = false
) : Parcelable

@Parcelize
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
) : Parcelable

@Parcelize
data class TestAnalysis(
    val strongTopics: List<String>,
    val weakTopics: List<String>,
    val recommendations: List<String>,
    val timeManagement: String,
    val accuracyRate: Double
) : Parcelable

// ================================================================================
// 🤔 Doubt Solving Models
// ================================================================================

@Parcelize
data class DoubtRequest(
    val question: String,
    val subject: String = "Mathematics",
    val userId: String,
    val userPlan: String = "basic",
    val context: String? = null,
    val imageData: String? = null // Base64 encoded image
) : Parcelable

@Parcelize
data class DoubtSolution(
    val question: String,
    val answer: String,
    val steps: List<SolutionStep>,
    val metadata: DoubtMetadata,
    val mobileFormat: MobileFormat,
    val whatsappFormat: String
) : Parcelable

@Parcelize
data class SolutionStep(
    val stepNumber: Int,
    val title: String,
    val explanation: String,
    val confidence: Double
) : Parcelable

@Parcelize
data class DoubtMetadata(
    val topic: String,
    val difficulty: String,
    val confidence: Double,
    val method: String,
    val cost: Double,
    val timeTaken: Double,
    val retryAttempts: Int
) : Parcelable

@Parcelize
data class MobileFormat(
    val shortAnswer: String,
    val keySteps: List<String>,
    val visualAids: List<String>,
    val practiceProblems: List<String>
) : Parcelable

// ================================================================================
// 👤 User Management Models
// ================================================================================

@Parcelize
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
) : Parcelable

@Parcelize
data class UserProfile(
    val user: User,
    val stats: UserStats,
    val achievements: List<Achievement>,
    val subscription: SubscriptionInfo
) : Parcelable

@Parcelize
data class UserStats(
    val totalQuizzes: Int,
    val totalTests: Int,
    val totalDoubts: Int,
    val averageScore: Double,
    val studyStreak: Int,
    val hoursStudied: Double
) : Parcelable

@Parcelize
data class Achievement(
    val name: String,
    val description: String,
    val earnedDate: String,
    val iconUrl: String? = null
) : Parcelable

@Parcelize
data class SubscriptionInfo(
    val plan: String,
    val doubtsRemaining: Int? = null, // null for unlimited
    val renewalDate: String,
    val features: List<String>
) : Parcelable

// ================================================================================
// 📊 Analytics Models
// ================================================================================

@Parcelize
data class UserAnalytics(
    val userMetrics: Map<String, String>,
    val insights: Map<String, String>,
    val recommendations: List<String>,
    val costEfficiency: Map<String, String>
) : Parcelable

// ================================================================================
// 🌐 API Response Wrappers
// ================================================================================

data class ApiResponse<T>(
    val success: Boolean,
    val data: T? = null,
    val error: String? = null,
    val message: String? = null
)

data class PaginatedResponse<T>(
    val items: List<T>,
    val totalCount: Int,
    val hasMore: Boolean,
    val nextOffset: Int? = null
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
