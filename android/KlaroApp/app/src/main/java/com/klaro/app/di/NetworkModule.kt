package com.klaro.app.di

import android.content.Context
import com.klaro.app.BuildConfig
import com.klaro.app.data.api.KlaroApiService
import com.klaro.app.security.AuthorizationInterceptor
import com.klaro.app.security.TokenProvider
import com.klaro.app.security.DefaultTokenProvider
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import okhttp3.Dns
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.net.InetAddress
import java.net.URI
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

/**
 * 🌐 Network Dependency Injection Module
 * 
 * Provides Retrofit, OkHttpClient, and API service instances
 */
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    private const val DEVELOPMENT_MODE = true // Set to false for production
    private const val MOCK_BASE_URL = "https://mock.klaro.app/api/"

    @Provides
    @Singleton
    fun provideLoggingInterceptor(): HttpLoggingInterceptor {
        return HttpLoggingInterceptor().apply {
            level = if (BuildConfig.DEBUG) {
                HttpLoggingInterceptor.Level.BODY
            } else {
                HttpLoggingInterceptor.Level.NONE
            }
        }
    }

    @Provides
    @Singleton
    fun provideTokenProvider(
        @ApplicationContext context: Context
    ): TokenProvider = DefaultTokenProvider(context)

    @Provides
    @Singleton
    fun provideAuthorizationInterceptor(
        tokenProvider: TokenProvider
    ): AuthorizationInterceptor = AuthorizationInterceptor(tokenProvider)

    @Provides
    @Singleton
    fun provideOkHttpClient(
        loggingInterceptor: HttpLoggingInterceptor,
        authorizationInterceptor: AuthorizationInterceptor
    ): OkHttpClient {
        val builder = OkHttpClient.Builder()
            // Add auth header first so it's captured in logs too
            .addInterceptor(authorizationInterceptor)
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)

        // Debug DNS pinning disabled to avoid stale IPs. Using system DNS.

        return builder.build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(
        okHttpClient: OkHttpClient
    ): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BuildConfig.BASE_API_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideKlaroApiService(
        retrofit: Retrofit
    ): KlaroApiService {
        return retrofit.create(KlaroApiService::class.java)
    }
}
