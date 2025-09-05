package com.klaro.app.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
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
import com.klaro.app.presentation.Screen
import com.klaro.app.presentation.viewmodels.JeeTestViewModel
import com.klaro.app.presentation.ui.design.*
import com.klaro.app.presentation.ui.design.*
import com.klaro.app.presentation.ui.design.*

/**
 * 🎯 JEE Tests - Student-Focused Practice
 * 
 * Core Purpose: Help students practice JEE questions effectively
 * - Clear test options
 * - Simple selection process
 * - No analytics or complex tracking
 * - Focus on learning
 */
@Composable
fun JeeTestScreen(
    navController: NavController,
    viewModel: JeeTestViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(KlaroDesign.Spacing.ScreenPadding)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.SectionGap)
    ) {
        
        // Simple Header
        CleanCard {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    Icons.Filled.School,
                    contentDescription = null,
                    tint = KlaroDesign.Colors.LearningBlue,
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge)
                )
                Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
                Column {
                    Text(
                        text = "JEE Practice",
                        fontSize = KlaroDesign.Typography.Headline,
                        fontWeight = KlaroDesign.Typography.Bold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    Text(
                        text = "Master JEE with focused practice",
                        fontSize = KlaroDesign.Typography.Body,
                        color = KlaroDesign.Colors.NeutralMedium
                    )
                }
            }
        }
        
        // Test Options - Simple and focused
        SimpleTestCard(
            title = "Full Mock Test",
            subtitle = "Complete JEE simulation",
            duration = "3 hours • 75 questions",
            icon = Icons.Filled.Timer,
            enabled = !uiState.isCreatingTest,
            isLoading = uiState.isCreatingTest,
            onClick = { viewModel.startFullMockTest() }
        )
        
        SimpleTestCard(
            title = "Subject Practice",
            subtitle = "Focus on Math, Physics, or Chemistry",
            duration = "Choose your subject",
            icon = Icons.Filled.Book,
            onClick = { navController.navigate(Screen.JeeSubjectPractice.route) }
        )
        
        SimpleTestCard(
            title = "Topic Practice",
            subtitle = "Master specific topics",
            duration = "Targeted learning",
            icon = Icons.Filled.Topic,
            onClick = { navController.navigate(Screen.JeeTopicPractice.route) }
        )
        
        SimpleTestCard(
            title = "Previous Papers",
            subtitle = "Solve past JEE questions",
            duration = "2019-2024 papers",
            icon = Icons.Filled.History,
            onClick = { navController.navigate(Screen.JeePreviousPapers.route) }
        )
        
        // Messages - Minimal feedback
        uiState.success?.let { message ->
            MessageCard(message = message, type = MessageType.SUCCESS)
        }
        
        uiState.error?.let { _ ->
            MessageCard(message = "Couldn't start the test. Please try again.", type = MessageType.ERROR)
        }
    }
}

/**
 * Simple Test Card - Clean and actionable
 */
@Composable
fun SimpleTestCard(
    title: String,
    subtitle: String,
    duration: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    enabled: Boolean = true,
    isLoading: Boolean = false,
    onClick: () -> Unit
) {
    CleanCard(
        onClick = if (enabled) onClick else null
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            
            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge),
                    color = KlaroDesign.Colors.LearningBlue
                )
            } else {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = if (enabled) KlaroDesign.Colors.LearningBlue 
                          else KlaroDesign.Colors.NeutralMedium,
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge)
                )
            }
            
            Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    fontSize = KlaroDesign.Typography.Title,
                    fontWeight = KlaroDesign.Typography.SemiBold,
                    color = if (enabled) KlaroDesign.Colors.NeutralDark
                           else KlaroDesign.Colors.NeutralMedium
                )
                Text(
                    text = subtitle,
                    fontSize = KlaroDesign.Typography.Body,
                    color = KlaroDesign.Colors.NeutralMedium
                )
                Text(
                    text = duration,
                    fontSize = KlaroDesign.Typography.Caption,
                    color = KlaroDesign.Colors.NeutralMedium
                )
            }
            
            if (enabled && !isLoading) {
                Icon(
                    imageVector = Icons.Filled.ChevronRight,
                    contentDescription = null,
                    tint = KlaroDesign.Colors.NeutralMedium,
                    modifier = Modifier.size(KlaroDesign.Components.IconMedium)
                )
            }
        }
    }
}
