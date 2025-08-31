package com.klaro.app.presentation.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController

/**
 * 🏠 Home Screen
 * 
 * Main dashboard with quick access to all 3 core features:
 * - PDF Quiz Generator
 * - JEE Online Tests
 * - Doubt Solving
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(navController: NavController) {
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        
        // Welcome Header
        item {
            WelcomeHeader()
        }
        
        // Quick Stats Card
        item {
            QuickStatsCard()
        }
        
        // Core Features
        item {
            Text(
                text = "🎯 Core Features",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(vertical = 8.dp)
            )
        }
        
        items(coreFeatures) { feature ->
            FeatureCard(
                feature = feature,
                onClick = {
                    navController.navigate(feature.route)
                }
            )
        }
        
        // Recent Activity
        item {
            RecentActivityCard()
        }
    }
}

@Composable
fun WelcomeHeader() {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
    ) {
        Box(
            modifier = Modifier
                .background(
                    Brush.horizontalGradient(
                        colors = listOf(
                            MaterialTheme.colorScheme.primary,
                            MaterialTheme.colorScheme.secondary
                        )
                    )
                )
                .padding(24.dp)
        ) {
            Column {
                Text(
                    text = "🎓 Welcome to Klaro!",
                    style = MaterialTheme.typography.headlineMedium,
                    color = Color.White,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Your AI-powered educational companion",
                    style = MaterialTheme.typography.bodyLarge,
                    color = Color.White.copy(alpha = 0.9f)
                )
            }
        }
    }
}

@Composable
fun QuickStatsCard() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "📊 Your Progress",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(12.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                StatItem("Quizzes Created", "12")
                StatItem("Tests Taken", "8")
                StatItem("Doubts Solved", "25")
            }
        }
    }
}

@Composable
fun StatItem(label: String, value: String) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = value,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
fun FeatureCard(
    feature: CoreFeature,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .padding(20.dp)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            
            // Feature Icon
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(feature.color.copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = feature.icon,
                    contentDescription = feature.title,
                    tint = feature.color,
                    modifier = Modifier.size(32.dp)
                )
            }
            
            // Feature Info
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = feature.title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = feature.description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = feature.status,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
            
            // Arrow Icon
            Icon(
                imageVector = Icons.Filled.ChevronRight,
                contentDescription = "Go to ${feature.title}",
                tint = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun RecentActivityCard() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "📈 Recent Activity",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(12.dp))
            
            recentActivities.forEach { activity ->
                ActivityItem(activity)
                if (activity != recentActivities.last()) {
                    Divider(modifier = Modifier.padding(vertical = 8.dp))
                }
            }
        }
    }
}

@Composable
fun ActivityItem(activity: RecentActivity) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = activity.icon,
            contentDescription = activity.action,
            tint = activity.color,
            modifier = Modifier.size(20.dp)
        )
        
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = activity.action,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = activity.details,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        Text(
            text = activity.time,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

// ================================================================================
// 📋 Data Classes
// ================================================================================

data class CoreFeature(
    val title: String,
    val description: String,
    val status: String,
    val icon: ImageVector,
    val color: Color,
    val route: String
)

data class RecentActivity(
    val action: String,
    val details: String,
    val time: String,
    val icon: ImageVector,
    val color: Color
)

// ================================================================================
// 🎯 Static Data
// ================================================================================

val coreFeatures = listOf(
    CoreFeature(
        title = "📄 PDF Quiz Generator",
        description = "Create custom practice tests and download as PDF",
        status = "Ready • Generate unlimited quizzes",
        icon = Icons.Filled.Assignment,
        color = Color(0xFF4CAF50),
        route = Screen.PdfGenerator.route
    ),
    CoreFeature(
        title = "🎯 JEE Online Tests",
        description = "Take customizable JEE Main mock tests with real-time scoring",
        status = "Ready • Exact JEE 2024 format",
        icon = Icons.Filled.Quiz,
        color = Color(0xFF2196F3),
        route = Screen.JeeTest.route
    ),
    CoreFeature(
        title = "🤔 AI Doubt Solver",
        description = "Get step-by-step solutions with camera OCR support",
        status = "Ready • Text & Image support",
        icon = Icons.Filled.QuestionAnswer,
        color = Color(0xFFFF9800),
        route = Screen.DoubtSolver.route
    )
)

val recentActivities = listOf(
    RecentActivity(
        action = "Created PDF Quiz",
        details = "Algebra Practice - 15 questions",
        time = "2 hours ago",
        icon = Icons.Filled.Assignment,
        color = Color(0xFF4CAF50)
    ),
    RecentActivity(
        action = "Completed JEE Test",
        details = "Mathematics Mock - Score: 85%",
        time = "1 day ago",
        icon = Icons.Filled.Quiz,
        color = Color(0xFF2196F3)
    ),
    RecentActivity(
        action = "Solved Doubt",
        details = "Integration by parts method",
        time = "2 days ago",
        icon = Icons.Filled.QuestionAnswer,
        color = Color(0xFFFF9800)
    )
)
