"""
Natural conversation handler with product-focused responses
Maintains conversation context and provides human-like, product-specific replies
Supports per-user conversation tracking and memory-based personalization
"""
import random

# Conversation state per user (for multi-user support with memory)
# Structure: { user_id: { "last_product": "Product Name", "conversation_history": [...] } }
user_conversations = {}

# Product prices
PRODUCT_PRICES = {
    "Smartwatch X": 59,
    "Bluetooth Speaker Mini": 29,
    "Wireless Earbuds Pro": 79,
    "Power Bank 20000mAh": 300,
    "Smart Home Hub": 450,
    "4K Action Camera": 850,
    "Fitness Tracker Band": 35,
    "Smart LED Strip Lights": 49,
    "Portable Projector Pro": 320,
    "Smart Security Camera": 210,
    "Wireless Charging Pad": 45,
    "Noise-Cancelling Headphones": 180,
    "Smart Thermostat": 220,
    "Smart Light Bulb (4-Pack)": 99,
    "Mini Drone X2": 250,
    "Laptop Stand Pro": 75,
    "Foldable Wireless Keyboard": 89,
    "Smart Doorbell Cam": 190,
    "VR Headset Max": 480,
    "Portable Solar Charger": 99,
    "Fitness Band Pro": 120,
}

# Product specifications for detailed info
PRODUCT_SPECS = {
    "Smartwatch X": "Tracks steps, sleep, and heart rate with a bright OLED display and 5-day battery.",
    "Bluetooth Speaker Mini": "Compact speaker with crisp sound, deep bass, and 12-hour battery life.",
    "Wireless Earbuds Pro": "Noise-cancelling earbuds with waterproof design and 24-hour total playtime.",
    "Power Bank 20000mAh": "Fast-charging dual-port power bank that keeps devices powered for days.",
    "Smart Home Hub": "Connects and controls all your smart home devices in one sleek hub.",
    "4K Action Camera": "Waterproof 4K camera with ultra-stable video and 120° wide-angle lens.",
    "Fitness Tracker Band": "Monitors heart rate, sleep, calories, and daily steps with real-time syncing.",
    "Smart LED Strip Lights": "16 million colors, voice control, music sync, and app-controlled mood lighting.",
    "Portable Projector Pro": "Pocket-sized projector with HDMI, wireless casting, and 120-inch display capability.",
    "Smart Security Camera": "1080p live feed with night vision, motion alerts, and two-way audio.",
    "Wireless Charging Pad": "15W fast wireless charger with LED indicator, auto-shutoff, and case-friendly design.",
    "Noise-Cancelling Headphones": "Active noise cancellation with 30-hour battery and premium comfort.",
    "Smart Thermostat": "AI-powered temperature control with energy-saving schedules and remote access.",
    "Smart Light Bulb (4-Pack)": "16 million colors, voice control, scheduling, and energy-efficient LED bulbs.",
    "Mini Drone X2": "HD camera, gesture control, obstacle avoidance, and foldable compact design.",
    "Laptop Stand Pro": "Ergonomic aluminum stand with 6-level height adjustment and cooling design.",
    "Foldable Wireless Keyboard": "Full-size keyboard that folds to pocket size with Bluetooth connectivity.",
    "Smart Doorbell Cam": "1080p video doorbell with motion detection, two-way talk, and cloud storage.",
    "VR Headset Max": "Immersive VR experience with 4K display, spatial audio, and wireless freedom.",
    "Portable Solar Charger": "20W solar panel with dual USB ports and weather-resistant foldable design.",
    "Fitness Band Pro": "Advanced fitness tracking with GPS, heart rate, sleep analysis, and 14-day battery."
}

