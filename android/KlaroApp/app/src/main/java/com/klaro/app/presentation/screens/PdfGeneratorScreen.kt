package com.klaro.app.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.horizontalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.klaro.app.data.repository.MockDataProvider
import com.klaro.app.presentation.syllabus.SyllabusData
import com.klaro.app.presentation.viewmodels.PdfGeneratorViewModel
import com.klaro.app.presentation.ui.design.*

/**
 * 📄 Quiz Generator - World-Class Form Design
 * 
 * Design Philosophy: "Progressive Disclosure + Zero Confusion"
 * - Single-column flow for focus
 * - Smart defaults reduce decisions
 * - Clear visual feedback at every step
 * - Form feels conversational, not overwhelming
 */

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PdfGeneratorScreen(
    navController: NavController,
    viewModel: PdfGeneratorViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    
    // Form state with smart defaults
    var selectedSubject by remember { mutableStateOf("Mathematics") }
    var selectedClass by remember { mutableStateOf("Class 12") }
    var selectedTopic by remember { mutableStateOf("All Chapters") }
    var selectedSubtopic by remember { mutableStateOf("All Subtopics") }

    // Load chapters when subject or class changes
    LaunchedEffect(selectedSubject, selectedClass) {
        selectedTopic = "All Chapters"
        selectedSubtopic = "All Subtopics"
        viewModel.loadChapters(subject = selectedSubject, grade = selectedClass)
    }
    var selectedDifficulty by remember { mutableStateOf("Medium") }
    var selectedQuestionTypes by remember { mutableStateOf(setOf("MCQ")) }
    var numberOfQuestions by remember { mutableStateOf(10) }
    var selectedSource by remember { mutableStateOf("NCERT") }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(KlaroDesign.Spacing.ScreenPadding)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.SectionGap)
    ) {
        
        // Page Header - Clear purpose
        CleanCard {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    Icons.Filled.CreateNewFolder,
                    contentDescription = null,
                    tint = KlaroDesign.Colors.LearningBlue,
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge)
                )
                Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
                Column {
                    Text(
                        text = "Create Quiz",
                        fontSize = KlaroDesign.Typography.Headline,
                        fontWeight = KlaroDesign.Typography.Bold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    Text(
                        text = "Personalized practice questions",
                        fontSize = KlaroDesign.Typography.Body,
                        color = KlaroDesign.Colors.NeutralMedium
                    )
                }
            }
        }
        
        // Form Section 1: Subject & Class (Most Important)
        CleanCard {
            Text(
                text = "What to study?",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            
            // Subject selection - Most important choice
            CleanDropdown(
                label = "Subject",
                selectedValue = selectedSubject,
                options = SyllabusData.getSubjects(),
                onValueChange = { 
                    selectedSubject = it
                    selectedTopic = "All Chapters" // Reset dependent choice
                    selectedSubtopic = "All Subtopics"
                }
            )
            
            // Class level - Context for difficulty
            CleanDropdown(
                label = "Class Level",
                selectedValue = selectedClass,
                options = SyllabusData.getClasses(),
                onValueChange = { 
                    selectedClass = it 
                    selectedTopic = "All Chapters"
                    selectedSubtopic = "All Subtopics"
                }
            )
        }
        
        // Form Section 2: Topic Focus (Progressive Disclosure)
        CleanCard {
            Text(
                text = "Focus area?",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            
            // Loading indicator for chapters
            if (uiState.isChaptersLoading) {
                LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
                Spacer(modifier = Modifier.height(KlaroDesign.Spacing.Small))
            }

            CleanDropdown(
                label = "Chapter",
                selectedValue = selectedTopic,
                options = listOf("All Chapters") + uiState.chapters,
                onValueChange = { 
                    selectedTopic = it 
                    selectedSubtopic = "All Subtopics"
                    // Load subtopics for selected chapter
                    viewModel.loadSubtopics(selectedSubject, selectedClass, it)
                }
            )

            // Retry button if chapters failed to load
            if (!uiState.isChaptersLoading && uiState.chapters.isEmpty()) {
                TextButton(onClick = { viewModel.loadChapters(selectedSubject, selectedClass) }) {
                    Text("Retry loading chapters")
                }
            }

            // Loading indicator for subtopics
            if (uiState.isSubtopicsLoading) {
                LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
                Spacer(modifier = Modifier.height(KlaroDesign.Spacing.Small))
            }

            CleanDropdown(
                label = "Subtopic",
                selectedValue = selectedSubtopic,
                options = listOf("All Subtopics") + uiState.subtopics,
                onValueChange = { selectedSubtopic = it }
            )
        }
        
        // Form Section 3: Source Selection
        CleanCard {
            Text(
                text = "Source",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            val sourceOptions = listOf(
                "NCERT",
                "CBSE reference books",
                "IIT JEE books",
                "IIT JEE coaching material",
                "NEET books",
                "NEET coaching material",
                "PYQ boards",
                "PYQ JEE mains",
                "PYQ JEE advanced",
                "PYQ NEET"
            )
            CleanDropdown(
                label = "Select source",
                selectedValue = selectedSource,
                options = sourceOptions,
                onValueChange = { selectedSource = it }
            )
        }

        // Form Section 4: Quiz Configuration
        CleanCard {
            Text(
                text = "Quiz setup",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            
            // Question types (multi-select)
            MultiSelectDropdown(
                label = "Question Types",
                selectedValues = selectedQuestionTypes.toList(),
                options = listOf("MCQ", "Short Answer", "Long Answer", "Numerical"),
                onSelectionChange = { selectedQuestionTypes = it.toSet() }
            )
            
            // Difficulty
            CleanDropdown(
                label = "Difficulty",
                selectedValue = selectedDifficulty,
                options = listOf("Easy", "Medium", "Hard", "Mixed"),
                onValueChange = { selectedDifficulty = it }
            )
            
            // Question count with clear visual
            Column {
                Text(
                    text = "Number of Questions: $numberOfQuestions",
                    fontSize = KlaroDesign.Typography.Body,
                    fontWeight = KlaroDesign.Typography.Medium,
                    color = KlaroDesign.Colors.NeutralDark
                )
                Spacer(modifier = Modifier.height(KlaroDesign.Spacing.Small))
                Slider(
                    value = numberOfQuestions.toFloat(),
                    onValueChange = { numberOfQuestions = it.toInt() },
                    valueRange = 5f..30f,
                    steps = 4,
                    modifier = Modifier.fillMaxWidth()
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("5", fontSize = KlaroDesign.Typography.Caption, color = KlaroDesign.Colors.NeutralMedium)
                    Text("30", fontSize = KlaroDesign.Typography.Caption, color = KlaroDesign.Colors.NeutralMedium)
                }
            }
        }
        
        // Primary Action - Confident and clear
        PrimaryActionButton(
            text = "Generate Quiz",
            onClick = {
                val topicsArg = when {
                    selectedTopic == "All Chapters" -> emptyList()
                    selectedSubtopic != "All Subtopics" -> listOf(selectedSubtopic)
                    else -> listOf(selectedTopic)
                }
                val typeCode: (String) -> String = { t ->
                    when (t) {
                        "MCQ" -> "mcq"
                        "Short Answer" -> "short"
                        "Long Answer" -> "long"
                        "Numerical" -> "numerical"
                        else -> t.lowercase()
                    }
                }
                viewModel.generateQuiz(
                    topics = topicsArg,
                    numQuestions = numberOfQuestions,
                    questionTypes = selectedQuestionTypes.map(typeCode),
                    difficultyLevels = listOf(selectedDifficulty.lowercase()),
                    subject = selectedSubject,
                    source = selectedSource
                )
            },
            isLoading = uiState.isGenerating,
            icon = Icons.Filled.AutoAwesome
        )
        
        // Feedback Messages - Minimal and clear
        uiState.success?.let { message ->
            MessageCard(message = message, type = MessageType.SUCCESS)
        }
        
        uiState.error?.let { error ->
            MessageCard(message = error, type = MessageType.ERROR)
        }
    }
}

/**
 * Clean Dropdown Component - Minimal and functional
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CleanDropdown(
    label: String,
    selectedValue: String,
    options: List<String>,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var expanded by remember { mutableStateOf(false) }
    
    Column(modifier = modifier) {
        Text(
            text = label,
            fontSize = KlaroDesign.Typography.Caption,
            fontWeight = KlaroDesign.Typography.Medium,
            color = KlaroDesign.Colors.NeutralMedium,
            modifier = Modifier.padding(bottom = KlaroDesign.Spacing.XSmall)
        )
        
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = { expanded = !expanded }
        ) {
            OutlinedTextField(
                value = selectedValue,
                onValueChange = {},
                readOnly = true,
                trailingIcon = {
                    ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded)
                },
                modifier = Modifier
                    .menuAnchor()
                    .fillMaxWidth(),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = KlaroDesign.Colors.LearningBlue,
                    unfocusedBorderColor = KlaroDesign.Colors.NeutralMedium.copy(alpha = 0.3f)
                )
            )
            
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                options.forEach { option ->
                    DropdownMenuItem(
                        text = { 
                            Text(
                                option,
                                fontSize = KlaroDesign.Typography.Body
                            ) 
                        },
                        onClick = {
                            onValueChange(option)
                            expanded = false
                        }
                    )
                }
            }
        }
    }
}

/**
 * Multi-select dropdown with checkbox items and a compact summary.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MultiSelectDropdown(
    label: String,
    selectedValues: List<String>,
    options: List<String>,
    onSelectionChange: (List<String>) -> Unit,
    modifier: Modifier = Modifier
) {
    var expanded by remember { mutableStateOf(false) }
    val summary = if (selectedValues.isEmpty()) "Select one or more" else selectedValues.joinToString(", ")

    Column(modifier = modifier) {
        Text(
            text = label,
            fontSize = KlaroDesign.Typography.Caption,
            fontWeight = KlaroDesign.Typography.Medium,
            color = KlaroDesign.Colors.NeutralMedium,
            modifier = Modifier.padding(bottom = KlaroDesign.Spacing.XSmall)
        )

        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = { expanded = !expanded }
        ) {
            OutlinedTextField(
                value = summary,
                onValueChange = {},
                readOnly = true,
                trailingIcon = {
                    ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded)
                },
                modifier = Modifier
                    .menuAnchor()
                    .fillMaxWidth(),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = KlaroDesign.Colors.LearningBlue,
                    unfocusedBorderColor = KlaroDesign.Colors.NeutralMedium.copy(alpha = 0.3f)
                )
            )

            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                options.forEach { option ->
                    val isSelected = selectedValues.contains(option)
                    DropdownMenuItem(
                        text = {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Checkbox(checked = isSelected, onCheckedChange = null)
                                Spacer(Modifier.width(8.dp))
                                Text(option, fontSize = KlaroDesign.Typography.Body)
                            }
                        },
                        onClick = {
                            val newSelection = if (isSelected) selectedValues - option else selectedValues + option
                            onSelectionChange(newSelection)
                        }
                    )
                }
            }
        }

        // Selected chips (horizontal scroll to handle overflow gracefully)
        if (selectedValues.isNotEmpty()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                selectedValues.forEach { value ->
                    AssistChip(onClick = { /* no-op */ }, label = { Text(value) })
                }
            }
        }
    }
}

// Smart content helpers
fun getTopicsForSubject(subject: String): List<String> {
    return when (subject) {
        "Mathematics" -> listOf("All Topics", "Algebra", "Calculus", "Geometry", "Trigonometry", "Statistics")
        "Physics" -> listOf("All Topics", "Mechanics", "Thermodynamics", "Electromagnetism", "Optics", "Modern Physics")
        "Chemistry" -> listOf("All Topics", "Physical Chemistry", "Organic Chemistry", "Inorganic Chemistry")
        "Biology" -> listOf("All Topics", "Cell Biology", "Genetics", "Ecology", "Human Physiology", "Plant Biology")
        else -> listOf("All Topics")
    }
}
