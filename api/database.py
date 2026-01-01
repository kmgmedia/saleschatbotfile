"""
Database Connection Manager
Handles database initialization, session management, and utilities
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

try:
    from .models import Base, User, Conversation, Analytics, ConversationSession, ProductView, ChatMessageHistory
except ImportError:
    from models import Base, User, Conversation, Analytics, ConversationSession, ProductView, ChatMessageHistory

# Database configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'sqlite:///saleschatbot.db'  # Default to SQLite for local development
)

# Handle Vercel's postgres:// to postgresql://
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create engine with proper settings
if 'sqlite' in DATABASE_URL:
    # For SQLite (local development)
    engine = create_engine(
        DATABASE_URL,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
        echo=False
    )
else:
    # For PostgreSQL (production)
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=3600
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully", file=sys.stderr)
    except Exception as e:
        print(f"❌ Database initialization error: {e}", file=sys.stderr)
        raise


def get_session() -> Session:
    """Get a new database session"""
    return SessionLocal()


def get_or_create_user(user_id: int, username: str = None, first_name: str = None) -> User:
    """
    Get existing user or create new one
    
    Args:
        user_id: Telegram user ID
        username: Telegram username
        first_name: User's first name
    
    Returns:
        User object
    """
    session = get_session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name
            )
            session.add(user)
            session.commit()
            print(f"✅ New user created: {user_id}", file=sys.stderr)
        else:
            # Update last active
            user.last_active = __import__('datetime').datetime.utcnow()
            session.commit()
        
        return user
    finally:
        session.close()


def save_conversation(
    user_id: int,
    user_message: str,
    bot_response: str,
    current_product: str = None,
    emotion_detected: str = None,
    intent: str = None
) -> Conversation:
    """
    Save conversation to database
    
    Args:
        user_id: Telegram user ID
        user_message: User's message
        bot_response: Bot's response
        current_product: Product being discussed
        emotion_detected: Detected emotion (frustration, urgency, etc.)
        intent: User intent (price, buy, specs, etc.)
    
    Returns:
        Conversation object
    """
    session = get_session()
    try:
        conversation = Conversation(
            user_id=user_id,
            user_message=user_message,
            bot_response=bot_response,
            current_product=current_product,
            emotion_detected=emotion_detected,
            intent=intent
        )
        session.add(conversation)
        session.commit()
        return conversation
    finally:
        session.close()


def get_conversation_history(user_id: int, limit: int = 10) -> list:
    """
    Get recent conversation history for user
    
    Args:
        user_id: Telegram user ID
        limit: Number of recent messages to retrieve
    
    Returns:
        List of Conversation objects
    """
    session = get_session()
    try:
        conversations = session.query(Conversation)\
            .filter(Conversation.user_id == user_id)\
            .order_by(Conversation.created_at.desc())\
            .limit(limit)\
            .all()
        
        return list(reversed(conversations))  # Return in chronological order
    finally:
        session.close()


def track_analytics(
    user_id: int,
    event_type: str,
    event_data: dict = None,
    product_viewed: str = None,
    is_conversion: bool = False,
    conversion_value: float = None
):
    """
    Track user analytics event
    
    Args:
        user_id: Telegram user ID
        event_type: Type of event (message, button_click, product_view, purchase)
        event_data: Additional event data
        product_viewed: Product name if applicable
        is_conversion: Whether this is a conversion event
        conversion_value: Value of conversion if applicable
    """
    session = get_session()
    try:
        analytics = Analytics(
            user_id=user_id,
            event_type=event_type,
            event_data=event_data or {},
            product_viewed=product_viewed,
            is_conversion=is_conversion,
            conversion_value=conversion_value
        )
        session.add(analytics)
        session.commit()
    finally:
        session.close()


def track_product_view(user_id: int, product_name: str, view_type: str = 'general'):
    """
    Track product view or interaction
    
    Args:
        user_id: Telegram user ID
        product_name: Product name
        view_type: Type of view (general, price, specs, purchase)
    """
    session = get_session()
    try:
        product_view = session.query(ProductView)\
            .filter(ProductView.user_id == user_id, ProductView.product_name == product_name)\
            .first()
        
        from datetime import datetime
        if not product_view:
            product_view = ProductView(
                user_id=user_id,
                product_name=product_name
            )
            session.add(product_view)
        else:
            product_view.views_count += 1
            product_view.last_viewed_at = datetime.utcnow()
        
        # Track specific view type
        if view_type == 'price':
            product_view.price_inquiries += 1
        elif view_type == 'specs':
            product_view.spec_inquiries += 1
        elif view_type == 'purchase':
            product_view.purchase_attempts += 1
        
        session.commit()
    finally:
        session.close()


def get_user_stats(user_id: int) -> dict:
    """
    Get comprehensive user statistics
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        Dictionary with user stats
    """
    session = get_session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            return None
        
        # Count conversations
        conversation_count = session.query(Conversation)\
            .filter(Conversation.user_id == user_id)\
            .count()
        
        # Get top products
        top_products = session.query(ProductView)\
            .filter(ProductView.user_id == user_id)\
            .order_by(ProductView.views_count.desc())\
            .limit(5)\
            .all()
        
        # Get conversion rate
        total_events = session.query(Analytics)\
            .filter(Analytics.user_id == user_id)\
            .count()
        
        conversion_events = session.query(Analytics)\
            .filter(Analytics.user_id == user_id, Analytics.is_conversion == True)\
            .count()
        
        conversion_rate = (conversion_events / total_events * 100) if total_events > 0 else 0
        
        return {
            'user_id': user_id,
            'username': user.username,
            'total_messages': user.total_messages,
            'total_conversations': conversation_count,
            'total_purchases': user.total_purchases,
            'total_spent': float(user.total_spent),
            'conversion_rate': round(conversion_rate, 2),
            'top_products': [
                {
                    'product_name': p.product_name,
                    'views': p.views_count,
                    'price_inquiries': p.price_inquiries,
                    'purchase_attempts': p.purchase_attempts
                }
                for p in top_products
            ],
            'created_at': user.created_at.isoformat(),
            'last_active': user.last_active.isoformat()
        }
    finally:
        session.close()


def save_chat_message(user_id: int, role: str, content: str, session_id: int = None, response_time_ms: int = None):
    """
    Save individual chat message for LangChain history
    
    Args:
        user_id: Telegram user ID
        role: 'user' or 'assistant'
        content: Message content
        session_id: Conversation session ID
        response_time_ms: Response time in milliseconds
    """
    session = get_session()
    try:
        message = ChatMessageHistory(
            user_id=user_id,
            session_id=session_id,
            role=role,
            content=content,
            response_time_ms=response_time_ms
        )
        session.add(message)
        session.commit()
    finally:
        session.close()


def get_chat_history(user_id: int, limit: int = 20) -> list:
    """
    Get complete chat message history for LangChain
    
    Args:
        user_id: Telegram user ID
        limit: Number of messages
    
    Returns:
        List of messages in format suitable for LangChain
    """
    session = get_session()
    try:
        messages = session.query(ChatMessageHistory)\
            .filter(ChatMessageHistory.user_id == user_id)\
            .order_by(ChatMessageHistory.created_at.desc())\
            .limit(limit)\
            .all()
        
        # Convert to LangChain format
        history = []
        for msg in reversed(messages):
            if msg.role == 'user':
                from langchain.schema import HumanMessage
                history.append(HumanMessage(content=msg.content))
            else:
                from langchain.schema import AIMessage
                history.append(AIMessage(content=msg.content))
        
        return history
    finally:
        session.close()
