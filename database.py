#!/usr/bin/env python3
"""
🗄️ PostgreSQL Database Layer for Klaro

Complete database schema and async connection management for:
- User management & authentication
- Doubt solving history
- Usage analytics & billing
- Subscription management
"""

import asyncio
import asyncpg
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import os
from contextlib import asynccontextmanager

# ================================================================================
# 📊 Database Models
# ================================================================================

@dataclass
class User:
    user_id: str
    email: str
    name: str
    phone: Optional[str]
    plan: str  # 'basic' or 'premium'
    created_at: datetime
    last_active: Optional[datetime]
    subscription_expires: Optional[datetime]
    total_doubts_solved: int = 0
    favorite_subjects: List[str] = None

@dataclass
class DoubtRecord:
    doubt_id: str
    user_id: str
    question_text: str
    image_data: Optional[bytes]
    subject: str
    solution_text: str
    steps: List[Dict]
    metadata: Dict
    method_used: str
    cost_incurred: float
    time_taken: float
    confidence_score: float
    created_at: datetime
    route: str

@dataclass
class UsageRecord:
    usage_id: str
    user_id: str
    route: str
    method: str
    cost: float
    tokens_used: int
    timestamp: datetime
    success: bool
    error_message: Optional[str]

# ================================================================================
# 🔌 Database Connection Manager
# ================================================================================

class PostgreSQLManager:
    """Async PostgreSQL connection manager with pooling"""
    
    def __init__(self, database_url: str, min_connections: int = 5, max_connections: int = 20):
        self.database_url = database_url
        self.min_connections = min_connections
        self.max_connections = max_connections
        self.pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=self.min_connections,
                max_size=self.max_connections,
                command_timeout=30,
                server_settings={
                    'application_name': 'klaro_api',
                    'jit': 'off'
                }
            )
            
            # Create tables if they don't exist
            await self.create_tables()
            print("🗄️ PostgreSQL connection pool initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize PostgreSQL: {e}")
            raise
    
    async def close(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self.pool.acquire() as connection:
            yield connection
    
    async def create_tables(self):
        """Create all necessary tables"""
        
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(255) PRIMARY KEY,
            email VARCHAR(255) UNIQUE,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            plan VARCHAR(20) DEFAULT 'basic',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            last_active TIMESTAMP WITH TIME ZONE,
            subscription_expires TIMESTAMP WITH TIME ZONE,
            total_doubts_solved INTEGER DEFAULT 0,
            favorite_subjects JSONB DEFAULT '[]'::jsonb,
            metadata JSONB DEFAULT '{}'::jsonb
        );
        """
        
        create_doubts_table = """
        CREATE TABLE IF NOT EXISTS doubts (
            doubt_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) REFERENCES users(user_id),
            question_text TEXT,
            image_data BYTEA,
            subject VARCHAR(100),
            solution_text TEXT,
            steps JSONB,
            metadata JSONB,
            method_used VARCHAR(50),
            cost_incurred DECIMAL(10,6),
            time_taken DECIMAL(8,3),
            confidence_score DECIMAL(5,4),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            route VARCHAR(50),
            saved BOOLEAN DEFAULT FALSE
        );
        """
        
        create_usage_table = """
        CREATE TABLE IF NOT EXISTS usage_analytics (
            usage_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) REFERENCES users(user_id),
            route VARCHAR(50),
            method VARCHAR(50),
            cost DECIMAL(10,6),
            tokens_used INTEGER,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            success BOOLEAN,
            error_message TEXT,
            request_metadata JSONB
        );
        """
        
        create_subscriptions_table = """
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) REFERENCES users(user_id),
            plan VARCHAR(20) NOT NULL,
            start_date TIMESTAMP WITH TIME ZONE,
            end_date TIMESTAMP WITH TIME ZONE,
            payment_method VARCHAR(50),
            amount DECIMAL(10,2),
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Create indexes for performance
        create_indexes = [
            "CREATE INDEX IF NOT EXISTS idx_doubts_user_id ON doubts(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_doubts_created_at ON doubts(created_at);",
            "CREATE INDEX IF NOT EXISTS idx_usage_user_id ON usage_analytics(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_usage_timestamp ON usage_analytics(timestamp);",
            "CREATE INDEX IF NOT EXISTS idx_usage_route ON usage_analytics(route);",
            "CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);"
        ]
        
        async with self.get_connection() as conn:
            await conn.execute(create_users_table)
            await conn.execute(create_doubts_table)
            await conn.execute(create_usage_table)
            await conn.execute(create_subscriptions_table)
            
            for index_query in create_indexes:
                await conn.execute(index_query)