# Product-specific natural responses (multiple variations for each product)
PRODUCT_RESPONSES = {
    "Smartwatch X": [
        "Ah, the Smartwatch X! It's like having a mini fitness coach on your wrist — it tracks your steps, sleep, and heart rate effortlessly. 💪",
        "If you're serious about your fitness, this watch's real-time heart rate tracking and sleep insights will blow your mind. Want to know if it's waterproof too? 🌊",
        "Smartwatch X has a clean display and battery that can last days. Are you more into style or performance when choosing a smartwatch? ⌚",
        "This beauty syncs perfectly with your phone and gives you notifications without pulling out your device. Perfect for busy days! 📱",
    ],
    
    "Bluetooth Speaker Mini": [
        "Bluetooth Speaker Mini packs a punch for its size — crisp sound, deep bass, and 12 hours of non-stop music. 🔊",
        "Perfect for parties, beach days, or just vibing in your room. Want to hear about its waterproof version? 🎉",
        "It's small but mighty. Do you care more about portability or sound power? 🎵",
        "This little guy connects in seconds and the battery life is insane for such a compact speaker! 🔋",
    ],
    
    "Wireless Earbuds Pro": [
        "Wireless Earbuds Pro gives studio-level sound and blocks out noise like magic. 🎧✨",
        "They're waterproof and fit snugly even during workouts. Would you like to know about battery life or sound modes? 💦",
        "These are perfect for your daily commute — no wires, no stress. Want me to show color options? 🚇",
        "The noise cancelling on these is next level — you'll be in your own world. Plus, they charge super fast! ⚡",
    ],
    
    "Power Bank 20000mAh": [
        "Power Bank 20000mAh keeps you powered for days — dual USB, fast charging, and built like a tank. 🔋💪",
        "Imagine charging your phone four times before needing to recharge it. Need details on compatibility? 📱",
        "It's a travel essential. Want me to tell you if it supports laptops or tablets too? ✈️",
        "This beast never lets you down — whether you're camping or just had a long day. Charge multiple devices at once! 🏕️",
    ],
    
    "Smart Home Hub": [
        "The Smart Home Hub brings your home to life — control your lights, music, and security all in one touch. 🏠✨",
        "It syncs seamlessly with Alexa, Google Home, and your smart devices. Want to know how it sets up? 🎤",
        "It's perfect for creating a connected space. Are you building a new setup or upgrading an existing one? 🔌",
        "Voice control everything from your couch — lights, temperature, even your coffee maker. The future is here! ☕",
    ],
    
    "4K Action Camera": [
        "4K Action Camera captures your adventures in jaw-dropping detail — even when you're on the move. 📹🏔️",
        "It's got image stabilization and waterproof housing. Planning to use it for sports or travel? 🌊",
        "This is a vlogger's dream — crisp footage and easy mounts. Want to see bundle options? 🎥",
        "Imagine reliving your wildest moments in crystal-clear 4K. It handles extreme conditions like a pro! 🏄",
    ],
    
    "Fitness Tracker Band": [
        "Fitness Tracker Band is built for serious fitness tracking — heart rate, calories, steps, all in real-time. 💪📊",
        "It's lightweight and syncs directly to your phone. Want to see how it compares to Smartwatch X? 📱",
        "Perfect for your fitness goals — it even tracks sleep quality. Are you more into running or gym workouts? 🏃",
        "This baby won't even notice you're wearing it, but it'll notice EVERYTHING you do. Great for daily motivation! 🎯",
    ],
    
    "Smart LED Strip Lights": [
        "Smart LED Strip Lights transform any room into a vibe — 16 million colors at your fingertips! 💡🌈",
        "Control them with your phone or voice. Perfect for gaming setups, bedrooms, or parties! 🎮",
        "Want to sync them with your music? They react to beats and create an amazing atmosphere! 🎵",
        "Easy to install, easy to love. Are you going for a chill mood or party mode? 🎉",
    ],
    
    "Portable Projector Pro": [
        "Portable Projector Pro brings cinema anywhere — pocket-sized with HDMI and wireless casting! 📽️🍿",
        "Movie nights under the stars? Gaming on a huge screen? This little guy does it all. What's your dream setup? ⭐",
        "It's surprisingly bright and clear. Want to know about battery life or compatible devices? 🔋",
        "From backyard movies to presentations, this projector is a game-changer. Portable entertainment! 🎬",
    ],
    
    "Smart Security Camera": [
        "Smart Security Camera keeps your home safe 24/7 with 1080p live feed and night vision. 🎥🌙",
        "Motion alerts sent straight to your phone. You'll always know what's happening at home! 📱",
        "It's weatherproof and has two-way audio — talk to delivery people or scare off intruders! 🔊",
        "Peace of mind in a package. Indoor or outdoor — where are you thinking of placing it? 🏠",
    ],
    
    "Wireless Charging Pad": [
        "Wireless Charging Pad is the cable-free life you deserve — sleek, fast, Qi-certified! ⚡✨",
        "Just drop your phone and go. Works with iPhone, Samsung, and most modern devices! 📱",
        "No more tangled cables or broken ports. It's simple, elegant, and efficient! 🎯",
        "Charges fast and looks premium on any desk or nightstand. Minimalist dream! 🌟",
    ],
    
    "Noise-Cancelling Headphones": [
        "Noise-Cancelling Headphones deliver immersive sound that blocks out the world. 🎧🌍",
        "Perfect for travel, work, or just escaping into your music. Comfort for hours! ✈️",
        "The ANC technology is top-tier — you won't hear a thing except pure audio bliss! 🎵",
        "Whether you're creating content or relaxing, these headphones are your best companion! 🎬",
    ],
    
    "Smart Thermostat": [
        "Smart Thermostat saves energy and money while keeping you perfectly comfortable. 🌡️💰",
        "Control temperature from anywhere with your phone or voice. Coming home to the perfect temp! 📱",
        "It learns your schedule and adjusts automatically. Smart heating/cooling for smart people! 🧠",
        "Eco-friendly and stylish. Want to know how much you can save on bills? 💚",
    ],
    
    "Smart Light Bulb (4-Pack)": [
        "Smart Light Bulb 4-Pack with 16 million colors and voice control — light up your life! 💡🎨",
        "Works with Alexa and Google Home. Set schedules, scenes, and moods! 🎤",
        "Four bulbs = four rooms of smart lighting magic. Which rooms are you upgrading? 🏠",
        "From warm white to disco purple — these bulbs do it all. Energy-efficient too! ⚡",
    ],
    
    "Mini Drone X2": [
        "Mini Drone X2 is your personal aerial photographer — HD camera, gesture control, obstacle avoidance! 🚁📸",
        "Compact enough to fit in your bag, powerful enough for stunning shots. Adventure ready! 🎒",
        "Beginner-friendly but packed with pro features. Ever flown a drone before? 🎮",
        "Capture angles you never thought possible. Perfect for travel content creators! 🌍",
    ],
    
    "Laptop Stand Pro": [
        "Laptop Stand Pro elevates your workspace — literally! Better posture, better airflow. 💻✨",
        "Ergonomic aluminum design that looks sleek and feels solid. Your neck will thank you! 🙏",
        "Adjustable height and angle. Working from home or office? This is a must-have! 🏠",
        "Say goodbye to back pain and hello to productivity. Compatible with all laptops! 📈",
    ],
    
    "Foldable Wireless Keyboard": [
        "Foldable Wireless Keyboard fits in your pocket and unfolds to full-size typing bliss! ⌨️✈️",
        "Perfect for remote work, travel, or coffee shop productivity sessions! ☕",
        "Bluetooth connects to everything — phone, tablet, laptop. Type anywhere, anytime! 📱",
        "It's like having a full keyboard without the bulk. Digital nomad essential! 🌏",
    ],
    
    "Smart Doorbell Cam": [
        "Smart Doorbell Cam lets you see and talk to visitors from anywhere in the world! 🔔📱",
        "Real-time motion alerts and two-way audio. Never miss a delivery again! 📦",
        "Night vision ensures 24/7 security. See who's at your door, even in the dark! 🌙",
        "Easy installation, huge peace of mind. Thinking of upgrading your home security? 🏠",
    ],
    
    "VR Headset Max": [
        "VR Headset Max transports you to other worlds — immersive gaming and exploration! 🥽🌌",
        "Compatible with major platforms and games. Ready to step into the metaverse? 🎮",
        "Crystal-clear visuals and comfortable for extended sessions. Gaming or virtual travel? ✈️",
        "The future of entertainment is here. What kind of experiences are you most excited about? 🚀",
    ],
    
    "Portable Solar Charger": [
        "Portable Solar Charger harnesses the sun to keep you powered — eco-friendly and unlimited! ☀️🔋",
        "Perfect for camping, hiking, or any outdoor adventure. Never run out of juice! 🏕️",
        "Folds up compact, unfolds to charge multiple devices. Mother Nature's power bank! 🌲",
        "Sustainable energy for sustainable adventures. Where's your next off-grid trip? 🌍",
    ],
}

