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
import androidx.navigation.NavController
import com.klaro.app.presentation.ui.design.*

/**
 * 👤 Profile - Student-Focused Simplicity
 * 
 * Core Purpose: Basic profile info and essential settings
 * - Student information
 * - Learning progress (simple)
 * - Essential settings only
 * - No billing, API usage, or complex analytics
 */
@Composable
fun ProfileScreen(navController: NavController) {
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(KlaroDesign.Spacing.ScreenPadding)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.SectionGap)
    ) {
        
        // Profile Header
        CleanCard {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    Icons.Filled.Person,
                    contentDescription = null,
                    tint = KlaroDesign.Colors.LearningBlue,
                    modifier = Modifier.size(KlaroDesign.Components.IconLarge)
                )
                Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
                Column {
                    Text(
                        text = "Your Profile",
                        fontSize = KlaroDesign.Typography.Headline,
                        fontWeight = KlaroDesign.Typography.Bold,
                        color = KlaroDesign.Colors.NeutralDark
                    )
                    Text(
                        text = "Track your learning journey",
                        fontSize = KlaroDesign.Typography.Body,
                        color = KlaroDesign.Colors.NeutralMedium
                    )
                }
            }
        }
        
        // Student Info - Essential only
        CleanCard {
            Text(
                text = "Student Information",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            
            SimpleProfileItem(
                icon = Icons.Filled.Person,
                label = "Name",
                value = "Student"
            )
            
            SimpleProfileItem(
                icon = Icons.Filled.School,
                label = "Class",
                value = "Class 12"
            )
            
            SimpleProfileItem(
                icon = Icons.Filled.Book,
                label = "Stream",
                value = "Science"
            )
        }
        
        // Simple Progress - No complex analytics
        CleanCard {
            Text(
                text = "Learning Progress",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                MinimalStatCard("Quizzes", "5")
                MinimalStatCard("Tests", "3")
                MinimalStatCard("Questions", "12")
            }
        }
        
        // Essential Settings Only
        CleanCard {
            Text(
                text = "Settings",
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.SemiBold,
                color = KlaroDesign.Colors.NeutralDark
            )
            
            SimpleSettingItem(
                icon = Icons.Filled.Notifications,
                title = "Notifications",
                subtitle = "Study reminders"
            )
            
            SimpleSettingItem(
                icon = Icons.Filled.Help,
                title = "Help & Support",
                subtitle = "Get assistance"
            )
            
            SimpleSettingItem(
                icon = Icons.Filled.Info,
                title = "About",
                subtitle = "App information"
            )
        }
    }
}

@Composable
fun SimpleProfileItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    label: String,
    value: String
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = KlaroDesign.Colors.LearningBlue,
            modifier = Modifier.size(KlaroDesign.Components.IconMedium)
        )
        Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = label,
                fontSize = KlaroDesign.Typography.Caption,
                color = KlaroDesign.Colors.NeutralMedium
            )
            Text(
                text = value,
                fontSize = KlaroDesign.Typography.Body,
                fontWeight = KlaroDesign.Typography.Medium,
                color = KlaroDesign.Colors.NeutralDark
            )
        }
    }
}

@Composable
fun MinimalStatCard(label: String, value: String) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = KlaroDesign.Colors.BackgroundLight
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column(
            modifier = Modifier.padding(KlaroDesign.Spacing.Medium),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = value,
                fontSize = KlaroDesign.Typography.Title,
                fontWeight = KlaroDesign.Typography.Bold,
                color = KlaroDesign.Colors.LearningBlue
            )
            Text(
                text = label,
                fontSize = KlaroDesign.Typography.Caption,
                color = KlaroDesign.Colors.NeutralMedium
            )
        }
    }
}

@Composable
fun SimpleSettingItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    title: String,
    subtitle: String
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = KlaroDesign.Colors.NeutralMedium,
            modifier = Modifier.size(KlaroDesign.Components.IconMedium)
        )
        Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Medium))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = title,
                fontSize = KlaroDesign.Typography.Body,
                fontWeight = KlaroDesign.Typography.Medium,
                color = KlaroDesign.Colors.NeutralDark
            )
            Text(
                text = subtitle,
                fontSize = KlaroDesign.Typography.Caption,
                color = KlaroDesign.Colors.NeutralMedium
            )
        }
        Icon(
            imageVector = Icons.Filled.ChevronRight,
            contentDescription = null,
            tint = KlaroDesign.Colors.NeutralMedium,
            modifier = Modifier.size(KlaroDesign.Components.IconSmall)
        )
    }
}
