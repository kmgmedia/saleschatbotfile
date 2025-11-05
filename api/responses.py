"""
Fallback keyword-based responses for the bot
"""

# Try to import smart recommendation system and conversation handler
try:
    from .product_catalog import get_smart_recommendation, detect_intent, recommend_products
    from .conversation_handler import handle_user_input as handle_conversation
except ImportError:
    from product_catalog import get_smart_recommendation, detect_intent, recommend_products
    from conversation_handler import handle_user_input as handle_conversation

def get_fallback_response(message, user_id=None):
    """
    Smart fallback responses using:
    1. Natural conversation handler (product-focused with memory)
    2. Intent detection for category browsing
    3. Bundle recommendations
    4. FAQ responses
    
    Args:
        message: User's message text
        user_id: User ID for conversation tracking and memory
    """
    msg = message.lower()
    
    # Priority 1: Use natural conversation handler for product-specific discussions
    # This maintains conversation context and gives human-like responses with memory
    conversation_response = handle_conversation(message, user_id)
    
    # If conversation handler gave a meaningful response (not the generic greeting), use it
    if conversation_response and not conversation_response.startswith("Hey there!"):
        return conversation_response
    
    if any(word in msg for word in ['hi', 'hello', 'hey', 'start']):
        return "👋 Hello! I'm ShopBot from KMGMedia Design & Technologies! We now have 20 amazing tech products ranging from $29 to $850. Browse our Smart Home devices, Audio gear, Wearables, Cameras, and more! What interests you?"
    
    if any(word in msg for word in ['product', 'sell', 'have', 'what', 'show', 'all', 'catalog', 'list']):
        return """🛍️ **Our Complete Product Catalog** (20 Items):

💡 **SMART HOME** ($49-$450)
• Smart LED Strip Lights - $49
• Smart Light Bulb 4-Pack - $99
• Smart Doorbell Cam - $190
• Smart Security Camera - $210
• Smart Thermostat - $220
• Smart Home Hub - $450

🎧 **AUDIO** ($29-$180)
• Bluetooth Speaker Mini - $29
• Wireless Earbuds Pro - $79
• Noise-Cancelling Headphones - $180

⌚ **WEARABLES** ($35-$59)
• Fitness Tracker Band - $35
• Smartwatch X - $59

🔋 **POWER & CHARGING** ($45-$300)
• Wireless Charging Pad - $45
• Portable Solar Charger - $99
• Power Bank 20000mAh - $300

💻 **PRODUCTIVITY** ($75-$89)
• Laptop Stand Pro - $75
• Foldable Wireless Keyboard - $89

📹 **CAMERAS & ENTERTAINMENT** ($250-$850)
• Mini Drone X2 - $250
• Portable Projector Pro - $320
• VR Headset Max - $480
• 4K Action Camera - $850

Which category interests you?"""
    
    # Category browsing (MUST be before individual product detection!)
    if ('smart home' in msg or msg.strip() == 'smart home') and not any(word in msg for word in ['automate', 'automation', 'control lights', 'voice control', 'home security', 'protect home']):
        return """🏠 **SMART HOME PRODUCTS** (6 Items):

💡 **Smart LED Strip Lights** - $49
16 million colors, voice control, music sync, and app-controlled mood lighting. Transform any room!

💡 **Smart Light Bulb (4-Pack)** - $99
Voice-controlled bulbs with 16M colors. Works with Alexa and Google Home. Set schedules & scenes!

🔔 **Smart Doorbell Cam** - $190
See and talk to visitors from anywhere. Real-time motion alerts. Never miss a delivery!

🎥 **Smart Security Camera** - $210
1080p live feed, night vision, and motion alerts. Keep your home safe 24/7. Peace of mind guaranteed!

🌡️ **Smart Thermostat** - $220
AI-powered temperature control with energy-saving schedules and remote access. Save energy in style!

🏠 **Smart Home Hub** - $450
Control all your smart devices from one central hub - lights, thermostats, security, and more!

---

🎁 **SMART HOME BUNDLES:**

**💡 Lighting Starter** - $148 (Save $25!)
LED Strip Lights + Light Bulb 4-Pack

**🔒 Security Bundle** - $400 (Save $50!)
Doorbell Cam + Security Camera

**🏡 Complete Smart Home** - $1,218 (Save $100!)
All 6 smart home products!

Which product or bundle interests you? 🎯"""
    
    if 'audio' in msg and not any(word in msg for word in ['earbud', 'speaker', 'headphone']):
        return """🎧 **AUDIO PRODUCTS** (3 Items):

🔊 **Bluetooth Speaker Mini** - $29
Amazing sound quality with 12-hour battery life. Perfect for any occasion! Compact and powerful.

🎧 **Wireless Earbuds Pro** - $79
Noise cancelling, waterproof, and perfect for workouts and commuting! Great sound quality.

🎧 **Noise-Cancelling Headphones** - $180
Immersive sound and comfort for travelers and creators. Block out the world, focus on what matters!

---

🎁 **AUDIO BUNDLE - Save $20!**
Get all 3 audio products for just **$268** (Regular $288)
✅ Complete audio solution for every situation!

Which audio product interests you? Or type "bundle" to get them all! 🎵"""
    
    if 'wearable' in msg:
        return """⌚ **WEARABLES** (2 Items):

💪 **Fitness Tracker Band** - $35
Lightweight, waterproof, tracks calories & heart rate. For everyday health monitoring. Affordable fitness!

⌚ **Smartwatch X** - $59
Tracks steps, sleep, and heart rate. Perfect for fitness enthusiasts! Great deal!

---

🎁 **FITNESS BUNDLE - Save $15!**
Get both wearables for just **$79** (Regular $94)
✅ Complete fitness tracking solution!

Which one fits your lifestyle? Or get the bundle! 💪"""
    
    if 'power' in msg and 'charging' in msg:
        return """🔋 **POWER & CHARGING** (3 Items):

⚡ **Wireless Charging Pad** - $45
Sleek and fast Qi-certified charger for all devices. Goodbye cables! Clean and convenient!

☀️ **Portable Solar Charger** - $99
Eco-friendly energy solution for camping and travel lovers. Never run out of power outdoors!

🔋 **Power Bank 20000mAh** - $300
Fast-charging with dual USB ports - charge multiple devices at once! Never run out of power!

---

🎁 **POWER BUNDLE - Save $35!**
Get all 3 power products for just **$409** (Regular $444)
✅ Complete power solution for home & travel!

Which power solution do you need? 🔌"""
    
    if 'productivity' in msg or ('work' in msg and 'work from home' not in msg):
        return """💻 **PRODUCTIVITY** (2 Items):

💻 **Laptop Stand Pro** - $75
Ergonomic aluminum stand for better posture and airflow. Work comfortably all day!

⌨️ **Foldable Wireless Keyboard** - $89
Portable Bluetooth keyboard that fits in your bag. Perfect for remote work and travel!

---

🎁 **WORKSPACE BUNDLE - Save $20!**
Get both for just **$144** (Regular $164)
✅ Complete ergonomic workspace setup!

Which one interests you? Or grab the bundle! 💼"""
    
    if ('camera' in msg or 'entertainment' in msg) and not any(word in msg for word in ['security camera', 'doorbell cam', 'action camera', '4k camera']):
        return """📹 **CAMERAS & ENTERTAINMENT** (4 Items):

🚁 **Mini Drone X2** - $250
Compact drone with HD camera, gesture control, and obstacle avoidance. Perfect for aerial photography!

📽️ **Portable Projector Pro** - $320
Pocket-sized projector with HDMI and wireless casting. Movie nights, anywhere! Cinema in your pocket!

🥽 **VR Headset Max** - $480
Immersive gaming and exploration. Compatible with major devices. Step into another world!

📹 **4K Action Camera** - $850
Capture stunning 4K videos with professional image stabilization. Waterproof and rugged for extreme adventures!

---

🎁 **ENTERTAINMENT BUNDLE - Save $120!**
Get all 4 for just **$1,780** (Regular $1,900)
✅ Complete content creation & entertainment setup!

Which one excites you most? 🎬"""
    
    # Smart Home Products (individual items)

    if 'led' in msg or 'strip light' in msg or 'mood light' in msg:
        return "💡 Smart LED Strip Lights - $49! Customizable colors via app control. Set the mood for any room or event. Perfect for gaming setups, bedrooms, or parties! Want one?"
    
    if 'light bulb' in msg or 'smart bulb' in msg or 'alexa' in msg or 'google home' in msg:
        return "💡 Smart Light Bulb 4-Pack - $99! Voice-controlled bulbs with 16M colors. Works with Alexa and Google Home. Transform your home lighting! Interested?"
    
    if 'doorbell' in msg or 'door cam' in msg or 'doorbell cam' in msg:
        return "� Smart Doorbell Cam - $190! See and talk to visitors from anywhere. Real-time motion alerts included. Never miss a delivery! Want to learn more?"
    
    if 'security camera' in msg or 'security cam' in msg or 'surveillance' in msg:
        return "🎥 Smart Security Camera - $210! 1080p live feed, night vision, and motion alerts. Keep your home safe 24/7. Peace of mind guaranteed! Interested?"
    
    if 'thermostat' in msg or 'temperature' in msg or 'heating' in msg or 'cooling' in msg:
        return "�️ Smart Thermostat - $220! Adjust temperature with your phone or voice assistant. Save energy in style and reduce bills! Want one?"
    
    # Audio Products
    if 'earbud' in msg or 'wireless earbuds' in msg:
        return "🎧 Wireless Earbuds Pro - $79! Noise cancelling, waterproof, and perfect for workouts and commuting! Great sound quality. Interested?"
    
    if 'headphone' in msg or 'noise cancel' in msg or 'anc' in msg:
        return "🎧 Noise-Cancelling Headphones - $180! Immersive sound and comfort for travelers and creators. Block out the world, focus on what matters! Want them?"
    
    if 'speaker' in msg or 'bluetooth speaker' in msg:
        return "🔊 Bluetooth Speaker Mini - $29! Amazing sound quality with 12-hour battery life. Perfect for any occasion! Great value! Interested?"
    
    # Wearables
    if 'watch' in msg or 'smartwatch' in msg:
        return "⌚ Smartwatch X - $59! Tracks steps, sleep, and heart rate. Perfect for fitness enthusiasts! Great deal! Want one?"
    
    if 'fitness tracker' in msg or 'fitness band' in msg or 'health monitor' in msg:
        return "💪 Fitness Tracker Band - $35! Lightweight, waterproof, tracks calories and heart rate. For everyday health monitoring. Affordable fitness! Interested?"
    
    # Power & Charging
    if 'wireless charging' in msg or 'charging pad' in msg or 'qi charger' in msg:
        return "⚡ Wireless Charging Pad - $45! Sleek and fast Qi-certified charger for all devices. Goodbye cables! Clean and convenient! Want one?"
    
    if 'solar' in msg or 'solar charger' in msg or 'eco' in msg:
        return "☀️ Portable Solar Charger - $99! Eco-friendly energy solution for camping and travel lovers. Never run out of power outdoors! Interested?"
    
    if 'power bank' in msg or 'powerbank' in msg or 'battery pack' in msg:
        return "🔋 Power Bank 20000mAh - $300! Fast-charging with dual USB ports - charge multiple devices at once! Never run out of power! Want one?"
    
    # Productivity
    if 'laptop stand' in msg or 'stand' in msg or 'ergonomic' in msg:
        return "💻 Laptop Stand Pro - $75! Ergonomic aluminum stand for better posture and airflow. Work comfortably all day! Interested?"
    
    if 'keyboard' in msg or 'wireless keyboard' in msg or 'foldable' in msg:
        return "⌨️ Foldable Wireless Keyboard - $89! Portable Bluetooth keyboard that fits in your bag. Perfect for remote work and travel! Want one?"
    
    # Cameras & Entertainment
    if 'drone' in msg or 'mini drone' in msg or 'quadcopter' in msg:
        return "🚁 Mini Drone X2 - $250! Compact drone with HD camera, gesture control, and obstacle avoidance. Perfect for aerial photography! Interested?"
    
    if 'projector' in msg or 'portable projector' in msg or 'movie' in msg:
        return "📽️ Portable Projector Pro - $320! Pocket-sized projector with HDMI and wireless casting. Movie nights, anywhere! Cinema in your pocket! Want it?"
    
    if 'vr' in msg or 'virtual reality' in msg or 'vr headset' in msg:
        return "🥽 VR Headset Max - $480! Immersive gaming and exploration. Compatible with major devices. Step into another world! Interested?"
    
    if 'camera' in msg or 'action camera' in msg or '4k' in msg or 'video' in msg:
        return "📹 4K Action Camera - $850! Capture stunning 4K videos with professional image stabilization. Waterproof and rugged for extreme adventures! Want one?"
    
    if 'smart home' in msg or 'home hub' in msg or 'hub' in msg:
        return "🏠 Smart Home Hub - $450! Control all your smart devices from one central hub - lights, thermostats, security, and more! Make your home smarter! Interested?"
    
    if 'price' in msg or 'cost' in msg or 'how much' in msg:
        return """💰 **Our Price Range:**

**Budget-Friendly** ($29-$59)
🔊 Speaker Mini: $29 | 💪 Fitness Band: $35 | ⚡ Charging Pad: $45 | 💡 LED Strips: $49 | ⌚ Smartwatch X: $59

**Mid-Range** ($75-$220)
💻 Laptop Stand: $75 | 🎧 Earbuds Pro: $79 | ⌨️ Keyboard: $89 | � Light Bulbs: $99 | ☀️ Solar Charger: $99 | 🎧 Headphones: $180 | 🔔 Doorbell Cam: $190 | 🎥 Security Cam: $210 | 🌡️ Thermostat: $220

**Premium** ($250-$850)
🚁 Mini Drone: $250 | 🔋 Power Bank: $300 | 📽️ Projector: $320 | 🏠 Smart Hub: $450 | 🥽 VR Headset: $480 | 📹 4K Camera: $850

Which price range interests you?"""
    
    if any(word in msg for word in ['buy', 'order', 'purchase', 'want', 'get']):
        return "🎉 Awesome! I'd love to help you with that! To complete your order:\n\n1️⃣ Tell me which product(s) you want\n2️⃣ Contact our team at @Store_help_bot\n3️⃣ We'll send payment & shipping details\n\n✅ Free shipping on orders over $100\n✅ 30-day money-back guarantee\n✅ 1-year warranty on all products\n\nWhich product are you interested in?"
    
    if 'shipping' in msg or 'delivery' in msg or 'ship' in msg:
        return "📦 Shipping Information:\n\n✅ Free shipping on orders over $100\n✅ Standard delivery: 5-7 business days\n✅ Express delivery: 2-3 business days (+$15)\n✅ Track your order online\n\nWe ship worldwide! 🌍"
    
    if 'warranty' in msg or 'guarantee' in msg or 'return' in msg:
        return "🛡️ Protection & Returns:\n\n✅ 30-day money-back guarantee\n✅ 1-year warranty on all products\n✅ Free returns on defective items\n✅ Easy exchange process\n\nYour satisfaction is our priority! 💯"
    
    # Fitness Intent Detection with Smart Bundles
    if any(word in msg for word in ['fitness', 'track health', 'workout', 'gym', 'exercise', 'run', 'running', 'steps', 'heart rate', 'calories', 'hydration', 'health', 'cardio', 'training', 'athlete']):
        return """💪 **Fitness & Health Tracking Solutions!**

**Individual Products:**
⌚ **Smartwatch X** - $59
Tracks steps, sleep, heart rate. Perfect fitness companion!

💪 **Fitness Tracker Band** - $35
Lightweight, waterproof, tracks calories & heart rate. Daily monitoring made easy!

🎧 **Wireless Earbuds Pro** - $79
Noise cancelling & waterproof. Perfect for intense workouts!

🎧 **Noise-Cancelling Headphones** - $180
Immersive sound for focused training sessions.

---

🎁 **RECOMMENDED BUNDLES - SAVE MORE!**

**🏃 Starter Fitness Bundle - $94** (Save $20!)
✅ Fitness Tracker Band ($35)
✅ Smartwatch X ($59)
→ Track everything: steps, calories, heart rate, sleep!

**💪 Complete Workout Bundle - $173** (Save $31!)
✅ Smartwatch X ($59)
✅ Wireless Earbuds Pro ($79)
✅ Fitness Tracker Band ($35)
→ Ultimate fitness tracking + premium workout audio!

**🎯 Premium Athlete Bundle - $314** (Save $45!)
✅ Smartwatch X ($59)
✅ Noise-Cancelling Headphones ($180)
✅ Fitness Tracker Band ($35)
✅ Wireless Charging Pad ($45)
→ Complete setup for serious athletes!

Which option works best for your fitness goals? 🏋️"""
    
    # Smart Home Intent Detection
    if any(word in msg for word in ['smart home', 'automate', 'automation', 'control lights', 'voice control', 'home security', 'protect home']):
        return """🏠 **Smart Home Solutions!**

**Individual Products:**
💡 Smart LED Strip Lights - $49
💡 Smart Light Bulb 4-Pack - $99
🔔 Smart Doorbell Cam - $190
🎥 Smart Security Camera - $210
🌡️ Smart Thermostat - $220
🏠 Smart Home Hub - $450

---

🎁 **SMART HOME BUNDLES:**

**💡 Lighting Starter - $148** (Save $25!)
✅ Smart LED Strip Lights ($49)
✅ Smart Light Bulb 4-Pack ($99)
→ Transform your home lighting with colors & voice control!

**🔒 Security Bundle - $400** (Save $50!)
✅ Smart Doorbell Cam ($190)
✅ Smart Security Camera ($210)
→ Complete home security monitoring!

**🏡 Complete Smart Home - $1,218** (Save $100!)
✅ All 6 smart home products
→ Fully automated, voice-controlled smart home!

Ready to make your home smarter? 🎯"""
    
    # Entertainment/Gaming Intent
    if any(word in msg for word in ['entertainment', 'gaming', 'game', 'play', 'movie', 'watch', 'stream', 'fun', 'party']):
        return """🎮 **Entertainment & Gaming Setup!**

**Individual Products:**
📽️ Portable Projector Pro - $320
🥽 VR Headset Max - $480
🎧 Noise-Cancelling Headphones - $180
🔊 Bluetooth Speaker Mini - $29
💡 Smart LED Strip Lights - $49

---

🎁 **ENTERTAINMENT BUNDLES:**

**🎬 Movie Night Bundle - $398** (Save $51!)
✅ Portable Projector Pro ($320)
✅ Bluetooth Speaker Mini ($29)
✅ Smart LED Strip Lights ($49)
→ Cinema experience anywhere!

**🎮 Ultimate Gaming Bundle - $709** (Save $71!)
✅ VR Headset Max ($480)
✅ Noise-Cancelling Headphones ($180)
✅ Smart LED Strip Lights ($49)
→ Immersive gaming paradise!

**🎉 Party Bundle - $78** (Save $20!)
✅ Bluetooth Speaker Mini ($29)
✅ Smart LED Strip Lights ($49)
→ Perfect ambiance for any event!

What's your entertainment style? 🎯"""
    
    # Work from Home / Productivity Intent
    if any(word in msg for word in ['work from home', 'remote work', 'productivity', 'office', 'desk setup', 'ergonomic', 'typing', 'computer']):
        return """💼 **Work From Home & Productivity Setup!**

**Individual Products:**
💻 Laptop Stand Pro - $75
⌨️ Foldable Wireless Keyboard - $89
⚡ Wireless Charging Pad - $45
🎧 Noise-Cancelling Headphones - $180

---

🎁 **PRODUCTIVITY BUNDLES:**

**⚙️ Essential Workspace - $164** (Save $25!)
✅ Laptop Stand Pro ($75)
✅ Foldable Wireless Keyboard ($89)
→ Ergonomic setup for better posture & typing!

**🎯 Focus Bundle - $344** (Save $46!)
✅ Laptop Stand Pro ($75)
✅ Foldable Wireless Keyboard ($89)
✅ Noise-Cancelling Headphones ($180)
→ Ultimate focus and comfort for productivity!

**⚡ Complete Home Office - $389** (Save $60!)
✅ All 4 productivity products
→ Professional workspace with wireless convenience!

Ready to upgrade your workspace? 🚀"""
    
    # Travel Intent
    if any(word in msg for word in ['travel', 'trip', 'vacation', 'portable', 'camping', 'adventure', 'backpack', 'on the go']):
        return """✈️ **Travel & Adventure Essentials!**

**Individual Products:**
🔋 Power Bank 20000mAh - $300
☀️ Portable Solar Charger - $99
📽️ Portable Projector Pro - $320
⌨️ Foldable Wireless Keyboard - $89
🎧 Wireless Earbuds Pro - $79
📹 4K Action Camera - $850
🚁 Mini Drone X2 - $250

---

🎁 **TRAVELER BUNDLES:**

**🎒 Backpacker's Power Bundle - $399** (Save $78!)
✅ Power Bank 20000mAh ($300)
✅ Portable Solar Charger ($99)
✅ Wireless Earbuds Pro ($79)
→ Never run out of power on the road!

**📸 Adventure Creator - $1,100** (Save $149!)
✅ 4K Action Camera ($850)
✅ Mini Drone X2 ($250)
→ Capture stunning content from land & sky!

**💼 Digital Nomad Bundle - $808** (Save $120!)
✅ Portable Projector Pro ($320)
✅ Foldable Wireless Keyboard ($89)
✅ Power Bank 20000mAh ($300)
✅ Portable Solar Charger ($99)
→ Work & play anywhere in the world!

Where's your next adventure? 🌍"""
    
    if 'thank' in msg or 'thanks' in msg:
        return "😊 You're welcome! Happy to help! Let me know if you need anything else!"
    
    return """I'm here to help you find the perfect tech product! 🛍️

**Browse by Category:**
💡 Smart Home (6 products)
🎧 Audio (3 products)
⌚ Wearables (2 products)
🔋 Power & Charging (3 products)
💻 Productivity (2 products)
📹 Cameras & Entertainment (4 products)

**Or tell me your use case:**
💪 Fitness & Health
🏠 Smart Home Automation
🎮 Entertainment & Gaming
💼 Work From Home
✈️ Travel & Adventure

Type a category or use case!"""
    
    # Category browsing
    if ('smart home' in msg or msg.strip() == 'smart home') and not any(word in msg for word in ['automate', 'automation', 'control lights', 'voice control', 'home security', 'protect home']):
        return """🏠 **SMART HOME PRODUCTS** (6 Items):

💡 **Smart LED Strip Lights** - $49
16 million colors, voice control, music sync, and app-controlled mood lighting. Transform any room!

💡 **Smart Light Bulb (4-Pack)** - $99
Voice-controlled bulbs with 16M colors. Works with Alexa and Google Home. Set schedules & scenes!

🔔 **Smart Doorbell Cam** - $190
See and talk to visitors from anywhere. Real-time motion alerts. Never miss a delivery!

🎥 **Smart Security Camera** - $210
1080p live feed, night vision, and motion alerts. Keep your home safe 24/7. Peace of mind guaranteed!

🌡️ **Smart Thermostat** - $220
AI-powered temperature control with energy-saving schedules and remote access. Save energy in style!

🏠 **Smart Home Hub** - $450
Control all your smart devices from one central hub - lights, thermostats, security, and more!

---

🎁 **SMART HOME BUNDLES:**

**💡 Lighting Starter** - $148 (Save $25!)
LED Strip Lights + Light Bulb 4-Pack

**🔒 Security Bundle** - $400 (Save $50!)
Doorbell Cam + Security Camera

**🏡 Complete Smart Home** - $1,218 (Save $100!)
All 6 smart home products!

Which product or bundle interests you? 🎯"""
    
    if 'audio' in msg and not any(word in msg for word in ['earbud', 'speaker', 'headphone']):
        return """🎧 **AUDIO PRODUCTS** (3 Items):

🔊 **Bluetooth Speaker Mini** - $29
Amazing sound quality with 12-hour battery life. Perfect for any occasion! Compact and powerful.

🎧 **Wireless Earbuds Pro** - $79
Noise cancelling, waterproof, and perfect for workouts and commuting! Great sound quality.

🎧 **Noise-Cancelling Headphones** - $180
Immersive sound and comfort for travelers and creators. Block out the world, focus on what matters!

---

🎁 **AUDIO BUNDLE - Save $20!**
Get all 3 audio products for just **$268** (Regular $288)
✅ Complete audio solution for every situation!

Which audio product interests you? Or type "bundle" to get them all! 🎵"""
    
    if 'wearable' in msg:
        return """⌚ **WEARABLES** (2 Items):

💪 **Fitness Tracker Band** - $35
Lightweight, waterproof, tracks calories & heart rate. For everyday health monitoring. Affordable fitness!

⌚ **Smartwatch X** - $59
Tracks steps, sleep, and heart rate. Perfect for fitness enthusiasts! Great deal!

---

🎁 **FITNESS BUNDLE - Save $15!**
Get both wearables for just **$79** (Regular $94)
✅ Complete fitness tracking solution!

Which one fits your lifestyle? Or get the bundle! 💪"""
    
    if 'power' in msg and 'charging' in msg:
        return """🔋 **POWER & CHARGING** (3 Items):

⚡ **Wireless Charging Pad** - $45
Sleek and fast Qi-certified charger for all devices. Goodbye cables! Clean and convenient!

☀️ **Portable Solar Charger** - $99
Eco-friendly energy solution for camping and travel lovers. Never run out of power outdoors!

🔋 **Power Bank 20000mAh** - $300
Fast-charging with dual USB ports - charge multiple devices at once! Never run out of power!

---

🎁 **POWER BUNDLE - Save $35!**
Get all 3 power products for just **$409** (Regular $444)
✅ Complete power solution for home & travel!

Which power solution do you need? 🔌"""
    
    if 'productivity' in msg or 'work' in msg and not 'work from home' in msg:
        return """💻 **PRODUCTIVITY** (2 Items):

💻 **Laptop Stand Pro** - $75
Ergonomic aluminum stand for better posture and airflow. Work comfortably all day!

⌨️ **Foldable Wireless Keyboard** - $89
Portable Bluetooth keyboard that fits in your bag. Perfect for remote work and travel!

---

🎁 **WORKSPACE BUNDLE - Save $20!**
Get both for just **$144** (Regular $164)
✅ Complete ergonomic workspace setup!

Which one interests you? Or grab the bundle! 💼"""
    
    if 'camera' in msg or 'entertainment' in msg:
        return """📹 **CAMERAS & ENTERTAINMENT** (4 Items):

🚁 **Mini Drone X2** - $250
Compact drone with HD camera, gesture control, and obstacle avoidance. Perfect for aerial photography!

📽️ **Portable Projector Pro** - $320
Pocket-sized projector with HDMI and wireless casting. Movie nights, anywhere! Cinema in your pocket!

🥽 **VR Headset Max** - $480
Immersive gaming and exploration. Compatible with major devices. Step into another world!

📹 **4K Action Camera** - $850
Capture stunning 4K videos with professional image stabilization. Waterproof and rugged for extreme adventures!

---

🎁 **ENTERTAINMENT BUNDLE - Save $120!**
Get all 4 for just **$1,780** (Regular $1,900)
✅ Complete content creation & entertainment setup!

Which one excites you most? 🎬"""
    
    if 'thank' in msg or 'thanks' in msg:
        return "😊 You're welcome! Happy to help! Let me know if you need anything else!"
    
    return """I'm here to help you find the perfect tech product! 🛍️

**Browse by Category:**
💡 Smart Home (6 products)
🎧 Audio (3 products)
⌚ Wearables (2 products)
🔋 Power & Charging (3 products)
💻 Productivity (2 products)
📹 Cameras & Entertainment (4 products)

**Or tell me your use case:**
💪 Fitness & Health
🏠 Smart Home Automation
🎮 Entertainment & Gaming
💼 Work From Home
✈️ Travel & Adventure

Type a category or use case!"""