# Product keyword mapping (for detection)
PRODUCT_KEYWORDS = {
    "smartwatch": "Smartwatch X",
    "smart watch": "Smartwatch X",
    "watch": "Smartwatch X",
    
    "speaker": "Bluetooth Speaker Mini",
    "bluetooth speaker": "Bluetooth Speaker Mini",
    
    "earbuds": "Wireless Earbuds Pro",
    "wireless earbuds": "Wireless Earbuds Pro",
    "headphones": "Noise-Cancelling Headphones",
    "noise cancelling": "Noise-Cancelling Headphones",
    
    "power bank": "Power Bank 20000mAh",
    "powerbank": "Power Bank 20000mAh",
    "portable charger": "Power Bank 20000mAh",
    
    "smart home hub": "Smart Home Hub",
    "home hub": "Smart Home Hub",
    "hub": "Smart Home Hub",
    
    "action camera": "4K Action Camera",
    "4k camera": "4K Action Camera",
    "camera": "4K Action Camera",
    
    "fitness band": "Fitness Tracker Band",
    "fitness tracker": "Fitness Tracker Band",
    "tracker band": "Fitness Tracker Band",
    
    "led strip": "Smart LED Strip Lights",
    "led lights": "Smart LED Strip Lights",
    "strip lights": "Smart LED Strip Lights",
    
    "projector": "Portable Projector Pro",
    "portable projector": "Portable Projector Pro",
    
    "security camera": "Smart Security Camera",
    "security cam": "Smart Security Camera",
    
    "charging pad": "Wireless Charging Pad",
    "wireless charger": "Wireless Charging Pad",
    
    "thermostat": "Smart Thermostat",
    
    "light bulb": "Smart Light Bulb (4-Pack)",
    "smart bulb": "Smart Light Bulb (4-Pack)",
    
    "drone": "Mini Drone X2",
    "mini drone": "Mini Drone X2",
    
    "laptop stand": "Laptop Stand Pro",
    
    "keyboard": "Foldable Wireless Keyboard",
    "wireless keyboard": "Foldable Wireless Keyboard",
    
    "doorbell": "Smart Doorbell Cam",
    "doorbell cam": "Smart Doorbell Cam",
    
    "vr headset": "VR Headset Max",
    "vr": "VR Headset Max",
    "virtual reality": "VR Headset Max",
    
    "solar charger": "Portable Solar Charger",
    "solar": "Portable Solar Charger",
}


