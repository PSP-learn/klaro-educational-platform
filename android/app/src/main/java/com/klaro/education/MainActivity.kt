package com.klaro.education

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
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
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.klaro.education.ui.theme.KlaroEducationTheme

/**
 * 📱 Klaro Educational Platform - Android App
 * 
 * Main Activity using Jetpack Compose with Material Design 3
 * Android-first educational quiz generation platform
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        setContent {
            KlaroEducationTheme {
                KlaroApp()
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun KlaroApp() {
    val navController = rememberNavController()
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Text(
                        "🎓 Klaro Education",
                        fontWeight = FontWeight.Bold
                    ) 
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        },
        bottomBar = {
            NavigationBar {
                val items = listOf(
                    NavigationItem("Home", Icons.Default.Home, "home"),
                    NavigationItem("Quiz", Icons.Default.Quiz, "quiz"),
                    NavigationItem("Library", Icons.Default.LibraryBooks, "library"),
                    NavigationItem("Progress", Icons.Default.Analytics, "progress"),
                    NavigationItem("Profile", Icons.Default.Person, "profile")
                )
                
                items.forEach { item ->
                    NavigationBarItem(
                        icon = { Icon(item.icon, contentDescription = item.label) },
                        label = { Text(item.label) },
                        selected = false, // TODO: Track current route
                        onClick = { navController.navigate(item.route) }
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(innerPadding)
        ) {
            composable("home") { HomeScreen(navController) }
            composable("quiz") { QuizCreatorScreen(navController) }
            composable("library") { LibraryScreen(navController) }
            composable("progress") { ProgressScreen(navController) }
            composable("profile") { ProfileScreen(navController) }
        }
    }
}

// ================================================================================
// 🏠 Home Dashboard Screen
// ================================================================================

@Composable
fun HomeScreen(navController: NavController) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            // Welcome Section
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            ) {
                Column(
                    modifier = Modifier.padding(20.dp)
                ) {
                    Text(
                        "Welcome back! 👋",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        "Ready to create some amazing quizzes?",
                        style = MaterialTheme.typography.bodyLarge
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Chip(
                            onClick = { },
                            label = { Text("🔥 5-day streak") }
                        )
                        Chip(
                            onClick = { },
                            label = { Text("📊 78% avg score") }
                        )
                    }
                }
            }
        }
        
        item {
            // Quick Actions
            Text(
                "Quick Actions",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
        }
        
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Create Quiz Button
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    onClick = { navController.navigate("quiz") }
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Icon(
                            Icons.Default.Add,
                            contentDescription = "Create Quiz",
                            modifier = Modifier.size(32.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            "Create Quiz",
                            style = MaterialTheme.typography.titleMedium,
                            textAlign = TextAlign.Center
                        )
                    }
                }
                
                // Browse Library Button  
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    onClick = { navController.navigate("library") }
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Icon(
                            Icons.Default.LibraryBooks,
                            contentDescription = "Library",
                            modifier = Modifier.size(32.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            "Browse Library",
                            style = MaterialTheme.typography.titleMedium,
                            textAlign = TextAlign.Center
                        )
                    }
                }
            }
        }
        
        item {
            // Recent Quizzes
            Text(
                "Recent Quizzes",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
        }
        
        items(listOf(
            "Algebra Practice - 85%",
            "Trigonometry Test - 92%", 
            "Geometry Quiz - 76%"
        )) { quiz ->
            Card(
                modifier = Modifier.fillMaxWidth(),
                onClick = { /* Navigate to quiz details */ }
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Default.Quiz,
                        contentDescription = "Quiz",
                        tint = MaterialTheme.colorScheme.secondary
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    Text(
                        quiz,
                        style = MaterialTheme.typography.bodyLarge,
                        modifier = Modifier.weight(1f)
                    )
                    Icon(
                        Icons.Default.ChevronRight,
                        contentDescription = "View"
                    )
                }
            }
        }
    }
}

// ================================================================================
// 🎯 Quiz Creator Screen  
// ================================================================================

