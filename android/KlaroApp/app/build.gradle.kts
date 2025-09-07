plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("kotlin-kapt")
    id("dagger.hilt.android.plugin")
    id("kotlin-parcelize")
}

android {
    namespace = "com.klaro.app"
    compileSdk = 34

    // Load Supabase configuration from gradle.properties (safe defaults provided)
    val supabaseUrlProp = project.findProperty("SUPABASE_URL") as String? ?: "https://YOUR_PROJECT_ID.supabase.co"
    val supabaseAnonKeyProp = project.findProperty("SUPABASE_ANON_KEY") as String? ?: "YOUR_SUPABASE_ANON_KEY"

    defaultConfig {
        applicationId = "com.klaro.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }

        // API Configuration
        buildConfigField("String", "BASE_API_URL", "\"https://klaro-educational-platform-production.up.railway.app/api/\"")
        buildConfigField("String", "APP_NAME", "\"Klaro\"")
        // Supabase (provided via gradle.properties)
        buildConfigField("String", "SUPABASE_URL", "\"${supabaseUrlProp}\"")
        buildConfigField("String", "SUPABASE_ANON_KEY", "\"${supabaseAnonKeyProp}\"")
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            buildConfigField("String", "BASE_API_URL", "\"https://api.klaro.app/api/\"")
            // Supabase config inherited from defaultConfig
        }
        debug {
            isDebuggable = true
            buildConfigField("String", "BASE_API_URL", "\"https://klaro-educational-platform-production.up.railway.app/api/\"")
            // Supabase config inherited from defaultConfig
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = "1.8"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.8"
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    // ================================================================================
    // 📱 Core Android
    // ================================================================================
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")

    // ================================================================================
    // 🎨 Jetpack Compose UI
    // ================================================================================
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")

    // Navigation
    implementation("androidx.navigation:navigation-compose:2.7.6")

    // ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")
    // ================================================================================
    // 🌐 Networking & API
    // ================================================================================
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

    // ================================================================================
    // 🔐 Supabase Auth (GoTrue) + Ktor engine
    // ================================================================================
    implementation(platform("io.github.jan-tennert.supabase:bom:2.5.4"))
    implementation("io.github.jan-tennert.supabase:supabase-kt")
    implementation("io.github.jan-tennert.supabase:gotrue-kt")
    // Optional future modules
    // implementation("io.github.jan-tennert.supabase:postgrest-kt")
    // implementation("io.github.jan-tennert.supabase:storage-kt")
    implementation("io.ktor:ktor-client-okhttp:2.3.7")

    // ================================================================================
    // 💉 Dependency Injection
    // ================================================================================
    implementation("com.google.dagger:hilt-android:2.48.1")
    kapt("com.google.dagger:hilt-compiler:2.48.1")
    implementation("androidx.hilt:hilt-navigation-compose:1.1.0")

    // ================================================================================
    // 📸 Camera & Image Processing
    // ================================================================================
    implementation("androidx.camera:camera-camera2:1.3.1")
    implementation("androidx.camera:camera-lifecycle:1.3.1")
    implementation("androidx.camera:camera-view:1.3.1")
    implementation("androidx.camera:camera-extensions:1.3.1")

    // Image Loading
    implementation("io.coil-kt:coil-compose:2.5.0")

    // ================================================================================
    // 🗄️ Local Database
    // ================================================================================
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    // // kapt("androidx.room:room-compiler:2.6.1")

    // ================================================================================
    // 📊 Analytics & Monitoring
    // ================================================================================
    implementation("com.google.firebase:firebase-analytics-ktx:21.5.0")
    implementation("com.google.firebase:firebase-crashlytics-ktx:18.6.1")

    // ================================================================================
    // 💳 In-App Purchases
    // ================================================================================
    implementation("com.android.billingclient:billing-ktx:6.1.0")

    // ================================================================================
    // 📄 PDF & File Handling
    // ================================================================================
    implementation("androidx.work:work-runtime-ktx:2.9.0")

    // ================================================================================
    // 🧪 Testing
    // ================================================================================
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.mockito:mockito-core:5.7.0")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")

    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation(platform("androidx.compose:compose-bom:2024.02.00"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")

    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
