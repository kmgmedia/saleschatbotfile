"""
User Memory Module
Manages conversation state and history for each user
"""

# Conversation state per user (for multi-user support with memory)
# Structure: { user_id: { "last_product": "Product Name", "conversation_history": [...] } }
user_conversations = {}


def get_user_state(user_id):
    """
    Get conversation state for a specific user
    
    Args:
        user_id: Unique user identifier
    
    Returns:
        User state dictionary or None if user not found
    """
    return user_conversations.get(user_id)


def set_last_product(user_id, product_name):
    """
    Store the last product discussed with a user
    
    Args:
        user_id: Unique user identifier
        product_name: Name of the product
    """
    if user_id not in user_conversations:
        user_conversations[user_id] = {
            "last_product": product_name,
            "conversation_history": []
        }
    else:
        user_conversations[user_id]["last_product"] = product_name


def get_last_product(user_id):
    """
    Retrieve the last product discussed with a user
    
    Args:
        user_id: Unique user identifier
    
    Returns:
        Product name or None
    """
    if user_id in user_conversations:
        return user_conversations[user_id].get("last_product")
    return None


def add_to_history(user_id, message):
    """
    Add a message to user's conversation history
    
    Args:
        user_id: Unique user identifier
        message: Message to add to history
    """
    if user_id not in user_conversations:
        user_conversations[user_id] = {
            "last_product": None,
            "conversation_history": [message]
        }
    else:
        user_conversations[user_id]["conversation_history"].append(message)
        
        # Keep only last 10 messages to prevent memory overflow
        if len(user_conversations[user_id]["conversation_history"]) > 10:
            user_conversations[user_id]["conversation_history"] = \
                user_conversations[user_id]["conversation_history"][-10:]


def get_conversation_history(user_id, limit=5):
    """
    Get recent conversation history for a user
    
    Args:
        user_id: Unique user identifier
        limit: Number of recent messages to retrieve
    
    Returns:
        List of recent messages
    """
    if user_id in user_conversations:
        history = user_conversations[user_id].get("conversation_history", [])
        return history[-limit:] if history else []
    return []


def clear_user_state(user_id):
    """
    Clear all conversation state for a user
    
    Args:
        user_id: Unique user identifier
    """
    if user_id in user_conversations:
        del user_conversations[user_id]


def has_context(user_id):
    """
    Check if user has existing conversation context
    
    Args:
        user_id: Unique user identifier
    
    Returns:
        Boolean indicating if context exists
    """
    return user_id in user_conversations and user_conversations[user_id].get("last_product") is not None
