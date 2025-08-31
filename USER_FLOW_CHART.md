# 📱 Klaro Android App - Complete User Flow Chart

## 🎯 App Launch & Navigation Flow

```
📱 App Opens
    │
    ▼
🔐 Authentication Check
    │
    ├─ New User ──────► 📝 Sign Up Screen
    │                     │
    │                     ▼
    │                  ✅ Profile Setup
    │                     │
    └─ Existing User ──────┴─► 🏠 HOME SCREEN (Main Hub)
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    📄 PDF GENERATOR    🎯 JEE TESTS     🤔 DOUBT SOLVER
       Feature #1        Feature #2        Feature #3
```

---

## 🏠 HOME SCREEN - Central Dashboard

```
🏠 HOME SCREEN
├─ 🎓 Welcome Header
├─ 📊 Quick Stats (Quizzes: 12, Tests: 8, Doubts: 25)
├─ 🎯 Core Features:
│   ├─ 📄 PDF Quiz Generator ────► "Ready • Generate unlimited quizzes"
│   ├─ 🎯 JEE Online Tests ──────► "Ready • Exact JEE 2024 format"  
│   └─ 🤔 AI Doubt Solver ───────► "Ready • Text & Image support"
└─ 📈 Recent Activity
    ├─ "Created PDF Quiz - Algebra Practice"
    ├─ "Completed JEE Test - Score: 85%"
    └─ "Solved Doubt - Integration method"

👆 User taps any feature to navigate
```

---

## 📄 FEATURE #1: PDF GENERATOR FLOW

```
📄 PDF GENERATOR SCREEN
    │
    ▼
📝 CUSTOMIZATION PROCESS:
    │
    ├─ 📝 Quiz Title: "Enter custom title"
    │
    ├─ 🎯 Topic Selection:
    │   └─ Mathematics: [Algebra] [Trigonometry] [Calculus] [Geometry]
    │       └─ User selects: ✅ Algebra ✅ Trigonometry
    │
    ├─ 📊 Question Count: Slider (5-50 questions)
    │   └─ User selects: 15 questions
    │
    ├─ ⚡ Difficulty: [🟢 Easy] [🟡 Medium] [🔴 Hard]
    │   └─ User selects: ✅ Medium ✅ Hard
    │
    ├─ 📝 Question Types: [🔘 MCQ] [✏️ Short] [📝 Essay]
    │   └─ User selects: ✅ MCQ ✅ Short Answer
    │
    └─ 🚀 GENERATE BUTTON
        │
        ▼
    ⏳ GENERATION PROCESS:
        │
        ├─ "Generating Quiz..." (Loading spinner)
        ├─ API Call: POST /api/quiz/create
        ├─ Backend generates PDF
        │
        ▼
    ✅ DOWNLOAD READY:
        │
        ├─ 📥 "Download PDF Quiz" button
        ├─ 📤 "Share Quiz" option
        │
        └─ 📚 Added to "Recent Quizzes" list
```

---

## 🎯 FEATURE #2: JEE TEST FLOW

```
🎯 JEE TEST SCREEN
    │
    ▼
📑 TAB NAVIGATION:
    │
    ├─ 🚀 TAKE TEST TAB:
    │   │
    │   ├─ ⚡ Quick Start:
    │   │   └─ 🚀 "Start Full Mock Test" (75 questions, 3 hours)
    │   │
    │   ├─ 📝 Test Types:
    │   │   ├─ Full Mock Test (3 hours, all subjects)
    │   │   ├─ Subject Practice (1 hour, single subject)
    │   │   └─ Topic Practice (30 mins, specific topic)
    │   │
    │   ├─ 📚 Subject Practice:
    │   │   ├─ [📐 Math] [⚛️ Physics] [🧪 Chemistry]
    │   │   └─ Each: 25 questions, 1 hour
    │   │
    │   └─ 📅 Previous Year Questions:
    │       └─ [2024] [2023] [2022] [2021] [2020]
    │
    ├─ 📊 RESULTS TAB:
    │   │
    │   └─ 📈 Test History:
    │       ├─ "JEE Mock #5 - 85% - AIR 2,847"
    │       ├─ "Math Practice - 78% - Subject rank"
    │       └─ Subject breakdown: Math 92%, Physics 78%, Chemistry 85%
    │
    └─ 📈 ANALYTICS TAB:
        │
        ├─ 📊 Performance Overview:
        │   └─ Tests: 12, Avg: 78%, Best: 92%, Trend: ↗️ +15
        │
        ├─ 🔬 Subject Analysis:
        │   ├─ Mathematics: 82% (↗️ Improving)
        │   ├─ Physics: 75% (→ Stable)  
        │   └─ Chemistry: 68% (↘️ Needs attention)
        │
        └─ 💡 Suggestions:
            ├─ "Focus more on Chemistry"
            ├─ "Practice time management in Physics"
            └─ "Review coordinate geometry in Math"

USER TAKES TEST:
🚀 Start Test ──► 📝 Question Interface ──► ⏱️ Timer ──► ✅ Submit ──► 📊 Results
```

