package com.klaro.app.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController

/**
 * 📄 PDF Quiz Generator Screen
 * 
 * Create custom practice tests and download as PDF
 * Uses existing backend: /api/quiz/create
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PdfGeneratorScreen(navController: NavController) {
    
    var selectedTopics by remember { mutableStateOf(setOf<String>()) }
    var numQuestions by remember { mutableStateOf(10f) }
    var selectedDifficulty by remember { mutableStateOf(setOf("medium")) }
    var selectedTypes by remember { mutableStateOf(setOf("mcq")) }
    var quizTitle by remember { mutableStateOf("") }
    var isGenerating by remember { mutableStateOf(false) }
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        
        // Header
        item {
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            ) {
                Column(
                    modifier = Modifier.padding(20.dp)
                ) {
                    Text(
                        text = "📄 PDF Quiz Generator",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "Create custom practice tests tailored to your needs",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f)
                    )
                }
            }
        }
        
        // Quiz Title Input
        item {
            QuizTitleSection(
                title = quizTitle,
                onTitleChange = { quizTitle = it }
            )
        }
        
        // Topic Selection
        item {
            TopicSelectionSection(
                selectedTopics = selectedTopics,
                onTopicToggle = { topic ->
                    selectedTopics = if (topic in selectedTopics) {
                        selectedTopics - topic
                    } else {
                        selectedTopics + topic
                    }
                }
            )
        }
        
        // Number of Questions
        item {
            QuestionCountSection(
                numQuestions = numQuestions,
                onCountChange = { numQuestions = it }
            )
        }
        
        // Difficulty Selection
        item {
            DifficultySelectionSection(
                selectedDifficulty = selectedDifficulty,
                onDifficultyToggle = { difficulty ->
                    selectedDifficulty = if (difficulty in selectedDifficulty) {
                        selectedDifficulty - difficulty
                    } else {
                        selectedDifficulty + difficulty
                    }
                }
            )
        }
        
        // Question Types
        item {
            QuestionTypesSection(
                selectedTypes = selectedTypes,
                onTypeToggle = { type ->
                    selectedTypes = if (type in selectedTypes) {
                        selectedTypes - type
                    } else {
                        selectedTypes + type
                    }
                }
            )
        }
        
        // Generate Button
        item {
            GenerateQuizButton(
                isEnabled = selectedTopics.isNotEmpty() && !isGenerating,
                isLoading = isGenerating,
                onClick = {
                    isGenerating = true
                    // TODO: Call API to generate quiz
                    // For now, simulate generation
                    // generateQuiz(selectedTopics, numQuestions.toInt(), etc.)
                }
            )
        }
        
        // Recent Quizzes
        item {
            RecentQuizzesSection()
        }
    }
}

@Composable
fun QuizTitleSection(
    title: String,
    onTitleChange: (String) -> Unit
) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📝 Quiz Title",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))
            OutlinedTextField(
                value = title,
                onValueChange = onTitleChange,
                label = { Text("Enter quiz title (optional)") },
                placeholder = { Text("e.g., Algebra Practice Test") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )
        }
    }
}

@Composable
fun TopicSelectionSection(
    selectedTopics: Set<String>,
    onTopicToggle: (String) -> Unit
) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "🎯 Select Topics",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            // Mathematics Topics
            Text(
                text = "Mathematics",
                style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(8.dp))
            
            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(mathTopics) { topic ->
                    TopicChip(
                        topic = topic,
                        isSelected = topic in selectedTopics,
                        onToggle = { onTopicToggle(topic) }
                    )
                }
            }
        }
    }
}

@Composable
fun LazyRow(
    horizontalArrangement: Arrangement.Horizontal,
    content: @Composable () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = horizontalArrangement
    ) {
        content()
    }
}

@Composable
fun TopicChip(
    topic: String,
    isSelected: Boolean,
    onToggle: () -> Unit
) {
    FilterChip(
        onClick = onToggle,
        label = { Text(topic) },
        selected = isSelected,
        leadingIcon = if (isSelected) {
            { Icon(Icons.Filled.Check, contentDescription = null, modifier = Modifier.size(18.dp)) }
        } else null
    )
}

@Composable
fun QuestionCountSection(
    numQuestions: Float,
    onCountChange: (Float) -> Unit
) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📊 Number of Questions: ${numQuestions.toInt()}",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            Slider(
                value = numQuestions,
                onValueChange = onCountChange,
                valueRange = 5f..50f,
                steps = 8, // 5, 10, 15, 20, 25, 30, 40, 50
                modifier = Modifier.fillMaxWidth()
            )
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("5", style = MaterialTheme.typography.bodySmall)
                Text("50", style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}

@Composable
fun DifficultySelectionSection(
    selectedDifficulty: Set<String>,
    onDifficultyToggle: (String) -> Unit
) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "⚡ Difficulty Level",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                difficultyLevels.forEach { difficulty ->
                    FilterChip(
                        onClick = { onDifficultyToggle(difficulty.key) },
                        label = { Text("${difficulty.value.icon} ${difficulty.value.name}") },
                        selected = difficulty.key in selectedDifficulty
                    )
                }
            }
        }
    }
}

@Composable
fun QuestionTypesSection(
    selectedTypes: Set<String>,
    onTypeToggle: (String) -> Unit
) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📝 Question Types",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                questionTypes.forEach { type ->
                    FilterChip(
                        onClick = { onTypeToggle(type.key) },
                        label = { Text("${type.value.icon} ${type.value.name}") },
                        selected = type.key in selectedTypes
                    )
                }
            }
        }
    }
}

@Composable
fun GenerateQuizButton(
    isEnabled: Boolean,
    isLoading: Boolean,
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        enabled = isEnabled,
        modifier = Modifier
            .fillMaxWidth()
            .height(56.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        if (isLoading) {
            CircularProgressIndicator(
                modifier = Modifier.size(20.dp),
                color = Color.White
            )
            Spacer(modifier = Modifier.width(8.dp))
            Text("Generating Quiz...")
        } else {
            Icon(Icons.Filled.Download, contentDescription = null)
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = "🚀 Generate PDF Quiz",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

@Composable
fun RecentQuizzesSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📚 Recent Quizzes",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            recentQuizzes.forEach { quiz ->
                RecentQuizItem(quiz)
                if (quiz != recentQuizzes.last()) {
                    Divider(modifier = Modifier.padding(vertical = 8.dp))
                }
            }
        }
    }
}

@Composable
fun RecentQuizItem(quiz: RecentQuiz) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* TODO: Download or view quiz */ },
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = Icons.Filled.Assignment,
            contentDescription = "Quiz",
            tint = MaterialTheme.colorScheme.primary
        )
        
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = quiz.title,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = "${quiz.questions} questions • ${quiz.difficulty}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        Text(
            text = quiz.createdDate,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        
        IconButton(onClick = { /* TODO: Download quiz */ }) {
            Icon(Icons.Filled.Download, contentDescription = "Download")
        }
    }
}

