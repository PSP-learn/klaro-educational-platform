package com.klaro.app.security

import android.content.Context
import android.content.SharedPreferences

/**
 * Provides access to the current auth token (Supabase JWT).
 * Store and retrieve the token for Authorization header injection.
 */
interface TokenProvider {
    fun getToken(): String?
    fun setToken(token: String)
    fun clearToken()
}

class DefaultTokenProvider(context: Context) : TokenProvider {
    private val prefs: SharedPreferences =
        context.getSharedPreferences("klaro_auth", Context.MODE_PRIVATE)

    override fun getToken(): String? = prefs.getString(KEY_TOKEN, null)

    override fun setToken(token: String) {
        prefs.edit().putString(KEY_TOKEN, token).apply()
    }

    override fun clearToken() {
        prefs.edit().remove(KEY_TOKEN).apply()
    }

    private companion object {
        const val KEY_TOKEN = "supabase_jwt"
    }
}
