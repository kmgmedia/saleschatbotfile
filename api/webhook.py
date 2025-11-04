"""
Vercel webhook endpoint for Telegram bot
"""
import os
import json
import urllib.request
import urllib.parse

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')

# Simple keyword-based responses (DRY_RUN mode)
def get_response(message):
    """Get chatbot response based on keywords"""
    msg = message.lower()
    
    # Greetings
    if any(word in msg for word in ['hi', 'hello', 'hey', 'start']):
        return "👋 Hello! I'm ShopBot, your shopping assistant. We have amazing products: Wireless Earbuds Pro ($79), Smartwatch X ($59), and Bluetooth Speaker Mini ($29). What interests you?"
    
    # Product queries
    if any(word in msg for word in ['product', 'sell', 'have', 'what', 'show']):
        return "🛍️ Here are our amazing products:\n\n🎧 Wireless Earbuds Pro - $79\nNoise cancelling, waterproof, perfect for workouts!\n\n⌚ Smartwatch X - $59\nTracks fitness, sleep & heart rate\n\n🔊 Bluetooth Speaker Mini - $29\nAmazing sound, 12-hour battery\n\nWhich one interests you?"
    
    # Earbuds
    if 'earbud' in msg or 'headphone' in msg:
        return "🎧 Great choice! Our Wireless Earbuds Pro are $79. They're noise cancelling, waterproof, and perfect for workouts! Would you like to know more?"
    
    # Watch
    if 'watch' in msg or 'smartwatch' in msg:
        return "⌚ The Smartwatch X is $59! It tracks your fitness, sleep, and heart rate. It's a fantastic deal! Interested?"
    
    # Speaker
    if 'speaker' in msg:
        return "🔊 Our Bluetooth Speaker Mini is just $29! Amazing sound quality with 12-hour battery life. Perfect for any occasion! Want one?"
    
    # Price queries
    if 'price' in msg or 'cost' in msg or 'how much' in msg:
        return "💰 Our prices:\n🎧 Earbuds Pro: $79\n⌚ Smartwatch X: $59\n🔊 Speaker Mini: $29\n\nGreat deals on quality products! Which one would you like?"
    
    # Buy/order
    if any(word in msg for word in ['buy', 'order', 'purchase', 'want']):
        return "🎉 Awesome! I'd love to help you with that! Please contact our team to complete your order. Which product are you interested in?"
    
    # Thanks
    if 'thank' in msg or 'thanks' in msg:
        return "😊 You're welcome! Happy to help! Let me know if you need anything else!"
    
    # Default
    return "I'm here to help you find the perfect product! We have Wireless Earbuds ($79), Smartwatch ($59), and Bluetooth Speaker ($29). What would you like to know more about?"

def send_message(chat_id, text):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        'chat_id': chat_id,
        'text': text
    }).encode()
    
    try:
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def handler(event, context):
    """Main handler for Vercel serverless function"""
    try:
        # Handle GET request (health check)
        if event.get('httpMethod') == 'GET' or event.get('requestContext', {}).get('http', {}).get('method') == 'GET':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/plain'},
                'body': 'Telegram Bot Webhook is running!'
            }
        
        # Handle POST request (webhook)
        body = event.get('body', '{}')
        if isinstance(body, str):
            update = json.loads(body)
        else:
            update = body
        
        # Extract message
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            
            if 'text' in message:
                user_message = message['text']
                
                # Get response
                response = get_response(user_message)
                
                # Send response
                send_message(chat_id, response)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'ok': True})
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
