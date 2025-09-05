package com.klaro.app.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Topic
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
fun TopicPracticeScreen(
    navController: NavController,
    viewModel: JeeTestViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var selectedSubject by remember { mutableStateOf("Mathematics") }
    var selectedTopics by remember { mutableStateOf(setOf<String>()) }

    val topicsBySubject = mapOf(
        "Mathematics" to listOf("Algebra", "Calculus", "Trigonometry", "Geometry"),
        "Physics" to listOf("Mechanics", "Optics", "Electricity", "Thermodynamics"),
        "Chemistry" to listOf("Organic", "Inorganic", "Physical")
    )

    val topics = topicsBySubject[selectedSubject] ?: emptyList()

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
                    Icons.Filled.Topic,
                    contentDescription = null,
                    tint = KlaroDesign.Colors.LearningBlue,
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge)
                )
                Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
                Column {
                    Text(
                        text = "Topic Practice",
                        fontSize = KlaroDesign.Typography.Headline,
                        fontWeight = KlaroDesign.Typography.Bold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    Text(
                        text = "Pick a subject and topics",
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
                        onClick = {
                            selectedSubject = subject
                            selectedTopics = emptySet()
                        },
                        label = { Text(subject) }
                    )
                }
            }
        }

        // Topic chips
        CleanCard {
            Text(
                text = "Topics",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            Row(horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Small)) {
                topics.forEach { topic ->
                    FilterChip(
                        selected = selectedTopics.contains(topic),
                        onClick = {
                            selectedTopics = if (selectedTopics.contains(topic)) selectedTopics - topic else selectedTopics + topic
                        },
                        label = { Text(topic) }
                    )
                }
            }
        }

        PrimaryActionButton(
            text = "Start Topic Practice",
            onClick = { if (selectedTopics.isNotEmpty()) viewModel.startTopicTest(selectedTopics.toList(), selectedSubject) },
            isLoading = uiState.isCreatingTest,
            enabled = selectedTopics.isNotEmpty()
        )

        uiState.success?.let { MessageCard(it, type = MessageType.SUCCESS) }
        uiState.error?.let { MessageCard("Couldn't create topic test. Please try again.", type = MessageType.ERROR) }
    }
}

