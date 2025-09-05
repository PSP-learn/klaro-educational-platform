package com.klaro.app.data.repository

import com.klaro.app.data.api.KlaroApiService
import com.klaro.app.data.models.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 🎯 JEE Test Repository
 * 
 * Handles API calls for JEE test creation, management, and submissions
 */
@Singleton
class JeeTestRepository @Inject constructor(
    private val apiService: KlaroApiService
) {
    
    /**
     * Create a new JEE test based on type and configuration
     */
    suspend fun createJEETest(
        testType: String = "full_mock",
        subjects: List<String> = listOf("Mathematics", "Physics", "Chemistry"),
        topics: List<String> = emptyList(),
        duration: Int = 180,
        difficulty: String = "mixed"
    ): Result<JEETestResponse> = withContext(Dispatchers.IO) {
        try {
            val request = JEETestRequest(
                testType = testType,
                subjects = subjects,
                topics = topics,
                duration = duration,
                difficulty = difficulty
            )
            
            val response = apiService.createJEETest(request)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                // Fallback to mock test
                Result.success(com.klaro.app.data.repository.MockDataProvider.mockJEETestResponse(subjects, topics, duration))
            }
        } catch (e: Exception) {
            // Fallback to mock test
            Result.success(com.klaro.app.data.repository.MockDataProvider.mockJEETestResponse(subjects, topics, duration))
        }
    }
    
    /**
     * Get an existing JEE test by ID
     */
    suspend fun getJEETest(testId: String): Result<JEETestResponse> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getJEETest(testId)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to get JEE test: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * Submit JEE test answers and get results
     */
    suspend fun submitJEETest(
        testId: String,
        answers: List<JEEAnswer>
    ): Result<JEETestResult> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.submitJEETest(testId, answers)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to submit JEE test: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * Get available JEE test presets
     */
    suspend fun getJEETestPresets(): Result<Map<String, Any>> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getJEETestPresets()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                // Fallback to simple presets
                Result.success(mapOf("full_mock" to mapOf("duration" to 180), "subject_practice" to mapOf("duration" to 60)))
            }
        } catch (e: Exception) {
            // Fallback to simple presets
            Result.success(mapOf("full_mock" to mapOf("duration" to 180), "subject_practice" to mapOf("duration" to 60)))
        }
    }
    
    /**
     * Get previous year questions for practice
     */
    suspend fun getJEEPreviousYearQuestions(
        subject: String? = null,
        year: Int? = null,
        limit: Int = 20
    ): Result<List<JEEQuestion>> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getJEEPreviousYearQuestions(subject, year, limit)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                // Fallback to mock questions
                Result.success(com.klaro.app.data.repository.MockDataProvider.mockPYQs(subject, year, limit))
            }
        } catch (e: Exception) {
            // Fallback to mock questions
            Result.success(com.klaro.app.data.repository.MockDataProvider.mockPYQs(subject, year, limit))
        }
    }
}
