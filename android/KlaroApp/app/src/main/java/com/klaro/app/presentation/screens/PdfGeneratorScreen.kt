package com.klaro.app.presentation.screens

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.klaro.app.data.models.BlueprintConfig
import com.klaro.app.data.models.QuizRequest
import com.klaro.app.data.models.SectionConfig
import com.klaro.app.presentation.viewmodels.PdfGeneratorViewModel
import com.klaro.app.presentation.ui.design.*
import java.io.File

// Section row model for dynamic sections
data class SectionRow(var name: String, var types: MutableSet<String>, var count: String)

/**
 * 📄 Practice Test Builder (Native Compose)
 * 
 * Domain-aware form for CBSE/JEE/NEET with blueprint, marks, header/instructions,
 * preview and generation, plus downloads.
 */

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PdfGeneratorScreen(
    navController: NavController,
    viewModel: PdfGeneratorViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current

    // -----------------------------------------------------------------------------
    // Core selection state
    // -----------------------------------------------------------------------------
    val domainOptions = listOf("CBSE", "JEE", "NEET")
    var domain by remember { mutableStateOf("CBSE") }

    val gradeOptions = listOf("Class 9", "Class 10", "Class 11", "Class 12")
    var gradeLabel by remember { mutableStateOf("Class 12") }
    val gradeValue: String = remember(gradeLabel) { gradeLabel.removePrefix("Class ").trim() }

    // Subject(s)
    var singleSubject by remember { mutableStateOf("Mathematics") }
    val cbseSubjectOptions = listOf("Mathematics", "Science", "Physics", "Chemistry", "Biology")
    val jeeSubjects = listOf("Mathematics", "Physics", "Chemistry")
    val neetSubjects = listOf("Physics", "Chemistry", "Biology")
    var selectedSubjects by remember { mutableStateOf(setOf<String>()) } // for JEE/NEET multi

    // Chapters/Subtopics via catalog
    var selectedChapter by remember { mutableStateOf("All Chapters") }
    var selectedSubtopic by remember { mutableStateOf("All Subtopics") }

    // Load catalog when singleSubject or grade changes (for CBSE primarily)
    LaunchedEffect(singleSubject, gradeLabel) {
        selectedChapter = "All Chapters"
        selectedSubtopic = "All Subtopics"
        viewModel.loadChapters(subject = singleSubject, grade = gradeLabel)
    }

    // Source / mode / render
    var booksDir by remember { mutableStateOf("") }
    var scopeFilter by remember { mutableStateOf("") }
    var centersCsv by remember { mutableStateOf("") }
    var streamsCsv by remember { mutableStateOf("") }
    var language by remember { mutableStateOf("English") }
    var mode by remember { mutableStateOf("mixed") }
    var render by remember { mutableStateOf("auto") }
    var outputEngine by remember { mutableStateOf("reportlab") }

    // Header / Instructions / Include Solutions
    var header by remember { mutableStateOf("") }
    var instructionsText by remember { mutableStateOf("") } // one per line
    var includeSolutions by remember { mutableStateOf(false) }

    // Blueprint: base counts
    var bpTotal by remember { mutableStateOf("25") }
    var bpMcq by remember { mutableStateOf("10") }
    var bpShort by remember { mutableStateOf("10") }
    var bpLong by remember { mutableStateOf("5") }
    var bpEasy by remember { mutableStateOf("10") }
    var bpMedium by remember { mutableStateOf("10") }
    var bpHard by remember { mutableStateOf("5") }
    var bpDuration by remember { mutableStateOf("") }

    // CBSE specific counts
    var cbseSingle by remember { mutableStateOf("0") }
    var cbseAR by remember { mutableStateOf("0") }
    var cbseShort2 by remember { mutableStateOf("0") }
    var cbseLong3 by remember { mutableStateOf("0") }
    var cbseVeryLong5 by remember { mutableStateOf("0") }
    var cbseCase by remember { mutableStateOf("0") }

    // Marks per type
    var marksMcq by remember { mutableStateOf("1") }
    var marksShort by remember { mutableStateOf("3") }
    var marksLong by remember { mutableStateOf("5") }
    var marksSingle by remember { mutableStateOf("1") }
    var marksAR by remember { mutableStateOf("1") }
    var marksShort2 by remember { mutableStateOf("2") }
    var marksLong3 by remember { mutableStateOf("3") }
    var marksVeryLong5 by remember { mutableStateOf("5") }
    var marksCase by remember { mutableStateOf("4") }

// Sections list
    var sections by remember { mutableStateOf(listOf(
        SectionRow("Section A", mutableSetOf("mcq"), "10"),
        SectionRow("Section B", mutableSetOf("short"), "10"),
        SectionRow("Section C", mutableSetOf("long"), "5")
    )) }

    // Handle saving downloaded file when available
    var lastSavedPath by remember { mutableStateOf<String?>(null) }
    LaunchedEffect(uiState.downloadedFile) {
        val body = uiState.downloadedFile ?: return@LaunchedEffect
        try {
            val bytes = body.bytes()
            val isPdf = bytes.size >= 4 && bytes[0] == '%'.code.toByte() && bytes[1] == 'P'.code.toByte() && bytes[2] == 'D'.code.toByte() && bytes[3] == 'F'.code.toByte()
            val ext = if (isPdf) "pdf" else "txt"
            val type = uiState.lastDownloadType ?: "file"
            val quizId = uiState.lastGeneratedQuiz?.quizId ?: System.currentTimeMillis().toString()
            val outDir = context.getExternalFilesDir(null) ?: context.filesDir
            val outFile = File(outDir, "${quizId}_${type}.${ext}")
            outFile.writeBytes(bytes)
            lastSavedPath = outFile.absolutePath
        } catch (_: Exception) {
            lastSavedPath = null
        } finally {
            viewModel.clearDownloadedFile()
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(KlaroDesign.Spacing.ScreenPadding)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.SectionGap)
    ) {
        // Header
        CleanCard {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Filled.CreateNewFolder, contentDescription = null, tint = KlaroDesign.Colors.LearningBlue, modifier = Modifier.size(KlaroDesign.Components.IconLarge))
                Spacer(Modifier.width(KlaroDesign.Spacing.Medium))
                Column {
                    Text("Practice Test Builder", fontSize = KlaroDesign.Typography.Headline, fontWeight = KlaroDesign.Typography.Bold, color = KlaroDesign.Colors.NeutralDark)
                    Text("Customize domain, blueprint, and output", fontSize = KlaroDesign.Typography.Body, color = KlaroDesign.Colors.NeutralMedium)
                }
            }
        }

        // 1) Domain / Grade / Subject(s)
        CleanCard {
            Text("Basics", fontSize = KlaroDesign.Typography.Title, fontWeight = KlaroDesign.Typography.SemiBold, color = KlaroDesign.Colors.NeutralDark)
DropdownField("Domain", domain, domainOptions) { domain = it }
            if (domain == "CBSE") {
DropdownField("Grade", gradeLabel, gradeOptions) { gradeLabel = it }
DropdownField("Subject", singleSubject, cbseSubjectOptions) {
                    singleSubject = it
                    selectedChapter = "All Chapters"
                    selectedSubtopic = "All Subtopics"
                    viewModel.loadChapters(singleSubject, gradeLabel)
                }
            } else {
                val opts = if (domain == "JEE") jeeSubjects else neetSubjects
MultiSelectField(
                    label = "Subjects",
                    selectedValues = selectedSubjects.toList(),
                    options = opts,
                    onSelectionChange = { selectedSubjects = it.toSet() }
                )
                // Fallback single subject context for catalog selections
DropdownField("Context Subject", singleSubject, opts) { singleSubject = it }
            }
DropdownField("Language", language, listOf("English", "Hindi")) { language = it }
        }

        // 2) Subjects & Topics (Catalog)
        CleanCard {
            Text("Subjects & Topics", fontSize = KlaroDesign.Typography.Title, fontWeight = KlaroDesign.Typography.SemiBold, color = KlaroDesign.Colors.NeutralDark)
            if (uiState.isChaptersLoading) {
                LinearProgressIndicator(modifier = Modifier.fillMaxWidth()); Spacer(Modifier.height(KlaroDesign.Spacing.Small))
            }
DropdownField("Chapter", selectedChapter, listOf("All Chapters") + uiState.chapters) {
                selectedChapter = it
                selectedSubtopic = "All Subtopics"
                viewModel.loadSubtopics(singleSubject, gradeLabel, it)
            }
            if (uiState.isSubtopicsLoading) {
                LinearProgressIndicator(modifier = Modifier.fillMaxWidth()); Spacer(Modifier.height(KlaroDesign.Spacing.Small))
            }
DropdownField("Subtopic", selectedSubtopic, listOf("All Subtopics") + uiState.subtopics) { selectedSubtopic = it }
        }

        // 3) Source material / rendering
        CleanCard {
            Text("Source & Rendering", fontSize = KlaroDesign.Typography.Title, fontWeight = KlaroDesign.Typography.SemiBold, color = KlaroDesign.Colors.NeutralDark)
            TwoFieldRow(label1 = "Books Directory", value1 = booksDir, on1 = { booksDir = it }, label2 = "Scope Filter", value2 = scopeFilter, on2 = { scopeFilter = it })
            TwoFieldRow(label1 = "Centers (csv)", value1 = centersCsv, on1 = { centersCsv = it }, label2 = "Streams (csv)", value2 = streamsCsv, on2 = { streamsCsv = it })
            Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
Column(modifier = Modifier.weight(1f)) { DropdownField("Mode", mode, listOf("mixed","source","parametric")) { mode = it } }
Column(modifier = Modifier.weight(1f)) { DropdownField("Render", render, listOf("auto","image","text")) { render = it } }
Column(modifier = Modifier.weight(1f)) { DropdownField("Engine", outputEngine, listOf("reportlab","latex")) { outputEngine = it } }
            }
        }

        // 4) Blueprint
        CleanCard {
            Text("Blueprint", fontSize = KlaroDesign.Typography.Title, fontWeight = FontWeight.SemiBold, color = KlaroDesign.Colors.NeutralDark)
            Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("Total Questions", bpTotal, modifier = Modifier.weight(1f)) { bpTotal = it }
NumberField("Duration (min)", bpDuration, modifier = Modifier.weight(1f)) { bpDuration = it }
            }
            Text("By Type (Base)", fontSize = KlaroDesign.Typography.Subtitle, fontWeight = FontWeight.Medium)
            Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("MCQ", bpMcq, modifier = Modifier.weight(1f)) { bpMcq = it }
