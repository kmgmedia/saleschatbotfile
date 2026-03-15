"""
Google Gemini API integration for intelligent bot responses
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

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')

def get_response(message, user_id=None):
    """
    Get chatbot response using Google Gemini API with fallback.
    
    Args:
        message: User's message text
        user_id: User ID for conversation memory
    """
    
    # If Google API key is not available, fall back to keyword responses
    if not GOOGLE_API_KEY:
        print("WARNING: No Google API key - using fallback responses", file=sys.stderr)
        return get_fallback_response(message, user_id)
    
    try:
        # Get conversation history if user_id provided
        conversation_history = ""
        if user_id:
            try:
                from .database_memory import get_user_memory
                user_memory = get_user_memory(user_id)
                messages = user_memory.get_messages(limit=10)  # Last 10 messages
                # Format conversation history
                if messages:
                    conversation_history = "\n\n**Recent Conversation:**\n"
                    for msg in messages[-6:]:  # Last 6 messages (3 exchanges)
                        role = msg.get('role', 'user')
                        content = msg.get('content', '')
                        if role == 'user':
                            conversation_history += f"User: {content}\n"
                        else:
                            conversation_history += f"Alex: {content}\n"
            except Exception as e:
                print(f"Could not load conversation history: {e}", file=sys.stderr)

        # --- Prompt Injection Mitigation ---
        import re
        def sanitize_user_input(text):
            """Basic sanitization to prevent prompt injection"""
            # Remove dangerous prompt tokens and excessive whitespace
            text = re.sub(r'["\'`]', '', text)
            text = re.sub(r'[{}]', '', text)
            text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
            # Limit length
            return text[:500]

        def validate_user_input(text):
            """Validate user input for allowed characters and length"""
            # Only allow letters, numbers, basic punctuation
            if not re.match(r'^[\w\s.,!?@#\-:;()]+$', text):
                return "[Invalid input detected]"
            if len(text) > 500:
                return text[:500]
            return text

        def escape_user_input(text):
            """Escape special characters to prevent prompt injection"""
            # Replace newlines and tabs
            text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            # Escape percent and dollar signs
            text = text.replace('%', '%%').replace('$', '\$')
            return text

        # Apply all protections
        safe_message = sanitize_user_input(message)
        safe_message = validate_user_input(safe_message)
        safe_message = escape_user_input(safe_message)

        # Build the full prompt from loaded files
        full_prompt = f"""{SYSTEM_PROMPT}

{SALES_STYLE}

{PRODUCTS_LIST}{conversation_history}

User: {safe_message}

Alex:"""

        # Google Gemini API endpoint - using Gemini 2.5 Flash
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}'
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            'contents': [{
                'parts': [{
                    'text': full_prompt
                }]
            }],
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': 1024,  # Increased for Gemini 2.5 thinking tokens
                'topP': 0.8,
                'topK': 40
            }
        }
        
        response = requests.post(url, 
                                headers=headers, 
                                json=data,
                                timeout=25)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0].get('content', {})
                parts = content.get('parts', [])
                if parts and len(parts) > 0:
                    reply = parts[0].get('text', '').strip()
                    print(f"Google Gemini response successful", file=sys.stderr)
                    return reply
                else:
                    print(f"No parts in Gemini response", file=sys.stderr)
                    return get_fallback_response(message, user_id)
            else:
                print(f"No candidates in Gemini response", file=sys.stderr)
                return get_fallback_response(message, user_id)
        else:
            print(f"Google Gemini API error: {response.status_code} - {response.text}", file=sys.stderr)
            return get_fallback_response(message, user_id)
            
    except Exception as e:
        print(f"Google Gemini exception: {str(e)}", file=sys.stderr)
        return get_fallback_response(message, user_id)
