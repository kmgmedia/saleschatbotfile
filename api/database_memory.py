"""
LangChain Persistent Memory Module
Integrates database persistence with LangChain for conversation memory
"""
import sys
from datetime import datetime
from typing import List
try:
    from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
except ImportError:
    from langchain.schema import BaseMessage, HumanMessage, AIMessage

try:
    from .database import (
        get_session, save_chat_message, get_chat_history,
        save_conversation, get_conversation_history
    )
    from .models import ConversationSession, ChatMessageHistory
except ImportError:
    from database import (
        get_session, save_chat_message, get_chat_history,
        save_conversation, get_conversation_history
    )
    from models import ConversationSession, ChatMessageHistory


class PersistentChatHistory:
    """
    Wrapper for storing and retrieving chat history from database
    Compatible with LangChain memory systems
    """
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session_id = None
    
    def create_session(self) -> int:
        """Create new conversation session"""
        session = get_session()
        try:
            conv_session = ConversationSession(user_id=self.user_id)
            session.add(conv_session)
            session.commit()
            self.session_id = conv_session.session_id
            return self.session_id
        finally:
            session.close()
    
    def add_message(self, role: str, content: str, response_time_ms: int = None):
        """
        Add message to history
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
            response_time_ms: Response time in milliseconds
        """
        try:
            save_chat_message(
                user_id=self.user_id,
                role=role,
                content=content,
                session_id=self.session_id,
                response_time_ms=response_time_ms
            )
        except Exception as e:
            print(f"Error adding message: {e}", file=sys.stderr)
    
    def get_messages(self, limit: int = 20) -> List:
        """
        Get recent messages
        
        Args:
            limit: Number of messages
        
        Returns:
            List of messages in LangChain format
        """
        try:
            return get_chat_history(self.user_id, limit)
        except Exception as e:
            print(f"Error retrieving messages: {e}", file=sys.stderr)
            return []
    
    def clear_history(self):
        """Clear conversation history"""
        session = get_session()
        try:
            session.query(ChatMessageHistory)\
                .filter(ChatMessageHistory.user_id == self.user_id)\
                .delete()
            session.commit()
        finally:
            session.close()
    
    def __len__(self) -> int:
        """Get message count"""
        session = get_session()
        try:
            count = session.query(ChatMessageHistory)\
                .filter(ChatMessageHistory.user_id == self.user_id)\
                .count()
            return count
        finally:
            session.close()


class PersistentConversationMemory:
    """
    LangChain-compatible conversation memory that persists to database
    """
    
    def __init__(self, user_id: int, buffer_size: int = 10):
        self.user_id = user_id
        self.buffer_size = buffer_size
        self.chat_history = PersistentChatHistory(user_id)
        self._messages = []
    
    def add_user_message(self, message: str):
        """Add user message to memory"""
        self.chat_history.add_message('user', message)
        self._messages.append({'role': 'user', 'content': message})
        self._trim_buffer()
    
    def add_ai_message(self, message: str):
        """Add AI message to memory"""
        self.chat_history.add_message('assistant', message)
        self._messages.append({'role': 'assistant', 'content': message})
        self._trim_buffer()
    
    def _trim_buffer(self):
        """Keep only recent messages in memory"""
        if len(self._messages) > self.buffer_size:
            self._messages = self._messages[-self.buffer_size:]
    
    def get_context(self) -> str:
        """
        Get formatted context string for prompt
        
        Returns:
            Formatted conversation context
        """
        context = "Previous conversation:\n"
        for msg in self._messages[-5:]:  # Last 5 messages
            role = "User" if msg['role'] == 'user' else "Assistant"
            context += f"{role}: {msg['content']}\n"
        return context
    
    def get_messages(self) -> List[dict]:
        """Get all messages"""
        return self._messages
    
    def load_from_db(self, limit: int = 10):
        """Load message history from database"""
        try:
            session = __import__('database').get_session()
            messages = session.query(ChatMessageHistory)\
                .filter(ChatMessageHistory.user_id == self.user_id)\
                .order_by(ChatMessageHistory.created_at.desc())\
                .limit(limit)\
                .all()
            
            session.close()
            
            self._messages = [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.created_at.isoformat()
                }
                for msg in reversed(messages)
            ]
        except Exception as e:
            print(f"Error loading from database: {e}", file=sys.stderr)
    
    def clear(self):
        """Clear all messages"""
        self.chat_history.clear_history()
        self._messages = []


class ConversationContextManager:
    """
    Manages conversation context including current product, emotion, intent
    """
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.current_product = None
        self.current_emotion = None
        self.current_intent = None
        self.user_history = []
    
    def set_context(self, product: str = None, emotion: str = None, intent: str = None):
        """Update conversation context"""
        if product:
            self.current_product = product
        if emotion:
            self.current_emotion = emotion
        if intent:
            self.current_intent = intent
    
    def get_context_summary(self) -> dict:
        """Get current context"""
        return {
            'product': self.current_product,
            'emotion': self.current_emotion,
            'intent': self.current_intent
        }
    
    def save_interaction(self, user_msg: str, bot_msg: str):
        """Save user-bot interaction to database"""
        try:
            save_conversation(
                user_id=self.user_id,
                user_message=user_msg,
                bot_response=bot_msg,
                current_product=self.current_product,
                emotion_detected=self.current_emotion,
                intent=self.current_intent
            )
        except Exception as e:
            print(f"Error saving interaction: {e}", file=sys.stderr)
    
    def get_recent_interactions(self, limit: int = 5) -> list:
        """Get recent interactions"""
        return get_conversation_history(self.user_id, limit)


# Global memory manager per user
_memory_cache = {}


def get_user_memory(user_id: int) -> PersistentConversationMemory:
    """
    Get or create memory for user
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        PersistentConversationMemory instance
    """
    if user_id not in _memory_cache:
        _memory_cache[user_id] = PersistentConversationMemory(user_id)
        _memory_cache[user_id].load_from_db(limit=10)
    
    return _memory_cache[user_id]


def get_user_context_manager(user_id: int) -> ConversationContextManager:
    """
    Get or create context manager for user
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        ConversationContextManager instance
    """
    if not hasattr(get_user_memory, '_context_cache'):
        get_user_memory._context_cache = {}
    
    if user_id not in get_user_memory._context_cache:
        get_user_memory._context_cache[user_id] = ConversationContextManager(user_id)
    
    return get_user_memory._context_cache[user_id]


def clear_user_memory(user_id: int):
    """Clear user's memory cache"""
    if user_id in _memory_cache:
        del _memory_cache[user_id]
    
    if hasattr(get_user_memory, '_context_cache') and user_id in get_user_memory._context_cache:
        del get_user_memory._context_cache[user_id]
