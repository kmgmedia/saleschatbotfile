"""
Emotion Detection Module
Detects emotional states in user messages and provides empathetic responses
"""

# Emotion keyword lists
FRUSTRATION_KEYWORDS = [
    'frustrated', 'frustrating', 'annoyed', 'annoying', 'ridiculous', 'stupid',
    'terrible', 'awful', 'worst', 'horrible', 'disappointed', 'disappointing',
    'upset', 'angry', 'mad', 'furious', 'unacceptable', 'pathetic',
    'third time', 'second time', 'again and again', 'keep asking', 'still waiting'
]

URGENCY_KEYWORDS = [
    'urgent', 'asap', 'immediately', 'right now', 'now', 'today', 
    'quickly', 'fast', 'hurry', 'rush'
]

HESITATION_KEYWORDS = [
    'not sure', 'unsure', 'doubt', 'hesitant', 'thinking about it', 
    'maybe', 'hmm', 'dunno', 'don\'t know'
]

BUDGET_CONCERN_KEYWORDS = [
    'too expensive', 'can\'t afford', 'out of budget', 'pricey', 
    'too much', 'cheaper alternative', 'budget'
]


def detect_emotion(user_input):
    """
    Detect emotional state from user input
    Returns: emotion type ('frustration', 'urgency', 'hesitation', 'budget_concern') or None
    """
    user_input_lower = user_input.lower()
    
    if any(keyword in user_input_lower for keyword in FRUSTRATION_KEYWORDS):
        return 'frustration'
    
    if any(keyword in user_input_lower for keyword in URGENCY_KEYWORDS):
        return 'urgency'
    
    if any(phrase in user_input_lower for phrase in HESITATION_KEYWORDS):
        return 'hesitation'
    
    if any(phrase in user_input_lower for phrase in BUDGET_CONCERN_KEYWORDS):
        return 'budget_concern'
    
    return None


def get_empathetic_response(emotion_type, product_name=None, product_price=None):
    """
    Generate empathetic response based on detected emotion
    
    Args:
        emotion_type: Type of emotion detected
        product_name: Optional product name for context
        product_price: Optional product price for budget responses
    
    Returns:
        Empathetic response string
    """
    if emotion_type == 'frustration':
        return """I sincerely apologize for any frustration you're experiencing. That's definitely not the experience we want for you. 😔

Let me help make this right immediately. Please contact our dedicated support team at @Store_help_bot, and they'll prioritize your case to ensure you get the best solution.

Is there anything specific I can clarify{product_context} right now? I'm here to help.""".format(
            product_context=f" about the {product_name}" if product_name else ""
        )
    
    elif emotion_type == 'urgency':
        urgency_response = """I understand you need this urgently! ⚡

{product_context}Good news: {product_name}The product is in stock and ready for immediate dispatch!

🚀 **Express Options:**
• Same-day delivery available in select areas
• Express shipping: 2-3 business days
• Priority processing for urgent orders

Contact @Store_help_bot right now with "URGENT" and they'll fast-track your order! 

Need the specs quickly before deciding? Just ask! ⏱️"""
        
        if product_name:
            return urgency_response.format(
                product_context=f"The {product_name} is in stock and ready for immediate dispatch!\n\n",
                product_name=""
            )
        else:
            return urgency_response.format(
                product_context="",
                product_name="The product is "
            )
    
    elif emotion_type == 'hesitation':
        return """I totally understand - it's important to feel confident about your purchase! 🤔

Let me help you decide{product_context}:

✅ **Peace of Mind:** 30-day money-back guarantee (no questions asked!)
✅ **Quality Assured:** 1-year warranty included
✅ **Risk-Free:** Try it, and if it's not perfect, return it!

What specific concerns do you have? I'm here to answer any questions! 😊""".format(
            product_context=f" about the {product_name}" if product_name else ""
        )
    
    elif emotion_type == 'budget_concern':
        price_info = f" (${product_price})" if product_price else ""
        product_info = f"the **{product_name}**{price_info}" if product_name else "this product"
        
        return f"""I completely understand budget is important! 💰

For {product_info}, here are your options:

1️⃣ **Cheaper Alternatives:** Type "cheapest" to see our most affordable products
2️⃣ **Bundle Deals:** Type "bundles" for multi-product savings (up to 25% off!)
3️⃣ **Payment Options:** Many customers love our flexible payment plans

Would you like to see more budget-friendly options, or learn about the value this product offers? 🤗"""
    
    return None


def is_emotional_message(user_input):
    """Quick check if message contains emotional indicators"""
    return detect_emotion(user_input) is not None