NumberField("Short", bpShort, modifier = Modifier.weight(1f)) { bpShort = it }
NumberField("Long", bpLong, modifier = Modifier.weight(1f)) { bpLong = it }
            }
            Text("By Difficulty", fontSize = KlaroDesign.Typography.Subtitle, fontWeight = FontWeight.Medium)
            Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("Easy", bpEasy, modifier = Modifier.weight(1f)) { bpEasy = it }
NumberField("Medium", bpMedium, modifier = Modifier.weight(1f)) { bpMedium = it }
NumberField("Hard", bpHard, modifier = Modifier.weight(1f)) { bpHard = it }
            }
            if (domain == "CBSE") {
                Divider()
                Text("CBSE Types", fontSize = KlaroDesign.Typography.Subtitle, fontWeight = FontWeight.Medium)
                Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("Single Correct (1M)", cbseSingle, modifier = Modifier.weight(1f)) { cbseSingle = it }
NumberField("Assertion-Reason (1M)", cbseAR, modifier = Modifier.weight(1f)) { cbseAR = it }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("Short (2M)", cbseShort2, modifier = Modifier.weight(1f)) { cbseShort2 = it }
NumberField("Long (3M)", cbseLong3, modifier = Modifier.weight(1f)) { cbseLong3 = it }
NumberField("Very Long (5M)", cbseVeryLong5, modifier = Modifier.weight(1f)) { cbseVeryLong5 = it }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("Case Study (4M)", cbseCase, modifier = Modifier.weight(1f)) { cbseCase = it }
                }
            }
        }

        // 5) Scoring / Marks
        CleanCard {
            Text("Scoring & Marks", fontSize = KlaroDesign.Typography.Title, fontWeight = FontWeight.SemiBold, color = KlaroDesign.Colors.NeutralDark)
            Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("Marks/MCQ", marksMcq, modifier = Modifier.weight(1f)) { marksMcq = it }
NumberField("Marks/Short", marksShort, modifier = Modifier.weight(1f)) { marksShort = it }
NumberField("Marks/Long", marksLong, modifier = Modifier.weight(1f)) { marksLong = it }
            }
            if (domain == "CBSE") {
                Divider()
                Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("CBSE Single", marksSingle, modifier = Modifier.weight(1f)) { marksSingle = it }
NumberField("CBSE A-R", marksAR, modifier = Modifier.weight(1f)) { marksAR = it }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("CBSE Short(2)", marksShort2, modifier = Modifier.weight(1f)) { marksShort2 = it }
NumberField("CBSE Long(3)", marksLong3, modifier = Modifier.weight(1f)) { marksLong3 = it }
NumberField("CBSE VeryLong(5)", marksVeryLong5, modifier = Modifier.weight(1f)) { marksVeryLong5 = it }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
NumberField("CBSE Case", marksCase, modifier = Modifier.weight(1f)) { marksCase = it }
                }
            }
        }

        // 6) Sections (dynamic)
        CleanCard {
            Text("Sections", fontSize = KlaroDesign.Typography.Title, fontWeight = FontWeight.SemiBold)
            sections.forEachIndexed { idx, s ->
                SectionRowEditor(
                    row = s,
                    onChange = { newRow -> sections = sections.toMutableList().also { it[idx] = newRow } },
                    onRemove = { sections = sections.toMutableList().also { it.removeAt(idx) } }
                )
                if (idx < sections.lastIndex) Divider()
            }
            TextButton(onClick = { sections = sections + SectionRow("Section", mutableSetOf("mcq"), "5") }) {
                Icon(Icons.Filled.Add, contentDescription = null); Spacer(Modifier.width(8.dp)); Text("Add Section")
            }
        }

        // 7) Rendering & Instructions
        CleanCard {
            Text("Header & Instructions", fontSize = KlaroDesign.Typography.Title, fontWeight = FontWeight.SemiBold)
            OutlinedTextField(value = header, onValueChange = { header = it }, label = { Text("Header / Institute Name") }, modifier = Modifier.fillMaxWidth())
            Spacer(Modifier.height(KlaroDesign.Spacing.Small))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Switch(checked = includeSolutions, onCheckedChange = { includeSolutions = it }); Spacer(Modifier.width(8.dp)); Text("Include Solutions in outputs")
            }
            Spacer(Modifier.height(KlaroDesign.Spacing.Small))
            OutlinedTextField(
                value = instructionsText,
                onValueChange = { instructionsText = it },
                label = { Text("Instructions (one per line)") },
                modifier = Modifier.fillMaxWidth(),
                maxLines = 5
            )
        }

        // Preview & Generate
        Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
            PrimaryActionButton(text = "Preview", onClick = {
                val req = buildRequest(
                    domain = domain,
                    gradeValue = gradeValue,
                    singleSubject = singleSubject,
                    selectedSubjects = selectedSubjects.toList(),
                    selectedChapter = selectedChapter,
                    selectedSubtopic = selectedSubtopic,
                    booksDir = booksDir,
                    scopeFilter = scopeFilter,
                    centersCsv = centersCsv,
                    streamsCsv = streamsCsv,
                    language = language,
                    mode = mode,
                    render = render,
                    outputEngine = outputEngine,
                    header = header,
                    instructionsText = instructionsText,
                    includeSolutions = includeSolutions,
                    bpTotal = bpTotal, bpMcq = bpMcq, bpShort = bpShort, bpLong = bpLong,
                    bpEasy = bpEasy, bpMedium = bpMedium, bpHard = bpHard, bpDuration = bpDuration,
                    cbseSingle = cbseSingle, cbseAR = cbseAR, cbseShort2 = cbseShort2, cbseLong3 = cbseLong3, cbseVeryLong5 = cbseVeryLong5, cbseCase = cbseCase,
                    marksMcq = marksMcq, marksShort = marksShort, marksLong = marksLong,
                    marksSingle = marksSingle, marksAR = marksAR, marksShort2 = marksShort2, marksLong3 = marksLong3, marksVeryLong5 = marksVeryLong5, marksCase = marksCase,
                    sections = sections
                )
                viewModel.previewQuiz(req)
}, isLoading = uiState.isPreviewing, icon = Icons.Filled.Visibility)
            PrimaryActionButton(text = "Generate PDF", onClick = {
                val req = buildRequest(
                    domain = domain,
                    gradeValue = gradeValue,
                    singleSubject = singleSubject,
                    selectedSubjects = selectedSubjects.toList(),
                    selectedChapter = selectedChapter,
                    selectedSubtopic = selectedSubtopic,
                    booksDir = booksDir,
                    scopeFilter = scopeFilter,
                    centersCsv = centersCsv,
                    streamsCsv = streamsCsv,
                    language = language,
                    mode = mode,
                    render = render,
                    outputEngine = outputEngine,
                    header = header,
                    instructionsText = instructionsText,
                    includeSolutions = includeSolutions,
                    bpTotal = bpTotal, bpMcq = bpMcq, bpShort = bpShort, bpLong = bpLong,
                    bpEasy = bpEasy, bpMedium = bpMedium, bpHard = bpHard, bpDuration = bpDuration,
                    cbseSingle = cbseSingle, cbseAR = cbseAR, cbseShort2 = cbseShort2, cbseLong3 = cbseLong3, cbseVeryLong5 = cbseVeryLong5, cbseCase = cbseCase,
                    marksMcq = marksMcq, marksShort = marksShort, marksLong = marksLong,
                    marksSingle = marksSingle, marksAR = marksAR, marksShort2 = marksShort2, marksLong3 = marksLong3, marksVeryLong5 = marksVeryLong5, marksCase = marksCase,
                    sections = sections
                )
                viewModel.generateQuizAdvanced(req)
            }, isLoading = uiState.isGenerating, icon = Icons.Filled.AutoAwesome)
        }

        // Summary Preview
        uiState.preview?.let { p ->
            CleanCard {
                Text("Preview", fontSize = KlaroDesign.Typography.Title, fontWeight = FontWeight.SemiBold)
                Text("Total Questions: ${p.totals["total_questions"] ?: 0}")
                p.totals["total_marks"]?.let { tm -> Text("Total Marks: $tm") }
                Text("Estimated Duration: ${p.durationEstimate} minutes")
                if (p.warnings.isNotEmpty()) {
                    Spacer(Modifier.height(KlaroDesign.Spacing.Small))
                    Text("Warnings:", fontWeight = FontWeight.SemiBold)
                    p.warnings.forEach { Text("• $it") }
                }
            }
        }

        // Generated quiz + download options
        uiState.lastGeneratedQuiz?.let { qr ->
            CleanCard {
                Text("Quiz Ready", fontSize = KlaroDesign.Typography.Title, fontWeight = FontWeight.SemiBold)
                Text("ID: ${qr.quizId}")
                Spacer(Modifier.height(KlaroDesign.Spacing.Small))
                Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium)) {
                    Button(onClick = { viewModel.downloadQuiz(qr.quizId, "questions") }) { Text("Download Questions") }
                    Button(onClick = { viewModel.downloadQuiz(qr.quizId, "answers") }, enabled = qr.pdfAnswersFile != null) { Text("Download Answers") }
                    Button(onClick = { viewModel.downloadQuiz(qr.quizId, "marking_scheme") }, enabled = qr.pdfMarkingSchemeFile != null) { Text("Marking Scheme") }
                }
                lastSavedPath?.let { path ->
                    Spacer(Modifier.height(KlaroDesign.Spacing.Small))
                    Text("Saved to: $path", color = KlaroDesign.Colors.NeutralMedium)
                }
            }
        }

        // Messages
        uiState.success?.let { MessageCard(it, MessageType.SUCCESS) }
        uiState.error?.let { MessageCard(it, MessageType.ERROR) }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DropdownField(
    label: String,
    selectedValue: String,
    options: List<String>,
    modifier: Modifier = Modifier,
    onValueChange: (String) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    Column(modifier = modifier) {
        Text(label, fontSize = KlaroDesign.Typography.Caption, fontWeight = KlaroDesign.Typography.Medium, color = KlaroDesign.Colors.NeutralMedium, modifier = Modifier.padding(bottom = KlaroDesign.Spacing.XSmall))
        ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
            OutlinedTextField(
                value = selectedValue,
                onValueChange = {},
                readOnly = true,
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                modifier = Modifier.menuAnchor().fillMaxWidth(),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = KlaroDesign.Colors.LearningBlue,
                    unfocusedBorderColor = KlaroDesign.Colors.NeutralMedium.copy(alpha = 0.3f)
                )
            )
            ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                options.forEach { option ->
                    DropdownMenuItem(text = { Text(option, fontSize = KlaroDesign.Typography.Body) }, onClick = {
                        onValueChange(option); expanded = false
                    })
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MultiSelectField(
    label: String,
    selectedValues: List<String>,
    options: List<String>,
    modifier: Modifier = Modifier,
    onSelectionChange: (List<String>) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    val summary = if (selectedValues.isEmpty()) "Select one or more" else selectedValues.joinToString(", ")
    Column(modifier = modifier) {
        Text(label, fontSize = KlaroDesign.Typography.Caption, fontWeight = KlaroDesign.Typography.Medium, color = KlaroDesign.Colors.NeutralMedium, modifier = Modifier.padding(bottom = KlaroDesign.Spacing.XSmall))
        ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
            OutlinedTextField(
                value = summary,
                onValueChange = {},
                readOnly = true,
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                modifier = Modifier.menuAnchor().fillMaxWidth(),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = KlaroDesign.Colors.LearningBlue,
                    unfocusedBorderColor = KlaroDesign.Colors.NeutralMedium.copy(alpha = 0.3f)
                )
            )
            ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
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
        if (selectedValues.isNotEmpty()) {
            Row(
                modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                selectedValues.forEach { value -> AssistChip(onClick = { }, label = { Text(value) }) }
            }
        }
    }
}

@Composable
fun NumberField(label: String, value: String, modifier: Modifier = Modifier, onChange: (String) -> Unit) {
    OutlinedTextField(
        value = value,
        onValueChange = { new -> onChange(new.filter { it.isDigit() }) },
        label = { Text(label) },
        modifier = modifier
    )
}

@Composable
fun TwoFieldRow(label1: String, value1: String, on1: (String) -> Unit, label2: String, value2: String, on2: (String) -> Unit) {
    Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), modifier = Modifier.fillMaxWidth()) {
        OutlinedTextField(value = value1, onValueChange = on1, label = { Text(label1) }, modifier = Modifier.weight(1f))
        OutlinedTextField(value = value2, onValueChange = on2, label = { Text(label2) }, modifier = Modifier.weight(1f))
    }
}

