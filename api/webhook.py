"""
Vercel webhook endpoint for Telegram bot
"""
import os
import requests
from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')

# Log for debugging
print(f"Token loaded: {'Yes' if TELEGRAM_TOKEN else 'No'}", file=sys.stderr)
print(f"Token prefix: {TELEGRAM_TOKEN[:10]}..." if TELEGRAM_TOKEN else "No token", file=sys.stderr)

# Simple keyword-based responses
def get_response(message):
    """Get chatbot response based on keywords"""
    msg = message.lower()
    
    if any(word in msg for word in ['hi', 'hello', 'hey', 'start']):
        return "👋 Hello! I'm ShopBot, your shopping assistant. We have amazing products: Wireless Earbuds Pro ($79), Smartwatch X ($59), and Bluetooth Speaker Mini ($29). What interests you?"
    
    if any(word in msg for word in ['product', 'sell', 'have', 'what', 'show']):
        return "🛍️ Here are our amazing products:\n\n🎧 Wireless Earbuds Pro - $79\nNoise cancelling, waterproof, perfect for workouts!\n\n⌚ Smartwatch X - $59\nTracks fitness, sleep & heart rate\n\n🔊 Bluetooth Speaker Mini - $29\nAmazing sound, 12-hour battery\n\nWhich one interests you?"
    
    if 'earbud' in msg or 'headphone' in msg:
        return "🎧 Great choice! Our Wireless Earbuds Pro are $79. They're noise cancelling, waterproof, and perfect for workouts! Would you like to know more?"
    
    if 'watch' in msg or 'smartwatch' in msg:
        return "⌚ The Smartwatch X is $59! It tracks your fitness, sleep, and heart rate. It's a fantastic deal! Interested?"
    
    if 'speaker' in msg:
        return "🔊 Our Bluetooth Speaker Mini is just $29! Amazing sound quality with 12-hour battery life. Perfect for any occasion! Want one?"
    
    if 'price' in msg or 'cost' in msg or 'how much' in msg:
        return "💰 Our prices:\n🎧 Earbuds Pro: $79\n⌚ Smartwatch X: $59\n🔊 Speaker Mini: $29\n\nGreat deals on quality products! Which one would you like?"
    
    if any(word in msg for word in ['buy', 'order', 'purchase', 'want']):
        return "🎉 Awesome! I'd love to help you with that! Please contact our team to complete your order. Which product are you interested in?"
    
    if 'thank' in msg or 'thanks' in msg:
        return "😊 You're welcome! Happy to help! Let me know if you need anything else!"
    
    return "I'm here to help you find the perfect product! We have Wireless Earbuds ($79), Smartwatch ($59), and Bluetooth Speaker ($29). What would you like to know more about?"

@app.route('/', methods=['GET'])
def health():
    return 'Telegram Bot Webhook is running!'

@app.route('/', methods=['POST'])
def webhook():
    try:
        print("Received POST request", file=sys.stderr)
        update = request.get_json()
        print(f"Update: {update}", file=sys.stderr)
        
        if not TELEGRAM_TOKEN:
            print("ERROR: No TELEGRAM_TOKEN found!", file=sys.stderr)
            return jsonify({'error': 'No token configured'}), 500
        
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            print(f"Chat ID: {chat_id}", file=sys.stderr)
            
            if 'text' in message:
                user_message = message['text']
                print(f"User message: {user_message}", file=sys.stderr)
                response_text = get_response(user_message)
                print(f"Bot response: {response_text}", file=sys.stderr)
                
                # Send response via Telegram API
                url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
                payload = {'chat_id': chat_id, 'text': response_text}
                print(f"Sending to Telegram...", file=sys.stderr)
                
                result = requests.post(url, json=payload)
                print(f"Telegram API response: {result.status_code}", file=sys.stderr)
                print(f"Response body: {result.text}", file=sys.stderr)
        
        return jsonify({'ok': True})
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg, file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500
