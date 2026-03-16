"""
Conversation Handler - Main Orchestrator
Simplified to coordinate between specialized modules
"""
import random
import re

# Handle both relative and direct imports
try:
    from .product_data import (
        PRODUCT_PRICES, PRODUCT_SPECS, detect_product, 
        get_product_responses, get_product_price
    )
    from .emotion_detector import detect_emotion, get_empathetic_response
    from .sales_psychology import (
        enhance_product_response, get_buying_intent_message,
        add_value_proposition, add_social_proof, add_urgency_trigger
    )
    from .user_memory import (
        get_last_product, set_last_product, has_context,
        user_conversations  # Export for backward compatibility
    )
except ImportError:
    from product_data import (
        PRODUCT_PRICES, PRODUCT_SPECS, detect_product, 
        get_product_responses, get_product_price
    )
    from emotion_detector import detect_emotion, get_empathetic_response
    from sales_psychology import (
        enhance_product_response, get_buying_intent_message,
        add_value_proposition, add_social_proof, add_urgency_trigger
    )
    from user_memory import (
        get_last_product, set_last_product, has_context,
        user_conversations  # Export for backward compatibility
    )


def get_product_response(product_name):
    """Get a beautiful, engaging, and personalized response for any product"""
    responses = get_product_responses(product_name)
    price = get_product_price(product_name) or 999
    if responses:
        base_response = random.choice(responses)
        beautiful_intro = f"🌟 {product_name} is a fantastic pick! "
        guidance = "Let me know if you have any goals, preferences, or want to see related products or bundles. I'm here to help you find the perfect match!"
        personalized = "Are you looking for something to help with general wellness, or do you have specific goals in mind? 😊"
        enhanced = (
            beautiful_intro
            + base_response
            + add_value_proposition(price)
            + add_social_proof(price)
            + add_urgency_trigger(price)
            + "\n"
            + guidance
            + "\n"
            + personalized
        )
        return enhanced
    return f"🌟 {product_name} is a fantastic pick! Let me know if you want details, recommendations, or help finding the perfect match! 😊"


