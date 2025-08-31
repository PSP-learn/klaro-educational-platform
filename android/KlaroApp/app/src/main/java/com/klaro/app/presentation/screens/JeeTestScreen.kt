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
 * 🎯 JEE Test Screen
 * 
 * Take customizable JEE Main mock tests with real-time scoring
 * Uses existing backend: /api/jee/*
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun JeeTestScreen(navController: NavController) {
    
    var selectedTab by remember { mutableStateOf(0) }
    val tabs = listOf("🚀 Take Test", "📊 Results", "📈 Analytics")
    
    Column(
        modifier = Modifier.fillMaxSize()
    ) {
        
        // Header Card
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.secondaryContainer
            )
        ) {
            Column(modifier = Modifier.padding(20.dp)) {
                Text(
                    text = "🎯 JEE Main Tests",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSecondaryContainer
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Exact JEE Main 2024 format • 75 questions • 3 hours",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSecondaryContainer.copy(alpha = 0.8f)
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
            0 -> TakeTestTab()
            1 -> ResultsTab()
            2 -> AnalyticsTab()
        }
    }
}

@Composable
fun TakeTestTab() {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        
        // Quick Start Tests
        item {
            QuickStartSection()
        }
        
        // Test Types
        item {
            TestTypesSection()
        }
        
        // Subject Practice
        item {
            SubjectPracticeSection()
        }
        
        // Previous Year Questions
        item {
            PreviousYearSection()
        }
    }
}

@Composable
fun QuickStartSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "⚡ Quick Start",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            Button(
                onClick = { /* TODO: Start full mock test */ },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary
                )
            ) {
                Icon(Icons.Filled.PlayArrow, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = "🚀 Start Full Mock Test",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = "75 questions • 3 hours • All subjects",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

@Composable
fun TestTypesSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📝 Test Types",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            testTypes.forEach { testType ->
                TestTypeCard(testType)
                if (testType != testTypes.last()) {
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }
        }
    }
}

@Composable
fun TestTypeCard(testType: JEETestType) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* TODO: Start test of this type */ },
        colors = CardDefaults.cardColors(
            containerColor = testType.color.copy(alpha = 0.1f)
        )
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = testType.icon,
                contentDescription = testType.name,
                tint = testType.color,
                modifier = Modifier.size(24.dp)
            )
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = testType.name,
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = testType.description,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            Text(
                text = testType.duration,
                style = MaterialTheme.typography.bodySmall,
                color = testType.color,
                fontWeight = FontWeight.Medium
            )
        }
    }
}

@Composable
fun SubjectPracticeSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📚 Subject Practice",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                subjects.forEach { subject ->
                    SubjectCard(
                        subject = subject,
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }
    }
}

@Composable
fun SubjectCard(
    subject: JEESubject,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .clickable { /* TODO: Start subject test */ },
        colors = CardDefaults.cardColors(
            containerColor = subject.color.copy(alpha = 0.1f)
        )
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                imageVector = subject.icon,
                contentDescription = subject.name,
                tint = subject.color,
                modifier = Modifier.size(32.dp)
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = subject.name,
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold,
                textAlign = TextAlign.Center
            )
            Text(
                text = "25 Qs",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun PreviousYearSection() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📅 Previous Year Questions",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            pyqYears.forEach { year ->
                PYQYearCard(year)
                if (year != pyqYears.last()) {
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }
        }
    }
}

@Composable
fun PYQYearCard(year: String) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* TODO: Start PYQ test */ },
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Filled.CalendarMonth,
                contentDescription = "Year $year",
                tint = MaterialTheme.colorScheme.primary
            )
            
            Text(
                text = "JEE Main $year",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Medium,
                modifier = Modifier.weight(1f)
            )
            
            Icon(
                imageVector = Icons.Filled.ChevronRight,
                contentDescription = "Take test",
                tint = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun ResultsTab() {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        
        item {
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            ) {
                Column(modifier = Modifier.padding(20.dp)) {
                    Text(
                        text = "📊 Your Test Results",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "Track your performance and improvement over time",
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            }
        }
        
        items(sampleResults) { result ->
            TestResultCard(result)
        }
    }
}

@Composable
fun TestResultCard(result: TestResult) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* TODO: View detailed analysis */ }
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = result.testName,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = result.date,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                Column(horizontalAlignment = Alignment.End) {
                    Text(
                        text = "${result.score}%",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        color = when {
                            result.score >= 80 -> Color(0xFF4CAF50)
                            result.score >= 60 -> Color(0xFFFF9800)
                            else -> Color(0xFFF44336)
                        }
                    )
                    Text(
                        text = "${result.rank} rank",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            // Subject scores
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                result.subjectScores.forEach { (subject, score) ->
                    SubjectScore(subject, score)
                }
            }
        }
    }
}

@Composable
fun SubjectScore(subject: String, score: Int) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = "$score%",
            style = MaterialTheme.typography.titleSmall,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
        Text(
            text = subject,
            style = MaterialTheme.typography.bodySmall
        )
    }
}