@Composable
fun SectionRowEditor(row: SectionRow, onChange: (SectionRow) -> Unit, onRemove: () -> Unit) {
    val r = row as SectionRow
    Column(modifier = Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Small)) {
        OutlinedTextField(value = r.name, onValueChange = { onChange(r.copy(name = it)) }, label = { Text("Name") }, modifier = Modifier.fillMaxWidth())
        Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium), verticalAlignment = Alignment.CenterVertically) {
            TypeCheckbox("MCQ", "mcq", r.types) { onChange(r.copy(types = it.toMutableSet())) }
            TypeCheckbox("Short", "short", r.types) { onChange(r.copy(types = it.toMutableSet())) }
            TypeCheckbox("Long", "long", r.types) { onChange(r.copy(types = it.toMutableSet())) }
            Spacer(Modifier.weight(1f))
            OutlinedTextField(value = r.count, onValueChange = { onChange(r.copy(count = it.filter { c -> c.isDigit() })) }, label = { Text("Count") }, modifier = Modifier.width(120.dp))
            IconButton(onClick = onRemove) { Icon(Icons.Filled.Delete, contentDescription = null) }
        }
    }
}

@Composable
fun TypeCheckbox(label: String, code: String, current: MutableSet<String>, onTypes: (Set<String>) -> Unit) {
    val checked = current.contains(code)
    Row(verticalAlignment = Alignment.CenterVertically) {
        Checkbox(checked = checked, onCheckedChange = {
            val next = current.toMutableSet()
            if (it == true) next.add(code) else next.remove(code)
            onTypes(next)
        })
        Text(label)
    }
}


