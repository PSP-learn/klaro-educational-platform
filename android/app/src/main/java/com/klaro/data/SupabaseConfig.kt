package com.klaro.data

import io.github.jan.supabase.createSupabaseClient
import io.github.jan.supabase.gotrue.GoTrue
import io.github.jan.supabase.postgrest.Postgrest
import io.github.jan.supabase.storage.Storage

/**
 * 🟢 Supabase Configuration for Android
 * 
 * Handles authentication, database, and file storage
 * through Supabase while AI features use Railway backend
 */
object SupabaseConfig {
    
    // TODO: Replace with your actual Supabase project details
    const val SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
    const val SUPABASE_ANON_KEY = "your_anon_key_here"
    
    // Railway backend for AI features
    const val RAILWAY_API_URL = "https://your-railway-url.up.railway.app"
    
    // Initialize Supabase client
    val supabase = createSupabaseClient(
        supabaseUrl = SUPABASE_URL,
        supabaseKey = SUPABASE_ANON_KEY
    ) {
        install(GoTrue) {
            // Authentication configuration
            autoRefreshToken = true
        }
        install(Postgrest) {
            // Database configuration
        }
        install(Storage) {
            // File storage configuration
        }
    }
}

/**
 * 🔐 Authentication Helper
 */
object AuthHelper {
    
    suspend fun signUp(email: String, password: String, name: String): Result<String> {
        return try {
            val response = SupabaseConfig.supabase.auth.signUpWith(io.github.jan.supabase.gotrue.providers.builtin.Email) {
                this.email = email
                this.password = password
                data = mapOf("name" to name)
            }
            
            if (response?.user != null) {
                Result.success("Registration successful. Please check your email to verify.")
            } else {
                Result.failure(Exception("Registration failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun signIn(email: String, password: String): Result<String> {
        return try {
            val response = SupabaseConfig.supabase.auth.signInWith(io.github.jan.supabase.gotrue.providers.builtin.Email) {
                this.email = email
                this.password = password
            }
            
            if (response?.user != null) {
                Result.success(response.session?.accessToken ?: "")
            } else {
                Result.failure(Exception("Invalid credentials"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun signOut(): Result<Unit> {
        return try {
            SupabaseConfig.supabase.auth.signOut()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    fun getCurrentUser() = SupabaseConfig.supabase.auth.currentUserOrNull()
    
    fun getAccessToken() = SupabaseConfig.supabase.auth.currentSessionOrNull()?.accessToken
}

/**
 * 📁 File Storage Helper
 */
object StorageHelper {
    private const val BUCKET_NAME = "klaro-files"
    
    suspend fun uploadFile(
        userId: String,
        fileType: String, // "doubt_image", "profile_image", etc.
        fileName: String,
        fileData: ByteArray
    ): Result<String> {
        return try {
            val timestamp = System.currentTimeMillis()
            val storagePath = "$userId/$fileType/${timestamp}_$fileName"
            
            val response = SupabaseConfig.supabase.storage
                .from(BUCKET_NAME)
                .upload(storagePath, fileData)
            
            // Get public URL
            val publicUrl = SupabaseConfig.supabase.storage
                .from(BUCKET_NAME)
                .publicUrl(storagePath)
            
            Result.success(publicUrl)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun deleteFile(filePath: String): Result<Unit> {
        return try {
            SupabaseConfig.supabase.storage
                .from(BUCKET_NAME)
                .delete(filePath)
            
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
