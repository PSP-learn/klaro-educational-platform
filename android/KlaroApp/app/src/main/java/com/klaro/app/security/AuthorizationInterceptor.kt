package com.klaro.app.security

import okhttp3.Interceptor
import okhttp3.Response

/**
 * OkHttp interceptor that injects Authorization: Bearer <token> if available.
 */
class AuthorizationInterceptor(
    private val tokenProvider: TokenProvider
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()
        val token = tokenProvider.getToken()
        return if (!token.isNullOrBlank()) {
            val newReq = original.newBuilder()
                .header("Authorization", "Bearer $token")
                .build()
            chain.proceed(newReq)
        } else {
            chain.proceed(original)
        }
    }
}
