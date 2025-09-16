package com.klaro.app.presentation.screens

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.clickable
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.platform.LocalContext
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import coil.compose.AsyncImage
import com.klaro.app.presentation.viewmodels.DoubtSolvingViewModel
import com.klaro.app.BuildConfig
import com.klaro.app.presentation.ui.design.*

/**
 * 🤔 Doubt Solver - Student-Focused Simplicity
 * 
 * Core Purpose: Help students get answers to questions quickly
 * - Clean question input
 * - Simple subject selection  
 * - Clear solution display
 * - Zero distractions
 */
@Composable
fun DoubtSolverScreen(
    navController: NavController,
    viewModel: DoubtSolvingViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val currentSolution by viewModel.currentSolution.collectAsStateWithLifecycle()

    // Basic auth presence check (token stored by AuthViewModel)
    val ctx = LocalContext.current
    val tokenProvider = remember(ctx) { com.klaro.app.security.DefaultTokenProvider(ctx) }
    val hasToken = remember { mutableStateOf(!tokenProvider.getToken().isNullOrBlank()) }

    // Refresh token presence when composable recomposes
    LaunchedEffect(uiState.isSolving) {
        hasToken.value = !tokenProvider.getToken().isNullOrBlank()
    }
    
    var doubtText by remember { mutableStateOf("") }
    var selectedSubject by remember { mutableStateOf("Mathematics") }
    
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
                    Icons.Filled.Psychology,
                    contentDescription = null,
                    tint = KlaroDesign.Colors.LearningBlue,
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge)
                )
                Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
                Column {
                    Text(
                        text = "Ask Question",
                        fontSize = KlaroDesign.Typography.Headline,
                        fontWeight = KlaroDesign.Typography.Bold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    Text(
                        text = "Get instant help with any topic",
                        fontSize = KlaroDesign.Typography.Body,
                        color = KlaroDesign.Colors.NeutralMedium
                    )
                }
            }
        }
        
        // Debug banner (shows active API URL and handwriting presence)
        if (BuildConfig.DEBUG) {
            CleanCard {
                Text(
                    text = "API: ${BuildConfig.BASE_API_URL}",
                    fontSize = KlaroDesign.Typography.Caption,
                    color = KlaroDesign.Colors.NeutralMedium
                )
                val hwImagesCount = currentSolution?.handwrittenImages?.size ?: 0
                val hasPdf = !(currentSolution?.handwrittenPdfUrl.isNullOrBlank())
                Text(
                    text = "HW images: $hwImagesCount | HW PDF: $hasPdf",
                    fontSize = KlaroDesign.Typography.Caption,
                    color = KlaroDesign.Colors.NeutralMedium
                )
            }
        }

        // Question Input
        CleanCard {
            Text(
                text = "What's your question?",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            
            OutlinedTextField(
                value = doubtText,
                onValueChange = { doubtText = it },
                placeholder = { Text("Type your question here...", fontSize = KlaroDesign.Typography.Body) },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(120.dp),
                maxLines = 4,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = KlaroDesign.Colors.LearningBlue,
                    unfocusedBorderColor = KlaroDesign.Colors.NeutralMedium.copy(alpha = 0.3f)
                )
            )
            
            // Subject chips - minimal
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Small)
            ) {
                listOf("Math", "Physics", "Chemistry", "Biology").forEach { subject ->
                    FilterChip(
                        onClick = { selectedSubject = subject },
                        label = { 
                            Text(
                                subject, 
                                fontSize = KlaroDesign.Typography.Caption
                            ) 
                        },
                        selected = selectedSubject.startsWith(subject)
                    )
                }
            }
        }
        
        // Auth reminder if not signed in
        if (!hasToken.value) {
            MessageCard(
                message = "Sign in required to solve doubts.",
                type = MessageType.INFO
            )
        }

        // Get Answer Button
        PrimaryActionButton(
            text = if (hasToken.value) "Get Answer" else "Sign in to solve",
            onClick = {
                if (doubtText.isNotBlank() && hasToken.value) {
                    viewModel.solveTextDoubt(doubtText, selectedSubject)
                }
            },
            enabled = doubtText.isNotBlank() && hasToken.value,
            isLoading = uiState.isSolving,
            icon = Icons.Filled.Psychology
        )
        
        // Solution Display
        currentSolution?.let { solution ->
            CleanCard {
                Text(
                    text = "Answer",
                    fontSize = KlaroDesign.Typography.Title,
                    fontWeight = KlaroDesign.Typography.Bold,
                    color = KlaroDesign.Colors.SuccessGreen
                )
                
                Text(
                    text = solution.answer,
                    fontSize = KlaroDesign.Typography.Body,
                    color = KlaroDesign.Colors.NeutralDark,
                    lineHeight = KlaroDesign.Typography.Body * 1.5
                )
                
                // Steps - Only if they exist and are useful
                if (solution.steps.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(KlaroDesign.Spacing.Medium))
                    Text(
                        text = "Solution Steps",
                        fontSize = KlaroDesign.Typography.Subtitle,
                        fontWeight = KlaroDesign.Typography.SemiBold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    
                    solution.steps.forEach { step ->
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(
                                containerColor = KlaroDesign.Colors.BackgroundLight
                            ),
                            elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
                        ) {
                            Column(
                                modifier = Modifier.padding(KlaroDesign.Spacing.Medium)
                            ) {
                                Text(
                                    text = "${step.stepNumber}. ${step.title}",
                                    fontSize = KlaroDesign.Typography.Body,
                                    fontWeight = KlaroDesign.Typography.Medium,
                                    color = KlaroDesign.Colors.NeutralDark
                                )
                                if (step.explanation.isNotEmpty()) {
                                    Text(
                                        text = step.explanation,
                                        fontSize = KlaroDesign.Typography.Body,
                                        color = KlaroDesign.Colors.NeutralMedium,
                                        modifier = Modifier.padding(top = KlaroDesign.Spacing.XSmall)
                                    )
                                }
                            }
                        }
                    }
                }

                // Handwritten images preview
                val images = solution.handwrittenImages
                if (!images.isNullOrEmpty()) {
                    Spacer(modifier = Modifier.height(KlaroDesign.Spacing.Medium))
                    Text(
                        text = "Handwritten Solution",
                        fontSize = KlaroDesign.Typography.Subtitle,
                        fontWeight = KlaroDesign.Typography.SemiBold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState()),
                        horizontalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium)
                    ) {
                        images.forEach { url ->
                            Card(
                                colors = CardDefaults.cardColors(containerColor = KlaroDesign.Colors.NeutralWhite),
                                elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
                            ) {
                                AsyncImage(
                                    model = url,
                                    contentDescription = "Handwritten solution",
                                    modifier = Modifier
                                        .size(width = 180.dp, height = 240.dp)
                                        .clickable {
                                            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                                            ctx.startActivity(intent)
                                        }
                                )
                            }
                        }
                    }
                }

                // Handwritten PDF button
                val pdfUrl = solution.handwrittenPdfUrl
                if (!pdfUrl.isNullOrBlank()) {
                    Spacer(modifier = Modifier.height(KlaroDesign.Spacing.Medium))
                    OutlinedButton(
                        onClick = {
                            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(pdfUrl))
                            ctx.startActivity(intent)
                        }
                    ) {
                        Icon(Icons.Filled.PictureAsPdf, contentDescription = null)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Open Handwritten PDF")
                    }
                }
            }
        }
        
        // Messages - Minimal feedback
        uiState.success?.let { message ->
            MessageCard(message = message, type = MessageType.SUCCESS)
        }
        
        uiState.error?.let { _ ->
            MessageCard(message = "Couldn't solve this question. Please try rephrasing or check your connection.", type = MessageType.ERROR)
        }
    }
}
