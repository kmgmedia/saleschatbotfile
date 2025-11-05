"""
Telegram Bot API interaction handlers
"""
import os
import requests
import sys

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')

def send_message(chat_id, text):
    """Send a message to a Telegram chat"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}", file=sys.stderr)
        return None

def process_update(update, get_bot_response):
    """Process a Telegram update and return response"""
    try:
        # Extract message from update
        if 'message' not in update:
            print(f"No message in update: {update}", file=sys.stderr)
            return {'status': 'ignored', 'reason': 'no_message'}
        
        message = update['message']
        chat_id = message['chat']['id']
        
        # Handle text messages
        if 'text' in message:
            user_message = message['text']
            print(f"Received message from {chat_id}: {user_message}", file=sys.stderr)
            
            # Get bot response
            bot_reply = get_bot_response(user_message)
            
            # Send response
            result = send_message(chat_id, bot_reply)
            print(f"Sent response to {chat_id}", file=sys.stderr)
            
            return {
                'status': 'success',
                'chat_id': chat_id,
                'message': user_message,
                'response': bot_reply
            }
        else:
            print(f"Non-text message received: {message}", file=sys.stderr)
            return {'status': 'ignored', 'reason': 'non_text_message'}
            
    except Exception as e:
        print(f"Error processing update: {str(e)}", file=sys.stderr)
        return {'status': 'error', 'error': str(e)}
