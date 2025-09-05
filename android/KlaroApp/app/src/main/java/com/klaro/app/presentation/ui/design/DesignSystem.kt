package com.klaro.app.presentation.ui.design

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * 🎨 Klaro Design System - World-Class Minimal Design
 * Philosophy: "Study + Clean = Success"
 */

object KlaroDesign {
    
    // Colors - Minimal & Purposeful
    object Colors {
        val LearningBlue = Color(0xFF1565C0)
        val LearningBlueLight = Color(0xFFE3F2FD)
        val GrowthGreen = Color(0xFF2E7D32)
        val GrowthGreenLight = Color(0xFFE8F5E8)
        val FocusAmber = Color(0xFFE65100)
        val NeutralDark = Color(0xFF212121)
        val NeutralMedium = Color(0xFF757575)
        val NeutralLight = Color(0xFFF5F5F5)
        val NeutralWhite = Color(0xFFFFFFFF)
        val ErrorRed = Color(0xFFD32F2F)
        val SuccessGreen = Color(0xFF2E7D32)
        val BackgroundLight = Color(0xFFFAFAFA)
    }
    
    // Typography - Perfect Hierarchy
    object Typography {
        val Hero = 32.sp
        val Headline = 24.sp
        val Title = 20.sp
        val Body = 16.sp
        val Subtitle = 18.sp
        val Caption = 14.sp
        val Label = 12.sp
        
        val Bold = FontWeight.Bold
        val SemiBold = FontWeight.SemiBold
        val Medium = FontWeight.Medium
        val Regular = FontWeight.Normal
    }
    
    // Spacing - Mathematical Precision
    object Spacing {
        val XSmall = 4.dp
        val Small = 8.dp
        val Medium = 16.dp
        val Large = 24.dp
        val XLarge = 32.dp
        val XXLarge = 48.dp
        
        val CardPadding = Large
        val ScreenPadding = Medium
        val ElementGap = Medium
        val SectionGap = Large
    }
    
    // Components
    object Components {
        val CardElevation = 2.dp
        val CardRadius = 12.dp
        val ButtonHeight = 56.dp
        val ButtonRadius = 12.dp
        val InputRadius = 8.dp
        val IconSmall = 20.dp
        val IconMedium = 24.dp
        val IconLarge = 32.dp
    }
}

// Clean Components
@Composable
fun CleanCard(
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null,
    content: @Composable ColumnScope.() -> Unit
) {
    if (onClick != null) {
        Card(
            onClick = onClick,
            modifier = modifier.fillMaxWidth(),
            elevation = CardDefaults.cardElevation(defaultElevation = KlaroDesign.Components.CardElevation),
            shape = RoundedCornerShape(KlaroDesign.Components.CardRadius),
            colors = CardDefaults.cardColors(containerColor = KlaroDesign.Colors.NeutralWhite)
        ) {
            Column(
                modifier = Modifier.padding(KlaroDesign.Spacing.CardPadding),
                verticalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium),
                content = content
            )
        }
    } else {
        Card(
            modifier = modifier.fillMaxWidth(),
            elevation = CardDefaults.cardElevation(defaultElevation = KlaroDesign.Components.CardElevation),
            shape = RoundedCornerShape(KlaroDesign.Components.CardRadius),
            colors = CardDefaults.cardColors(containerColor = KlaroDesign.Colors.NeutralWhite)
        ) {
            Column(
                modifier = Modifier.padding(KlaroDesign.Spacing.CardPadding),
                verticalArrangement = Arrangement.spacedBy(KlaroDesign.Spacing.Medium),
                content = content
            )
        }
    }
}

@Composable
fun PrimaryActionButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    isLoading: Boolean = false,
    icon: androidx.compose.ui.graphics.vector.ImageVector? = null
) {
    Button(
        onClick = onClick,
        enabled = enabled && !isLoading,
        modifier = modifier
            .fillMaxWidth()
            .height(KlaroDesign.Components.ButtonHeight),
        shape = RoundedCornerShape(KlaroDesign.Components.ButtonRadius),
        colors = ButtonDefaults.buttonColors(
            containerColor = KlaroDesign.Colors.LearningBlue,
            contentColor = KlaroDesign.Colors.NeutralWhite
        )
    ) {
        if (isLoading) {
            CircularProgressIndicator(
                modifier = Modifier.size(KlaroDesign.Components.IconSmall),
                color = KlaroDesign.Colors.NeutralWhite
            )
            Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Small))
            Text("Loading...")
        } else {
            icon?.let {
                Icon(
                    imageVector = it,
                    contentDescription = null,
                    modifier = Modifier.size(KlaroDesign.Components.IconMedium)
                )
                Spacer(modifier = Modifier.width(KlaroDesign.Spacing.Small))
            }
            Text(
                text = text,
                fontSize = KlaroDesign.Typography.Body,
                fontWeight = KlaroDesign.Typography.SemiBold
            )
        }
    }
}

@Composable
fun MessageCard(
    message: String,
    type: MessageType = MessageType.SUCCESS,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = when (type) {
                MessageType.SUCCESS -> KlaroDesign.Colors.GrowthGreenLight
                MessageType.ERROR -> Color(0xFFFFEBEE)
                MessageType.INFO -> KlaroDesign.Colors.LearningBlueLight
            }
        )
    ) {
        Text(
            text = when (type) {
                MessageType.SUCCESS -> "✅ $message"
                MessageType.ERROR -> "⚠️ $message"
                MessageType.INFO -> "ℹ️ $message"
            },
            modifier = Modifier.padding(KlaroDesign.Spacing.Medium),
            fontSize = KlaroDesign.Typography.Body,
            color = when (type) {
                MessageType.SUCCESS -> KlaroDesign.Colors.GrowthGreen
                MessageType.ERROR -> KlaroDesign.Colors.ErrorRed
                MessageType.INFO -> KlaroDesign.Colors.LearningBlue
            }
        )
    }
}

enum class MessageType { SUCCESS, ERROR, INFO }
