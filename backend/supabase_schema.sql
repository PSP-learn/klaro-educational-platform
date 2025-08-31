-- ================================================================================
-- 🟢 Klaro Educational Platform - Supabase Schema
-- ================================================================================
-- This schema creates all the required tables for the Klaro educational platform
-- Run this in your Supabase SQL editor after creating the project
-- ================================================================================

-- 🔄 CLEAN SLATE SETUP
-- This will safely remove existing objects and recreate everything
-- Safe to run multiple times without errors

-- Drop existing policies first (if they exist)
DROP POLICY IF EXISTS "Users can view their own profile" ON users;
DROP POLICY IF EXISTS "Users can update their own profile" ON users;
DROP POLICY IF EXISTS "Users can view their own doubts" ON doubts;
DROP POLICY IF EXISTS "Users can insert their own doubts" ON doubts;
DROP POLICY IF EXISTS "Users can view their own quiz history" ON quiz_history;
DROP POLICY IF EXISTS "Users can insert their own quiz records" ON quiz_history;
DROP POLICY IF EXISTS "Users can view their own test results" ON jee_test_results;
DROP POLICY IF EXISTS "Users can insert their own test results" ON jee_test_results;
DROP POLICY IF EXISTS "Users can view their own analytics" ON usage_analytics;
DROP POLICY IF EXISTS "Service can insert analytics" ON usage_analytics;
DROP POLICY IF EXISTS "Users can view their own sessions" ON user_sessions;
DROP POLICY IF EXISTS "Users can manage their own sessions" ON user_sessions;
DROP POLICY IF EXISTS "Users can view their own files" ON file_metadata;
DROP POLICY IF EXISTS "Users can insert their own files" ON file_metadata;
DROP POLICY IF EXISTS "Users can view their own notifications" ON notifications;
DROP POLICY IF EXISTS "Users can update their own notifications" ON notifications;
DROP POLICY IF EXISTS "Service can insert notifications" ON notifications;
DROP POLICY IF EXISTS "Users can view their own progress" ON user_progress;
DROP POLICY IF EXISTS "Service can manage progress" ON user_progress;

-- Drop existing views (if they exist)
DROP VIEW IF EXISTS daily_user_activity;
DROP VIEW IF EXISTS user_performance_summary;

-- Drop existing tables (in reverse dependency order)
DROP TABLE IF EXISTS user_progress;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS file_metadata;
DROP TABLE IF EXISTS user_sessions;
DROP TABLE IF EXISTS usage_analytics;
DROP TABLE IF EXISTS jee_test_results;
DROP TABLE IF EXISTS quiz_history;
DROP TABLE IF EXISTS doubts;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS users;

-- Drop existing functions and triggers
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Enable Row Level Security (RLS) by default
-- This ensures users can only access their own data

-- ================================================================================
-- 👤 Users Table (extends Supabase Auth)
-- ================================================================================

CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    total_doubts_solved INTEGER DEFAULT 0,
    total_quizzes_generated INTEGER DEFAULT 0,
    total_jee_tests_taken INTEGER DEFAULT 0,
    subscription_status TEXT DEFAULT 'free' CHECK (subscription_status IN ('free', 'premium', 'unlimited')),
    preferences JSONB DEFAULT '{}',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can only see their own profile
CREATE POLICY "Users can view their own profile" ON users
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update their own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- ================================================================================
-- 🤔 Doubts Table
-- ================================================================================

CREATE TABLE doubts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    solution_data JSONB NOT NULL DEFAULT '{}',
    subject TEXT DEFAULT 'Mathematics',
    method_used TEXT DEFAULT 'unknown',
    cost_incurred DECIMAL(10,4) DEFAULT 0.0,
    time_taken DECIMAL(10,2) DEFAULT 0.0,
    confidence_score DECIMAL(5,2) DEFAULT 0.0,
    route TEXT DEFAULT 'doubts',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE doubts ENABLE ROW LEVEL SECURITY;

-- Users can only see their own doubts
CREATE POLICY "Users can view their own doubts" ON doubts
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own doubts
CREATE POLICY "Users can insert their own doubts" ON doubts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create indexes for performance
CREATE INDEX idx_doubts_user_id ON doubts(user_id);
CREATE INDEX idx_doubts_created_at ON doubts(created_at DESC);
CREATE INDEX idx_doubts_subject ON doubts(subject);

-- ================================================================================
-- 📄 Quiz History Table
-- ================================================================================

