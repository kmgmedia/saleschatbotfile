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
    from .telegram_handler import send_message, edit_message, TELEGRAM_TOKEN
    from .landing_page import get_landing_page
    from .inline_keyboard import handle_button_callback, product_buttons
    print("✅ Successfully imported modular components", file=sys.stderr)
except ImportError as e:
    print(f"⚠️ Import error: {e}, using inline functions", file=sys.stderr)
    # Fallback: import inline functions if modules don't work
    from openai_handler import get_response
    from telegram_handler import send_message, edit_message, TELEGRAM_TOKEN
    from landing_page import get_landing_page
    from inline_keyboard import handle_button_callback, product_buttons

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
    """Handle incoming Telegram updates (messages and callback queries)"""
    try:
        print("=" * 50, file=sys.stderr)
        print("WEBHOOK CALLED!", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        
        update = request.get_json()
        print(f"Update received: {update}", file=sys.stderr)
        
        if not TELEGRAM_TOKEN:
            print("ERROR: NO TELEGRAM_TOKEN found!", file=sys.stderr)
            return jsonify({'error': 'No token configured'}), 500
        
        # Handle callback queries (button clicks)
        if 'callback_query' in update:
            callback_query = update['callback_query']
            callback_data = callback_query['data']
            user_id = callback_query['from']['id']
            message_id = callback_query['message']['message_id']
            chat_id = callback_query['message']['chat']['id']
            
            print(f"Callback query: {callback_data} from user {user_id}", file=sys.stderr)
            
            # Handle the button click
            response = handle_button_callback(callback_data, user_id)
            
            # Edit the message with new text and buttons
            edit_result = edit_message(
                chat_id=chat_id,
                message_id=message_id,
                text=response['text'],
                reply_markup=response.get('reply_markup')
            )
            
            # Answer callback query to remove loading state
            answer_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery"
            requests.post(answer_url, json={'callback_query_id': callback_query['id']})
            
            print(f"✅ Button click handled successfully", file=sys.stderr)
            return jsonify({'ok': True})
        
        # Handle regular messages
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            print(f"Chat ID: {chat_id}, User ID: {user_id}", file=sys.stderr)
            
            if 'text' in message:
                user_message = message['text']
                print(f"User message: {user_message}", file=sys.stderr)
                
                # Handle /start command with product keyboard
                if user_message.startswith('/start'):
                    from .inline_keyboard import get_product_list_keyboard
                    welcome_text = """👋 Hey! I'm Alex, your personal tech consultant here at KMGMedia Design & Technologies.

With 7 years helping folks find their perfect gadgets, I'm here to make sure you get exactly what you need - not just what's on sale! 😊

I can help you find the perfect gadget! Choose a product below or just tell me what you're looking for:

• "Tell me about the smartwatch"
• "Show me wireless earbuds"  
• "I want a fitness tracker"

What brings you in today? Let's find something awesome for you! 🎯"""
                    
                    send_message(chat_id, welcome_text, reply_markup=get_product_list_keyboard())
                    return jsonify({'ok': True})
                
                # Get response from OpenAI handler (with automatic fallback)
                # Pass user_id for conversation memory
                try:
                    response_text = get_response(user_message, user_id)
                    print(f"Bot response: {response_text}", file=sys.stderr)
                    
                    # Check if response mentions a specific product - if so, add buttons
                    from .conversation_handler import detect_product
                    detected_product = detect_product(user_message)
                    
                    if detected_product:
                        # Send with product buttons
                        send_message(chat_id, response_text, reply_markup=product_buttons(detected_product))
                    else:
                        # Send without buttons
                        send_message(chat_id, response_text)
                        
                except Exception as resp_err:
                    print(f"ERROR getting response: {resp_err}", file=sys.stderr)
                    response_text = "Sorry, I'm having trouble right now. Please try again!"
                    send_message(chat_id, response_text)
                
                print(f"✅ Message sent successfully", file=sys.stderr)
        
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
