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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController

/**
 * 🤔 Doubt Solver Screen
 * 
 * AI-powered doubt solving with text input and camera OCR
 * Uses existing backend: doubt_solving_engine_production.py
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DoubtSolverScreen(navController: NavController) {
    
    var selectedTab by remember { mutableStateOf(0) }
    val tabs = listOf("📝 Ask Doubt", "🤖 Solutions", "📊 Usage")
    
    Column(modifier = Modifier.fillMaxSize()) {
        
        // Header Card
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.tertiaryContainer
            )
        ) {
            Column(modifier = Modifier.padding(20.dp)) {
                Text(
                    text = "🤔 AI Doubt Solver",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onTertiaryContainer
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Get step-by-step solutions • Text & Image support",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onTertiaryContainer.copy(alpha = 0.8f)
                )
            }
        }
        
        // Tab Row
        TabRow(
            selectedTabIndex = selectedTab,
            modifier = Modifier.padding(horizontal = 16.dp)
        ) {
            tabs.forEachIndexed { index, title ->
                Tab(
                    selected = selectedTab == index,
                    onClick = { selectedTab = index },
                    text = { Text(title) }
                )
            }
        }
        
        // Tab Content
        when (selectedTab) {
            0 -> AskDoubtTab()
            1 -> SolutionsTab()
            2 -> UsageTab()
        }
    }
}

@Composable
fun AskDoubtTab() {
    var doubtText by remember { mutableStateOf("") }
    var selectedSubject by remember { mutableStateOf("Mathematics") }
    var isLoading by remember { mutableStateOf(false) }
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        
        // Quick Input Methods
        item {
            InputMethodsSection()
        }
        
        // Text Input Section
        item {
            Card(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "📝 Type Your Question",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    OutlinedTextField(
                        value = doubtText,
                        onValueChange = { doubtText = it },
                        label = { Text("Ask your doubt here...") },
                        placeholder = { Text("e.g., Solve x² + 5x + 6 = 0") },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(120.dp),
                        maxLines = 4
                    )
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    // Subject Selection
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Text(
                            text = "Subject:",
                            style = MaterialTheme.typography.bodyMedium,
                            modifier = Modifier.align(Alignment.CenterVertically)
                        )
                        
                        doubtSubjects.forEach { subject ->
                            FilterChip(
                                onClick = { selectedSubject = subject },
                                label = { Text(subject) },
                                selected = selectedSubject == subject
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Submit Button
                    Button(
                        onClick = {
                            if (doubtText.isNotBlank()) {
                                isLoading = true
                                // TODO: Submit doubt to API
                            }
                        },
                        enabled = doubtText.isNotBlank() && !isLoading,
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(48.dp)
                    ) {
                        if (isLoading) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(20.dp),
                                color = Color.White
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Solving...")
                        } else {
                            Icon(Icons.Filled.Send, contentDescription = null)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("🤖 Solve My Doubt")
                        }
                    }
                }
            }
        }
        
        // Recent Doubts
        item {
            RecentDoubtsSection()
        }
    }
}

@Composable
fun InputMethodsSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "🎯 How to Ask",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                
                // Camera Capture
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .clickable { /* TODO: Open camera */ },
                    colors = CardDefaults.cardColors(
                        containerColor = Color(0xFF4CAF50).copy(alpha = 0.1f)
                    )
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Icon(
                            imageVector = Icons.Filled.CameraAlt,
                            contentDescription = "Camera",
                            tint = Color(0xFF4CAF50),
                            modifier = Modifier.size(32.dp)
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "📸 Camera",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.Bold,
                            textAlign = TextAlign.Center
                        )
                        Text(
                            text = "Photo OCR",
                            style = MaterialTheme.typography.bodySmall,
                            textAlign = TextAlign.Center
                        )
                    }
                }
                
                // Voice Input (Future)
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .clickable { /* TODO: Voice input */ },
                    colors = CardDefaults.cardColors(
                        containerColor = Color(0xFF2196F3).copy(alpha = 0.1f)
                    )
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Icon(
                            imageVector = Icons.Filled.Mic,
                            contentDescription = "Voice",
                            tint = Color(0xFF2196F3),
                            modifier = Modifier.size(32.dp)
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "🎤 Voice",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.Bold,
                            textAlign = TextAlign.Center
                        )
                        Text(
                            text = "Coming Soon",
                            style = MaterialTheme.typography.bodySmall,
                            textAlign = TextAlign.Center
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun RecentDoubtsSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📚 Recent Doubts",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            recentDoubts.forEach { doubt ->
                RecentDoubtItem(doubt)
                if (doubt != recentDoubts.last()) {
                    Divider(modifier = Modifier.padding(vertical = 8.dp))
                }
            }
        }
    }
}