---

## 🤔 FEATURE #3: DOUBT SOLVER FLOW

```
🤔 DOUBT SOLVER SCREEN
    │
    ▼
📑 TAB NAVIGATION:
    │
    ├─ 📝 ASK DOUBT TAB:
    │   │
    │   ├─ 🎯 Input Methods:
    │   │   ├─ 📸 Camera OCR ──► 📷 Capture ──► 🔍 OCR ──► 📝 Text
    │   │   └─ 🎤 Voice Input (Coming Soon)
    │   │
    │   ├─ 📝 Text Input:
    │   │   ├─ Question Field: "Ask your doubt here..."
    │   │   ├─ Subject: [Mathematics] [Physics] [Chemistry] [Biology]
    │   │   └─ 🤖 "Solve My Doubt" button
    │   │
    │   └─ 📚 Recent Doubts:
    │       ├─ "Solve x² + 5x + 6 = 0" - Wolfram - 98% confidence
    │       └─ "Find derivative of sin(x²)" - GPT-3.5 - 92% confidence
    │
    ├─ 🤖 SOLUTIONS TAB:
    │   │
    │   ├─ 🤖 Latest Solution Display:
    │   │   ├─ ❓ Question: "Solve x² + 5x + 6 = 0"
    │   │   ├─ ✅ Answer: "x = -2 or x = -3"
    │   │   ├─ 📋 Solution Steps:
    │   │   │   ├─ Step 1: Identify equation (a=1, b=5, c=6)
    │   │   │   ├─ Step 2: Apply factoring ((x+2)(x+3)=0)
    │   │   │   └─ Step 3: Solve for x (x=-2 or x=-3)
    │   │   └─ [💾 Save] [📤 Share] buttons
    │   │
    │   └─ 💾 Saved Solutions: "No saved solutions yet..."
    │
    └─ 📊 USAGE TAB:
        │
        ├─ 📊 Usage Overview:
        │   └─ This Month: 18/20, Success: 94%, Avg Time: 12s, Cost Saved: ₹24.50
        │
        ├─ 💎 Plan Status:
        │   └─ "Basic Plan - 2 doubts remaining" [Upgrade] button
        │
        ├─ 📈 Monthly Breakdown:
        │   ├─ 📚 Textbook (Free): 8 uses - ₹0.000
        │   ├─ 🔬 Wolfram Alpha: 6 uses - ₹0.015  
        │   └─ 🤖 GPT-3.5: 4 uses - ₹0.016
        │
        └─ 💰 Cost Methods:
            ├─ 📚 Textbook Search: Free
            ├─ 🔬 Wolfram Alpha: ₹0.0025
            ├─ 🤖 GPT-3.5: ₹0.004
            └─ 🧠 GPT-4 Premium: ₹0.09

DOUBT SOLVING PROCESS:
📝 User Types Question ──► 🤖 AI Processing ──► 📊 Solution Display
    │                       │
    │                       ├─ Try Textbook (Free)
    │                       ├─ Try Wolfram (₹0.0025)
    │                       ├─ Try GPT-3.5 (₹0.004)
    │                       └─ Try GPT-4 (₹0.09) [Premium only]
    │
    📸 OR Camera Photo ──► 🔍 OCR Extraction ──► 📝 Text ──► 🤖 AI Processing
```

---

## 👤 PROFILE & SETTINGS FLOW