def detect_product(user_input):
    """Detect which product the user is asking about"""
    user_input_lower = user_input.lower()
    
    # Check for exact matches first (longer phrases)
    for keyword in sorted(PRODUCT_KEYWORDS.keys(), key=len, reverse=True):
        if keyword in user_input_lower:
            return PRODUCT_KEYWORDS[keyword]
    
    return None


def get_product_response(product_name):
    """Get a natural, random response for the specified product"""
    responses = PRODUCT_RESPONSES.get(product_name, [])
    if responses:
        return random.choice(responses)
    return f"I can tell you more about the {product_name} if you'd like! 😊"


def continue_conversation(product_name, user_input):
    """Continue conversation about the current product based on user intent"""
    user_input_lower = user_input.lower()
    
    # Price inquiry
    if any(word in user_input_lower for word in ['price', 'cost', 'how much', 'expensive', 'cheap']):
        price = PRODUCT_PRICES.get(product_name, "N/A")
        return f"The {product_name} costs ${price}. 💰 Great value for what you get! Would you like to order one?"
    
    # Buying intent
    elif any(word in user_input_lower for word in ['buy', 'purchase', 'order', 'get it', 'take it']):
        return f"Awesome choice! 🎉 I can help you place an order for the {product_name}. Would you like it delivered or picked up? Contact our team at @Store_help_bot for immediate assistance!"
    
    # Comparison request
    elif any(word in user_input_lower for word in ['compare', 'difference', 'better than', 'vs']):
        return "Sure thing! Which product would you like me to compare it with? 🤔 I can help you decide!"
    
    # Color options
    elif 'color' in user_input_lower or 'colour' in user_input_lower:
        return f"The {product_name} comes in several stylish colors — black, silver, and midnight blue. Which one catches your eye? 🎨"
    
    # Features/specs inquiry
    elif any(word in user_input_lower for word in ['feature', 'spec', 'detail', 'info', 'tell me more', 'how does']):
        return get_product_response(product_name)  # Give another variation
    
    # Availability/stock
    elif any(word in user_input_lower for word in ['available', 'stock', 'in stock', 'can i get']):
        return f"Yes! The {product_name} is in stock and ready to ship! 📦✨ Want to place an order?"
    
    # Shipping inquiry
    elif any(word in user_input_lower for word in ['ship', 'delivery', 'arrive', 'how long', 'pickup', 'pick up']):
        return "We offer free shipping on orders over $100! 📦 Standard delivery is 5-7 business days, or express for 2-3 days (+$15). Pickup available at our store! 🌍"
    
    # Warranty/guarantee
    elif any(word in user_input_lower for word in ['warranty', 'guarantee', 'return', 'refund']):
        return "You're covered! 🛡️ 30-day money-back guarantee + 1-year warranty on all products. We stand behind our quality!"
    
    # Positive response
    elif any(word in user_input_lower for word in ['yes', 'yeah', 'sure', 'okay', 'sounds good', 'interested']):
        return get_product_response(product_name)  # Give another variation
    
    # Negative response
    elif any(word in user_input_lower for word in ['no', 'nah', 'not interested', 'maybe later']):
        return "No worries! 😊 Is there anything else you'd like to know, or would you prefer to check out other products?"
    
    # Thank you
    elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
        return "You're very welcome! I'm here if you need any more help. Happy shopping! 🛍️✨"
    
    # Default: give another product variation
    else:
        return get_product_response(product_name)


