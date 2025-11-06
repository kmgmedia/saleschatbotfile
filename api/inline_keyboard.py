"""
Inline keyboard (button) handler for Telegram.
Provides interactive buttons for better user experience.
"""

def product_buttons(product_name):
    """
    Generate inline keyboard buttons for a product.
    Returns Telegram InlineKeyboardMarkup structure.
    """
    return {
        "inline_keyboard": [
            [
                {"text": "💰 See Price", "callback_data": f"price:{product_name}"},
                {"text": "📋 See Specs", "callback_data": f"specs:{product_name}"}
            ],
            [
                {"text": "🛒 Buy Now", "callback_data": f"buy:{product_name}"},
                {"text": "🔄 Compare", "callback_data": f"compare:{product_name}"}
            ],
            [
                {"text": "🏠 Back to Products", "callback_data": "back"}
            ]
        ]
    }


def handle_button_callback(callback_data, user_id):
    """
    Handle button clicks (callback queries).
    
    Args:
        callback_data: The callback_data string from the button click
        user_id: User ID for conversation tracking
    
    Returns:
        dict with 'text' and optional 'reply_markup' keys
    """
    try:
        from . import conversation_handler
    except ImportError:
        import conversation_handler
    
    # Back to products menu
    if callback_data == "back":
        conversation_handler.reset_conversation(user_id)
        return {
            "text": "🏠 Back to main menu. What would you like to explore?\n\n• Browse categories\n• Ask about specific products\n• See cheapest options\n• Compare products\n\nJust let me know! 😊",
            "reply_markup": get_product_list_keyboard()
        }
    
    # Handle product selection from main menu
    if callback_data.startswith("product:"):
        product = callback_data.replace("product:", "")
        # Update user's last product in memory
        if user_id not in conversation_handler.user_conversations:
            conversation_handler.user_conversations[user_id] = {
                "last_product": None,
                "conversation_history": []
            }
        conversation_handler.user_conversations[user_id]["last_product"] = product
        
        # Get product intro
        intro = conversation_handler.get_random_intro(product)
        response = conversation_handler.get_product_response(product)
        
        return {
            "text": f"{intro}\n\n{response}",
            "reply_markup": product_buttons(product)
        }
    
    # Parse action and product name
    try:
        action, product = callback_data.split(":", 1)
    except ValueError:
        return {"text": "Oops! Something went wrong. Please try again.", "reply_markup": None}
    
    # Update user's last product in memory
    if user_id not in conversation_handler.user_conversations:
        conversation_handler.user_conversations[user_id] = {
            "last_product": None,
            "conversation_history": []
        }
    
    conversation_handler.user_conversations[user_id]["last_product"] = product
    
    # Handle different button actions
    if action == "price":
        price = conversation_handler.PRODUCT_PRICES.get(product, "N/A")
        return {
            "text": f"💰 The {product} costs ${price:,.2f}.\n\nGreat value for what you get! Want me to help you buy it?",
            "reply_markup": product_buttons(product)
        }
    
    elif action == "specs":
        spec = conversation_handler.get_product_spec(product)
        return {
            "text": f"📋 **Specs for {product}:**\n\n{spec}",
            "reply_markup": product_buttons(product)
        }
    
    elif action == "buy":
        return {
            "text": f"🛒 Great choice! You can buy the **{product}** now.\n\n✅ We offer:\n• Free delivery within 3 days 🚚\n• 30-day money-back guarantee\n• 1-year warranty\n\nContact @Store_help_bot to complete your order!",
            "reply_markup": product_buttons(product)
        }
    
    elif action == "compare":
        return {
            "text": f"🔄 Let's compare the **{product}**!\n\nWhich other product would you like to compare it with? Just type the product name!",
            "reply_markup": product_buttons(product)
        }
    
    else:
        return {
            "text": "I'm not sure how to handle that. Try asking about a product!",
            "reply_markup": None
        }


def get_product_list_keyboard():
    """Generate a keyboard with popular products"""
    return {
        "inline_keyboard": [
            [
                {"text": "⌚ Smartwatch", "callback_data": "product:Smartwatch X"},
                {"text": "🎧 Earbuds", "callback_data": "product:Wireless Earbuds Pro"}
            ],
            [
                {"text": "📷 Camera", "callback_data": "product:4K Action Camera"},
                {"text": "🏠 Smart Hub", "callback_data": "product:Smart Home Hub"}
            ],
            [
                {"text": "🔋 Power Bank", "callback_data": "product:Power Bank 20000mAh"},
                {"text": "🔊 Speaker", "callback_data": "product:Bluetooth Speaker Mini"}
            ],
            [
                {"text": "💪 Fitness Band", "callback_data": "product:Fitness Band Pro"},
                {"text": "🥽 VR Headset", "callback_data": "product:VR Headset Max"}
            ]
        ]
    }
