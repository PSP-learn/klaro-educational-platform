package com.klaro.app.presentation.auth

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.klaro.app.BuildConfig
import com.klaro.app.security.TokenProvider
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class AuthViewModel @Inject constructor(
    private val tokenProvider: TokenProvider
) : ViewModel() {

    private val _isLoggedIn = MutableStateFlow(!tokenProvider.getToken().isNullOrBlank())
    val isLoggedIn: StateFlow<Boolean> = _isLoggedIn

    private val _lastMessage = MutableStateFlow<String?>(null)
    val lastMessage: StateFlow<String?> = _lastMessage

    fun signInWithGoogle(context: Context) {
        viewModelScope.launch {
            try {
                _lastMessage.value = "Opening Google sign-in…"
                val authorizeUrl =
                    "${BuildConfig.SUPABASE_URL}/auth/v1/authorize" +
                        "?provider=google" +
                        "&redirect_to=klaroauth://callback" +
                        "&scopes=openid%20email%20profile"
                context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(authorizeUrl)))
            } catch (e: Exception) {
                e.printStackTrace()
                _lastMessage.value = "Sign-in failed: ${e.message ?: "Unknown error"}"
            }
        }
    }

    fun handleDeepLink(uri: Uri) {
        // With FlowType.IMPLICIT, Supabase redirects with access_token in the URI fragment
        val fragment = uri.fragment ?: ""
        if (fragment.isNotBlank()) {
            val params = fragment.split('&').mapNotNull { pair ->
                val idx = pair.indexOf('=')
                if (idx > 0) pair.substring(0, idx) to pair.substring(idx + 1) else null
            }.toMap()
            val accessToken = params["access_token"]
            if (!accessToken.isNullOrBlank()) {
                tokenProvider.setToken(accessToken)
                _isLoggedIn.value = true
                _lastMessage.value = "Signed in successfully"
            } else {
                _lastMessage.value = "Sign-in callback missing token"
            }
        }
    }

    fun signOut() {
        viewModelScope.launch {
            tokenProvider.clearToken()
            _isLoggedIn.value = false
            _lastMessage.value = "Signed out"
        }
    }

    fun clearMessage() {
        _lastMessage.value = null
    }
}