def handle_user_input(user_input, user_id=None):
    """
    Main conversation handler with context awareness and memory-based personalization.
    
    Args:
        user_input: User's message text
        user_id: Unique user identifier for conversation tracking (optional for backwards compatibility)
    
    Returns:
        Response string or dict with 'text' and 'reply_markup' keys
    """
    # If no user_id provided, use default (for backwards compatibility)
    if user_id is None:
        user_id = "default"
    
    # Initialize user memory if not exists
    if user_id not in user_conversations:
        user_conversations[user_id] = {
            "last_product": None,
            "conversation_history": []
        }
    
    user_memory = user_conversations[user_id]
    
    # Memory-based recall: "show me again", "what was that", "tell me more"
    if any(phrase in user_input.lower() for phrase in ['show me again', 'what was that', 'remind me', 'that one']):
        if user_memory["last_product"]:
            product = user_memory["last_product"]
            return f"Sure! You were looking at the **{product}** earlier. {get_product_response(product)}"
        else:
            return "I don't think we've discussed any products yet! What interests you? 😊"
    
    # Detect if user mentioned a new product
    detected_product = detect_product(user_input)
    
    if detected_product:
        # User mentioned a product - update memory and respond
        user_memory["last_product"] = detected_product
        user_memory["conversation_history"].append({
            "product": detected_product,
            "input": user_input
        })
        
        # Keep only last 5 interactions to save memory
        if len(user_memory["conversation_history"]) > 5:
            user_memory["conversation_history"] = user_memory["conversation_history"][-5:]
        
        return get_product_response(detected_product)
    
    # Continue talking about the current product
    if user_memory["last_product"]:
        return continue_conversation(user_memory["last_product"], user_input)
    
    # No product context yet - ask what they're looking for
    return """Hey there! 👋 What are you shopping for today? 

I can help you find:
💪 Fitness gear (Smartwatch, Fitness Band)
🎧 Audio products (Earbuds, Speakers, Headphones)
🏠 Smart Home devices (Hub, Lights, Cameras, Thermostat)
🎮 Entertainment (VR, Projector, Drone, Action Camera)
💼 Work from home (Laptop Stand, Keyboard)
🔋 Power solutions (Power Bank, Wireless Charger, Solar Charger)

Just tell me what interests you! 😊"""


def reset_conversation(user_id=None):
    """Reset conversation context for a specific user"""
    if user_id is None:
        user_id = "default"
    
    if user_id in user_conversations:
        user_conversations[user_id] = {
            "last_product": None,
            "conversation_history": []
        }


def get_user_memory(user_id):
    """Get conversation memory for a specific user"""
    return user_conversations.get(user_id, {
        "last_product": None,
        "conversation_history": []
    })


def get_product_spec(product_name):
    """Get detailed specifications for a product"""
    return PRODUCT_SPECS.get(product_name, "Detailed specs coming soon!")


def get_random_intro(product_name):
    """Get a randomized introduction for a product"""
    intros = [
        f"You'll love the **{product_name}**! It's one of our bestsellers. 👇",
        f"Let's talk about the **{product_name}** — a customer favorite for good reason!",
        f"Sure thing! Here's what makes the **{product_name}** awesome 👇",
        f"Great choice! The **{product_name}** is amazing. Here's why:",
        f"Ah, the **{product_name}**! Let me tell you about this gem 💎"
    ]
    return random.choice(intros)
