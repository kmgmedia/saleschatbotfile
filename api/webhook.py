"""
Vercel webhook endpoint for Telegram bot
This receives messages from Telegram and responds immediately
"""
import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Add parent directory to path to import chatbot
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set DRY_RUN for imports
os.environ['DRY_RUN'] = '1'

# Import chatbot
try:
    from importlib.machinery import SourceFileLoader
    chatbot_module = SourceFileLoader(
        'chatbot_main',
        os.path.join(os.path.dirname(__file__), '..', 'ecommerce-chatbot', 'main.py')
    ).load_module()
    chatbot_response = chatbot_module.chatbot_response
except Exception as e:
    print(f"Warning: Could not import chatbot: {e}")
    def chatbot_response(msg):
        return "Hello! I'm your shopping assistant. How can I help you today?"

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')

def send_message(chat_id, text):
    """Send message back to Telegram"""
    import urllib.request
    import urllib.parse
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        'chat_id': chat_id,
        'text': text
    }).encode()
    
    try:
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data.decode('utf-8'))
            
            # Extract message
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                
                if 'text' in message:
                    user_message = message['text']
                    
                    # Handle /start command
                    if user_message == '/start':
                        response = "👋 Welcome to ShopBot! I'm here to help you find amazing products. What are you looking for today?"
                    else:
                        # Get response from chatbot
                        response = chatbot_response(user_message)
                    
                    # Send response
                    send_message(chat_id, response)
            
            # Return success
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True}).encode())
            
        except Exception as e:
            print(f"Error processing webhook: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_GET(self):
        # Health check endpoint
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Telegram Bot Webhook is running!')
