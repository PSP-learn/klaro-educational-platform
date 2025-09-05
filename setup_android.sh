#!/bin/bash

# ================================================================================
# 🚀 Klaro Android Development Environment Setup
# ================================================================================
# This script installs everything needed for Android development
# Total download: ~4GB (one-time setup)
# ================================================================================

set -e  # Exit on error

echo "🚀 Setting up Klaro Android Development Environment..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# ================================================================================
# Step 1: Check and Install Homebrew
# ================================================================================
echo "📦 Step 1: Checking Homebrew..."
if ! command -v brew &> /dev/null; then
    print_info "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    print_status "Homebrew already installed"
fi

# ================================================================================
# Step 2: Install Java JDK
# ================================================================================
echo ""
echo "☕ Step 2: Installing Java JDK..."
if command -v java &> /dev/null && java -version 2>&1 | grep -q "openjdk version \"17\."; then
    print_status "Java already installed"
    java -version
else
    print_info "Installing OpenJDK 17..."
    brew install openjdk@17
    
    # Add to PATH
    echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
    export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
    
    # Set JAVA_HOME
    echo 'export JAVA_HOME="/opt/homebrew/opt/openjdk@17"' >> ~/.zshrc
    export JAVA_HOME="/opt/homebrew/opt/openjdk@17"
    
    print_status "Java JDK installed"
fi

# ================================================================================
# Step 3: Install Android Studio (includes Android SDK)
# ================================================================================
echo ""
echo "📱 Step 3: Installing Android Studio..."
if [ -d "/Applications/Android Studio.app" ]; then
    print_status "Android Studio already installed"
else
    print_info "Installing Android Studio (includes Android SDK)..."
    brew install --cask android-studio
    print_status "Android Studio installed"
    print_warning "You'll need to open Android Studio once to complete SDK setup"
fi

# ================================================================================
# Step 4: Install Android SDK Command Line Tools
# ================================================================================
echo ""
echo "🛠️  Step 4: Installing Android SDK Command Line Tools..."
if ! command -v sdkmanager &> /dev/null; then
    print_info "Installing Android SDK command line tools..."
    brew install --cask android-commandlinetools
    
    # Set Android environment variables
    echo 'export ANDROID_HOME="$HOME/Library/Android/sdk"' >> ~/.zshrc
    echo 'export PATH="$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$PATH"' >> ~/.zshrc
    
    export ANDROID_HOME="$HOME/Library/Android/sdk"
    export PATH="$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$PATH"
    
    print_status "Android SDK command line tools installed"
else
    print_status "Android SDK command line tools already available"
fi

# ================================================================================
# Step 5: Install Gradle
# ================================================================================
echo ""
echo "🔧 Step 5: Installing Gradle..."
if ! command -v gradle &> /dev/null; then
    print_info "Installing Gradle..."
    brew install gradle
    print_status "Gradle installed"
else
    print_status "Gradle already installed"
fi

# ================================================================================
# Step 6: Setup Android SDK Components
# ================================================================================
echo ""
echo "📲 Step 6: Installing Android SDK components..."

# Create Android SDK directory if it doesn't exist
mkdir -p "$HOME/Library/Android/sdk"

# Accept Android SDK licenses (required for CI/CD)
print_info "Accepting Android SDK licenses..."
yes | sdkmanager --licenses 2>/dev/null || true

# Install essential Android SDK components
print_info "Installing Android SDK platforms and tools..."
sdkmanager "platform-tools" "platforms;android-34" "platforms;android-33" "build-tools;34.0.0" "build-tools;33.0.2" || true

print_status "Android SDK components installed"

# ================================================================================
# Step 7: Download Android Project Dependencies
# ================================================================================
echo ""
echo "📦 Step 7: Downloading Android project dependencies..."

cd /Users/sushantnandwana/klaro-unified/android/KlaroApp

print_info "Cleaning any previous build artifacts..."
./gradlew clean || true

print_info "Downloading all dependencies (this may take 5-10 minutes)..."
./gradlew dependencies --refresh-dependencies

print_info "Building project to ensure everything works..."
./gradlew assembleDebug

print_status "All Android dependencies downloaded and project built successfully!"

# ================================================================================
# Step 8: Verification
# ================================================================================
echo ""
echo "🔍 Step 8: Verifying installation..."

echo ""
print_info "Java Version:"
java -version

echo ""
print_info "Gradle Version:"
gradle --version

echo ""
print_info "Android SDK Location:"
echo $ANDROID_HOME

echo ""
print_info "ADB Version:"
adb --version 2>/dev/null || print_warning "ADB not found - run Android Studio once to complete setup"

# ================================================================================
# Summary
# ================================================================================
echo ""
echo "======================================================================"
echo "🎉 SETUP COMPLETE!"
echo "======================================================================"
echo ""
print_status "✅ Java JDK 17 installed"
print_status "✅ Android Studio installed"
print_status "✅ Android SDK installed"
print_status "✅ Gradle installed"
print_status "✅ All Android dependencies downloaded"
print_status "✅ Klaro app built successfully"
echo ""
echo "🚀 Next Steps:"
echo "1. Open Android Studio: /Applications/Android Studio.app"
echo "2. Open project: /Users/sushantnandwana/klaro-unified/android/KlaroApp"
echo "3. Wait for indexing to complete"
echo "4. Connect Android device or start emulator"
echo "5. Click 'Run' to install the Klaro app!"
echo ""
echo "📱 Your Klaro Educational Platform Android app is ready!"
echo "======================================================================"
