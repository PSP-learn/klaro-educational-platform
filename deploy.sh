#!/bin/bash

# 🚀 Klaro Educational Platform - Quick Deploy Script
# This script helps you set up the deployment environment quickly

set -e  # Exit on any error

echo "🟢 Klaro Educational Platform - Deployment Setup"
echo "================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required files exist
print_step "Checking project structure..."

required_files=(
    "backend/main_with_supabase.py"
    "backend/supabase_client.py"
    "backend/supabase_schema.sql"
    "backend/requirements.txt"
    "railway.json"
    "DEPLOYMENT_GUIDE.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✅ $file exists"
    else
        print_error "❌ $file is missing!"
        exit 1
    fi
done

# Check if Python dependencies can be installed
print_step "Checking Python environment..."

if command -v python3 &> /dev/null; then
    print_success "✅ Python 3 is available"
else
    print_error "❌ Python 3 is not installed!"
    exit 1
fi

if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    print_success "✅ pip is available"
else
    print_error "❌ pip is not installed!"
    exit 1
fi

# Test backend dependencies (optional)
print_step "Testing backend dependencies (this may take a moment)..."

# Create a temporary virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "✅ Created virtual environment"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
if pip install -r backend/requirements.txt > /dev/null 2>&1; then
    print_success "✅ All Python dependencies can be installed"
else
    print_warning "⚠️  Some dependencies may have issues. Check manually with:"
    echo "    pip install -r backend/requirements.txt"
fi

# Deactivate virtual environment
deactivate

# Check Android project structure
print_step "Checking Android project structure..."

android_files=(
    "android/app/build.gradle.kts"
    "android/app/src/main/java/com/klaro/data/SupabaseConfig.kt"
    "android/build.gradle.kts"
)

for file in "${android_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✅ $file exists"
    else
        print_warning "⚠️  $file is missing (will be created during Android development)"
    fi
done

# Generate deployment checklist
print_step "Generating deployment checklist..."

cat > DEPLOYMENT_CHECKLIST.md << 'EOF'
# 📋 Klaro Deployment Checklist

## 🗄️ Supabase Setup
- [ ] Created Supabase project at supabase.com
- [ ] Ran `backend/supabase_schema.sql` in SQL Editor
- [ ] Created `klaro-files` storage bucket
- [ ] Configured bucket policies for file access
- [ ] Copied Project URL and API keys

## 🚂 Railway Deployment
- [ ] Connected GitHub repository to Railway
- [ ] Added all environment variables:
  - [ ] `SUPABASE_URL`
  - [ ] `SUPABASE_ANON_KEY`
  - [ ] `SUPABASE_SERVICE_ROLE_KEY`
  - [ ] `OPENAI_API_KEY`
  - [ ] `ANTHROPIC_API_KEY`
  - [ ] `GOOGLE_API_KEY`
  - [ ] `ENVIRONMENT=production`
- [ ] Configured build settings
- [ ] Deployed successfully
- [ ] Tested `/health` endpoint

## 📱 Android Configuration
- [ ] Added Supabase dependencies to `build.gradle.kts`
- [ ] Created `SupabaseConfig.kt` with your project details
- [ ] Updated API endpoints to point to Railway backend
- [ ] Tested authentication flow
- [ ] Tested all core features

## ✅ Final Verification
- [ ] Full stack registration/login works
- [ ] Doubt solver processes images correctly
- [ ] PDF quiz generation works
- [ ] JEE test system functions properly
- [ ] File uploads work through Supabase Storage
- [ ] Analytics are being recorded

## 🚀 Ready for Launch!
EOF

print_success "✅ Created DEPLOYMENT_CHECKLIST.md"

# Summary
echo ""
echo "================================================="
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "================================================="
echo ""
echo "📋 Next Steps:"
echo "1. Follow the detailed guide in DEPLOYMENT_GUIDE.md"
echo "2. Use DEPLOYMENT_CHECKLIST.md to track your progress"
echo "3. Set up Supabase project first"
echo "4. Deploy backend to Railway"
echo "5. Update Android app configuration"
echo "6. Test the full stack"
echo ""
echo "💡 Pro Tips:"
echo "• Keep your API keys secure and never commit them to git"
echo "• Test each component individually before integrating"
echo "• Use the Railway logs to debug any deployment issues"
echo "• Supabase has excellent documentation if you get stuck"
echo ""
echo "🔗 Useful Links:"
echo "• Supabase: https://supabase.com"
echo "• Railway: https://railway.app"
echo "• Deployment Guide: ./DEPLOYMENT_GUIDE.md"
echo ""
print_success "Happy deploying! 🚀"
