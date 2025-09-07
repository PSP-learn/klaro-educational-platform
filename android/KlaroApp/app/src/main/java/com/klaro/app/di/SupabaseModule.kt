package com.klaro.app.di

import android.util.Log
import com.klaro.app.BuildConfig
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import io.github.jan.supabase.SupabaseClient
import io.github.jan.supabase.createSupabaseClient
import io.ktor.client.engine.okhttp.OkHttp
import javax.inject.Singleton

/**
 * Provides a singleton SupabaseClient configured with GoTrue (Auth).
 * Uses a custom OAuth redirect scheme: klaroauth://callback
 */
@Module
@InstallIn(SingletonComponent::class)
object SupabaseModule {

    @Provides
    @Singleton
    fun provideSupabaseClient(): SupabaseClient {
        val supabaseUrl = BuildConfig.SUPABASE_URL
        val supabaseAnonKey = BuildConfig.SUPABASE_ANON_KEY

        return createSupabaseClient(
            supabaseUrl = supabaseUrl,
            supabaseKey = supabaseAnonKey
        ) {
            httpEngine = OkHttp.create()
            // GoTrue install omitted for now; using manual OAuth URL flow
        }
    }
}