CREATE TABLE quiz_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quiz_title TEXT NOT NULL,
    topics TEXT[] DEFAULT '{}',
    questions_count INTEGER DEFAULT 0,
    difficulty_levels TEXT[] DEFAULT '{}',
    quiz_file_url TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE quiz_history ENABLE ROW LEVEL SECURITY;

-- Users can only see their own quiz history
CREATE POLICY "Users can view their own quiz history" ON quiz_history
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own quiz records
CREATE POLICY "Users can insert their own quiz records" ON quiz_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create indexes
CREATE INDEX idx_quiz_history_user_id ON quiz_history(user_id);
CREATE INDEX idx_quiz_history_created_at ON quiz_history(created_at DESC);

-- ================================================================================
-- 🎯 JEE Test Results Table
-- ================================================================================

CREATE TABLE jee_test_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    test_id TEXT NOT NULL,
    test_type TEXT DEFAULT 'full_mock' CHECK (test_type IN ('full_mock', 'subject_wise', 'chapter_wise', 'practice')),
    total_score INTEGER DEFAULT 0,
    max_score INTEGER DEFAULT 300,
    subject_scores JSONB DEFAULT '{}',
    time_taken INTEGER DEFAULT 0, -- in minutes
    questions_attempted INTEGER DEFAULT 0,
    questions_correct INTEGER DEFAULT 0,
    questions_incorrect INTEGER DEFAULT 0,
    questions_unanswered INTEGER DEFAULT 0,
    percentile DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE jee_test_results ENABLE ROW LEVEL SECURITY;

-- Users can only see their own test results
CREATE POLICY "Users can view their own test results" ON jee_test_results
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own test results
CREATE POLICY "Users can insert their own test results" ON jee_test_results
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create indexes
CREATE INDEX idx_jee_results_user_id ON jee_test_results(user_id);
CREATE INDEX idx_jee_results_created_at ON jee_test_results(created_at DESC);
CREATE INDEX idx_jee_results_test_type ON jee_test_results(test_type);

-- ================================================================================
-- 📊 Usage Analytics Table
-- ================================================================================

CREATE TABLE usage_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    route TEXT NOT NULL,
    method TEXT NOT NULL,
    cost DECIMAL(10,4) DEFAULT 0.0,
    success BOOLEAN DEFAULT TRUE,
    response_time DECIMAL(10,3) DEFAULT 0.0, -- in seconds
    error_message TEXT DEFAULT '',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE usage_analytics ENABLE ROW LEVEL SECURITY;

-- Users can only see their own analytics
CREATE POLICY "Users can view their own analytics" ON usage_analytics
    FOR SELECT USING (auth.uid() = user_id);

-- Service role can insert analytics (bypasses RLS)
CREATE POLICY "Service can insert analytics" ON usage_analytics
    FOR INSERT WITH CHECK (TRUE);

-- Create indexes
CREATE INDEX idx_analytics_user_id ON usage_analytics(user_id);
CREATE INDEX idx_analytics_created_at ON usage_analytics(created_at DESC);
CREATE INDEX idx_analytics_route ON usage_analytics(route);

-- ================================================================================
-- 📱 User Sessions Table (for mobile app state)
-- ================================================================================

CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id TEXT NOT NULL,
    device_type TEXT DEFAULT 'android' CHECK (device_type IN ('android', 'ios', 'web')),
    app_version TEXT DEFAULT '1.0.0',
    session_token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;

-- Users can only see their own sessions
CREATE POLICY "Users can view their own sessions" ON user_sessions
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert/update their own sessions
CREATE POLICY "Users can manage their own sessions" ON user_sessions
    FOR ALL USING (auth.uid() = user_id);

-- Create indexes
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_sessions_active ON user_sessions(is_active, expires_at);

-- ================================================================================
-- 📁 File Storage Metadata Table
-- ================================================================================

CREATE TABLE file_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL CHECK (file_type IN ('pdf_quiz', 'doubt_image', 'profile_image')),
    file_size INTEGER DEFAULT 0,
    storage_path TEXT NOT NULL,
    public_url TEXT DEFAULT '',
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE file_metadata ENABLE ROW LEVEL SECURITY;

-- Users can only see their own files
CREATE POLICY "Users can view their own files" ON file_metadata
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own files
CREATE POLICY "Users can insert their own files" ON file_metadata
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create indexes
CREATE INDEX idx_files_user_id ON file_metadata(user_id);
CREATE INDEX idx_files_type ON file_metadata(file_type);
CREATE INDEX idx_files_created_at ON file_metadata(created_at DESC);

