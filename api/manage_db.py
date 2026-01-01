"""
Database Setup & Migration Guide
Initialize and manage database schema for persistent storage
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, engine
from models import Base


def setup_database():
    """
    Initialize database with all tables
    Run this once after first deployment
    """
    print("🚀 Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully!")
        print(f"✅ All tables created")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


def reset_database():
    """
    DANGER: Drop all tables and recreate
    Only use in development
    """
    response = input("⚠️ WARNING: This will DELETE all data! Type 'yes' to confirm: ")
    
    if response.lower() != 'yes':
        print("Cancelled")
        return False
    
    print("Dropping all tables...")
    try:
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped")
        
        print("Recreating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables recreated")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_connection():
    """Check database connection"""
    print("🔍 Checking database connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute(__import__('sqlalchemy').text('SELECT 1'))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def get_stats():
    """Get database statistics"""
    from database import get_session
    from models import User, Conversation, Analytics, ProductView
    
    session = get_session()
    try:
        user_count = session.query(User).count()
        conversation_count = session.query(Conversation).count()
        analytics_count = session.query(Analytics).count()
        product_views = session.query(ProductView).count()
        
        print("\n📊 Database Statistics:")
        print(f"  Users: {user_count}")
        print(f"  Conversations: {conversation_count}")
        print(f"  Analytics Events: {analytics_count}")
        print(f"  Product Views: {product_views}")
        
    finally:
        session.close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Database management utilities')
    parser.add_argument('command', choices=['init', 'check', 'stats', 'reset'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        setup_database()
    elif args.command == 'check':
        check_connection()
    elif args.command == 'stats':
        get_stats()
    elif args.command == 'reset':
        reset_database()
