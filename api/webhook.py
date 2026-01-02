"""
Vercel webhook endpoint for Telegram bot with Google Gemini AI
Clean and modular architecture - main entry point
With database persistence and analytics tracking
"""
import os
import sys
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Import our modular components
try:
    # Try relative imports first (when run as module)
    from .gemini_handler import get_response
    from .telegram_handler import send_message, send_photo, send_media_group, edit_message, TELEGRAM_TOKEN
    from .landing_page import get_landing_page
    from .inline_keyboard import handle_button_callback, product_buttons
    from .database import init_db, get_or_create_user
    from .database_memory import get_user_memory, get_user_context_manager
    from .analytics import (
        log_user_message, log_button_click, log_product_view, log_purchase, log_error
    )
    from .admin_routes import admin_bp
    print("✅ Successfully imported modular components (relative)", file=sys.stderr)
except (ImportError, ValueError) as e:
    print(f"⚠️ Relative import failed: {e}, trying direct import", file=sys.stderr)
    try:
        # Fallback: import directly when run as script
        from gemini_handler import get_response
        from telegram_handler import send_message, send_photo, send_media_group, edit_message, TELEGRAM_TOKEN
        from landing_page import get_landing_page
        from inline_keyboard import handle_button_callback, product_buttons
        from database import init_db, get_or_create_user
        from database_memory import get_user_memory, get_user_context_manager
        from analytics import (
            log_user_message, log_button_click, log_product_view, log_purchase, log_error
        )
        from admin_routes import admin_bp
        print("✅ Successfully imported modular components (direct)", file=sys.stderr)
    except ImportError as e2:
        print(f"❌ Both import methods failed: {e2}", file=sys.stderr)
        raise

# Create Flask app with static folder configuration
app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')), static_url_path='/static')

# Register admin routes for analytics dashboard
app.register_blueprint(admin_bp)

# Serve static files (dashboard) - also serve via direct route
@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files (dashboard HTML, etc)"""
    from flask import send_from_directory
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    return send_from_directory(static_dir, filename)

# Initialize database
try:
    init_db()
    print("✅ Database initialized", file=sys.stderr)
except Exception as e:
    print(f"⚠️ Database init warning: {e}", file=sys.stderr)


# Log for debugging
print(f"Webhook initialized - Modular architecture with Database & Analytics", file=sys.stderr)
print(f"Telegram Token loaded: {'Yes' if TELEGRAM_TOKEN else 'No'}", file=sys.stderr)

@app.route('/health', methods=['GET'])
def ping():
    """Simple health check"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@app.route('/', methods=['GET'])
