"""
Database Models - SQLAlchemy ORM Models
Defines data structures for users, conversations, and analytics
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User profile and conversation state"""
    __tablename__ = 'users'
    
    user_id = Column(BigInteger, primary_key=True, unique=True)  # Telegram user ID (can be > 2B)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), default='en')
    
    # User preferences
    preferred_products = Column(JSON, default={})  # {product_name: view_count}
    last_viewed_product = Column(String(255), nullable=True)
    budget = Column(Float, nullable=True)  # User's budget preference
    
    # Engagement tracking
    total_messages = Column(Integer, default=0)
    total_conversations = Column(Integer, default=0)
    total_purchases = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    conversations = relationship('Conversation', back_populates='user', cascade='all, delete-orphan')
    analytics = relationship('Analytics', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User {self.user_id}: {self.username}>"


class Conversation(Base):
    """Conversation history for LangChain memory persistence"""
    __tablename__ = 'conversations'
    
    conversation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    
    # Message content
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    
    # Context tracking
    current_product = Column(String(255), nullable=True)
    emotion_detected = Column(String(50), nullable=True)  # frustration, urgency, etc.
    intent = Column(String(100), nullable=True)  # price, buy, specs, compare
    
    # Message metadata
    message_quality_score = Column(Float, default=0.0)  # 0.0-1.0
    user_satisfied = Column(Boolean, nullable=True)  # Track satisfaction
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='conversations')
    
    def __repr__(self):
        return f"<Conversation {self.conversation_id}>"


class Analytics(Base):
    """Real-time analytics and metrics"""
    __tablename__ = 'analytics'
    
    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    
    # Event tracking
    event_type = Column(String(50), nullable=False)  # message, button_click, product_view, purchase
    event_data = Column(JSON, nullable=True)  # Extra data specific to event
    
    # Funnel tracking
    funnel_stage = Column(String(50), nullable=True)  # greeting, browsing, consideration, purchase
    product_viewed = Column(String(255), nullable=True)
    time_on_product = Column(Integer, nullable=True)  # seconds
    
    # Conversion metrics
    is_conversion = Column(Boolean, default=False)
    conversion_value = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='analytics')
    
    def __repr__(self):
        return f"<Analytics {self.metric_id}>"


class ConversationSession(Base):
    """Session-level conversation tracking for multi-turn context"""
    __tablename__ = 'conversation_sessions'
    
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    
    # Session context
    session_start = Column(DateTime, default=datetime.utcnow)
    session_end = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Session stats
    message_count = Column(Integer, default=0)
    products_viewed = Column(JSON, default={})  # List of products viewed
    is_completed = Column(Boolean, default=False)  # Did user make a purchase?
    
    # LangChain memory (serialized)
    memory_buffer = Column(Text, nullable=True)  # Serialized conversation buffer
    
    def __repr__(self):
        return f"<Session {self.session_id}>"


class ProductView(Base):
    """Track which products users view and their interactions"""
    __tablename__ = 'product_views'
    
    view_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    
    # Interaction tracking
    views_count = Column(Integer, default=1)
    price_inquiries = Column(Integer, default=0)
    spec_inquiries = Column(Integer, default=0)
    purchase_attempts = Column(Integer, default=0)
    
    # Sentiment
    user_interest_level = Column(String(20), nullable=True)  # high, medium, low
    
    first_viewed_at = Column(DateTime, default=datetime.utcnow)
    last_viewed_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProductView {self.product_name}>"


class ChatMessageHistory(Base):
    """Complete message history for LangChain integration"""
    __tablename__ = 'chat_message_history'
    
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    session_id = Column(Integer, ForeignKey('conversation_sessions.session_id'), nullable=True)
    
    # Message details
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    
    # Message metadata
    tokens_used = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Message {self.message_id}>"
