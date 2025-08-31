package com.klaro.app.presentation

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import dagger.hilt.android.AndroidEntryPoint

import com.klaro.app.presentation.ui.theme.KlaroTheme
import com.klaro.app.presentation.screens.*

/**
 * 🎓 Klaro Main Activity
 * 
 * Main entry point with Bottom Navigation for 3 core features:
 * 1. PDF Generator
 * 2. JEE Tests  
 * 3. Doubt Solver
 */
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        setContent {
            KlaroTheme {
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
        bottomBar = {
            KlaroBottomBar(navController = navController)
        }
    ) { paddingValues ->
        NavHost(
            navController = navController,
            startDestination = Screen.Home.route,
            modifier = Modifier.padding(paddingValues)
        ) {
            composable(Screen.Home.route) {
                HomeScreen(navController = navController)
            }
            
            composable(Screen.PdfGenerator.route) {
                PdfGeneratorScreen(navController = navController)
            }
            
            composable(Screen.JeeTest.route) {
                JeeTestScreen(navController = navController)
            }
            
            composable(Screen.DoubtSolver.route) {
                DoubtSolverScreen(navController = navController)
            }
            
            composable(Screen.Profile.route) {
                ProfileScreen(navController = navController)
            }
        }
    }
}

@Composable
fun KlaroBottomBar(navController: androidx.navigation.NavController) {
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination

    NavigationBar {
        bottomNavItems.forEach { screen ->
            NavigationBarItem(
                icon = { Icon(screen.icon, contentDescription = screen.title) },
                label = { Text(screen.title) },
                selected = currentDestination?.hierarchy?.any { it.route == screen.route } == true,
                onClick = {
                    navController.navigate(screen.route) {
                        // Pop up to the start destination of the graph to
                        // avoid building up a large stack of destinations
                        popUpTo(navController.graph.findStartDestination().id) {
                            saveState = true
                        }
                        // Avoid multiple copies of the same destination when
                        // reselecting the same item
                        launchSingleTop = true
                        // Restore state when reselecting a previously selected item
                        restoreState = true
                    }
                }
            )
        }
    }
}

// ================================================================================
// 🧭 Navigation Configuration
// ================================================================================

sealed class Screen(val route: String, val title: String, val icon: ImageVector) {
    object Home : Screen("home", "Home", Icons.Filled.Home)
    object PdfGenerator : Screen("pdf_generator", "PDF Quiz", Icons.Filled.Assignment)
    object JeeTest : Screen("jee_test", "JEE Tests", Icons.Filled.Quiz)
    object DoubtSolver : Screen("doubt_solver", "Doubts", Icons.Filled.QuestionAnswer)
    object Profile : Screen("profile", "Profile", Icons.Filled.Person)
}

val bottomNavItems = listOf(
    Screen.Home,
    Screen.PdfGenerator,
    Screen.JeeTest,
    Screen.DoubtSolver,
    Screen.Profile
)
