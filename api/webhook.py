"""
Vercel webhook endpoint for Telegram bot with OpenAI
"""
import os
import requests
from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Load prompts from files
def load_prompt(filename):
    """Load prompt content from prompts folder"""
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error loading {filename}: {e}", file=sys.stderr)
        return ""

SYSTEM_PROMPT = load_prompt('system_prompt.txt')
PRODUCTS_LIST = load_prompt('products.txt')
SALES_STYLE = load_prompt('sales_style.txt')

# Log for debugging
print(f"Telegram Token loaded: {'Yes' if TELEGRAM_TOKEN else 'No'}", file=sys.stderr)
print(f"OpenAI Key loaded: {'Yes' if OPENAI_API_KEY else 'No'}", file=sys.stderr)
print(f"Token prefix: {TELEGRAM_TOKEN[:10]}..." if TELEGRAM_TOKEN else "No token", file=sys.stderr)
print(f"Prompts loaded - System: {len(SYSTEM_PROMPT)} chars, Products: {len(PRODUCTS_LIST)} chars", file=sys.stderr)

# OpenAI-powered response function
def get_response(message):
    """Get chatbot response using OpenAI API"""
    
    # If OpenAI key is not available, fall back to keyword responses
    if not OPENAI_API_KEY:
        print("WARNING: No OpenAI key - using fallback responses", file=sys.stderr)
        return get_fallback_response(message)
    
    try:
        # Build the full prompt from loaded files
        prompt = f"""{SYSTEM_PROMPT}

{PRODUCTS_LIST}

User: {message}

ShopBot:"""

        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': SALES_STYLE},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 200
        }
        
        response = requests.post('https://api.openai.com/v1/chat/completions', 
                                headers=headers, 
                                json=data,
                                timeout=25)
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content'].strip()
            print(f"OpenAI response successful", file=sys.stderr)
            return reply
        else:
            print(f"OpenAI API error: {response.status_code} - {response.text}", file=sys.stderr)
            return get_fallback_response(message)
            
    except Exception as e:
        print(f"OpenAI exception: {str(e)}", file=sys.stderr)
        return get_fallback_response(message)

def get_fallback_response(message):
    """Simple keyword-based responses as fallback"""
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

@app.route('/', methods=['GET'])
def health():
    # Serve a nice landing page
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="15; url=https://t.me/Store_help_bot">
        <title>ShopBot - AI Shopping Assistant</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: white;
                text-align: center;
                padding: 20px;
            }
            .container {
                max-width: 500px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            .logo {
                font-size: 80px;
                margin-bottom: 20px;
                animation: bounce 2s infinite;
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 15px;
            }
            p {
                font-size: 1.2rem;
                margin-bottom: 30px;
                opacity: 0.9;
            }
            .btn {
                display: inline-block;
                background: #0088cc;
                color: white;
                padding: 15px 40px;
                text-decoration: none;
                border-radius: 50px;
                font-size: 1.1rem;
                font-weight: bold;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(0, 136, 204, 0.4);
            }
            .btn:hover {
                background: #006ba3;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 136, 204, 0.6);
            }
            .products {
                margin-top: 30px;
                font-size: 0.9rem;
                opacity: 0.8;
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            .loader {
                margin-top: 20px;
                font-size: 0.9rem;
                opacity: 0.7;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🛍️</div>
            <h1>ShopBot</h1>
            <p>Your AI Shopping Assistant</p>
            <a href="https://t.me/Store_help_bot" class="btn">
                💬 Open on Telegram
            </a>
            <div class="products">
                <p>Browse our amazing tech products:</p>
                <p>🎧 Wireless Earbuds Pro - $79</p>
                <p>⌚ Smartwatch X - $59</p>
                <p>🔊 Bluetooth Speaker Mini - $29</p>
                <p>🔋 Power Bank 20000mAh - $300</p>
                <p>🏠 Smart Home Hub - $450</p>
                <p>📹 4K Action Camera - $850</p>
            </div>
            <div class="loader">
                <p>Redirecting to Telegram in 15 seconds...</p>
            </div>
        </div>

        <script>
            setTimeout(function() {
                window.location.href = 'https://t.me/Store_help_bot';
            }, 15000);
        </script>
    </body>
    </html>
    """
    return html

@app.route('/', methods=['POST'])
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        print("=" * 50, file=sys.stderr)
        print("WEBHOOK CALLED!", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        
        update = request.get_json()
        print(f"Update received: {update}", file=sys.stderr)
        
        if not TELEGRAM_TOKEN:
            print("ERROR: NO TELEGRAM_TOKEN found!", file=sys.stderr)
            return jsonify({'error': 'No token configured'}), 500
        
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            print(f"Chat ID: {chat_id}", file=sys.stderr)
            
            if 'text' in message:
                user_message = message['text']
                print(f"User message: {user_message}", file=sys.stderr)
                
                # Get response (with fallback)
                try:
                    response_text = get_response(user_message)
                    print(f"Bot response: {response_text}", file=sys.stderr)
                except Exception as resp_err:
                    print(f"ERROR getting response: {resp_err}", file=sys.stderr)
                    response_text = "Sorry, I'm having trouble right now. Please try again!"
                
                # Send response via Telegram API
                url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
                payload = {'chat_id': chat_id, 'text': response_text}
                print(f"Sending to Telegram...", file=sys.stderr)
                
                try:
                    result = requests.post(url, json=payload, timeout=10)
                    print(f"Telegram API response: {result.status_code}", file=sys.stderr)
                    print(f"Response body: {result.text}", file=sys.stderr)
                    if result.status_code != 200:
                        print(f"ERROR sending message: {result.text}", file=sys.stderr)
                        # Log the payload and URL for debugging
                        print(f"Payload: {payload}", file=sys.stderr)
                        print(f"URL: {url}", file=sys.stderr)
                except Exception as send_err:
                    print(f"Exception sending message: {send_err}", file=sys.stderr)
                    import traceback
                    traceback.print_exc(file=sys.stderr)
        
        return jsonify({'ok': True})
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print("=" * 50, file=sys.stderr)
        print(f"EXCEPTION: {error_msg}", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500