# ================================================================================
# 👤 User Database Operations
# ================================================================================

class UserDatabase:
    """User management database operations"""
    
    def __init__(self, db_manager: PostgreSQLManager):
        self.db = db_manager
    
    async def create_user(self, user: User) -> bool:
        """Create a new user"""
        query = """
        INSERT INTO users (user_id, email, name, phone, plan, created_at, favorite_subjects)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (user_id) DO UPDATE SET
            last_active = NOW()
        """
        
        async with self.db.get_connection() as conn:
            await conn.execute(
                query,
                user.user_id, user.email, user.name, user.phone,
                user.plan, user.created_at, json.dumps(user.favorite_subjects or [])
            )
        return True
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = $1"
        
        async with self.db.get_connection() as conn:
            row = await conn.fetchrow(query, user_id)
            if row:
                return User(
                    user_id=row['user_id'],
                    email=row['email'],
                    name=row['name'],
                    phone=row['phone'],
                    plan=row['plan'],
                    created_at=row['created_at'],
                    last_active=row['last_active'],
                    subscription_expires=row['subscription_expires'],
                    total_doubts_solved=row['total_doubts_solved'],
                    favorite_subjects=json.loads(row['favorite_subjects']) if row['favorite_subjects'] else []
                )
        return None
    
    async def update_user_activity(self, user_id: str):
        """Update user's last active timestamp"""
        query = "UPDATE users SET last_active = NOW() WHERE user_id = $1"
        
        async with self.db.get_connection() as conn:
            await conn.execute(query, user_id)
    
    async def increment_doubts_solved(self, user_id: str):
        """Increment user's total doubts solved counter"""
        query = "UPDATE users SET total_doubts_solved = total_doubts_solved + 1 WHERE user_id = $1"
        
        async with self.db.get_connection() as conn:
            await conn.execute(query, user_id)

# ================================================================================
# 💭 Doubt History Database Operations
# ================================================================================

class DoubtDatabase:
    """Doubt records database operations"""
    
    def __init__(self, db_manager: PostgreSQLManager):
        self.db = db_manager
    
    async def save_doubt(self, doubt: DoubtRecord) -> bool:
        """Save solved doubt to database"""
        query = """
        INSERT INTO doubts (
            doubt_id, user_id, question_text, image_data, subject,
            solution_text, steps, metadata, method_used, cost_incurred,
            time_taken, confidence_score, created_at, route
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
        """
        
        async with self.db.get_connection() as conn:
            await conn.execute(
                query,
                doubt.doubt_id, doubt.user_id, doubt.question_text, doubt.image_data,
                doubt.subject, doubt.solution_text, json.dumps(doubt.steps),
                json.dumps(doubt.metadata), doubt.method_used, doubt.cost_incurred,
                doubt.time_taken, doubt.confidence_score, doubt.created_at, doubt.route
            )
        return True
    
    async def get_user_doubts(
        self, 
        user_id: str, 
        limit: int = 20, 
        offset: int = 0,
        subject: Optional[str] = None
    ) -> Tuple[List[DoubtRecord], int]:
        """Get user's doubt history with pagination"""
        
        where_clause = "WHERE user_id = $1"
        params = [user_id]
        
        if subject:
            where_clause += " AND subject = $2"
            params.append(subject)
        
        # Count query
        count_query = f"SELECT COUNT(*) FROM doubts {where_clause}"
        
        # Data query
        data_query = f"""
        SELECT * FROM doubts {where_clause}
        ORDER BY created_at DESC
        LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
        """
        params.extend([limit, offset])
        
        async with self.db.get_connection() as conn:
            total_count = await conn.fetchval(count_query, *params[:-2])
            rows = await conn.fetch(data_query, *params)
            
            doubts = [
                DoubtRecord(
                    doubt_id=row['doubt_id'],
                    user_id=row['user_id'],
                    question_text=row['question_text'],
                    image_data=row['image_data'],
                    subject=row['subject'],
                    solution_text=row['solution_text'],
                    steps=json.loads(row['steps']) if row['steps'] else [],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    method_used=row['method_used'],
                    cost_incurred=float(row['cost_incurred']),
                    time_taken=float(row['time_taken']),
                    confidence_score=float(row['confidence_score']),
                    created_at=row['created_at'],
                    route=row['route']
                )
                for row in rows
            ]
            
        return doubts, total_count
    
    async def save_doubt_to_favorites(self, doubt_id: str, user_id: str) -> bool:
        """Mark doubt as saved/favorite"""
        query = """
        UPDATE doubts SET saved = TRUE 
        WHERE doubt_id = $1 AND user_id = $2
        """
        
        async with self.db.get_connection() as conn:
            result = await conn.execute(query, doubt_id, user_id)
            return "UPDATE 1" in result

