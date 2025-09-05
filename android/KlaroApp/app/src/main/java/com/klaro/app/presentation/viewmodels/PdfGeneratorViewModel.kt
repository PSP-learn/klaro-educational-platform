package com.klaro.app.presentation.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.klaro.app.data.models.QuizPreset
import com.klaro.app.data.models.QuizResponse
import com.klaro.app.data.repository.PdfGeneratorRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * 📄 PDF Generator ViewModel
 * 
 * Manages state and API calls for PDF quiz generation
 */
@HiltViewModel
class PdfGeneratorViewModel @Inject constructor(
    private val repository: PdfGeneratorRepository,
    private val catalogRepository: com.klaro.app.data.repository.CatalogRepository
) : ViewModel() {

    // ================================================================================
    // UI State
    // ================================================================================
    
    private val _uiState = MutableStateFlow(PdfGeneratorUiState())
    val uiState: StateFlow<PdfGeneratorUiState> = _uiState.asStateFlow()
    
    private val _quizPresets = MutableStateFlow<Map<String, QuizPreset>>(emptyMap())
    val quizPresets: StateFlow<Map<String, QuizPreset>> = _quizPresets.asStateFlow()
    
    private val _recentQuizzes = MutableStateFlow<List<QuizResponse>>(emptyList())
    val recentQuizzes: StateFlow<List<QuizResponse>> = _recentQuizzes.asStateFlow()

    init {
        loadQuizPresets()
    }

    // ================================================================================
    // Public Methods
    // ================================================================================
    
    fun generateQuiz(
        topics: List<String>,
        numQuestions: Int,
        questionTypes: List<String>,
        difficultyLevels: List<String>,
        subject: String,
        title: String? = null
    ) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isGenerating = true, error = null)
            
            repository.createQuiz(
                topics = topics,
                numQuestions = numQuestions,
                questionTypes = questionTypes,
                difficultyLevels = difficultyLevels,
                subject = subject,
                title = title
            ).fold(
                onSuccess = { quizResponse ->
                    _uiState.value = _uiState.value.copy(
                        isGenerating = false,
                        lastGeneratedQuiz = quizResponse,
                        success = "Quiz generated successfully! Ready for download."
                    )
                    
                    // Add to recent quizzes
                    _recentQuizzes.value = listOf(quizResponse) + _recentQuizzes.value.take(9)
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isGenerating = false,
                        error = "Failed to generate quiz: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun generateQuizFromPreset(presetName: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isGenerating = true, error = null)
            
            repository.createQuizFromPreset(presetName).fold(
                onSuccess = { quizResponse ->
                    _uiState.value = _uiState.value.copy(
                        isGenerating = false,
                        lastGeneratedQuiz = quizResponse,
                        success = "Quiz generated from preset successfully!"
                    )
                    
                    // Add to recent quizzes
                    _recentQuizzes.value = listOf(quizResponse) + _recentQuizzes.value.take(9)
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isGenerating = false,
                        error = "Failed to generate quiz from preset: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun downloadQuiz(quizId: String, fileType: String = "questions") {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isDownloading = true, error = null)
            
            repository.downloadQuiz(quizId, fileType).fold(
                onSuccess = { responseBody ->
                    _uiState.value = _uiState.value.copy(
                        isDownloading = false,
                        downloadedFile = responseBody,
                        success = "Quiz downloaded successfully!"
                    )
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isDownloading = false,
                        error = "Failed to download quiz: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun clearMessages() {
        _uiState.value = _uiState.value.copy(error = null, success = null)
    }

    fun loadChapters(subject: String, grade: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isChaptersLoading = true, error = null)
            catalogRepository.getChapters(subject, grade).fold(
                onSuccess = { chapters ->
                    _uiState.value = _uiState.value.copy(
                        isChaptersLoading = false,
                        chapters = chapters
                    )
                },
                onFailure = { e ->
                    _uiState.value = _uiState.value.copy(
                        isChaptersLoading = false,
                        error = "Failed to load chapters: ${e.message}",
                        chapters = emptyList()
                    )
                }
            )
        }
    }
    
    // ================================================================================
    // Private Methods
    // ================================================================================
    
    private fun loadQuizPresets() {
        viewModelScope.launch {
            repository.getQuizPresets().fold(
                onSuccess = { presets ->
                    _quizPresets.value = presets
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        error = "Failed to load quiz presets: ${error.message}"
                    )
                }
            )
        }
    }
}

// ================================================================================
// UI State Data Class
// ================================================================================

data class PdfGeneratorUiState(
    val isGenerating: Boolean = false,
    val isDownloading: Boolean = false,
    val isChaptersLoading: Boolean = false,
    val chapters: List<String> = emptyList(),
    val lastGeneratedQuiz: QuizResponse? = null,
    val downloadedFile: okhttp3.ResponseBody? = null,
    val error: String? = null,
    val success: String? = null
)
