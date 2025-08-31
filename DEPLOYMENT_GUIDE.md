# 🚀 Klaro Educational Platform - Deployment Guide

## Complete step-by-step guide to deploy the hybrid Supabase + Railway architecture

This guide will take you from zero to a fully deployed, production-ready Klaro educational platform.

---

## 📋 Prerequisites

- [ ] GitHub account with your code repository
- [ ] Credit card for Railway (has free tier)
- [ ] Email account for Supabase signup

---

## 🗄️ Step 1: Set Up Supabase Database

### 1.1 Create Supabase Project

1. **Visit [supabase.com](https://supabase.com)** and click "Start your project"
2. **Sign up/Log in** with GitHub
3. **Create a new project:**
   - Organization: Choose or create one
   - Project name: `klaro-educational-platform`
   - Database password: Generate a strong password (save this!)
   - Region: Choose closest to your users
4. **Wait for project creation** (takes ~2 minutes)

### 1.2 Configure Database Schema

1. **Go to SQL Editor** (in left sidebar)
2. **Copy the entire contents** of `backend/supabase_schema.sql`
3. **Paste and run** the SQL script
4. **Verify tables created:**
   ```sql
   SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
   ```

### 1.3 Set Up File Storage

1. **Go to Storage** (in left sidebar)
2. **Create a new bucket:**
   - Name: `klaro-files`
   - Public: ✅ (checked)
3. **Create bucket policies** (go to bucket → Policies):
   ```sql
   -- Allow authenticated users to upload files
   CREATE POLICY "Users can upload files" ON storage.objects
   FOR INSERT WITH CHECK (auth.uid()::text = (storage.foldername(name))[1]);
   
   -- Allow users to view their own files
   CREATE POLICY "Users can view own files" ON storage.objects
   FOR SELECT USING (auth.uid()::text = (storage.foldername(name))[1]);
   ```

### 1.4 Enable Authentication

1. **Go to Authentication** → **Settings**
2. **Enable email authentication** (should be enabled by default)
3. **Configure email templates** (optional):
   - Go to Authentication → Templates
   - Customize signup/reset password emails

### 1.5 Get API Keys

1. **Go to Settings** → **API**
2. **Copy these values** (you'll need them later):
   - Project URL
   - Project API keys:
     - `anon` key (public)
     - `service_role` key (secret)

---

## 🚂 Step 2: Deploy Backend to Railway

### 2.1 Connect GitHub Repository

1. **Visit [railway.app](https://railway.app)** and click "Start a new project"
2. **Sign up with GitHub**
3. **Connect your repository:**
   - Click "Deploy from GitHub repo"
   - Authorize Railway to access your repositories
   - Select your `klaro-unified` repository

### 2.2 Configure Environment Variables

1. **Go to your project** → **Variables** tab
2. **Add all environment variables:**

```bash
# Supabase Configuration
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# API Keys (your existing ones)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Production Settings
ENVIRONMENT=production
LOG_LEVEL=info
WORKERS=2

# CORS Settings (update with your Android app domain)
ALLOWED_ORIGINS=*
```

### 2.3 Configure Build Settings

1. **Go to Settings** → **Build**
2. **Set these values:**
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `uvicorn backend.main_with_supabase:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `/` (leave default)

### 2.4 Deploy and Test

1. **Click "Deploy"** - Railway will automatically build and deploy
2. **Wait for deployment** (takes ~3-5 minutes)
3. **Get your Railway URL** (e.g., `https://klaro-production-abc123.up.railway.app`)
4. **Test the deployment:**
   ```bash
   curl https://your-railway-url.up.railway.app/health
   ```

---

## 📱 Step 3: Update Android App Configuration

### 3.1 Add Supabase to Android Project

1. **Add to `app/build.gradle.kts`:**
   ```kotlin
   implementation("io.github.jan-tennert.supabase:postgrest-kt:2.0.3")
   implementation("io.github.jan-tennert.supabase:gotrue-kt:2.0.3")
   implementation("io.github.jan-tennert.supabase:storage-kt:2.0.3")
   implementation("io.ktor:ktor-client-android:2.3.6")
   ```

### 3.2 Create Supabase Configuration

Create `app/src/main/java/com/klaro/data/SupabaseConfig.kt`:

```kotlin
object SupabaseConfig {
    const val SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
    const val SUPABASE_ANON_KEY = "your_anon_key_here"
    const val RAILWAY_API_URL = "https://your-railway-url.up.railway.app"
}
```

### 3.3 Update API Endpoints

Update all API calls in your Android app to point to:
- **Authentication & Database:** Supabase URLs
- **AI Features:** Railway backend URLs

---

## ✅ Step 4: Verification & Testing

### 4.1 Test the Full Stack

1. **Backend health check:**
   ```bash
   curl https://your-railway-url.up.railway.app/health
   ```

2. **Test user registration:**
   ```bash
   curl -X POST https://your-railway-url.up.railway.app/api/auth/register \
     -F "email=test@example.com" \
     -F "password=testpass123" \
     -F "name=Test User"
   ```

3. **Test authentication:**
   ```bash
   curl -X POST https://your-railway-url.up.railway.app/api/auth/login \
     -F "email=test@example.com" \
     -F "password=testpass123"
   ```

### 4.2 Verify Database

1. **Go to Supabase** → **Table Editor**
2. **Check that tables exist:**
   - users
   - doubts
   - quiz_history
   - jee_test_results
   - usage_analytics
   - notifications

### 4.3 Test Android App

1. **Build and run your Android app**
2. **Test each feature:**
   - User registration/login
   - Doubt solver with camera
   - PDF quiz generation
   - JEE test system

---

## 🔧 Step 5: Production Optimization

### 5.1 Supabase Settings

1. **Go to Settings** → **Database**
2. **Enable connection pooling** (recommended for production)
3. **Set up backup schedule**

### 5.2 Railway Settings

1. **Go to Settings** → **Environment**
2. **Set up custom domain** (optional)
3. **Enable auto-deployments** from main branch

### 5.3 Monitoring

1. **Supabase Monitoring:**
   - Go to Reports → API → Analytics
   - Monitor database performance

2. **Railway Monitoring:**
   - Go to Metrics tab
   - Monitor CPU, memory, and response times

---

## 🎯 Step 6: Android App Final Updates

### 6.1 Update Network Configuration

Update `app/src/main/java/com/klaro/network/ApiService.kt` with your Railway URL:

```kotlin
object ApiConfig {
    const val BASE_URL = "https://your-railway-url.up.railway.app/api/"
    const val SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
    const val SUPABASE_ANON_KEY = "your_anon_key_here"
}
```

### 6.2 Test Authentication Flow

Ensure your Android app can:
- ✅ Register new users
- ✅ Login existing users
- ✅ Store JWT tokens securely
- ✅ Make authenticated API calls

### 6.3 Test Core Features

Verify each feature works end-to-end:
- ✅ Camera doubt solving
- ✅ PDF quiz generation and download
- ✅ JEE test taking and results

---

## 🔒 Security Checklist

- [ ] **Environment variables** are set correctly on Railway
- [ ] **CORS origins** are configured properly (not `*` in production)
- [ ] **Row Level Security** is enabled on all Supabase tables
- [ ] **File upload limits** are configured appropriately
- [ ] **API rate limiting** is configured (Railway Pro feature)

---

## 💰 Cost Estimation

### Supabase (Free Tier Limits)
- ✅ **Database:** 500MB included
- ✅ **Auth:** 50,000 monthly active users
- ✅ **Storage:** 1GB included
- ✅ **Bandwidth:** 2GB included

### Railway (Starter Plan: $5/month)
- ✅ **CPU:** 0.5 vCPU
- ✅ **RAM:** 512MB
- ✅ **Network:** 100GB/month
- ✅ **Build time:** 500 hours/month

**Total estimated cost: $5-10/month for moderate usage**

---

## 🚨 Troubleshooting

### Common Issues

1. **Supabase connection fails:**
   - Verify API keys are correct
   - Check if IP is whitelisted (shouldn't be needed)

2. **Railway deployment fails:**
   - Check build logs for missing dependencies
   - Verify `railway.json` configuration

3. **Android app can't connect:**
   - Verify network security config allows HTTP/HTTPS
   - Check API endpoints are correct

4. **CORS errors:**
   - Update CORS origins in FastAPI configuration
   - Ensure preflight requests are handled

### Debug Commands

```bash
# Check Railway deployment logs
railway logs

# Test Supabase connection
curl -H "apikey: YOUR_ANON_KEY" \
     -H "Authorization: Bearer YOUR_ANON_KEY" \
     https://YOUR_PROJECT_ID.supabase.co/rest/v1/users

# Test Railway backend
curl https://your-railway-url.up.railway.app/health
```

---

## 🎉 Success!

Once you complete all steps, you'll have:

✅ **Secure user authentication** via Supabase  
✅ **Scalable database** with Row Level Security  
✅ **AI-powered backend** deployed on Railway  
✅ **File storage** for PDFs and images  
✅ **Analytics and monitoring** built-in  
✅ **Android app** connected to production APIs  

Your Klaro Educational Platform is now live and ready for users!

---

## 📞 Next Steps

1. **Test thoroughly** with real data
2. **Set up monitoring** and alerting
3. **Plan user onboarding** flow
4. **Prepare for app store submission**
5. **Set up analytics** and user feedback collection

**Ready to launch your educational platform! 🎓📱**
