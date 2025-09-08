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
        if (body == null) return null

        // Two possible backend shapes:
        // 1) { success: true, solution: { final_answer|answer, steps[], ... }, processing_time, cost }
        // 2) { question, answer|final_answer, steps[], metadata{...}, mobileFormat{...}, whatsappFormat }
        val hasNested = body["solution"] is Map<*, *>
        val solutionMap = if (hasNested) body["solution"] as Map<*, *> else body

        // Answer
        val answer = (solutionMap["final_answer"] as? String)
            ?: (solutionMap["answer"] as? String)
            ?: (solutionMap["shortAnswer"] as? String)
            ?: ""

        // Steps (support stepNumber or step_number)
        val stepsRaw = (solutionMap["steps"] as? List<*>) ?: emptyList<Any>()
        val steps = stepsRaw.mapIndexed { idx, it ->
            val m = it as? Map<*, *> ?: emptyMap<String, Any>()
            val stepNum = (m["stepNumber"] as? Number)?.toInt() ?: (m["step_number"] as? Number)?.toInt()
            val title = (m["title"] as? String) ?: (m["heading"] as? String) ?: "Step ${idx + 1}"
            val explanation = (m["explanation"] as? String) ?: (m["detail"] as? String) ?: ""
            val confidence = (m["confidence"] as? Number)?.toDouble() ?: 0.0
            SolutionStep(
                stepNumber = stepNum ?: (idx + 1),
                title = title,
                explanation = explanation,
                confidence = confidence
            )
        }

        // Whatsapp format
        val whatsappFormat = (solutionMap["whatsapp_format"] as? String)
            ?: (solutionMap["whatsappFormat"] as? String)
            ?: (body["whatsappFormat"] as? String)
            ?: answer

        // Mobile format
        val mobileFormatObj = (solutionMap["mobile_format"] as? Map<*, *>)
            ?: (solutionMap["mobileFormat"] as? Map<*, *>)
            ?: (body["mobileFormat"] as? Map<*, *>)
        val mobileFormat = if (mobileFormatObj != null) {
            MobileFormat(
                shortAnswer = (mobileFormatObj["shortAnswer"] as? String) ?: answer,
                keySteps = (mobileFormatObj["keySteps"] as? List<*>)?.mapNotNull { it as? String } ?: steps.map { it.title },
                visualAids = (mobileFormatObj["visualAids"] as? List<*>)?.mapNotNull { it as? String } ?: emptyList(),
                practiceProblems = (mobileFormatObj["practiceProblems"] as? List<*>)?.mapNotNull { it as? String } ?: emptyList()
            )
        } else {
            MobileFormat(
                shortAnswer = answer,
                keySteps = steps.map { it.title },
                visualAids = emptyList(),
                practiceProblems = emptyList()
            )
        }

        // Metadata (prefer explicit metadata node if present)
        val metadataObj = (solutionMap["metadata"] as? Map<*, *>) ?: (body["metadata"] as? Map<*, *>)
        val metadata = if (metadataObj != null) {
            DoubtMetadata(
                topic = (metadataObj["topic"] as? String) ?: subject,
                difficulty = (metadataObj["difficulty"] as? String) ?: "",
                confidence = (metadataObj["confidence"] as? Number)?.toDouble() ?: 0.0,
                method = (metadataObj["method"] as? String) ?: (solutionMap["solution_method"] as? String) ?: "unknown",
                cost = (metadataObj["cost"] as? Number)?.toDouble()
                    ?: (body["cost"] as? Number)?.toDouble()
                    ?: (solutionMap["cost_incurred"] as? Number)?.toDouble()
                    ?: (solutionMap["cost"] as? Number)?.toDouble() ?: 0.0,
                timeTaken = (metadataObj["timeTaken"] as? Number)?.toDouble()
                    ?: (body["processing_time"] as? Number)?.toDouble()
                    ?: (solutionMap["time_taken"] as? Number)?.toDouble() ?: 0.0,
                retryAttempts = (metadataObj["retryAttempts"] as? Number)?.toInt() ?: 0
            )
        } else {
            DoubtMetadata(
                topic = (solutionMap["topic"] as? String) ?: subject,
                difficulty = (solutionMap["difficulty"] as? String) ?: "",
                confidence = (solutionMap["confidence"] as? Number)?.toDouble() ?: 0.0,
                method = (solutionMap["method"] as? String) ?: (solutionMap["solution_method"] as? String) ?: "unknown",
                cost = (body["cost"] as? Number)?.toDouble()
                    ?: (solutionMap["cost_incurred"] as? Number)?.toDouble()
                    ?: (solutionMap["cost"] as? Number)?.toDouble() ?: 0.0,
                timeTaken = (body["processing_time"] as? Number)?.toDouble()
                    ?: (solutionMap["time_taken"] as? Number)?.toDouble() ?: 0.0,
                retryAttempts = 0
            )
        }

        return DoubtSolution(
            question = (solutionMap["question"] as? String) ?: question,
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
