# 🚀 Klaro Android Setup Guide

## Option 1: Automated Setup (Recommended)

Run this single command to install everything:

```bash
cd /Users/sushantnandwana/klaro-unified && ./setup_android.sh
```

**This will automatically:**
- Install Java JDK 17
- Install Android Studio + SDK
- Install Gradle
- Download all 40+ Android dependencies (~1GB)
- Build the Klaro app
- ⏱️ **Total time: 15-30 minutes** (depending on internet speed)

---

## Option 2: Manual Setup

### Step 1: Install Java
```bash
brew install openjdk@17
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
echo 'export JAVA_HOME="/opt/homebrew/opt/openjdk@17"' >> ~/.zshrc
source ~/.zshrc
```

### Step 2: Install Android Studio
```bash
brew install --cask android-studio
```

### Step 3: Install Gradle
```bash
brew install gradle
```

### Step 4: Open Android Studio
1. Launch Android Studio
2. Complete initial setup wizard
3. Install Android SDK when prompted
4. Open existing project: `/Users/sushantnandwana/klaro-unified/android/KlaroApp`

### Step 5: Download Dependencies
In Android Studio:
1. Wait for "Gradle sync" to complete
2. All dependencies will download automatically

---

## Option 3: Command Line Only

If you prefer terminal-only approach:

```bash
# Install tools
brew install openjdk@17 gradle
brew install --cask android-studio android-commandlinetools

# Setup environment
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$PATH"

# Go to project and build
cd /Users/sushantnandwana/klaro-unified/android/KlaroApp
./gradlew assembleDebug
```

---

## 📱 What You'll Get

After setup, you'll have a fully functional Android app with:

### ✅ **Features Ready:**
- **PDF Quiz Generator** - Upload PDFs, generate quizzes
- **JEE Online Test** - Mock tests, subject tests, PYQs  
- **AI Doubt Solver** - Text input, step-by-step solutions

### 🛠️ **Tech Stack:**
- **Kotlin** + **Jetpack Compose** (Modern UI)
- **Hilt** (Dependency Injection)
- **Retrofit** (API calls to Railway backend)
- **Material Design 3** (Google's latest design)
- **40+ Dependencies** all configured

### 🌐 **Backend Connected:**
- Railway deployment: `https://klaro-educational-platform-production.up.railway.app`
- All APIs integrated and working
- Real-time AI processing

---

## 🚀 Running the App

1. **Open Android Studio**
2. **Open Project:** `/Users/sushantnandwana/klaro-unified/android/KlaroApp`
3. **Connect Device** or **Start Emulator**
4. **Click Run** ▶️

The app will install and launch on your device!

---

## 📊 Download Sizes

| Component | Size | Purpose |
|-----------|------|---------|
| Java JDK | ~150MB | Required for Android development |
| Android Studio | ~1GB | IDE + Android SDK |
| Gradle | ~100MB | Build system |
| Dependencies | ~800MB | App libraries (one-time) |
| **Total** | **~2GB** | **Complete setup** |

---

## ⚡ Quick Start

**Fastest way to get started:**

```bash
# Run this single command
/Users/sushantnandwana/klaro-unified/setup_android.sh
```

Then open Android Studio and run the app! 🎉
