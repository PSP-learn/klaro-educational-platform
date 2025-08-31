package com.klaro.app.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController

/**
 * 👤 Profile Screen
 * 
 * User profile, subscription management, and app settings
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(navController: NavController) {
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        
        // Profile Header
        item {
            ProfileHeaderCard()
        }
        
        // Subscription Status
        item {
            SubscriptionCard()
        }
        
        // Statistics
        item {
            UserStatsCard()
        }
        
        // Settings
        item {
            SettingsSection()
        }
        
        // Support & Info
        item {
            SupportSection()
        }
    }
}

@Composable
fun ProfileHeaderCard() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        )
    ) {
        Column(
            modifier = Modifier.padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            
            // Profile Avatar
            Card(
                shape = CircleShape,
                modifier = Modifier.size(80.dp),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primary
                )
            ) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier.fillMaxSize()
                ) {
                    Icon(
                        imageVector = Icons.Filled.Person,
                        contentDescription = "Profile",
                        tint = Color.White,
                        modifier = Modifier.size(40.dp)
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = "Sushant Nandwana",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
            
            Text(
                text = "sushant@example.com",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f)
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            AssistChip(
                onClick = { /* TODO: Edit profile */ },
                label = { Text("Edit Profile") },
                leadingIcon = { Icon(Icons.Filled.Edit, contentDescription = null) }
            )
        }
    }
}

@Composable
fun SubscriptionCard() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "💎 Subscription Plan",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "Basic Plan",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
                
                Button(
                    onClick = { /* TODO: Upgrade to premium */ },
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("Upgrade")
                }
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            // Plan Features
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                PlanFeature("📝 20 doubts per month", true)
                PlanFeature("🤖 GPT-3.5 solutions", true)
                PlanFeature("📸 OCR support", true)
                PlanFeature("🧠 GPT-4 solutions", false)
                PlanFeature("📊 Advanced analytics", false)
                PlanFeature("⚡ Priority support", false)
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            LinearProgressIndicator(
                progress = 0.9f, // 18/20 doubts used
                modifier = Modifier.fillMaxWidth(),
                color = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.height(4.dp))
            
            Text(
                text = "18/20 doubts used this month",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun PlanFeature(feature: String, isIncluded: Boolean) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Icon(
            imageVector = if (isIncluded) Icons.Filled.CheckCircle else Icons.Filled.Cancel,
            contentDescription = if (isIncluded) "Included" else "Not included",
            tint = if (isIncluded) Color(0xFF4CAF50) else Color(0xFF9E9E9E),
            modifier = Modifier.size(16.dp)
        )
        Text(
            text = feature,
            style = MaterialTheme.typography.bodyMedium,
            color = if (isIncluded) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun UserStatsCard() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📊 Your Statistics",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                UserStatItem("Study Streak", "7 days", "🔥")
                UserStatItem("Total Score", "78.5%", "📈")
                UserStatItem("Best Rank", "AIR 2,847", "🏆")
                UserStatItem("Hours Studied", "45.2h", "⏰")
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Achievements
            Text(
                text = "🏅 Recent Achievements",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            achievements.forEach { achievement ->
                AchievementItem(achievement)
                if (achievement != achievements.last()) {
                    Spacer(modifier = Modifier.height(4.dp))
                }
            }
        }
    }
}

@Composable
fun UserStatItem(label: String, value: String, emoji: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = emoji,
            style = MaterialTheme.typography.headlineMedium
        )
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = value,
            style = MaterialTheme.typography.titleMedium,
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
fun AchievementItem(achievement: Achievement) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = achievement.emoji,
            style = MaterialTheme.typography.titleMedium
        )
        Text(
            text = achievement.name,
            style = MaterialTheme.typography.bodyMedium,
            modifier = Modifier.weight(1f)
        )
        Text(
            text = achievement.earnedDate,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun SettingsSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "⚙️ Settings",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            settingsItems.forEach { setting ->
                SettingItem(setting)
                if (setting != settingsItems.last()) {
                    Divider(modifier = Modifier.padding(vertical = 8.dp))
                }
            }
        }
    }
}

@Composable
fun SettingItem(setting: SettingItem) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* TODO: Handle setting click */ },
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = setting.icon,
            contentDescription = setting.title,
            tint = MaterialTheme.colorScheme.primary
        )
        
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = setting.title,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
            if (setting.subtitle.isNotBlank()) {
                Text(
                    text = setting.subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        
        if (setting.hasToggle) {
            Switch(
                checked = setting.isEnabled,
                onCheckedChange = { /* TODO: Handle toggle */ }
            )
        } else {
            Icon(
                imageVector = Icons.Filled.ChevronRight,
                contentDescription = "Open",
                tint = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun SupportSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "🤝 Support & Info",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            supportItems.forEach { item ->
                SupportItem(item)
                if (item != supportItems.last()) {
                    Divider(modifier = Modifier.padding(vertical = 8.dp))
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // App Version
            Text(
                text = "🎓 Klaro v1.0.0",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

@Composable
fun SupportItem(item: SupportItem) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* TODO: Handle support item click */ },
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = item.icon,
            contentDescription = item.title,
            tint = MaterialTheme.colorScheme.primary
        )
        
        Text(
            text = item.title,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Medium,
            modifier = Modifier.weight(1f)
        )
        
        Icon(
            imageVector = Icons.Filled.ChevronRight,
            contentDescription = "Open",
            tint = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

// ================================================================================
// 📋 Data Classes & Static Data
// ================================================================================

data class Achievement(
    val name: String,
    val emoji: String,
    val earnedDate: String
)

data class SettingItem(
    val title: String,
    val subtitle: String = "",
    val icon: ImageVector,
    val hasToggle: Boolean = false,
    val isEnabled: Boolean = false
)

data class SupportItem(
    val title: String,
    val icon: ImageVector
)

val achievements = listOf(
    Achievement("First Quiz Created", "🎉", "Aug 28"),
    Achievement("JEE Mock Completed", "🎯", "Aug 29"),
    Achievement("Week Streak", "🔥", "Aug 30"),
    Achievement("Problem Solver", "🤔", "Aug 31")
)

val settingsItems = listOf(
    SettingItem(
        title = "Notifications",
        subtitle = "Daily reminders and updates",
        icon = Icons.Filled.Notifications,
        hasToggle = true,
        isEnabled = true
    ),
    SettingItem(
        title = "Dark Theme",
        subtitle = "Switch between light and dark mode",
        icon = Icons.Filled.DarkMode,
        hasToggle = true,
        isEnabled = false
    ),
    SettingItem(
        title = "Language",
        subtitle = "English",
        icon = Icons.Filled.Language
    ),
    SettingItem(
        title = "Download Quality",
        subtitle = "High quality PDFs",
        icon = Icons.Filled.HighQuality
    ),
    SettingItem(
        title = "Auto-sync",
        subtitle = "Sync progress across devices",
        icon = Icons.Filled.Sync,
        hasToggle = true,
        isEnabled = true
    )
)

val supportItems = listOf(
    SupportItem("Help Center", Icons.Filled.Help),
    SupportItem("Contact Support", Icons.Filled.Support),
    SupportItem("Privacy Policy", Icons.Filled.Policy),
    SupportItem("Terms of Service", Icons.Filled.Description),
    SupportItem("Rate App", Icons.Filled.Star),
    SupportItem("Share with Friends", Icons.Filled.Share)
)
