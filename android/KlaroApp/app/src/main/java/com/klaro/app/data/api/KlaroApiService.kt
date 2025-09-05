package com.klaro.app.data.api

import com.klaro.app.data.models.*
import okhttp3.MultipartBody
import okhttp3.RequestBody
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

    @POST("quiz/create")
    suspend fun createQuiz(@Body request: QuizRequest): Response<QuizResponse>

    @POST("quiz/preset/{presetName}")
    suspend fun createQuizFromPreset(@Path("presetName") presetName: String): Response<QuizResponse>

    @GET("quiz/{quizId}/download")
    suspend fun downloadQuiz(
        @Path("quizId") quizId: String,
        @Query("file_type") fileType: String = "questions"
    ): Response<okhttp3.ResponseBody>

    // ================================================================================
    // 📚 Catalog Endpoints
    // ================================================================================

    @GET("catalog/chapters")
    suspend fun getChapters(
        @Query("subject") subject: String,
        @Query("grade") grade: String
    ): Response<ChaptersResponse>

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

    @GET("doubt/usage/{userId}")
    suspend fun getDoubtUsage(@Path("userId") userId: String): Response<UserAnalytics>

    // ================================================================================
    // 👤 User Management Endpoints
    // ================================================================================

    @POST("auth/register")
    suspend fun registerUser(
        @Field("email") email: String,
        @Field("name") name: String,
        @Field("password") password: String
    ): Response<ApiResponse<User>>

    @POST("auth/login")
    suspend fun loginUser(
        @Field("email") email: String,
        @Field("password") password: String
    ): Response<ApiResponse<Map<String, String>>>

    @GET("user/profile")
    suspend fun getUserProfile(): Response<UserProfile>

    @PUT("user/profile")
    suspend fun updateUserProfile(@Body profileData: Map<String, Any>): Response<ApiResponse<String>>

    @GET("user/quizzes")
    suspend fun getUserQuizzes(): Response<PaginatedResponse<QuizResponse>>

    // ================================================================================
    // 📊 Analytics Endpoints
    // ================================================================================

    @GET("analytics/user")
    suspend fun getUserAnalytics(): Response<UserAnalytics>

    @GET("analytics/dashboard")
    suspend fun getDashboardAnalytics(): Response<Map<String, Any>>

    // ================================================================================
    // 💳 Subscription Endpoints
    // ================================================================================

    @POST("subscription/upgrade")
    suspend fun upgradeSubscription(
        @Body upgrade: Map<String, String>
    ): Response<ApiResponse<SubscriptionInfo>>

    @GET("subscription/status")
    suspend fun getSubscriptionStatus(): Response<SubscriptionInfo>

    // ================================================================================
    // 📚 History & Saved Items
    // ================================================================================

    @GET("doubts/history")
    suspend fun getDoubtHistory(
        @Query("limit") limit: Int = 20,
        @Query("offset") offset: Int = 0,
        @Query("subject") subject: String? = null
    ): Response<PaginatedResponse<DoubtSolution>>

    @POST("doubts/{doubtId}/save")
    suspend fun saveDoubt(@Path("doubtId") doubtId: String): Response<ApiResponse<String>>

    // ================================================================================
    // 🏥 Health & System Status
    // ================================================================================

    @GET("health")
    suspend fun healthCheck(): Response<Map<String, Any>>

    @GET("system/stats")
    suspend fun getSystemStats(): Response<Map<String, Any>>
}