# ================================================================================
# 📊 Analytics Database Operations
# ================================================================================

class AnalyticsDatabase:
    """Usage analytics database operations"""
    
    def __init__(self, db_manager: PostgreSQLManager):
        self.db = db_manager
    
    async def record_usage(self, usage: UsageRecord) -> bool:
        """Record API usage"""
        query = """
        INSERT INTO usage_analytics (
            usage_id, user_id, route, method, cost, tokens_used,
            timestamp, success, error_message, request_metadata
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        """
        
        async with self.db.get_connection() as conn:
            await conn.execute(
                query,
                usage.usage_id, usage.user_id, usage.route, usage.method,
                usage.cost, usage.tokens_used, usage.timestamp,
                usage.success, usage.error_message, json.dumps({})
            )
        return True
    
    async def get_user_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        
        since_date = datetime.now() - timedelta(days=days)
        
        queries = {
            "total_usage": """
                SELECT 
                    COUNT(*) as total_requests,
                    SUM(cost) as total_cost,
                    AVG(cost) as avg_cost_per_request,
                    COUNT(*) FILTER (WHERE success = true) as successful_requests
                FROM usage_analytics 
                WHERE user_id = $1 AND timestamp >= $2
            """,
            
            "route_breakdown": """
                SELECT 
                    route, 
                    COUNT(*) as count,
                    SUM(cost) as total_cost,
                    AVG(cost) as avg_cost
                FROM usage_analytics 
                WHERE user_id = $1 AND timestamp >= $2
                GROUP BY route
                ORDER BY count DESC
            """,
            
            "method_breakdown": """
                SELECT 
                    method,
                    COUNT(*) as count,
                    SUM(cost) as total_cost
                FROM usage_analytics 
                WHERE user_id = $1 AND timestamp >= $2
                GROUP BY method
                ORDER BY total_cost DESC
            """,
            
            "daily_usage": """
                SELECT 
                    DATE(timestamp) as usage_date,
                    COUNT(*) as requests,
                    SUM(cost) as daily_cost
                FROM usage_analytics 
                WHERE user_id = $1 AND timestamp >= $2
                GROUP BY DATE(timestamp)
                ORDER BY usage_date DESC
            """
        }
        
        async with self.db.get_connection() as conn:
            results = {}
            
            for key, query in queries.items():
                rows = await conn.fetch(query, user_id, since_date)
                results[key] = [dict(row) for row in rows]
            
            return results
    
    async def get_system_analytics(self, days: int = 1) -> Dict[str, Any]:
        """Get system-wide analytics"""
        
        since_date = datetime.now() - timedelta(days=days)
        
        query = """
        SELECT 
            COUNT(*) as total_requests,
            SUM(cost) as total_cost,
            COUNT(DISTINCT user_id) as unique_users,
            AVG(cost) as avg_cost_per_request,
            COUNT(*) FILTER (WHERE success = true) as successful_requests,
            COUNT(*) FILTER (WHERE success = false) as failed_requests
        FROM usage_analytics 
        WHERE timestamp >= $1
        """
        
        async with self.db.get_connection() as conn:
            row = await conn.fetchrow(query, since_date)
            return dict(row) if row else {}

# ================================================================================
# 💳 Subscription Database Operations
# ================================================================================

