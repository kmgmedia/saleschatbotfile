"""
Stripe Payment Integration Handler
Manages payment processing, checkout sessions, and webhook handling
"""
import os
import stripe
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from .database import get_session
    from .models import User, Order, PaymentIntent
except ImportError:
    from database import get_session
    from models import User, Order, PaymentIntent

# Initialize Stripe with API key
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(user_id: int, line_items: list, success_url: str, cancel_url: str):
    """
    Create a Stripe checkout session for a user's cart
    
    Args:
        user_id: Telegram user ID
        line_items: List of Stripe line items (with price_data and quantity)
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect if payment cancelled
    
    Returns:
        dict with 'url', 'session_id', or 'error'
    """
    if not STRIPE_SECRET_KEY:
        print("ERROR: STRIPE_SECRET_KEY not configured", file=sys.stderr)
        return {'error': 'Payment processing not configured'}
    
    try:
        # Get user from database
        session = get_session()
        user = session.query(User).filter(User.user_id == user_id).first()
        session.close()
        
        if not user:
            print(f"User {user_id} not found", file=sys.stderr)
            return {'error': 'User not found'}
        
        # Calculate total amount
        total_amount = 0
        for item in line_items:
            price_cents = item['price_data']['unit_amount']
            quantity = item['quantity']
            total_amount += (price_cents / 100) * quantity
        
        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=f'user_{user_id}@saleschatbot.local',
            metadata={
                'user_id': user_id,
                'telegram_username': user.username or 'anonymous'
            }
        )
        
        # Save payment intent to database
        db_session = get_session()
        try:
            import json
            payment = PaymentIntent(
                user_id=user_id,
                stripe_session_id=checkout_session.id,
                stripe_payment_intent_id=checkout_session.payment_intent,
                total_amount=total_amount,
                status='pending',
                cart_items=json.dumps([{'name': item['price_data']['product_data']['name'], 'quantity': item['quantity']} for item in line_items])
            )
            db_session.add(payment)
            db_session.commit()
            print(f"✅ Checkout session created: {checkout_session.id} for user {user_id}", file=sys.stderr)
            
            return {
                'url': checkout_session.url,
                'session_id': checkout_session.id,
                'error': None
            }
        except Exception as e:
            print(f"Error saving payment to DB: {e}", file=sys.stderr)
            return {
                'url': checkout_session.url,
                'session_id': checkout_session.id,
                'error': str(e)
            }
        finally:
            db_session.close()
        
    except stripe.error.StripeError as e:
        print(f"❌ Stripe error creating checkout: {e}", file=sys.stderr)
        return {'error': str(e)}
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return {'error': str(e)}


def retrieve_session(session_id: str):
    """
    Retrieve a checkout session from Stripe
    
    Args:
        session_id: Stripe session ID
    
    Returns:
        Session object or None if error
    """
    if not STRIPE_SECRET_KEY:
        return None
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session
    except stripe.error.StripeError as e:
        print(f"Error retrieving session: {e}", file=sys.stderr)
        return None


def handle_payment_success(session_id: str):
    """
    Handle successful payment - update database
    
    Args:
        session_id: Stripe session ID
    
    Returns:
        dict with payment details or None if error
    """
    try:
        db_session = get_session()
        
        # Get the payment record
        payment = db_session.query(PaymentIntent)\
            .filter(PaymentIntent.stripe_session_id == session_id)\
            .first()
        
        if payment:
            payment.status = 'completed'
            payment.completed_at = datetime.utcnow()
            
            # Create order record
            order = Order(
                user_id=payment.user_id,
                payment_intent_id=payment.payment_intent_id,
                total_amount=payment.total_amount,
                status='confirmed',
                items=payment.cart_items
            )
            db_session.add(order)
            
            # Update user stats
            user = db_session.query(User).filter(User.user_id == payment.user_id).first()
            if user:
                user.total_purchases = (user.total_purchases or 0) + 1
                user.total_spent = (user.total_spent or 0) + payment.total_amount
            
            db_session.commit()
            print(f"✅ Payment {session_id} marked as completed", file=sys.stderr)
            
            return {
                'success': True,
                'order_id': order.order_id,
                'user_id': payment.user_id,
                'amount': payment.total_amount,
                'bot_username': 'SalesBot'  # Update with your bot username
            }
        else:
            print(f"Payment record not found for session {session_id}", file=sys.stderr)
            return None
    
    except Exception as e:
        print(f"Error handling payment success: {e}", file=sys.stderr)
        return None
    finally:
        db_session.close()


def get_payment_status(session_id: str):
    """
    Get payment status from database
    
    Args:
        session_id: Stripe session ID
    
    Returns:
        Payment status dict or None
    """
    try:
        session = get_session()
        payment = session.query(PaymentIntent)\
            .filter(PaymentIntent.stripe_session_id == session_id)\
            .first()
        
        if payment:
            status_dict = {
                'status': payment.status,
                'amount': payment.total_amount,
                'created_at': payment.created_at.isoformat(),
                'completed_at': payment.completed_at.isoformat() if payment.completed_at else None
            }
            return status_dict
        
        return None
    except Exception as e:
        print(f"Error getting payment status: {e}", file=sys.stderr)
        return None
    finally:
        session.close()


def get_user_orders(user_id: int, limit: int = 10):
    """
    Get user's order history
    
    Args:
        user_id: Telegram user ID
        limit: Number of orders to retrieve
    
    Returns:
        List of orders
    """
    try:
        session = get_session()
        orders = session.query(Order)\
            .filter(Order.user_id == user_id)\
            .order_by(Order.created_at.desc())\
            .limit(limit)\
            .all()
        
        return [
            {
                'order_id': o.order_id,
                'amount': float(o.total_amount),
                'status': o.status,
                'created_at': o.created_at.isoformat(),
                'items': o.items
            }
            for o in orders
        ]
    except Exception as e:
        print(f"Error retrieving orders: {e}", file=sys.stderr)
        return []
    finally:
        session.close()