@Composable
fun RecentDoubtItem(doubt: RecentDoubt) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* TODO: View solution */ },
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = if (doubt.hasImage) Icons.Filled.Image else Icons.Filled.TextSnippet,
            contentDescription = "Doubt type",
            tint = MaterialTheme.colorScheme.primary
        )
        
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = doubt.question,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium,
                maxLines = 2
            )
            Text(
                text = "${doubt.subject} • ${doubt.method} • ${doubt.confidence}% confidence",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        Column(horizontalAlignment = Alignment.End) {
            Text(
                text = doubt.solvedAt,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            if (doubt.cost > 0) {
                Text(
                    text = "₹${String.format("%.3f", doubt.cost)}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}

@Composable
fun SolutionsTab() {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        
        // Sample solution display
        item {
            SolutionDisplayCard()
        }
        
        // Saved Solutions
        item {
            SavedSolutionsSection()
        }
    }
}

@Composable
fun SolutionDisplayCard() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "🤖 Latest Solution",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            // Question
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                )
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(
                        text = "❓ Question:",
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "Solve the quadratic equation: x² + 5x + 6 = 0",
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            // Answer
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(
                        text = "✅ Answer:",
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    Text(
                        text = "x = -2 or x = -3",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            // Solution Steps
            Text(
                text = "📋 Solution Steps:",
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold
            )
            
            sampleSteps.forEachIndexed { index, step ->
                Spacer(modifier = Modifier.height(8.dp))
                SolutionStepCard(index + 1, step)
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Action Buttons
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedButton(
                    onClick = { /* TODO: Save solution */ },
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Filled.Bookmark, contentDescription = null)
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("Save")
                }
                
                Button(
                    onClick = { /* TODO: Share solution */ },
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Filled.Share, contentDescription = null)
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("Share")
                }
            }
        }
    }
}

@Composable
fun SolutionStepCard(stepNumber: Int, step: SolutionStepData) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
        )
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(
                text = "Step $stepNumber: ${step.title}",
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = step.explanation,
                style = MaterialTheme.typography.bodyMedium
            )
            if (step.calculation.isNotBlank()) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = step.calculation,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Medium,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}

@Composable
fun SavedSolutionsSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "💾 Saved Solutions",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            if (savedSolutions.isEmpty()) {
                Text(
                    text = "No saved solutions yet. Start solving doubts to save your favorites!",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.fillMaxWidth()
                )
            } else {
                savedSolutions.forEach { solution ->
                    SavedSolutionItem(solution)
                    if (solution != savedSolutions.last()) {
                        Divider(modifier = Modifier.padding(vertical = 8.dp))
                    }
                }
            }
        }
    }
}

@Composable
fun SavedSolutionItem(solution: SavedSolution) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* TODO: Open saved solution */ },
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = Icons.Filled.BookmarkAdded,
            contentDescription = "Saved",
            tint = MaterialTheme.colorScheme.primary
        )
        
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = solution.title,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium,
                maxLines = 1
            )
            Text(
                text = "${solution.subject} • ${solution.savedDate}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        IconButton(onClick = { /* TODO: Remove from saved */ }) {
            Icon(Icons.Filled.Remove, contentDescription = "Remove")
        }
    }
}

@Composable
fun UsageTab() {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        
        // Usage Overview
        item {
            UsageOverviewCard()
        }
        
        // Monthly Usage
        item {
            MonthlyUsageCard()
        }
        
        // Cost Breakdown
        item {
            CostBreakdownCard()
        }
    }
}

@Composable
fun UsageOverviewCard() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📊 Usage Overview",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                UsageMetric("This Month", "18/20")
                UsageMetric("Success Rate", "94%")
                UsageMetric("Avg. Time", "12s")
                UsageMetric("Cost Saved", "₹24.50")
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Plan Status
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.secondaryContainer
                )
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            text = "💎 Current Plan: Basic",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "2 doubts remaining this month",
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                    
                    Button(
                        onClick = { /* TODO: Upgrade plan */ },
                        size = ButtonDefaults.SmallButtonSize
                    ) {
                        Text("Upgrade")
                    }
                }
            }
        }
    }
}

