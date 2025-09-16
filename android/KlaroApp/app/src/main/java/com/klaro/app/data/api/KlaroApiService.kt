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

    // Preview blueprint and get totals/warnings
    @POST("quiz/preview")
    suspend fun previewQuiz(@Body request: QuizRequest): Response<PreviewResponse>

    // Create quiz with advanced request
    @POST("quiz/create")
    suspend fun createQuiz(@Body request: QuizRequest): Response<QuizResponse>

    @POST("quiz/preset/{presetName}")
    suspend fun createQuizFromPreset(@Path("presetName") presetName: String): Response<QuizResponse>

    // Download specific file type (questions|answers|marking_scheme)
    @GET("quiz/{quizId}/download")
    suspend fun downloadQuiz(
        @Path("quizId") quizId: String,
        @Query("file_type") fileType: String = "questions"
    ): Response<ResponseBody>

    // ================================================================================
    // 📚 Catalog Endpoints
    // ================================================================================

    @GET("catalog/chapters")
    suspend fun getChapters(
        @Query("subject") subject: String,
        @Query("grade") grade: String
    ): Response<ChaptersResponse>

    @GET("catalog/subtopics")
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

    // Production (Supabase-auth): text doubt via form-encoded field 'question'
    @FormUrlEncoded
    @POST("doubts/solve")
    suspend fun solveDoubtAuth(
        @Field("question") question: String
    ): Response<Map<String, Any>>

    // Legacy enhanced JSON (kept for compatibility with older backend variants)
    @POST("doubt/solve-enhanced")
    suspend fun solveDoubt(@Body request: DoubtRequest): Response<Map<String, Any>>

    @Multipart
    @POST("doubt/solve-image")
    suspend fun solveDoubtFromImage(
        @Part image: MultipartBody.Part,
        @Part("user_id") userId: RequestBody,
        @Part("user_plan") userPlan: RequestBody,
        @Part("subject") subject: RequestBody
    ): Response<DoubtSolution>
}
