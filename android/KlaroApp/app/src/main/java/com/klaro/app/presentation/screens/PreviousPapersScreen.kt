package com.klaro.app.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.History
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.klaro.app.presentation.ui.design.*
import com.klaro.app.presentation.viewmodels.JeeTestViewModel

@Composable
fun PreviousPapersScreen(
    navController: NavController,
    viewModel: JeeTestViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val questions by viewModel.pyqQuestions.collectAsStateWithLifecycle()

    var selectedSubject by remember { mutableStateOf<String?>("Mathematics") }
    var selectedYear by remember { mutableStateOf<Int?>(2024) }

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
                Icon(
                    Icons.Filled.History,
                    contentDescription = null,
                    tint = KlaroDesign.Colors.LearningBlue,
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge)
                )
                Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
                Column {
                    Text(
                        text = "Previous Papers",
                        fontSize = KlaroDesign.Typography.Headline,
                        fontWeight = KlaroDesign.Typography.Bold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    Text(
                        text = "Load PYQs by year/subject",
                        fontSize = KlaroDesign.Typography.Body,
                        color = KlaroDesign.Colors.NeutralMedium
                    )
                }
            }
        }

        // Filters
        CleanCard {
            Text(
                text = "Filters",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Small)) {
                listOf("Mathematics", "Physics", "Chemistry").forEach { subject ->
                    FilterChip(
                        selected = selectedSubject == subject,
                        onClick = { selectedSubject = subject },
                        label = { Text(subject) }
                    )
                }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Small)) {
                listOf(2024, 2023, 2022, 2021).forEach { year ->
                    FilterChip(
                        selected = selectedYear == year,
                        onClick = { selectedYear = year },
                        label = { Text(year.toString()) }
                    )
                }
            }
        }

        PrimaryActionButton(
            text = "Load Questions",
            onClick = { viewModel.loadPreviousYearQuestions(selectedSubject, selectedYear) },
            isLoading = false
        )

        // Results
        if (questions.isNotEmpty()) {
            CleanCard {
                Text(
                    text = "Questions",
                    fontSize = KlaroDesign.Typography.Title,
                    fontWeight = KlaroDesign.Typography.SemiBold,
                    color = KlaroDesign.Colors.NeutralDark
                )
                questions.take(20).forEach { q ->
                    Text(q.questionText, fontSize = KlaroDesign.Typography.Body, color = KlaroDesign.Colors.NeutralDark)
                }
            }
        }

        uiState.error?.let { MessageCard("Couldn't load questions. Please try again.", type = MessageType.ERROR) }
    }
}

