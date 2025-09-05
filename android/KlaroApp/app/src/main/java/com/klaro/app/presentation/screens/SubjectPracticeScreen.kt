package com.klaro.app.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Book
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
fun SubjectPracticeScreen(
    navController: NavController,
    viewModel: JeeTestViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var selectedSubject by remember { mutableStateOf("Mathematics") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(KlaroDesign.Spacing.ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.SectionGap)
    ) {
        // Header
        CleanCard {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    Icons.Filled.Book,
                    contentDescription = null,
                    tint = KlaroDesign.Colors.LearningBlue,
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge)
                )
                Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
                Column {
                    Text(
                        text = "Subject Practice",
                        fontSize = KlaroDesign.Typography.Headline,
                        fontWeight = KlaroDesign.Typography.Bold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    Text(
                        text = "Choose a subject and start",
                        fontSize = KlaroDesign.Typography.Body,
                        color = KlaroDesign.Colors.NeutralMedium
                    )
                }
            }
        }

        // Subject chips
        CleanCard {
            Text(
                text = "Subject",
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
        }

        PrimaryActionButton(
            text = "Start Practice",
            onClick = { viewModel.startSubjectTest(selectedSubject) },
            isLoading = uiState.isCreatingTest
        )

        uiState.success?.let { MessageCard(it, type = MessageType.SUCCESS) }
        uiState.error?.let { MessageCard("Couldn't create test. Please try again.", type = MessageType.ERROR) }
    }
}

