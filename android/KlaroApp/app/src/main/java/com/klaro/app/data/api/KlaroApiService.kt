package com.klaro.app.data.api

import com.klaro.app.data.models.*
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.*

/**
 * 🌐 Klaro API Service
 * 
 * Retrofit interface for communicating with Klaro FastAPI backend
 */
interface KlaroApiService {

    // ================================================================================
    // 📄 Quiz/PDF Generation Endpoints
    // ================================================================================

    @GET("quiz/presets")
    suspend fun getQuizPresets(): Response<Map<String, QuizPreset>>

    // Legacy JSON create (may be disabled in prod); kept for backward compat
    @POST("quiz/create")
    suspend fun createQuiz(@Body request: QuizRequest): Response<QuizResponse>

    // Authenticated generate (production): x-www-form-urlencoded
    @FormUrlEncoded
    @POST("quiz/generate")
    suspend fun generateQuiz(
        @Field("title") title: String,
        @Field("topics") topics: String, // comma-separated: "topic1,topic2"
        @Field("questions_count") questionsCount: Int = 10,
        @Field("difficulty") difficulty: String = "mixed",
        @Field("source") source: String? = null
    ): Response<Map<String, Any>>

    @POST("quiz/preset/{presetName}")
    suspend fun createQuizFromPreset(@Path("presetName") presetName: String): Response<QuizResponse>

    // New authenticated download path
    @GET("quiz/download/{quizId}")
    suspend fun downloadQuizAuth(
        @Path("quizId") quizId: String
    ): Response<ResponseBody>

    // Old download path (kept for compatibility with older backend variants)
    @GET("quiz/{quizId}/download")
    suspend fun downloadQuiz(
        @Path("quizId") quizId: String,
        @Query("file_type") fileType: String = "questions"
    ): Response<ResponseBody>

    // ================================================================================
    // 📚 Catalog Endpoints
    // ================================================================================

    @GET("/api/catalog/chapters")
    suspend fun getChapters(
        @Query("subject") subject: String,
        @Query("grade") grade: String
    ): Response<ChaptersResponse>

    @GET("/api/catalog/subtopics")
    suspend fun getSubtopics(
        @Query("subject") subject: String,
        @Query("grade") grade: String,
        @Query("chapter") chapter: String
    ): Response<SubtopicsResponse>

    // ================================================================================
    // 🎯 JEE Test Endpoints
    // ================================================================================

    @POST("jee/test/create")
    suspend fun createJEETest(@Body request: JEETestRequest): Response<JEETestResponse>

    @GET("jee/test/{testId}")
    suspend fun getJEETest(@Path("testId") testId: String): Response<JEETestResponse>

    @POST("jee/test/{testId}/submit")
    suspend fun submitJEETest(
        @Path("testId") testId: String,
        @Body answers: List<JEEAnswer>
    ): Response<JEETestResult>

    @GET("jee/test/presets")
    suspend fun getJEETestPresets(): Response<Map<String, Any>>

    @GET("jee/pyqs")
    suspend fun getJEEPreviousYearQuestions(
        @Query("subject") subject: String? = null,
        @Query("year") year: Int? = null,
        @Query("limit") limit: Int = 20
    ): Response<List<JEEQuestion>>

    // ================================================================================
    // 🤔 Doubt Solving Endpoints
    // ================================================================================

    @POST("doubt/solve-enhanced")
    suspend fun solveDoubt(@Body request: DoubtRequest): Response<DoubtSolution>

    @Multipart
    @POST("doubt/solve-image")
    suspend fun solveDoubtFromImage(
        @Part image: MultipartBody.Part,
        @Part("user_id") userId: RequestBody,
        @Part("user_plan") userPlan: RequestBody,
        @Part("subject") subject: RequestBody
    ): Response<DoubtSolution>
}
