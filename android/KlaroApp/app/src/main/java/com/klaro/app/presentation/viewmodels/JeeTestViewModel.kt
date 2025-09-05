package com.klaro.app.presentation.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.klaro.app.data.models.*
import com.klaro.app.data.repository.JeeTestRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * 🎯 JEE Test ViewModel
 * 
 * Manages state and API calls for JEE test creation and management
 */
@HiltViewModel
class JeeTestViewModel @Inject constructor(
    private val repository: JeeTestRepository
) : ViewModel() {

    // ================================================================================
    // UI State
    // ================================================================================
    
    private val _uiState = MutableStateFlow(JeeTestUiState())
    val uiState: StateFlow<JeeTestUiState> = _uiState.asStateFlow()
    
    private val _currentTest = MutableStateFlow<JEETestResponse?>(null)
    val currentTest: StateFlow<JEETestResponse?> = _currentTest.asStateFlow()
    
    private val _testResults = MutableStateFlow<List<JEETestResult>>(emptyList())
    val testResults: StateFlow<List<JEETestResult>> = _testResults.asStateFlow()
    
    private val _pyqQuestions = MutableStateFlow<List<JEEQuestion>>(emptyList())
    val pyqQuestions: StateFlow<List<JEEQuestion>> = _pyqQuestions.asStateFlow()

    init {
        loadTestPresets()
    }

    // ================================================================================
    // Public Methods
    // ================================================================================
    
    fun startFullMockTest() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isCreatingTest = true, error = null)
            
            repository.createJEETest(
                testType = "full_mock",
                subjects = listOf("Mathematics", "Physics", "Chemistry"),
                duration = 180
            ).fold(
                onSuccess = { testResponse ->
                    _currentTest.value = testResponse
                    _uiState.value = _uiState.value.copy(
                        isCreatingTest = false,
                        success = "Full mock test created! Ready to start."
                    )
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isCreatingTest = false,
                        error = "Failed to create test: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun startSubjectTest(subject: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isCreatingTest = true, error = null)
            
            repository.createJEETest(
                testType = "subject_practice",
                subjects = listOf(subject),
                duration = 60
            ).fold(
                onSuccess = { testResponse ->
                    _currentTest.value = testResponse
                    _uiState.value = _uiState.value.copy(
                        isCreatingTest = false,
                        success = "$subject practice test created!"
                    )
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isCreatingTest = false,
                        error = "Failed to create subject test: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun startTopicTest(topics: List<String>, subject: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isCreatingTest = true, error = null)
            
            repository.createJEETest(
                testType = "topic_practice",
                subjects = listOf(subject),
                topics = topics,
                duration = 30
            ).fold(
                onSuccess = { testResponse ->
                    _currentTest.value = testResponse
                    _uiState.value = _uiState.value.copy(
                        isCreatingTest = false,
                        success = "Topic practice test created!"
                    )
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isCreatingTest = false,
                        error = "Failed to create topic test: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun submitTest(testId: String, answers: List<JEEAnswer>) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isSubmittingTest = true, error = null)
            
            repository.submitJEETest(testId, answers).fold(
                onSuccess = { testResult ->
                    _testResults.value = listOf(testResult) + _testResults.value.take(9)
                    _uiState.value = _uiState.value.copy(
                        isSubmittingTest = false,
                        lastTestResult = testResult,
                        success = "Test submitted successfully! Check results tab."
                    )
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        isSubmittingTest = false,
                        error = "Failed to submit test: ${error.message}"
                    )
                }
            )
        }
    }
    
    fun loadPreviousYearQuestions(subject: String? = null, year: Int? = null) {
        viewModelScope.launch {
            repository.getJEEPreviousYearQuestions(subject, year).fold(
                onSuccess = { questions ->
                    _pyqQuestions.value = questions
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        error = "Failed to load PYQs: ${error.message}"
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
    
    private fun loadTestPresets() {
        viewModelScope.launch {
            repository.getJEETestPresets().fold(
                onSuccess = { presets ->
                    _uiState.value = _uiState.value.copy(testPresets = presets)
                },
                onFailure = { error ->
                    _uiState.value = _uiState.value.copy(
                        error = "Failed to load test presets: ${error.message}"
                    )
                }
            )
        }
    }
}

// ================================================================================
// UI State Data Class
// ================================================================================

data class JeeTestUiState(
    val isCreatingTest: Boolean = false,
    val isSubmittingTest: Boolean = false,
    val lastTestResult: JEETestResult? = null,
    val testPresets: Map<String, Any> = emptyMap(),
    val error: String? = null,
    val success: String? = null
)