@Composable
fun AnalyticsTab() {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        
        // Performance Overview
        item {
            PerformanceOverviewCard()
        }
        
        // Subject Analysis
        item {
            SubjectAnalysisCard()
        }
        
        // Improvement Suggestions
        item {
            ImprovementSuggestionsCard()
        }
    }
}

@Composable
fun PerformanceOverviewCard() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "📈 Performance Overview",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                PerformanceMetric("Tests Taken", "12")
                PerformanceMetric("Average Score", "78%")
                PerformanceMetric("Best Score", "92%")
                PerformanceMetric("Rank Trend", "↗️ +15")
            }
        }
    }
}

@Composable
fun PerformanceMetric(label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = value,
            style = MaterialTheme.typography.titleLarge,
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
fun SubjectAnalysisCard() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "🔬 Subject Analysis",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            subjectAnalysis.forEach { analysis ->
                SubjectAnalysisItem(analysis)
                if (analysis != subjectAnalysis.last()) {
                    Spacer(modifier = Modifier.height(12.dp))
                }
            }
        }
    }
}

@Composable
fun SubjectAnalysisItem(analysis: SubjectAnalysis) {
    Column {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "${analysis.icon} ${analysis.subject}",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = "${analysis.averageScore}%",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
                color = analysis.color
            )
        }
        
        Spacer(modifier = Modifier.height(4.dp))
        
        LinearProgressIndicator(
            progress = analysis.averageScore / 100f,
            modifier = Modifier.fillMaxWidth(),
            color = analysis.color
        )
        
        Spacer(modifier = Modifier.height(4.dp))
        
        Text(
            text = analysis.trend,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun ImprovementSuggestionsCard() {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "💡 Improvement Suggestions",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            
            suggestions.forEach { suggestion ->
                SuggestionItem(suggestion)
                if (suggestion != suggestions.last()) {
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }
        }
    }
}

@Composable
fun SuggestionItem(suggestion: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Icon(
            imageVector = Icons.Filled.Lightbulb,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.primary,
            modifier = Modifier.size(20.dp)
        )
        Text(
            text = suggestion,
            style = MaterialTheme.typography.bodyMedium,
            modifier = Modifier.weight(1f)
        )
    }
}

// ================================================================================
// 📋 Data Classes & Static Data
// ================================================================================

data class JEETestType(
    val name: String,
    val description: String,
    val duration: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val color: Color
)

data class JEESubject(
    val name: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val color: Color
)

data class TestResult(
    val testName: String,
    val date: String,
    val score: Int,
    val rank: String,
    val subjectScores: Map<String, Int>
)

data class SubjectAnalysis(
    val subject: String,
    val icon: String,
    val averageScore: Int,
    val trend: String,
    val color: Color
)

val testTypes = listOf(
    JEETestType(
        name = "Full Mock Test",
        description = "Complete JEE Main simulation",
        duration = "3 hours",
        icon = Icons.Filled.Quiz,
        color = Color(0xFF2196F3)
    ),
    JEETestType(
        name = "Subject Practice", 
        description = "Focus on single subject",
        duration = "1 hour",
        icon = Icons.Filled.MenuBook,
        color = Color(0xFF4CAF50)
    ),
    JEETestType(
        name = "Topic Practice",
        description = "Specific topic drilling",
        duration = "30 mins",
        icon = Icons.Filled.Target,
        color = Color(0xFFFF9800)
    )
)

val subjects = listOf(
    JEESubject("Math", Icons.Filled.Functions, Color(0xFF2196F3)),
    JEESubject("Physics", Icons.Filled.Science, Color(0xFF4CAF50)),
    JEESubject("Chemistry", Icons.Filled.Biotech, Color(0xFFFF9800))
)

val pyqYears = listOf("2024", "2023", "2022", "2021", "2020")

val sampleResults = listOf(
    TestResult(
        testName = "JEE Main Mock Test #5",
        date = "2 days ago",
        score = 85,
        rank = "AIR 2,847",
        subjectScores = mapOf("Math" to 92, "Physics" to 78, "Chemistry" to 85)
    ),
    TestResult(
        testName = "Mathematics Practice",
        date = "5 days ago", 
        score = 78,
        rank = "AIR 5,432",
        subjectScores = mapOf("Math" to 78)
    )
)

val subjectAnalysis = listOf(
    SubjectAnalysis("Mathematics", "📐", 82, "↗️ Improving (+5% this month)", Color(0xFF2196F3)),
    SubjectAnalysis("Physics", "⚛️", 75, "→ Stable (±2% this month)", Color(0xFF4CAF50)),
    SubjectAnalysis("Chemistry", "🧪", 68, "↘️ Needs attention (-3% this month)", Color(0xFFFF9800))
)

val suggestions = listOf(
    "Focus more on Chemistry - your weakest subject",
    "Practice time management - you're taking too long on Physics",
    "Review coordinate geometry concepts in Mathematics",
    "Take more topic-specific tests before attempting full mocks"
)
