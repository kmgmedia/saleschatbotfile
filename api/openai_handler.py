"""
OpenAI API integration for intelligent bot responses
"""
import os
import requests
import sys

# Try relative import first, fall back to direct import
try:
    from .responses import get_fallback_response
    from .prompt_loader import SYSTEM_PROMPT, PRODUCTS_LIST, SALES_STYLE
except ImportError:
    from responses import get_fallback_response
    from prompt_loader import SYSTEM_PROMPT, PRODUCTS_LIST, SALES_STYLE

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

def get_response(message, user_id=None):
    """
    Get chatbot response using OpenAI API with fallback.
    
    Args:
        message: User's message text
        user_id: User ID for conversation memory
    """
    
    # If OpenAI key is not available, fall back to keyword responses
    if not OPENAI_API_KEY:
        print("WARNING: No OpenAI key - using fallback responses", file=sys.stderr)
        return get_fallback_response(message, user_id)
    
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
            return get_fallback_response(message, user_id)
            
    except Exception as e:
        print(f"OpenAI exception: {str(e)}", file=sys.stderr)
        return get_fallback_response(message, user_id)