@Composable
fun UsageMetric(label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
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
fun MonthlyUsageCard() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📈 Monthly Breakdown",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            monthlyUsage.forEach { usage ->
                MonthlyUsageItem(usage)
                if (usage != monthlyUsage.last()) {
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }
        }
    }
}

@Composable
fun MonthlyUsageItem(usage: MonthlyUsageData) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column {
            Text(
                text = usage.method,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = "${usage.count} uses",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        Text(
            text = "₹${String.format("%.3f", usage.cost)}",
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Medium,
            color = MaterialTheme.colorScheme.primary
        )
    }
}

@Composable
fun CostBreakdownCard() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "💰 Cost Efficiency",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            Text(
                text = "Our AI engine automatically chooses the most cost-effective method:",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            costMethods.forEach { method ->
                CostMethodItem(method)
                if (method != costMethods.last()) {
                    Spacer(modifier = Modifier.height(4.dp))
                }
            }
        }
    }
}

@Composable
fun CostMethodItem(method: CostMethod) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = "${method.icon} ${method.name}",
            style = MaterialTheme.typography.bodyMedium
        )
        Text(
            text = method.cost,
            style = MaterialTheme.typography.bodyMedium,
            color = method.color
        )
    }
}

// ================================================================================
// 📋 Data Classes & Static Data
// ================================================================================

data class RecentDoubt(
    val question: String,
    val subject: String,
    val method: String,
    val confidence: Int,
    val solvedAt: String,
    val hasImage: Boolean,
    val cost: Double
)

data class SolutionStepData(
    val title: String,
    val explanation: String,
    val calculation: String = ""
)

data class SavedSolution(
    val title: String,
    val subject: String,
    val savedDate: String
)

data class MonthlyUsageData(
    val method: String,
    val count: Int,
    val cost: Double
)

data class CostMethod(
    val name: String,
    val cost: String,
    val icon: String,
    val color: Color
)

val doubtSubjects = listOf("Mathematics", "Physics", "Chemistry", "Biology")

val recentDoubts = listOf(
    RecentDoubt(
        question = "Solve x² + 5x + 6 = 0",
        subject = "Mathematics",
        method = "Wolfram",
        confidence = 98,
        solvedAt = "2 hours ago",
        hasImage = false,
        cost = 0.0025
    ),
    RecentDoubt(
        question = "Find derivative of sin(x²)",
        subject = "Mathematics", 
        method = "GPT-3.5",
        confidence = 92,
        solvedAt = "1 day ago",
        hasImage = true,
        cost = 0.004
    )
)

val sampleSteps = listOf(
    SolutionStepData(
        title = "Identify the quadratic equation",
        explanation = "This is in the standard form ax² + bx + c = 0",
        calculation = "a = 1, b = 5, c = 6"
    ),
    SolutionStepData(
        title = "Apply factoring method",
        explanation = "Look for two numbers that multiply to 6 and add to 5",
        calculation = "(x + 2)(x + 3) = 0"
    ),
    SolutionStepData(
        title = "Solve for x",
        explanation = "Set each factor equal to zero",
        calculation = "x + 2 = 0 or x + 3 = 0"
    )
)

val savedSolutions = listOf<SavedSolution>() // Empty for now

val monthlyUsage = listOf(
    MonthlyUsageData("📚 Textbook (Free)", 8, 0.0),
    MonthlyUsageData("🔬 Wolfram Alpha", 6, 0.015),
    MonthlyUsageData("🤖 GPT-3.5", 4, 0.016)
)

val costMethods = listOf(
    CostMethod("📚 Textbook Search", "Free", "📚", Color(0xFF4CAF50)),
    CostMethod("🔬 Wolfram Alpha", "₹0.0025", "🔬", Color(0xFF2196F3)),
    CostMethod("🤖 GPT-3.5", "₹0.004", "🤖", Color(0xFFFF9800)),
    CostMethod("🧠 GPT-4 Premium", "₹0.09", "🧠", Color(0xFF9C27B0))
)
