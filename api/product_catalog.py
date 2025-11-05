"""
Product catalog with categories for intelligent recommendations
"""

PRODUCTS = [
    # Fitness & Wearables
    {
        "id": 1,
        "name": "Smartwatch X",
        "price": 59,
        "category": "fitness",
        "description": "Tracks steps, sleep, and heart rate. Perfect for fitness enthusiasts!",
        "keywords": ["watch", "smartwatch", "fitness", "steps", "sleep", "heart rate"]
    },
    {
        "id": 2,
        "name": "Fitness Tracker Band",
        "price": 35,
        "category": "fitness",
        "description": "Lightweight, waterproof, tracks calories and heart rate. For everyday health monitoring.",
        "keywords": ["fitness", "tracker", "band", "health", "calories", "heart rate", "waterproof"]
    },
    
    # Audio
    {
        "id": 3,
        "name": "Bluetooth Speaker Mini",
        "price": 29,
        "category": "audio",
        "description": "Crisp sound and 12h battery life. Great for music lovers on the go!",
        "keywords": ["speaker", "bluetooth", "music", "audio", "sound"]
    },
    {
        "id": 4,
        "name": "Wireless Earbuds Pro",
        "price": 79,
        "category": "audio",
        "description": "Noise cancelling and waterproof. Ideal for workouts and commuting!",
        "keywords": ["earbuds", "headphones", "wireless", "noise", "cancelling", "workout"]
    },
    {
        "id": 5,
        "name": "Noise-Cancelling Headphones",
        "price": 180,
        "category": "audio",
        "description": "Immersive sound and comfort for travelers and creators.",
        "keywords": ["headphones", "noise", "cancelling", "audio", "travel", "comfort"]
    },
    
    # Power & Charging
    {
        "id": 6,
        "name": "Power Bank 20000mAh",
        "price": 300,
        "category": "power",
        "description": "Fast-charging power bank with dual USB ports. Never run out of power!",
        "keywords": ["power", "bank", "battery", "charging", "portable", "usb"]
    },
    {
        "id": 7,
        "name": "Wireless Charging Pad",
        "price": 45,
        "category": "power",
        "description": "Sleek and fast Qi-certified charger for all devices. Goodbye cables!",
        "keywords": ["wireless", "charging", "pad", "qi", "charger"]
    },
    {
        "id": 8,
        "name": "Portable Solar Charger",
        "price": 99,
        "category": "power",
        "description": "Eco-friendly energy solution for camping and travel lovers.",
        "keywords": ["solar", "charger", "portable", "eco", "camping", "travel"]
    },
    
    # Smart Home
    {
        "id": 9,
        "name": "Smart Home Hub",
        "price": 450,
        "category": "smart_home",
        "description": "Control all your smart devices from one hub. Make your home smarter!",
        "keywords": ["smart", "home", "hub", "automation", "control", "devices"]
    },
    {
        "id": 10,
        "name": "Smart LED Strip Lights",
        "price": 49,
        "category": "smart_home",
        "description": "Customizable colors via app control. Set the mood for any room or event.",
        "keywords": ["led", "lights", "strip", "smart", "colors", "app", "mood"]
    },
    {
        "id": 11,
        "name": "Smart Light Bulb (4-Pack)",
        "price": 99,
        "category": "smart_home",
        "description": "Voice-controlled bulbs with 16M colors. Works with Alexa and Google Home.",
        "keywords": ["light", "bulb", "smart", "voice", "alexa", "google", "colors"]
    },
    {
        "id": 12,
        "name": "Smart Doorbell Cam",
        "price": 190,
        "category": "smart_home",
        "description": "See and talk to visitors from anywhere. Real-time motion alerts included.",
        "keywords": ["doorbell", "camera", "smart", "security", "motion", "alerts"]
    },
    {
        "id": 13,
        "name": "Smart Security Camera",
        "price": 210,
        "category": "smart_home",
        "description": "1080p live feed, night vision, and motion alerts. Keep your home safe 24/7.",
        "keywords": ["security", "camera", "smart", "1080p", "night vision", "surveillance"]
    },
    {
        "id": 14,
        "name": "Smart Thermostat",
        "price": 220,
        "category": "smart_home",
        "description": "Adjust temperature with your phone or voice assistant. Save energy in style.",
        "keywords": ["thermostat", "smart", "temperature", "energy", "voice", "phone"]
    },
    
    # Cameras & Entertainment
    {
        "id": 15,
        "name": "4K Action Camera",
        "price": 850,
        "category": "entertainment",
        "description": "Capture stunning 4K videos with image stabilization. Perfect for adventures!",
        "keywords": ["camera", "4k", "action", "video", "adventure", "waterproof"]
    },
    {
        "id": 16,
        "name": "Portable Projector Pro",
        "price": 320,
        "category": "entertainment",
        "description": "Pocket-sized projector with HDMI and wireless casting. Movie nights, anywhere!",
        "keywords": ["projector", "portable", "movie", "hdmi", "wireless", "casting"]
    },
    {
        "id": 17,
        "name": "VR Headset Max",
        "price": 480,
        "category": "entertainment",
        "description": "Immersive gaming and exploration. Compatible with major devices.",
        "keywords": ["vr", "virtual reality", "headset", "gaming", "immersive"]
    },
    {
        "id": 18,
        "name": "Mini Drone X2",
        "price": 250,
        "category": "entertainment",
        "description": "Compact drone with HD camera, gesture control, and obstacle avoidance.",
        "keywords": ["drone", "camera", "hd", "flying", "aerial", "gesture"]
    },
    
    # Productivity
    {
        "id": 19,
        "name": "Laptop Stand Pro",
        "price": 75,
        "category": "productivity",
        "description": "Ergonomic aluminum stand for better posture and airflow.",
        "keywords": ["laptop", "stand", "ergonomic", "desk", "aluminum", "posture"]
    },
    {
        "id": 20,
        "name": "Foldable Wireless Keyboard",
        "price": 89,
        "category": "productivity",
        "description": "Portable Bluetooth keyboard that fits in your bag — perfect for remote work.",
        "keywords": ["keyboard", "wireless", "foldable", "portable", "bluetooth", "work"]
    },
]