def home():
    """Serve landing page"""
    return get_landing_page()

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Serve analytics dashboard"""
    import os
    from flask import send_file
    
    # Get the absolute path to dashboard.html
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'dashboard.html'))
    
    print(f"Dashboard path: {dashboard_path}", file=sys.stderr)
    print(f"File exists: {os.path.exists(dashboard_path)}", file=sys.stderr)
    
    if not os.path.exists(dashboard_path):
        return jsonify({'error': f'Dashboard not found at {dashboard_path}'}), 404
    
    try:
        return send_file(dashboard_path, mimetype='text/html')
    except Exception as e:
        print(f"Error serving dashboard: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['POST'])
@app.route('/webhook', methods=['POST'])
@app.route('/api/webhook', methods=['POST'])  # Handle Vercel path when route is /api/webhook
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
            
            # Ensure user exists in database
            user = get_or_create_user(user_id)
            
            # Log button click analytics
            button_type = callback_data.split('_')[0] if '_' in callback_data else 'unknown'
            log_button_click(user_id, button_type, button_data={'callback_data': callback_data})
            
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
            username = message['from'].get('username')
            first_name = message['from'].get('first_name')
            
            print(f"Chat ID: {chat_id}, User ID: {user_id}", file=sys.stderr)
            
            # Ensure user exists in database and load memory
            user = get_or_create_user(user_id, username, first_name)
            user_memory = get_user_memory(user_id)
            context_mgr = get_user_context_manager(user_id)
            
            if 'text' in message:
                user_message = message['text']
                print(f"User message: {user_message}", file=sys.stderr)
                
                # Log user message
                log_user_message(user_id, emotion=None)
                
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
                    
                    # Add to user memory
                    user_memory.add_user_message(user_message)
                    user_memory.add_ai_message(welcome_text)
                    
                    send_message(chat_id, welcome_text, reply_markup=get_product_list_keyboard())
                    return jsonify({'ok': True})
                
                # Get response from Google Gemini handler (with automatic fallback)
                # Pass user_id for conversation memory
                try:
                    response_text = get_response(user_message, user_id)
                    print(f"Bot response: {response_text}", file=sys.stderr)
                    
                    # Add to persistent memory
                    user_memory.add_user_message(user_message)
                    user_memory.add_ai_message(response_text)
                    
                    # Check if response mentions a specific product - if so, add buttons
                    from .conversation_handler import detect_product
                    from .user_memory import get_last_product
                    from .product_data import get_product_images, get_product_spec, get_product_price
                    
                    detected_product = detect_product(user_message)
                    
                    if detected_product:
                        # Log product view
                        log_product_view(user_id, detected_product)
                        context_mgr.set_context(product=detected_product, intent='view')
                        
                        # Check if product has images
                        product_images = get_product_images(detected_product)
                        
                        if product_images:
                            # Send product images with details
                            product_price = get_product_price(detected_product)
                            product_spec = get_product_spec(detected_product)
                            
                            # Create detailed caption for the media group
                            caption = f"*{detected_product}*\n\n"
                            caption += f"💰 *Price:* ${product_price}\n\n"
                            caption += f"📋 *Details:* {product_spec}\n\n"
                            caption += f"{response_text}"
                            
                            # Send all images as a carousel (media group) with caption on first image
                            send_media_group(chat_id, product_images, caption=caption)
                            
                            # Send buttons in a separate message immediately after
                            button_text = "👇 Choose an option below:"
                            send_message(chat_id, button_text, reply_markup=product_buttons(detected_product))
                        else:
                            # No images, send text with product buttons
                            send_message(chat_id, response_text, reply_markup=product_buttons(detected_product))
                    else:
                        # Check if user has a product in memory (e.g., from cheapest request)
                        last_product = get_last_product(user_id)
                        if last_product and any(word in user_message.lower() for word in ['cheap', 'cheapest', 'affordable', 'budget']):
                            # User asked for cheapest - check if product has images
                            product_images = get_product_images(last_product)
                            
                            if product_images:
                                # Send product images with details
                                product_price = get_product_price(last_product)
                                product_spec = get_product_spec(last_product)
                                
                                # Create detailed caption for the media group
                                caption = f"*{last_product}*\n\n"
                                caption += f"💰 *Price:* ${product_price}\n\n"
                                caption += f"📋 *Details:* {product_spec}\n\n"
                                caption += f"{response_text}"
                                
                                # Send all images as a carousel (media group) with caption on first image
                                send_media_group(chat_id, product_images, caption=caption)
                                
                                # Send buttons in a separate message immediately after
                                button_text = "👇 Choose an option below:"
                                send_message(chat_id, button_text, reply_markup=product_buttons(last_product))
                            else:
                                # No images, send with buttons for the cheapest product
                                send_message(chat_id, response_text, reply_markup=product_buttons(last_product))
                        else:
                            # Send without buttons
                            send_message(chat_id, response_text)
                    
                    # Save conversation to database
                    context_mgr.save_interaction(user_message, response_text)
                        
                except Exception as resp_err:
                    print(f"ERROR getting response: {resp_err}", file=sys.stderr)
                    log_error(user_id, 'response_error', str(resp_err))
                    response_text = "Sorry, I'm having trouble right now. Please try again!"
                    send_message(chat_id, response_text)
                
                print(f"✅ Message sent successfully", file=sys.stderr)
        
        return jsonify({'ok': True})
        
        return jsonify({'ok': True})
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print("=" * 50, file=sys.stderr)
        print(f"EXCEPTION: {error_msg}", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500
@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Initiate Stripe checkout for user's cart"""
    try:
        from .stripe_handler import create_checkout_session
        from .cart_manager import get_cart, get_cart_total, clear_cart
        
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get user's cart
        cart_items = get_cart(user_id)
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Convert cart to format for Stripe
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item.product_name},
                    'unit_amount': int(item.unit_price * 100)
                },
                'quantity': item.quantity
            }
            for item in cart_items
        ]
        
        # Get domain (adjust based on deployment)
        domain = request.host_url.rstrip('/')
        success_url = f"{domain}/api/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{domain}/api/payment-cancel"
        
        # Create Stripe session
        session_data = create_checkout_session(
            user_id=user_id,
            line_items=line_items,
            success_url=success_url,
            cancel_url=cancel_url
        )
        
        if session_data.get('error'):
            return jsonify({'error': session_data['error']}), 400
        
        return jsonify({
            'checkout_url': session_data.get('url'),
            'session_id': session_data.get('session_id')
        }), 200
    
    except Exception as e:
        print(f"Checkout error: {e}", file=sys.stderr)
        log_error(user_id, 'checkout_error', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/payment-success', methods=['GET'])
def payment_success():
    """Handle successful Stripe payment"""
    try:
        from .stripe_handler import handle_payment_success
        
        session_id = request.args.get('session_id')
        if not session_id:
            return jsonify({'error': 'Session ID required'}), 400
        
        result = handle_payment_success(session_id)
        if not result:
            return jsonify({'error': 'Payment processing failed'}), 400
        
        # Return success HTML page
        return f"""
        <html>
            <head>
                <title>Payment Successful</title>
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                    .success {{ color: green; font-size: 24px; }}
                </style>
            </head>
            <body>
                <div class="success">✅ Payment Successful!</div>
                <p>Thank you for your purchase. You will receive an email confirmation shortly.</p>
                <p><a href="https://t.me/{result.get('bot_username', 'your_bot')}">Return to Bot</a></p>
            </body>
        </html>
        """, 200
    
    except Exception as e:
        print(f"Payment success handler error: {e}", file=sys.stderr)
        return f"<html><body>Error processing payment: {e}</body></html>", 500


@app.route('/api/payment-cancel', methods=['GET'])
def payment_cancel():
    """Handle cancelled Stripe payment"""
    return """
    <html>
        <head>
            <title>Payment Cancelled</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .cancel { color: red; font-size: 24px; }
            </style>
        </head>
        <body>
            <div class="cancel">❌ Payment Cancelled</div>
            <p>Your payment was not completed. Your cart items are still saved.</p>
            <p><a href="https://t.me/your_bot">Return to Bot</a></p>
        </body>
    </html>
    """, 200


@app.route('/api/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    try:
        import stripe
        from .stripe_handler import handle_payment_success
        
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get('Stripe-Signature')
        
        # Verify webhook signature
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
            )
        except ValueError:
            return jsonify({'error': 'Invalid payload'}), 400
        except stripe.error.SignatureVerificationError:
            return jsonify({'error': 'Invalid signature'}), 400
        
        # Handle payment.succeeded event
        if event['type'] == 'checkout.session.completed':
            session_id = event['data']['object']['id']
            result = handle_payment_success(session_id)
            if result:
                print(f"Payment completed for session: {session_id}", file=sys.stderr)
        
        return jsonify({'success': True}), 200
    
    except Exception as e:
        print(f"Stripe webhook error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

# For local testing
if __name__ == '__main__':
    app.run(debug=True, port=5000)
