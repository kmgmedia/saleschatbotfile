"""
Vercel webhook endpoint for Telegram bot with OpenAI
Clean and modular architecture - main entry point
"""
import os
import sys
import requests
from flask import Flask, request, jsonify

# Import our modular components
try:
    from .openai_handler import get_response
    from .telegram_handler import send_message, TELEGRAM_TOKEN
    from .landing_page import get_landing_page
    print("✅ Successfully imported modular components", file=sys.stderr)
except ImportError as e:
    print(f"⚠️ Import error: {e}, using inline functions", file=sys.stderr)
    # Fallback: import inline functions if modules don't work
    from openai_handler import get_response
    from telegram_handler import send_message, TELEGRAM_TOKEN
    from landing_page import get_landing_page

app = Flask(__name__)

# Log for debugging
print(f"Webhook initialized - Modular architecture", file=sys.stderr)
print(f"Telegram Token loaded: {'Yes' if TELEGRAM_TOKEN else 'No'}", file=sys.stderr)

@app.route('/', methods=['GET'])
def health():
    """Serve landing page"""
    return get_landing_page()

@app.route('/', methods=['POST'])
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram updates"""
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
                
                # Get response from OpenAI handler (with automatic fallback)
                try:
                    response_text = get_response(user_message)
                    print(f"Bot response: {response_text}", file=sys.stderr)
                except Exception as resp_err:
                    print(f"ERROR getting response: {resp_err}", file=sys.stderr)
                    response_text = "Sorry, I'm having trouble right now. Please try again!"
                
                # Send response using telegram_handler
                result = send_message(chat_id, response_text)
                
                if result:
                    print(f"✅ Message sent successfully", file=sys.stderr)
                else:
                    print(f"❌ Failed to send message", file=sys.stderr)
        
        return jsonify({'ok': True})
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print("=" * 50, file=sys.stderr)
        print(f"EXCEPTION: {error_msg}", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500

# For local testing
if __name__ == '__main__':
    app.run(debug=True, port=5000)