// ================================================================================
// 📋 Data Classes & Static Data
// ================================================================================

data class DifficultyInfo(val name: String, val icon: String)
data class QuestionTypeInfo(val name: String, val icon: String)
data class RecentQuiz(
    val title: String,
    val questions: Int,
    val difficulty: String,
    val createdDate: String
)

val mathTopics = listOf(
    "Algebra", "Trigonometry", "Calculus", "Geometry", 
    "Coordinate Geometry", "Statistics", "Probability",
    "Quadratic Equations", "Polynomials", "Matrices"
)

val difficultyLevels = mapOf(
    "easy" to DifficultyInfo("Easy", "🟢"),
    "medium" to DifficultyInfo("Medium", "🟡"),
    "hard" to DifficultyInfo("Hard", "🔴")
)

val questionTypes = mapOf(
    "mcq" to QuestionTypeInfo("Multiple Choice", "🔘"),
    "short" to QuestionTypeInfo("Short Answer", "✏️"),
    "essay" to QuestionTypeInfo("Essay", "📝")
)

val recentQuizzes = listOf(
    RecentQuiz("Algebra Practice", 15, "Medium", "2 hours ago"),
    RecentQuiz("Trigonometry Test", 10, "Hard", "1 day ago"),
    RecentQuiz("Quick Revision", 20, "Easy", "3 days ago")
)
