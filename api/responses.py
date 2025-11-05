"""
Fallback keyword-based responses for the bot
"""

def get_fallback_response(message):
    """Simple keyword-based responses as fallback when OpenAI is unavailable"""
    msg = message.lower()
    
    if any(word in msg for word in ['hi', 'hello', 'hey', 'start']):
        return "👋 Hello! I'm ShopBot, your shopping assistant from KMGMedia Design & Technologies. We have amazing tech products: Wireless Earbuds Pro ($79), Smartwatch X ($59), Bluetooth Speaker Mini ($29), Power Bank 20000mAh ($300), Smart Home Hub ($450), and 4K Action Camera ($850). What interests you?"
    
    if any(word in msg for word in ['product', 'sell', 'have', 'what', 'show', 'all', 'catalog']):
        return "🛍️ Here are our amazing products:\n\n🎧 Wireless Earbuds Pro - $79\nNoise cancelling, waterproof, perfect for workouts!\n\n⌚ Smartwatch X - $59\nTracks fitness, sleep & heart rate\n\n🔊 Bluetooth Speaker Mini - $29\nAmazing sound, 12-hour battery\n\n🔋 Power Bank 20000mAh - $300\nFast-charging with dual USB ports\n\n🏠 Smart Home Hub - $450\nControl all your smart devices from one hub\n\n📹 4K Action Camera - $850\nCapture stunning 4K videos with image stabilization\n\nWhich one interests you?"
    
    if 'earbud' in msg or 'headphone' in msg:
        return "🎧 Great choice! Our Wireless Earbuds Pro are $79. They're noise cancelling, waterproof, and perfect for workouts! Would you like to know more?"
    
    if 'watch' in msg or 'smartwatch' in msg:
        return "⌚ The Smartwatch X is $59! It tracks your fitness, sleep, and heart rate. It's a fantastic deal! Interested?"
    
    if 'speaker' in msg:
        return "🔊 Our Bluetooth Speaker Mini is just $29! Amazing sound quality with 12-hour battery life. Perfect for any occasion! Want one?"
    
    if 'power bank' in msg or 'powerbank' in msg or 'battery' in msg or ('charger' in msg and 'port' in msg):
        return "🔋 Excellent choice! Our Power Bank 20000mAh is $300. Fast-charging with dual USB ports - charge multiple devices at once! Never run out of power again. Interested?"
    
    if 'smart home' in msg or 'home hub' in msg or 'hub' in msg:
        return "🏠 Amazing! The Smart Home Hub is $450. Control all your smart devices from one central hub - lights, thermostats, security, and more! Make your home smarter. Want to learn more?"
    
    if 'camera' in msg or 'action camera' in msg or '4k' in msg or 'video' in msg:
        return "📹 Perfect for adventure! Our 4K Action Camera is $850. Capture stunning 4K videos with professional image stabilization. Waterproof and rugged - built for extreme conditions! Ready to capture amazing moments?"
    
    if 'price' in msg or 'cost' in msg or 'how much' in msg:
        return "💰 Our prices:\n🎧 Earbuds Pro: $79\n⌚ Smartwatch X: $59\n🔊 Speaker Mini: $29\n🔋 Power Bank 20000mAh: $300\n🏠 Smart Home Hub: $450\n📹 4K Action Camera: $850\n\nGreat deals on quality tech products! Which one would you like?"
    
    if any(word in msg for word in ['buy', 'order', 'purchase', 'want', 'get']):
        return "🎉 Awesome! I'd love to help you with that! To complete your order:\n\n1️⃣ Tell me which product(s) you want\n2️⃣ Contact our team at @Store_help_bot\n3️⃣ We'll send payment & shipping details\n\n✅ Free shipping on orders over $100\n✅ 30-day money-back guarantee\n✅ 1-year warranty on all products\n\nWhich product are you interested in?"
    
    if 'shipping' in msg or 'delivery' in msg or 'ship' in msg:
        return "📦 Shipping Information:\n\n✅ Free shipping on orders over $100\n✅ Standard delivery: 5-7 business days\n✅ Express delivery: 2-3 business days (+$15)\n✅ Track your order online\n\nWe ship worldwide! 🌍"
    
    if 'warranty' in msg or 'guarantee' in msg or 'return' in msg:
        return "🛡️ Protection & Returns:\n\n✅ 30-day money-back guarantee\n✅ 1-year warranty on all products\n✅ Free returns on defective items\n✅ Easy exchange process\n\nYour satisfaction is our priority! 💯"
    
    if 'thank' in msg or 'thanks' in msg:
        return "😊 You're welcome! Happy to help! Let me know if you need anything else!"
    
    return "I'm here to help you find the perfect tech product! 🛍️\n\nWe have:\n🎧 Audio (Earbuds, Speaker)\n⌚ Wearables (Smartwatch)\n🔋 Power Solutions (Power Bank)\n🏠 Smart Home (Hub)\n📹 Cameras (4K Action Camera)\n\nWhat would you like to know more about?"
