package com.klaro.app.data.repository

import com.klaro.app.data.api.KlaroApiService
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CatalogRepository @Inject constructor(
    private val api: KlaroApiService
) {
    suspend fun getChapters(subject: String, grade: String): Result<List<String>> {
        return try {
            val resp = api.getChapters(subject = subject, grade = grade)
            if (resp.isSuccessful && resp.body() != null) {
                Result.success(resp.body()!!.chapters)
            } else {
                Result.failure(Exception("Failed to fetch chapters: ${resp.code()} ${resp.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