def continue_conversation(product_name, user_input, user_id=None):
    """Continue conversation about the current product based on user intent"""
    def sanitize_user_input(text):
        text = re.sub(r'["\'`]', '', text)
        text = re.sub(r'[{}]', '', text)
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        return text[:500]

    def validate_user_input(text):
        if not re.match(r'^[\w\s.,!?@#\-:;()]+$', text):
            return "[Invalid input detected]"
        if len(text) > 500:
            return text[:500]
        return text

    def escape_user_input(text):
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        text = text.replace('%', '%%').replace('$', '\$')
        return text

    safe_user_input = sanitize_user_input(user_input)
    safe_user_input = validate_user_input(safe_user_input)
    safe_user_input = escape_user_input(safe_user_input)
    user_input_lower = safe_user_input.lower()

    # Check for greetings FIRST - this resets context
    if any(word in user_input_lower for word in ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
        return None  # Defer to responses.py for fresh greeting
    
    # Check for emotional states
    emotion = detect_emotion(user_input)
    if emotion:
        price = get_product_price(product_name)
        return get_empathetic_response(emotion, product_name, price)
    
    # Bundle request - defer to responses.py
    if 'bundle' in user_input_lower:
        return None
    
    # Cheapest request - defer to responses.py
    if any(word in user_input_lower for word in ['cheapest', 'cheap', 'affordable', 'least expensive', 'lowest price']):
        return None
    
    # All products request - defer to responses.py
    if any(word in user_input_lower for word in ['all products', 'show all', 'full catalog', 'everything', 'complete list', 'what else', 'other products', 'more products']):
        return None
    
    # Price inquiry
    if any(word in user_input_lower for word in ['price', 'cost', 'how much', 'expensive']):
        price = get_product_price(product_name) or 0
        from .sales_psychology import add_scarcity_message
        psychology = add_scarcity_message(price)
        return f"💰 The {product_name} costs ${price}.\n\n{psychology}\n\n✅ Free shipping on orders over $100\n✅ 30-day money-back guarantee\n✅ 1-year warranty\n\nReady to order? Contact @Store_help_bot!"

    # Buying intent
    elif any(word in user_input_lower for word in ['buy', 'purchase', 'order', 'get it', 'take it']):
        price = get_product_price(product_name) or 0
        return get_buying_intent_message(product_name, price)

    # Specs/features request
    elif any(word in user_input_lower for word in ['spec', 'feature', 'detail', 'info', 'tell me more', 'what can it do']):
        specs = PRODUCT_SPECS.get(product_name, "Great product with amazing features!")
        price = get_product_price(product_name) or 0
        response = f"📋 **{product_name} Specs:**\n\n{specs}\n\n💰 **Price:** ${price}"
        from .sales_psychology import add_value_proposition
        response += add_value_proposition(price)
        return response + "\n\nWant to know more or ready to buy? 🛒"

    # Comparison request
    elif any(word in user_input_lower for word in ['compare', 'vs', 'versus', 'difference', 'better']):
        return None  # Defer to responses.py for comparison handling

    # Positive response
    elif any(word in user_input_lower for word in ['yes', 'yeah', 'sure', 'ok', 'okay', 'interested', 'sounds good']):
        return f"Awesome! The {product_name} is a solid choice! 🎉\n\nWant to know the price, specs, or ready to buy? Just let me know!"

    # Negative response
    elif any(word in user_input_lower for word in ['no', 'nah', 'not interested', 'maybe later']):
        return "No worries! 😊 Is there anything else you'd like to know, or would you prefer to check out other products?"

    # Thank you
    elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate', 'thx', 'ty']):
        return "You're very welcome! 😊 That's what I'm here for. Happy to help anytime! 🛒✨"

    # Goodbye
    elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you', 'later', 'exit', 'quit']):
        return "Goodbye! 👋 It was great chatting with you. I'm Alex, and I'm here whenever you need help finding the perfect tech! Have an awesome day! 😊"

    # Help request
    elif any(word in user_input_lower for word in ['help', 'what can you do', 'commands', 'options']):
        return "Hey! I'm Alex, your tech consultant with 7 years of experience helping people find perfect products! 🎯\n\n**Here's how I can help you:**\n• 📱 Give you the inside scoop on product details, specs, and prices\n• 💰 Find the best deals and cheapest items in any category\n• 🎁 Hook you up with bundle deals (save up to 25%!)\n• 🔍 Compare products side-by-side so you make the right choice\n• 🛒 Guide you through the purchase process\n\n**Try asking me:**\n• 'Show me smartwatches'\n• 'What's the cheapest fitness tracker?'\n• 'Compare earbuds and headphones'\n• 'Show me bundles'\n• 'Tell me about the 4K camera'\n\nWhat are you looking for today? I'm all ears! 😊"

    # Vague or context-dependent follow-ups
    elif any(word in user_input_lower for word in ['what was that product', 'show me what we were talking about', 'i want to buy it', 'i want to buy', 'i want to order', 'order', 'buy', 'purchase', 'interested', 'i want it', 'i want this', 'i want that', 'i want to see', 'show me', 'remind me', 'recall', 'repeat', 'again', 'previous', 'last', 'think about it', 'i changed my mind', 'actually']):
        # Recall last product and respond
        from .user_memory import get_last_product, set_last_product
        last_product = get_last_product(user_id) if user_id else None
        if last_product:
            set_last_product(user_id, last_product)
            return get_product_response(last_product)
        else:
            return "If you want to revisit a product or need help, just let me know the name or category! I'm here to help you find the perfect match."

    # Short or ambiguous messages
    elif len(user_input.split()) <= 2:
        from .user_memory import get_last_product, set_last_product
        last_product = get_last_product(user_id) if user_id else None
        if last_product:
            set_last_product(user_id, last_product)
            return get_product_response(last_product)
        else:
            return "Let me know what you're interested in, or ask about any product or category! 😊"

    # Default: Only repeat product info if it seems like they're still interested
    else:
        product_keywords = ['tell me more', 'interested', 'cool', 'nice', 'awesome', 'good', 'great', 'love it', 'like it', 'perfect', 'exactly', 'that works', 'sounds good']
        if any(keyword in user_input_lower for keyword in product_keywords):
            return get_product_response(product_name)
        else:
            return "I'm here to help! Ask about any product, category, or deal, and I'll guide you to the best options. 😊"


def handle_user_input(user_id, user_input):
    """
    Main entry point for handling user messages with memory
    
    Args:
        user_id: Unique user identifier
        user_input: User's message text
    
    Returns:
        Response text or None (to defer to responses.py)
    """
    user_input_lower = user_input.lower()
    
    # Check for greetings - clear context for fresh start
    if any(word in user_input_lower for word in ['hi', 'hello', 'hey', 'start']) and len(user_input.split()) <= 2:
        # Clear context if they're just saying hi (not "hi, tell me about...")
        from .user_memory import clear_user_state
        clear_user_state(user_id)
        return None  # Let responses.py handle the greeting
    
    # Check for goodbye first
    if any(word in user_input_lower for word in ['bye', 'goodbye', 'see you', 'later', 'exit', 'quit']):
        from .user_memory import clear_user_state
        clear_user_state(user_id)
        return "Goodbye! 👋 It was great chatting with you. I'm Alex, and I'm here whenever you need help finding the perfect tech! Have an awesome day! 😊"
    
    # Check for help
    if any(word in user_input_lower for word in ['help', 'what can you do', 'commands', 'options']):
        return """Hey! I'm Alex, your tech consultant with 7 years of experience helping people find perfect products! 🎯

**Here's how I can help you:**
• 📱 Give you the inside scoop on product details, specs, and prices
• 💰 Find the best deals and cheapest items in any category
• 🎁 Hook you up with bundle deals (save up to 25%!)
• 🔍 Compare products side-by-side so you make the right choice
• 🛒 Guide you through the purchase process

**Try asking me:**
• "Show me smartwatches"
• "What's the cheapest fitness tracker?"
• "Compare earbuds and headphones"
• "Show me bundles"
• "Tell me about the 4K camera"

What are you looking for today? I'm all ears! 😊"""
    
    # Check for thank you
    if any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate', 'thx', 'ty']):
        return "You're very welcome! 😊 That's what I'm here for. Happy to help anytime! 🛒✨"
    
    # Detect product mention
    detected_product = detect_product(user_input)
    
    if detected_product:
        # Store this product in memory
        set_last_product(user_id, detected_product)
        return get_product_response(detected_product)
    
    # If no product detected, check if user has context
    if has_context(user_id):
        last_product = get_last_product(user_id)
        response = continue_conversation(last_product, user_input)
        if response:
            return response
        # If continue_conversation returned None, clear context and defer to responses.py
        else:
            from .user_memory import clear_user_state
            clear_user_state(user_id)
            return None
    
    # No context - return None to let responses.py handle it
    return None


# Export key functions for backward compatibility
__all__ = [
    'get_product_response',
    'continue_conversation', 
    'handle_user_input',
    'detect_product',
    'user_conversations',
    'PRODUCT_PRICES',
    'PRODUCT_SPECS'
]
