package com.klaro.app.data.repository

import com.klaro.app.data.api.KlaroApiService
import com.klaro.app.data.models.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.File
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 🤔 Doubt Solving Repository
 * 
 * Handles API calls for doubt solving, image OCR, and usage tracking
 */
@Singleton
class DoubtSolvingRepository @Inject constructor(
    private val apiService: KlaroApiService
) {

    private fun mapSolutionFromBody(body: Map<String, Any>?, question: String, subject: String): DoubtSolution? {
        val solution = body?.get("solution") as? Map<*, *> ?: return null
        val answer = (solution["final_answer"] as? String)
            ?: (solution["answer"] as? String)
            ?: (solution["shortAnswer"] as? String)
            ?: ""
        val stepsRaw = (solution["steps"] as? List<*>) ?: emptyList<Any>()
        val steps = stepsRaw.mapIndexed { idx, it ->
            val m = it as? Map<*, *> ?: emptyMap<String, Any>()
            SolutionStep(
                stepNumber = (m["stepNumber"] as? Number)?.toInt() ?: (idx + 1),
                title = (m["title"] as? String) ?: (m["heading"] as? String) ?: "Step ${idx + 1}",
                explanation = (m["explanation"] as? String) ?: (m["detail"] as? String) ?: "",
                confidence = (m["confidence"] as? Number)?.toDouble() ?: 0.0
            )
        }
        val whatsappFormat = (solution["whatsapp_format"] as? String)
            ?: (solution["whatsappFormat"] as? String)
            ?: answer
        val mobileFormat = MobileFormat(
            shortAnswer = (solution["shortAnswer"] as? String) ?: answer,
            keySteps = steps.map { it.title },
            visualAids = emptyList(),
            practiceProblems = emptyList()
        )
        val metadata = DoubtMetadata(
            topic = (solution["topic"] as? String) ?: subject,
            difficulty = (solution["difficulty"] as? String) ?: "",
            confidence = (solution["confidence"] as? Number)?.toDouble() ?: 0.0,
            method = (solution["method"] as? String) ?: (solution["solution_method"] as? String) ?: "unknown",
            cost = (body?.get("cost") as? Number)?.toDouble()
                ?: (solution["cost_incurred"] as? Number)?.toDouble()
                ?: (solution["cost"] as? Number)?.toDouble() ?: 0.0,
            timeTaken = (body?.get("processing_time") as? Number)?.toDouble()
                ?: (solution["time_taken"] as? Number)?.toDouble() ?: 0.0,
            retryAttempts = 0
        )
        return DoubtSolution(
            question = question,
            answer = answer,
            steps = steps,
            metadata = metadata,
            mobileFormat = mobileFormat,
            whatsappFormat = whatsappFormat
        )
    }
    
    /**
     * Solve a text-based doubt
     */
    suspend fun solveDoubt(
        question: String,
        subject: String = "Mathematics",
        userId: String,
        userPlan: String = "basic",
        context: String? = null
    ): Result<DoubtSolution> = withContext(Dispatchers.IO) {
        try {
            // Call production Supabase-auth endpoint using form field 'question'
            val response = apiService.solveDoubtAuth(question)
            if (response.isSuccessful) {
                val mapped = mapSolutionFromBody(response.body(), question, subject)
                if (mapped != null) return@withContext Result.success(mapped)
            }
            // Fallback: legacy enhanced endpoint
            val legacyReq = DoubtRequest(
                question = question,
                subject = subject,
                userId = userId,
                userPlan = userPlan,
                context = context
            )
            val legacyResp = apiService.solveDoubt(legacyReq)
            if (legacyResp.isSuccessful) {
                val mapped = mapSolutionFromBody(legacyResp.body(), question, subject)
                if (mapped != null) return@withContext Result.success(mapped)
            }
            Result.failure(Exception("Failed to get solution from both endpoints"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * Solve doubt from image using OCR
     */
    suspend fun solveDoubtFromImage(
        imageFile: File,
        userId: String,
        userPlan: String = "basic",
        subject: String = "Mathematics"
    ): Result<DoubtSolution> = withContext(Dispatchers.IO) {
        try {
            val requestFile = imageFile.asRequestBody("image/*".toMediaTypeOrNull())
            val imagePart = MultipartBody.Part.createFormData("image", imageFile.name, requestFile)
            
            val userIdBody = userId.toRequestBody("text/plain".toMediaTypeOrNull())
            val userPlanBody = userPlan.toRequestBody("text/plain".toMediaTypeOrNull())
            val subjectBody = subject.toRequestBody("text/plain".toMediaTypeOrNull())
            
            val response = apiService.solveDoubtFromImage(
                image = imagePart,
                userId = userIdBody,
                userPlan = userPlanBody,
                subject = subjectBody
            )
            
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                // Fallback to mock solution
                Result.success(com.klaro.app.data.repository.MockDataProvider.mockDoubtSolution("(image doubt)"))
            }
        } catch (e: Exception) {
            // Fallback to mock solution
            Result.success(com.klaro.app.data.repository.MockDataProvider.mockDoubtSolution("(image doubt)"))
        }
    }
    
    /**
     * Get user's doubt usage analytics (stubbed until API is available)
     */
    suspend fun getDoubtUsage(userId: String): Result<UserAnalytics> = withContext(Dispatchers.IO) {
        // TODO: Replace with real API call when endpoint is ready
        Result.success(
            UserAnalytics(
                totalDoubts = 0,
                doubtsThisWeek = 0,
                averageResponseTime = 0.0,
                topSubjects = emptyList(),
                accuracyRate = 0.0
            )
        )
    }
    
    /**
     * Get doubt history for the user (stubbed until API is available)
     */
    suspend fun getDoubtHistory(
        limit: Int = 20,
        offset: Int = 0,
        subject: String? = null
    ): Result<PaginatedResponse<DoubtSolution>> = withContext(Dispatchers.IO) {
        // TODO: Replace with real API call when endpoint is ready
        Result.success(
            PaginatedResponse(
                items = emptyList(),
                total = 0,
                page = 0,
                limit = limit,
                hasNext = false
            )
        )
    }
    
    /**
     * Save a doubt solution for later reference (stubbed until API is available)
     */
    suspend fun saveDoubt(doubtId: String): Result<String> = withContext(Dispatchers.IO) {
        // TODO: Replace with real API call when endpoint is ready
        Result.success("Doubt saved (local stub)")
    }
}