class SubscriptionDatabase:
    """Subscription management database operations"""
    
    def __init__(self, db_manager: PostgreSQLManager):
        self.db = db_manager
    
    async def create_subscription(
        self,
        user_id: str,
        plan: str,
        duration_months: int = 1,
        payment_method: str = "card"
    ) -> str:
        """Create new subscription"""
        
        subscription_id = f"sub_{user_id}_{int(datetime.now().timestamp())}"
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30 * duration_months)
        
        # Plan pricing
        plan_prices = {"basic": 0.0, "premium": 299.0}  # INR
        amount = plan_prices.get(plan, 0.0)
        
        query = """
        INSERT INTO subscriptions (
            subscription_id, user_id, plan, start_date, end_date,
            payment_method, amount, status
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """
        
        async with self.db.get_connection() as conn:
            await conn.execute(
                query,
                subscription_id, user_id, plan, start_date, end_date,
                payment_method, amount, "active"
            )
            
            # Update user's plan and expiry
            update_user_query = """
            UPDATE users 
            SET plan = $1, subscription_expires = $2 
            WHERE user_id = $3
            """
            await conn.execute(update_user_query, plan, end_date, user_id)
        
        return subscription_id
    
    async def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's active subscription"""
        
        query = """
        SELECT * FROM subscriptions 
        WHERE user_id = $1 AND status = 'active' AND end_date > NOW()
        ORDER BY end_date DESC
        LIMIT 1
        """
        
        async with self.db.get_connection() as conn:
            row = await conn.fetchrow(query, user_id)
            return dict(row) if row else None

# ================================================================================
# 🏗️ Database Factory & Setup
# ================================================================================

class KlaroDatabase:
    """Main database interface combining all operations"""
    
    def __init__(self, database_url: str):
        self.manager = PostgreSQLManager(database_url)
        self.users = UserDatabase(self.manager)
        self.doubts = DoubtDatabase(self.manager)
        self.analytics = AnalyticsDatabase(self.manager)
        self.subscriptions = SubscriptionDatabase(self.manager)
    
    async def initialize(self):
        """Initialize all database components"""
        await self.manager.initialize()
    
    async def close(self):
        """Close database connections"""
        await self.manager.close()

# ================================================================================
# 🧪 Development Database Setup
# ================================================================================

async def setup_development_data(db: KlaroDatabase):
    """Setup mock data for development"""
    
    # Create test users
    test_users = [
        User(
            user_id="user_123",
            email="test@example.com",
            name="Test User",
            phone="+919876543210",
            plan="basic",
            created_at=datetime.now(),
            favorite_subjects=["Mathematics", "Physics"]
        ),
        User(
            user_id="premium_user",
            email="premium@example.com",
            name="Premium User",
            phone="+919876543211",
            plan="premium",
            created_at=datetime.now() - timedelta(days=30),
            favorite_subjects=["Chemistry", "Biology"]
        )
    ]
    
    for user in test_users:
        await db.users.create_user(user)
    
    print("✅ Development data setup complete")

# ================================================================================
# 🌐 Database Configuration
# ================================================================================

def get_database_url() -> str:
    """Get database URL from environment or use SQLite for development"""
    
    # Production PostgreSQL URL
    postgres_url = os.getenv("DATABASE_URL")
    if postgres_url:
        return postgres_url
    
    # Development fallback to PostgreSQL on localhost
    return "postgresql://postgres:password@localhost:5432/klaro_dev"

# Global database instance
db_instance: Optional[KlaroDatabase] = None

async def get_database() -> KlaroDatabase:
    """Get database instance"""
    global db_instance
    
    if not db_instance:
        database_url = get_database_url()
        db_instance = KlaroDatabase(database_url)
        await db_instance.initialize()
        
        # Setup development data if needed
        if "localhost" in database_url:
            await setup_development_data(db_instance)
    
    return db_instance

# ================================================================================
# 🧪 Database Testing Functions
# ================================================================================

async def test_database_operations():
    """Test all database operations"""
    
    db = await get_database()
    
    # Test user operations
    test_user = User(
        user_id="test_db_user",
        email="dbtest@example.com",
        name="DB Test User",
        phone="+919999999999",
        plan="basic",
        created_at=datetime.now(),
        favorite_subjects=["Mathematics"]
    )
    
    await db.users.create_user(test_user)
    retrieved_user = await db.users.get_user("test_db_user")
    
    print(f"✅ User operations test: {retrieved_user.name if retrieved_user else 'Failed'}")
    
    # Test analytics
    test_usage = UsageRecord(
        usage_id="test_usage_1",
        user_id="test_db_user",
        route="doubts",
        method="gpt35",
        cost=0.004,
        tokens_used=150,
        timestamp=datetime.now(),
        success=True,
        error_message=None
    )
    
    await db.analytics.record_usage(test_usage)
    user_analytics = await db.analytics.get_user_analytics("test_db_user")
    
    print(f"✅ Analytics operations test: {len(user_analytics)} metrics recorded")

if __name__ == "__main__":
    # Test database operations
    asyncio.run(test_database_operations())
