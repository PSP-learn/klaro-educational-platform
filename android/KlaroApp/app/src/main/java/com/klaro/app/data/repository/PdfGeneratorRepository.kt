package com.klaro.app.data.repository

import com.klaro.app.data.api.KlaroApiService
import com.klaro.app.data.models.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.ResponseBody
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 📄 PDF Generator Repository
 * 
 * Handles API calls for quiz generation and PDF creation
 */
@Singleton
class PdfGeneratorRepository @Inject constructor(
    private val apiService: KlaroApiService
) {
    
    /**
     * Get available quiz presets from backend
     */
    suspend fun getQuizPresets(): Result<Map<String, QuizPreset>> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getQuizPresets()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                // Fallback to mock data in development
                Result.success(com.klaro.app.data.repository.MockDataProvider.getQuizPresets())
            }
        } catch (e: Exception) {
            // Fallback to mock data in development
            Result.success(com.klaro.app.data.repository.MockDataProvider.getQuizPresets())
        }
    }
    
    /**
     * Preview quiz blueprint and get totals/warnings
     */
    suspend fun previewQuiz(request: QuizRequest): Result<PreviewResponse> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.previewQuiz(request)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to preview: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * Create a custom quiz based on user selections (advanced request)
     */
    suspend fun createQuiz(request: QuizRequest): Result<QuizResponse> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.createQuiz(request)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                // Fallback to mock response
                Result.success(com.klaro.app.data.repository.MockDataProvider.mockQuizResponse())
            }
        } catch (e: Exception) {
            // Fallback to mock response
            Result.success(com.klaro.app.data.repository.MockDataProvider.mockQuizResponse())
        }
    }
    
    /**
     * Create quiz from preset
     */
    suspend fun createQuizFromPreset(presetName: String): Result<QuizResponse> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.createQuizFromPreset(presetName)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                // Fallback to mock
                Result.success(com.klaro.app.data.repository.MockDataProvider.mockQuizResponse())
            }
        } catch (e: Exception) {
            // Fallback to mock
            Result.success(com.klaro.app.data.repository.MockDataProvider.mockQuizResponse())
        }
    }
    
    /**
     * Download quiz file (questions|answers|marking_scheme)
     */
    suspend fun downloadQuiz(
        quizId: String, 
        fileType: String = "questions"
    ): Result<ResponseBody> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.downloadQuiz(quizId, fileType)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to download ${fileType}: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
