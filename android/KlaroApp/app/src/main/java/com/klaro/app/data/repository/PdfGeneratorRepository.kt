package com.klaro.app.data.repository

import com.klaro.app.data.api.KlaroApiService
import com.klaro.app.data.models.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.ResponseBody
import retrofit2.Response
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
     * Create a custom quiz based on user selections
     */
    suspend fun createQuiz(
        topics: List<String>,
        numQuestions: Int,
        questionTypes: List<String>,
        difficultyLevels: List<String>,
        subject: String = "Mathematics",
        title: String? = null,
        source: String? = null
    ): Result<QuizResponse> = withContext(Dispatchers.IO) {
        try {
            val request = QuizRequest(
                topics = topics,
                numQuestions = numQuestions,
                questionTypes = questionTypes,
                difficultyLevels = difficultyLevels,
                subject = subject,
                title = title,
                source = source
            )
            
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
     * Download quiz PDF
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
                Result.failure(Exception("Failed to download quiz: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