```
👤 PROFILE SCREEN
    │
    ├─ 👤 Profile Header:
    │   ├─ 🔵 Avatar (S icon)
    │   ├─ "Sushant Nandwana"
    │   ├─ "sushant@example.com"
    │   └─ [✏️ Edit Profile] button
    │
    ├─ 💎 Subscription Card:
    │   ├─ Current Plan: "Basic Plan"
    │   ├─ Features Checklist:
    │   │   ├─ ✅ 20 doubts per month
    │   │   ├─ ✅ GPT-3.5 solutions
    │   │   ├─ ✅ OCR support
    │   │   ├─ ❌ GPT-4 solutions
    │   │   ├─ ❌ Advanced analytics
    │   │   └─ ❌ Priority support
    │   ├─ Usage Bar: 18/20 doubts used (90%)
    │   └─ [💎 Upgrade] button
    │
    ├─ 📊 Statistics:
    │   ├─ 🔥 Study Streak: 7 days
    │   ├─ 📈 Total Score: 78.5%
    │   ├─ 🏆 Best Rank: AIR 2,847
    │   ├─ ⏰ Hours Studied: 45.2h
    │   └─ 🏅 Achievements: First Quiz, JEE Mock, Week Streak
    │
    ├─ ⚙️ Settings:
    │   ├─ 🔔 Notifications [ON/OFF toggle]
    │   ├─ 🌙 Dark Theme [ON/OFF toggle]
    │   ├─ 🌐 Language: English
    │   ├─ 📥 Download Quality: High
    │   └─ 🔄 Auto-sync [ON/OFF toggle]
    │
    └─ 🤝 Support:
        ├─ ❓ Help Center
        ├─ 📞 Contact Support
        ├─ 🛡️ Privacy Policy
        ├─ 📄 Terms of Service
        ├─ ⭐ Rate App
        └─ 📤 Share with Friends
```

---

## 🔄 COMPLETE USER JOURNEY EXAMPLES

### 📖 **Scenario 1: Student wants to practice Algebra**

```
📱 Opens Klaro
    │
    ▼
🏠 Home Screen
    │
    └─ Taps "📄 PDF Quiz Generator"
        │
        ▼
    📄 PDF Generator Screen
        │
        ├─ Enters title: "Algebra Practice"
        ├─ Selects topics: ✅ Algebra ✅ Quadratic Equations
        ├─ Sets questions: 20 questions
        ├─ Chooses difficulty: ✅ Medium ✅ Hard
        ├─ Selects types: ✅ MCQ ✅ Short Answer
        │
        └─ Taps "🚀 Generate PDF Quiz"
            │
            ▼
        ⏳ "Generating Quiz..." (API processing)
            │
            ▼
        ✅ "Quiz Ready!"
            │
            ├─ 📥 Download PDF
            ├─ 📤 Share with friends
            └─ 📚 Added to Recent Quizzes
```

### 🎯 **Scenario 2: Student wants to take JEE mock test**

```
📱 Opens Klaro
    │
    ▼
🏠 Home Screen
    │
    └─ Taps "🎯 JEE Online Tests"
        │
        ▼
    🎯 JEE Test Screen
        │
        └─ "🚀 Take Test" tab selected
            │
            └─ Taps "🚀 Start Full Mock Test"
                │
                ▼
            🎮 TEST INTERFACE:
                │
                ├─ ⏱️ Timer: 3:00:00 countdown
                ├─ 📊 Progress: Question 1/75
                ├─ 📝 Question Display
                ├─ 🔘 Answer Options (MCQ) or 🔢 Number Input (Numerical)
                ├─ [⭐ Mark for Review] [➡️ Next] buttons
                │
                └─ After 75 questions or time up:
                    │
                    ▼
                📊 RESULTS SCREEN:
                    │
                    ├─ 🎯 Total Score: 255/300 (85%)
                    ├─ 🏆 Estimated Rank: AIR 2,847
                    ├─ 📈 Subject Scores:
                    │   ├─ Mathematics: 92% (23/25)
                    │   ├─ Physics: 78% (19.5/25)
                    │   └─ Chemistry: 85% (21.25/25)
                    ├─ ⏱️ Time Taken: 2h 45m
                    ├─ ✅ Correct: 58, ❌ Wrong: 12, ⚪ Skipped: 5
                    │
                    └─ 💡 Analysis & Recommendations:
                        ├─ "Strong in Mathematics - keep it up!"
                        ├─ "Work on Physics numericals"
                        └─ "Focus on Organic Chemistry"
```

### 🤔 **Scenario 3: Student has a math doubt**

