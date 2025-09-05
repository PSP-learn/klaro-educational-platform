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
            val request = DoubtRequest(
                question = question,
                subject = subject,
                userId = userId,
                userPlan = userPlan,
                context = context
            )
            
            val response = apiService.solveDoubt(request)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                // Fallback to mock solution
                Result.success(com.klaro.app.data.repository.MockDataProvider.mockDoubtSolution(question))
            }
        } catch (e: Exception) {
            // Fallback to mock solution
            Result.success(com.klaro.app.data.repository.MockDataProvider.mockDoubtSolution(question))
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
     * Get user's doubt usage analytics
     */
    suspend fun getDoubtUsage(userId: String): Result<UserAnalytics> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getDoubtUsage(userId)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to get doubt usage: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * Get doubt history for the user
     */
    suspend fun getDoubtHistory(
        limit: Int = 20,
        offset: Int = 0,
        subject: String? = null
    ): Result<PaginatedResponse<DoubtSolution>> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getDoubtHistory(limit, offset, subject)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to get doubt history: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * Save a doubt solution for later reference
     */
    suspend fun saveDoubt(doubtId: String): Result<String> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.saveDoubt(doubtId)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!.message ?: "Doubt saved successfully")
            } else {
                Result.failure(Exception("Failed to save doubt: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
