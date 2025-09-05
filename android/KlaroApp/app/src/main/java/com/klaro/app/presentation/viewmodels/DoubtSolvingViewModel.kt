package com.klaro.app.presentation.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.klaro.app.data.models.*
import com.klaro.app.data.repository.DoubtSolvingRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.io.File
import javax.inject.Inject

/**
 * 🤔 Doubt Solving ViewModel
 * 
 * Manages state and API calls for doubt solving functionality
 */
@HiltViewModel
class DoubtSolvingViewModel @Inject constructor(
    private val repository: DoubtSolvingRepository
) : ViewModel() {

    // ================================================================================
    // UI State
    // ================================================================================
    
    private val _uiState = MutableStateFlow(DoubtSolvingUiState())
    val uiState: StateFlow<DoubtSolvingUiState> = _uiState.asStateFlow()
    
    private val _currentSolution = MutableStateFlow<DoubtSolution?>(null)
    val currentSolution: StateFlow<DoubtSolution?> = _currentSolution.asStateFlow()
    
    private val _doubtHistory = MutableStateFlow<List<DoubtSolution>>(emptyList())
    val doubtHistory: StateFlow<List<DoubtSolution>> = _doubtHistory.asStateFlow()
    
    private val _userAnalytics = MutableStateFlow<UserAnalytics?>(null)
    val userAnalytics: StateFlow<UserAnalytics?> = _userAnalytics.asStateFlow()

    // Mock user ID for now - this would come from authentication
    private val mockUserId = "demo_user_123"

    init {
        loadDoubtHistory()
        loadUserAnalytics()
    }

    // ================================================================================
    // Public Methods
    // ================================================================================
    
    fun solveTextDoubt(
        question: String,
        subject: String = "Mathematics",
        context: String? = null
    ) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isSolving = true, error = null)
            
            repository.solveDoubt(
                question = question,
                subject = subject,
                userId = mockUserId,
                userPlan = "basic",
                context = context
            ).fold(
                onSuccess = { solution ->
                    _currentSolution.value = solution
                    _uiState.value = _uiState.value.copy(
                        isSolving = false,
                        success = "Doubt solved successfully!"
                    )
                    
                    // Add to history
                    _doubtHistory.value = listOf(solution) + _doubtHistory.value.take(19)
                    
                    // Refresh analytics
                    loadUserAnalytics()
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isSolving = false,
                        error = "Failed to solve doubt: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun solveImageDoubt(
        imageFile: File,
        subject: String = "Mathematics"
    ) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isSolving = true, error = null)
            
            repository.solveDoubtFromImage(
                imageFile = imageFile,
                userId = mockUserId,
                userPlan = "basic",
                subject = subject
            ).fold(
                onSuccess = { solution ->
                    _currentSolution.value = solution
                    _uiState.value = _uiState.value.copy(
                        isSolving = false,
                        success = "Image doubt solved successfully!"
                    )
                    
                    // Add to history
                    _doubtHistory.value = listOf(solution) + _doubtHistory.value.take(19)
                    
                    // Refresh analytics
                    loadUserAnalytics()
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isSolving = false,
                        error = "Failed to solve image doubt: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun saveDoubt(doubtId: String) {
        viewModelScope.launch {
            repository.saveDoubt(doubtId).fold(
                onSuccess = { message ->
                    _uiState.value = _uiState.value.copy(success = message)
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        error = "Failed to save doubt: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun loadMoreHistory(offset: Int = 0, subject: String? = null) {
        viewModelScope.launch {
            repository.getDoubtHistory(
                limit = 20,
                offset = offset,
                subject = subject
            ).fold(
                onSuccess = { paginatedResponse ->
                    if (offset == 0) {
                        _doubtHistory.value = paginatedResponse.items
                    } else {
                        _doubtHistory.value = _doubtHistory.value + paginatedResponse.items
                    }
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        error = "Failed to load doubt history: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun clearMessages() {
        _uiState.value = _uiState.value.copy(error = null, success = null)
    }
    
    // ================================================================================
    // Private Methods
    // ================================================================================
    
    private fun loadDoubtHistory() {
        viewModelScope.launch {
            repository.getDoubtHistory().fold(
                onSuccess = { paginatedResponse ->
                    _doubtHistory.value = paginatedResponse.items
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        error = "Failed to load doubt history: ${error.message}"
                    )
                }
            )
        }
    }
    
    private fun loadUserAnalytics() {
        viewModelScope.launch {
            repository.getDoubtUsage(mockUserId).fold(
                onSuccess = { analytics ->
                    _userAnalytics.value = analytics
                },
                onFailure = { error ->
                    // Analytics failure is not critical, just log it
                    _uiState.value = _uiState.value.copy(
                        error = "Failed to load analytics: ${error.message}"
                    )
                }
            )
        }
    }
}

// ================================================================================
// UI State Data Class
// ================================================================================

data class DoubtSolvingUiState(
    val isSolving: Boolean = false,
    val isUploadingImage: Boolean = false,
    val error: String? = null,
    val success: String? = null
)