-- ================================================================================
-- 🔔 Notifications Table
-- ================================================================================

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info' CHECK (type IN ('info', 'success', 'warning', 'error')),
    is_read BOOLEAN DEFAULT FALSE,
    action_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Users can only see their own notifications
CREATE POLICY "Users can view their own notifications" ON notifications
    FOR SELECT USING (auth.uid() = user_id);

-- Users can update their own notifications (mark as read)
CREATE POLICY "Users can update their own notifications" ON notifications
    FOR UPDATE USING (auth.uid() = user_id);

-- Service can insert notifications
CREATE POLICY "Service can insert notifications" ON notifications
    FOR INSERT WITH CHECK (TRUE);

-- Create indexes
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = FALSE;

-- ================================================================================
-- 📈 User Progress Tracking
-- ================================================================================

CREATE TABLE user_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    feature TEXT NOT NULL CHECK (feature IN ('doubt_solver', 'pdf_generator', 'jee_tests')),
    metric_name TEXT NOT NULL,
    metric_value DECIMAL(15,4) DEFAULT 0.0,
    date_recorded DATE DEFAULT CURRENT_DATE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Unique constraint to prevent duplicate metrics per day
    UNIQUE(user_id, feature, metric_name, date_recorded)
);

-- Enable RLS
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;

-- Users can only see their own progress
CREATE POLICY "Users can view their own progress" ON user_progress
    FOR SELECT USING (auth.uid() = user_id);

-- Service can insert/update progress
CREATE POLICY "Service can manage progress" ON user_progress
    FOR ALL WITH CHECK (TRUE);

-- Create indexes
CREATE INDEX idx_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_progress_feature ON user_progress(feature);
CREATE INDEX idx_progress_date ON user_progress(date_recorded DESC);

-- ================================================================================
-- 🔧 Database Functions and Triggers
-- ================================================================================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply the trigger to all tables with updated_at columns
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_doubts_updated_at BEFORE UPDATE ON doubts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quiz_history_updated_at BEFORE UPDATE ON quiz_history
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jee_test_results_updated_at BEFORE UPDATE ON jee_test_results
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_sessions_updated_at BEFORE UPDATE ON user_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ================================================================================
-- 📊 Useful Views for Analytics
-- ================================================================================

-- Daily user activity summary
CREATE OR REPLACE VIEW daily_user_activity AS
SELECT 
    user_id,
    DATE(created_at) as activity_date,
    COUNT(*) as total_activities,
    COUNT(CASE WHEN route = 'doubts' THEN 1 END) as doubts_solved,
    COUNT(CASE WHEN route = 'quiz' THEN 1 END) as quizzes_generated,
    COUNT(CASE WHEN route = 'jee' THEN 1 END) as jee_activities,
    SUM(cost) as total_cost,
    AVG(response_time) as avg_response_time
FROM usage_analytics 
GROUP BY user_id, DATE(created_at)
ORDER BY activity_date DESC;

-- User performance summary
CREATE OR REPLACE VIEW user_performance_summary AS
SELECT 
    u.id,
    u.name,
    u.email,
    u.total_doubts_solved,
    u.total_quizzes_generated,
    u.total_jee_tests_taken,
    COALESCE(AVG(jtr.total_score), 0) as avg_jee_score,
    COALESCE(AVG(jtr.percentile), 0) as avg_percentile,
    u.created_at,
    u.last_active
FROM users u
LEFT JOIN jee_test_results jtr ON u.id = jtr.user_id
GROUP BY u.id, u.name, u.email, u.total_doubts_solved, u.total_quizzes_generated, u.total_jee_tests_taken, u.created_at, u.last_active;

-- ================================================================================
-- 📚 Subjects Table (create before sample data)
-- ================================================================================

CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    icon TEXT DEFAULT '📚',
    description TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ================================================================================
-- 🚀 Sample Data (Optional - for testing)
-- ================================================================================

-- Insert sample subjects for easier filtering
INSERT INTO subjects (name, icon) VALUES 
    ('Mathematics', '📐'),
    ('Physics', '⚛️'),
    ('Chemistry', '🧪'),
    ('Biology', '🧬'),
    ('General', '📚')
ON CONFLICT (name) DO NOTHING;

-- Create subjects table if it doesn't exist
CREATE TABLE IF NOT EXISTS subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    icon TEXT DEFAULT '📚',
    description TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ================================================================================
-- 🎉 Setup Complete!
-- ================================================================================

-- You can now run the following to verify everything is set up:
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

COMMENT ON SCHEMA public IS 'Klaro Educational Platform - Production Ready Schema';
