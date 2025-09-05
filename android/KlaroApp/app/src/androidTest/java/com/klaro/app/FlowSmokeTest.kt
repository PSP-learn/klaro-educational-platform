package com.klaro.app

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.klaro.app.presentation.MainActivity
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class FlowSmokeTest {

    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun bottomNavFlow_home_pdfQuiz_jee_doubts_profile() {
        // Home
        composeRule.onNodeWithText("Your study companion").assertIsDisplayed()

        // PDF Quiz via bottom bar
        composeRule.onNodeWithText("PDF Quiz").performClick()
        composeRule.onNodeWithText("Create Quiz").assertIsDisplayed()
        composeRule.onNodeWithText("Subject").assertIsDisplayed()

        // JEE Tests via bottom bar
        composeRule.onNodeWithText("JEE Tests").performClick()
        composeRule.onNodeWithText("JEE Practice").assertIsDisplayed()
        composeRule.onNodeWithText("Full Mock Test").assertIsDisplayed()

        // Doubts via bottom bar
        composeRule.onNodeWithText("Doubts").performClick()
        composeRule.onNodeWithText("Ask Question").assertIsDisplayed()
        composeRule.onNodeWithText("Get Answer").assertIsDisplayed()

        // Profile via bottom bar
        composeRule.onNodeWithText("Profile").performClick()
        composeRule.onNodeWithText("Your Profile").assertIsDisplayed()
        composeRule.onNodeWithText("Settings").assertIsDisplayed()
    }
}