@Composable
fun QuizCreatorScreen(navController: NavController) {
    var selectedTopics by remember { mutableStateOf(setOf<String>()) }
    var numQuestions by remember { mutableStateOf(10f) }
    var selectedDifficulty by remember { mutableStateOf(setOf("easy", "medium")) }
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Text(
                "🎯 Create Your Quiz",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
        }
        
        item {
            // Topics Selection
            Card {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        "📚 Select Topics",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    val topics = listOf(
                        "Quadratic Equations", "Polynomials", "Trigonometry",
                        "Geometry", "Statistics", "Coordinate Geometry"
                    )
                    
                    topics.chunked(2).forEach { rowTopics ->
                        Row(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            rowTopics.forEach { topic ->
                                FilterChip(
                                    onClick = {
                                        selectedTopics = if (selectedTopics.contains(topic)) {
                                            selectedTopics - topic
                                        } else {
                                            selectedTopics + topic
                                        }
                                    },
                                    label = { Text(topic) },
                                    selected = selectedTopics.contains(topic),
                                    modifier = Modifier.weight(1f)
                                )
                            }
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                    }
                }
            }
        }
        
        item {
            // Number of Questions
            Card {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        "❓ Number of Questions: ${numQuestions.toInt()}",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                    Slider(
                        value = numQuestions,
                        onValueChange = { numQuestions = it },
                        valueRange = 5f..25f,
                        steps = 19
                    )
                }
            }
        }
        
        item {
            // Difficulty Selection
            Card {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        "⚡ Difficulty Level",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        listOf("Easy", "Medium", "Hard").forEach { difficulty ->
                            FilterChip(
                                onClick = {
                                    selectedDifficulty = if (selectedDifficulty.contains(difficulty.lowercase())) {
                                        selectedDifficulty - difficulty.lowercase()
                                    } else {
                                        selectedDifficulty + difficulty.lowercase()
                                    }
                                },
                                label = { Text(difficulty) },
                                selected = selectedDifficulty.contains(difficulty.lowercase())
                            )
                        }
                    }
                }
            }
        }
        
        item {
            // Generate Button
            Button(
                onClick = {
                    // TODO: Call API to generate quiz
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                enabled = selectedTopics.isNotEmpty()
            ) {
                Icon(Icons.Default.Auto, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    "Generate Quiz",
                    style = MaterialTheme.typography.titleMedium
                )
            }
        }
    }
}

// ================================================================================
// 📚 Other Screens (Placeholder implementations)
// ================================================================================

@Composable
fun LibraryScreen(navController: NavController) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            Icons.Default.LibraryBooks,
            contentDescription = "Library",
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.primary
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            "📚 Textbook Library",
            style = MaterialTheme.typography.headlineSmall
        )
        Text(
            "Browse and search your textbooks\nComing soon!",
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
fun ProgressScreen(navController: NavController) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            Icons.Default.Analytics,
            contentDescription = "Progress",
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.primary
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            "📊 Progress Analytics",
            style = MaterialTheme.typography.headlineSmall
        )
        Text(
            "Track your learning progress\nComing soon!",
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
fun ProfileScreen(navController: NavController) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            Icons.Default.Person,
            contentDescription = "Profile",
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.primary
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            "👤 User Profile",
            style = MaterialTheme.typography.headlineSmall
        )
        Text(
            "Manage your account settings\nComing soon!",
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
    }
}

// ================================================================================
// 🎨 UI Components
// ================================================================================

data class NavigationItem(
    val label: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val route: String
)

@Composable
fun Chip(
    onClick: () -> Unit,
    label: @Composable () -> Unit
) {
    SuggestionChip(
        onClick = onClick,
        label = label
    )
}

// ================================================================================
// 🎨 Preview for Development
// ================================================================================

@Preview(showBackground = true)
@Composable
fun HomeScreenPreview() {
    KlaroEducationTheme {
        HomeScreen(rememberNavController())
    }
}

@Preview(showBackground = true)
@Composable
fun QuizCreatorPreview() {
    KlaroEducationTheme {
        QuizCreatorScreen(rememberNavController())
    }
}