// Actual buildRequest overload with real SectionRow list
private fun buildRequest(
    domain: String,
    gradeValue: String,
    singleSubject: String,
    selectedSubjects: List<String>,
    selectedChapter: String,
    selectedSubtopic: String,
    booksDir: String,
    scopeFilter: String,
    centersCsv: String,
    streamsCsv: String,
    language: String,
    mode: String,
    render: String,
    outputEngine: String,
    header: String,
    instructionsText: String,
    includeSolutions: Boolean,
    bpTotal: String,
    bpMcq: String,
    bpShort: String,
    bpLong: String,
    bpEasy: String,
    bpMedium: String,
    bpHard: String,
    bpDuration: String,
    cbseSingle: String,
    cbseAR: String,
    cbseShort2: String,
    cbseLong3: String,
    cbseVeryLong5: String,
    cbseCase: String,
    marksMcq: String,
    marksShort: String,
    marksLong: String,
    marksSingle: String,
    marksAR: String,
    marksShort2: String,
    marksLong3: String,
    marksVeryLong5: String,
    marksCase: String,
sections: List<SectionRow>
): QuizRequest {
    val topics = when {
        selectedChapter == "All Chapters" -> emptyList()
        selectedSubtopic != "All Subtopics" -> listOf(selectedSubtopic)
        else -> listOf(selectedChapter)
    }
    val baseByType = mapOf(
        "mcq" to (bpMcq.toIntOrNull() ?: 0),
        "short" to (bpShort.toIntOrNull() ?: 0),
        "long" to (bpLong.toIntOrNull() ?: 0)
    )
    val cbseByType = mapOf(
        "single_correct" to (cbseSingle.toIntOrNull() ?: 0),
        "assertion_reason" to (cbseAR.toIntOrNull() ?: 0),
        "short2" to (cbseShort2.toIntOrNull() ?: 0),
        "long3" to (cbseLong3.toIntOrNull() ?: 0),
        "verylong5" to (cbseVeryLong5.toIntOrNull() ?: 0),
        "case_study" to (cbseCase.toIntOrNull() ?: 0)
    )
    val useCbse = domain == "CBSE" && cbseByType.values.any { it > 0 }
    val byType = if (useCbse) cbseByType else baseByType

    val marks = buildMap<String, Int> {
        put("mcq", marksMcq.toIntOrNull() ?: 1)
        put("short", marksShort.toIntOrNull() ?: 3)
        put("long", marksLong.toIntOrNull() ?: 5)
        if (useCbse) {
            put("single_correct", marksSingle.toIntOrNull() ?: 1)
            put("assertion_reason", marksAR.toIntOrNull() ?: 1)
            put("short2", marksShort2.toIntOrNull() ?: 2)
            put("long3", marksLong3.toIntOrNull() ?: 3)
            put("verylong5", marksVeryLong5.toIntOrNull() ?: 5)
            put("case_study", marksCase.toIntOrNull() ?: 4)
        }
    }

    val totalQ = bpTotal.toIntOrNull() ?: byType.values.sum().takeIf { it > 0 } ?: 10
    val blueprint = BlueprintConfig(
        totalQuestions = totalQ,
        byType = byType,
        byDifficulty = mapOf(
            "easy" to (bpEasy.toIntOrNull() ?: 0),
            "medium" to (bpMedium.toIntOrNull() ?: 0),
            "hard" to (bpHard.toIntOrNull() ?: 0)
        ),
        durationMinutes = bpDuration.toIntOrNull()
    )

    val sectionPayload = sections.mapNotNull { s ->
        val c = s.count.toIntOrNull() ?: 0
        if (c <= 0) null else SectionConfig(name = s.name, types = s.types.toList(), count = c)
    }

    val instructions = instructionsText.split('\n').map { it.trim() }.filter { it.isNotEmpty() }

    return QuizRequest(
        topics = if (topics.isEmpty()) listOf("general") else topics,
        numQuestions = totalQ,
        questionTypes = listOf("mcq","short","long"),
        difficultyLevels = listOf("easy","medium","hard"),
        subject = singleSubject,
        duration = blueprint.durationMinutes,
        title = null,
        domain = domain,
        grade = gradeValue,
        subjects = if (domain != "CBSE" && selectedSubjects.isNotEmpty()) selectedSubjects else null,
        header = header.ifBlank { null },
        instructions = if (instructions.isEmpty()) null else instructions,
        mode = mode,
        scopeFilter = scopeFilter.ifBlank { null },
        render = render,
        booksDir = booksDir.ifBlank { null },
        outputEngine = outputEngine,
        includeSolutions = includeSolutions,
        blueprint = blueprint,
        sections = if (sectionPayload.isEmpty()) null else sectionPayload,
        marks = marks,
        streams = streamsCsv.split(',').map { it.trim() }.filter { it.isNotEmpty() },
        classFilter = listOf(gradeValue),
        topicTags = emptyList(),
        subtopics = if (selectedSubtopic != "All Subtopics") listOf(selectedSubtopic) else emptyList(),
        levels = emptyList(),
        sourceMaterial = if (centersCsv.isNotBlank()) centersCsv.split(',').map { it.trim() }.filter { it.isNotEmpty() } else emptyList(),
        language = language,
        centers = if (centersCsv.isNotBlank()) centersCsv.split(',').map { it.trim() }.filter { it.isNotEmpty() } else emptyList()
    )
}

// Backwards compatible helper (kept for reference)
fun getTopicsForSubject(subject: String): List<String> {
    return when (subject) {
        "Mathematics" -> listOf("All Topics", "Algebra", "Calculus", "Geometry", "Trigonometry", "Statistics")
        "Physics" -> listOf("All Topics", "Mechanics", "Thermodynamics", "Electromagnetism", "Optics", "Modern Physics")
        "Chemistry" -> listOf("All Topics", "Physical Chemistry", "Organic Chemistry", "Inorganic Chemistry")
        "Biology" -> listOf("All Topics", "Cell Biology", "Genetics", "Ecology", "Human Physiology", "Plant Biology")
        else -> listOf("All Topics")
    }
}
