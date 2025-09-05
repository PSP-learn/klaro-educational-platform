package com.klaro.app.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.klaro.app.presentation.ui.design.*

/**
 * 🏠 Home Screen - World-Class Minimal Design
 * 
 * Design Philosophy: "First Impression = Everything"
 * - Instant clarity on what the app does
 * - Zero cognitive load
 * - Immediate access to core learning actions
 */

@Composable
fun HomeScreen(navController: NavController) {
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(KlaroDesign.Spacing.ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.SectionGap)
    ) {
        
        // Hero Welcome - Confident but not overwhelming
        item {
            CleanCard {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "Klaro",
                        fontSize = KlaroDesign.Typography.Hero,
                        fontWeight = KlaroDesign.Typography.Bold,
                        color = KlaroDesign.Colors.LearningBlue
                    )
                    Spacer(modifier = Modifier.height(KlaroDesign.Spacing.Small))
                    Text(
                        text = "Your study companion",
                        fontSize = KlaroDesign.Typography.Body,
                        fontWeight = KlaroDesign.Typography.Regular,
                        color = KlaroDesign.Colors.NeutralMedium
                    )
                }
            }
        }
        
        // Core Learning Actions - Perfect hierarchy
        items(learningActions) { action ->
            LearningActionCard(
                action = action,
                onClick = { navController.navigate(action.route) }
            )
        }
    }
}

@Composable
fun LearningActionCard(
    action: LearningAction,
    onClick: () -> Unit
) {
    CleanCard(
        modifier = Modifier.fillMaxWidth()
    ) {
        
        // Action performed through card click
        Card(
            onClick = onClick,
            colors = CardDefaults.cardColors(
                containerColor = action.color.copy(alpha = 0.05f)
            ),
            elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
        ) {
            Row(
                modifier = Modifier
                    .padding(KlaroDesign.Spacing.Large)
                    .fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                
                // Action Icon - Purposeful color coding
                Icon(
                    imageVector = action.icon,
                    contentDescription = null,
                    tint = action.color,
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge)
                )
                
                Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
                
                // Action Content - Clear hierarchy
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = action.title,
                        fontSize = KlaroDesign.Typography.Title,
                        fontWeight = KlaroDesign.Typography.SemiBold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    Spacer(modifier = Modifier.height(KlaroDesign.Spacing.XSmall))
                    Text(
                        text = action.description,
                        fontSize = KlaroDesign.Typography.Body,
                        fontWeight = KlaroDesign.Typography.Regular,
                        color = KlaroDesign.Colors.NeutralMedium
                    )
                }
                
                // Subtle visual cue
                Icon(
                    imageVector = Icons.Filled.ChevronRight,
                    contentDescription = null,
                    tint = KlaroDesign.Colors.NeutralMedium.copy(alpha = 0.6f),
                    modifier = Modifier.size(KlaroDesign.Components.IconMedium)
                )
            }
        }
    }
}

// ============================================================================
// 📋 LEARNING ACTIONS - Core Features Only
// ============================================================================

data class LearningAction(
    val title: String,
    val description: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val color: androidx.compose.ui.graphics.Color,
    val route: String
)

// Purposeful feature set - no feature bloat
val learningActions = listOf(
    LearningAction(
        title = "Generate Quiz",
        description = "Create personalized practice tests",
        icon = Icons.Filled.Quiz,
        color = KlaroDesign.Colors.LearningBlue,
        route = "pdf_generator"
    ),
    LearningAction(
        title = "Practice Tests",
        description = "JEE Main exam preparation",
        icon = Icons.Filled.School,
        color = KlaroDesign.Colors.GrowthGreen,
        route = "jee_test"
    ),
    LearningAction(
        title = "Solve Doubts",
        description = "Get instant step-by-step solutions",
        icon = Icons.Filled.Psychology,
        color = KlaroDesign.Colors.FocusAmber,
        route = "doubt_solver"
    )
)