```
📱 Opens Klaro
    │
    ▼
🏠 Home Screen
    │
    └─ Taps "🤔 AI Doubt Solver"
        │
        ▼
    🤔 Doubt Solver Screen
        │
        └─ "📝 Ask Doubt" tab selected
            │
            ├─ OPTION A: Text Input
            │   │
            │   ├─ Types: "Solve x² + 5x + 6 = 0"
            │   ├─ Selects Subject: Mathematics
            │   └─ Taps "🤖 Solve My Doubt"
            │
            └─ OPTION B: Camera Input
                │
                ├─ Taps "📸 Camera"
                ├─ 📷 Camera opens
                ├─ Takes photo of math problem
                ├─ 🔍 OCR processes image
                ├─ 📝 Extracted text shown for verification
                └─ Taps "🤖 Solve My Doubt"
                │
                ▼
            ⏳ AI PROCESSING:
                │
                ├─ "Solving..." (Loading animation)
                ├─ 🤖 AI Engine tries:
                │   ├─ 📚 Textbook search (Free)
                │   ├─ 🔬 Wolfram Alpha (₹0.0025)
                │   ├─ 🤖 GPT-3.5 (₹0.004)
                │   └─ 🧠 GPT-4 if Premium (₹0.09)
                │
                ▼
            ✅ SOLUTION DISPLAYED:
                │
                ├─ ❓ Question: "Solve x² + 5x + 6 = 0"
                ├─ ✅ Answer: "x = -2 or x = -3"
                ├─ 📋 Solution Steps:
                │   ├─ Step 1: Identify equation (a=1, b=5, c=6)
                │   ├─ Step 2: Apply factoring ((x+2)(x+3)=0)
                │   └─ Step 3: Solve for x (x=-2 or x=-3)
                ├─ 🎯 Confidence: 98%
                ├─ 🔬 Method: Wolfram Alpha
                ├─ 💰 Cost: ₹0.0025
                │
                └─ Actions:
                    ├─ [💾 Save Solution]
                    ├─ [📤 Share Solution]
                    └─ ➕ Added to "Recent Doubts"
```

---

## 🔄 NAVIGATION FLOW BETWEEN FEATURES

```
🏠 HOME ←──────────┐
    │               │
    ↕️               │
📄 PDF GENERATOR    │
    ↕️               │
🎯 JEE TESTS ←──────┤  👆 Bottom Navigation
    ↕️               │     Always Available
🤔 DOUBT SOLVER     │
    ↕️               │
👤 PROFILE ←────────┘

USER CAN:
• Tap any bottom nav icon to switch features instantly
• Use back button to return to previous screen
• Access all features without losing progress
```

---

## 📊 BACKEND API INTEGRATION FLOW

```
📱 ANDROID APP                    🌐 FASTAPI BACKEND
     │                               │
     ├─ PDF Generation ─────────────► /api/quiz/create
     │   └─ Downloads PDF ←──────────── File Response
     │
     ├─ JEE Tests ──────────────────► /api/jee/test/create
     │   ├─ Submit Answers ─────────► /api/jee/test/{id}/submit
     │   └─ Get Results ←───────────── JSON Response
     │
     ├─ Text Doubts ────────────────► /api/doubt/solve-enhanced
     │   └─ Get Solution ←──────────── JSON Response
     │
     ├─ Image Doubts ───────────────► /api/doubt/solve-image
     │   └─ OCR + Solution ←────────── JSON Response
     │
     ├─ User Profile ───────────────► /api/user/profile
     │   └─ User Data ←─────────────── JSON Response
     │
     └─ Analytics ──────────────────► /api/analytics/*
         └─ Usage Stats ←───────────── JSON Response
```

---

## 🎯 KEY USER BENEFITS

### ⚡ **Quick & Easy**:
```
🤔 Student has doubt ──► 📱 Opens Klaro ──► 🤖 Gets solution in 10 seconds
```

### 🎯 **Complete JEE Prep**:
```
📚 Student needs practice ──► 🎯 Takes mock test ──► 📊 Gets detailed analysis ──► 📈 Improves
```

### 📄 **Custom Practice**:
```
👨‍🏫 Teacher needs quiz ──► 📄 Generates custom PDF ──► 📥 Downloads ──► 🖨️ Prints for class
```

---

## 🚀 **SUMMARY: Complete User Experience**

**🎓 Klaro provides a seamless educational experience where users can:**

1. **📄 Generate custom practice tests** instantly
2. **🎯 Take JEE mock tests** with real-time analytics  
3. **🤔 Solve doubts** using AI with text or camera input
4. **📊 Track progress** with detailed analytics
5. **💎 Upgrade plans** for premium features

**All features are interconnected and accessible through intuitive bottom navigation!** 🎉
