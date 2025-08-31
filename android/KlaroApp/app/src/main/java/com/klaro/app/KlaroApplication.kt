package com.klaro.app

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

/**
 * 🎓 Klaro Application
 * 
 * Main application class with dependency injection setup
 */
@HiltAndroidApp
class KlaroApplication : Application() {
    
    override fun onCreate() {
        super.onCreate()
        
        // Initialize any global configurations here
        setupLogging()
        setupAnalytics()
    }
    
    private fun setupLogging() {
        // Setup logging for debug builds
        if (BuildConfig.DEBUG) {
            // Enable detailed logging
        }
    }
    
    private fun setupAnalytics() {
        // Setup analytics (Firebase, etc.)
        // Will be implemented later
    }
}