# Category definitions with keywords
INTENT_KEYWORDS = {
    "fitness": ["fitness", "workout", "track", "steps", "exercise", "health", "gym", "run", "running", "calories", "heart rate", "training", "athlete", "cardio"],
    "audio": ["music", "sound", "audio", "speaker", "headphones", "earbuds", "listen", "bluetooth", "noise", "bass"],
    "power": ["battery", "power", "charging", "charger", "energy", "portable power", "solar", "wireless charging"],
    "smart_home": ["smart home", "automation", "automate", "control", "lights", "security", "camera", "thermostat", "doorbell", "home"],
    "entertainment": ["gaming", "game", "movie", "watch", "entertainment", "fun", "vr", "projector", "drone", "camera", "video"],
    "productivity": ["work", "office", "desk", "productivity", "ergonomic", "laptop", "keyboard", "remote work", "typing"],
}


def detect_intent(user_input):
    """
    Detect user intent based on keywords in their message
    Returns the category name or 'general' if no match
    """
    user_input_lower = user_input.lower()
    
    # Check each category
    for category, keywords in INTENT_KEYWORDS.items():
        if any(keyword in user_input_lower for keyword in keywords):
            return category
    
    return "general"


def recommend_products(intent, max_results=5):
    """
    Recommend products based on detected intent
    Returns a list of matching products
    """
    if intent == "general":
        # Return top products from each category
        return PRODUCTS[:max_results]
    
    # Filter products by category
    recommendations = [p for p in PRODUCTS if p["category"] == intent]
    return recommendations[:max_results]


def format_product_list(products):
    """
    Format product list for display in chat
    """
    if not products:
        return "Hmm, I couldn't find a product for that yet. Try asking about fitness, audio, smart home, or entertainment!"
    
    result = []
    for product in products:
        result.append(f"• **{product['name']}** - ${product['price']}\n  {product['description']}")
    
    return "\n\n".join(result)


def get_category_name(category):
    """
    Get friendly category name
    """
    category_names = {
        "fitness": "Fitness & Health Tracking",
        "audio": "Audio & Sound",
        "power": "Power & Charging",
        "smart_home": "Smart Home",
        "entertainment": "Cameras & Entertainment",
        "productivity": "Productivity & Work"
    }
    return category_names.get(category, "General")


def get_smart_recommendation(user_message):
    """
    Main function: Detect intent and return smart product recommendations
    """
    intent = detect_intent(user_message)
    products = recommend_products(intent)
    
    if intent == "general":
        header = "🛍️ Here are our featured products:\n\n"
    else:
        category_name = get_category_name(intent)
        header = f"✨ Great choice! Here are our {category_name} products:\n\n"
    
    product_list = format_product_list(products)
    
    return header + product_list
