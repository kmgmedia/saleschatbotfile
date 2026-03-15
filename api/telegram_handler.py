"""
Telegram Bot API interaction handlers
"""
import os
import requests
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')

def send_message(chat_id, text, reply_markup=None):
    """
    Send a message to a Telegram chat.
    
    Args:
        chat_id: The chat ID to send to
        text: Message text
        reply_markup: Optional inline keyboard markup (dict)
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    if reply_markup:
        payload['reply_markup'] = reply_markup
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}", file=sys.stderr)
        return None


def send_photo(chat_id, photo_url, caption=None, reply_markup=None):
    """
    Send a photo to a Telegram chat.
    
    Args:
        chat_id: The chat ID to send to
        photo_url: URL or file_id of the photo
        caption: Optional caption text
        reply_markup: Optional inline keyboard markup (dict)
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        'chat_id': chat_id,
        'photo': photo_url,
        'parse_mode': 'Markdown'
    }
    
    if caption:
        payload['caption'] = caption
    
    if reply_markup:
        payload['reply_markup'] = reply_markup
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending photo: {e}", file=sys.stderr)
        return None


def send_media_group(chat_id, media_list, caption=None):
    """
    Send multiple photos as a media group (album).
    
    Args:
        chat_id: The chat ID to send to
        media_list: List of photo URLs
        caption: Optional caption for the first photo
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMediaGroup"
    
    # Format media array
    media = []
    for i, photo_url in enumerate(media_list):
        media_item = {
            'type': 'photo',
            'media': photo_url
        }
        # Add caption only to first photo
        if i == 0 and caption:
            media_item['caption'] = caption
            media_item['parse_mode'] = 'Markdown'
        media.append(media_item)
    
    payload = {
        'chat_id': chat_id,
        'media': media
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        return response.json()
    except Exception as e:
        print(f"Error sending media group: {e}", file=sys.stderr)
        return None



def edit_message(chat_id, message_id, text, reply_markup=None):
    """
    Edit an existing message (used for button callbacks).
    
    Args:
        chat_id: The chat ID
        message_id: The message ID to edit
        text: New message text
        reply_markup: Optional inline keyboard markup (dict)
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText"
    payload = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    if reply_markup:
        payload['reply_markup'] = reply_markup
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error editing message: {e}", file=sys.stderr)
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
