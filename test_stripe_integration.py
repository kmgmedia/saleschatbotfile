"""
Test Stripe Payment Integration
Tests checkout flow, cart management, and payment processing
"""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# Test 1: Import modules
print("=" * 50)
print("TEST 1: Import Stripe modules")
print("=" * 50)

try:
    from api.stripe_handler import create_checkout_session, handle_payment_success
    from api.cart_manager import add_to_cart, get_cart, get_cart_total, clear_cart, get_cart_summary
    from api.database import get_session, init_db
    from api.models import User, Order, PaymentIntent, CartItem
    print("✅ All modules imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Initialize database
print("\n" + "=" * 50)
print("TEST 2: Initialize database")
print("=" * 50)

try:
    init_db()
    print("✅ Database initialized")
except Exception as e:
    print(f"⚠️ Database warning (may already exist): {e}")

# Test 3: Create test user
print("\n" + "=" * 50)
print("TEST 3: Create test user")
print("=" * 50)

try:
    from api.database import get_or_create_user, get_session
    test_user_id = 123456789
    user = get_or_create_user(test_user_id, 'test_user')
    
    # Verify user exists by querying fresh
    session = get_session()
    user = session.query(User).filter(User.user_id == test_user_id).first()
    session.close()
    
    print(f"✅ Test user created: {user.user_id} (@{user.username})")
except Exception as e:
    print(f"❌ Failed to create user: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Cart management
print("\n" + "=" * 50)
print("TEST 4: Cart Management")
print("=" * 50)

try:
    # Add items to cart
    print("Adding items to cart...")
    add_to_cart(test_user_id, 'Smartwatch X', quantity=1)
    add_to_cart(test_user_id, 'Wireless Earbuds Pro', quantity=2)
    
    # Get cart
    cart = get_cart(test_user_id)
    print(f"✅ Cart items: {len(cart)}")
    for item in cart:
        print(f"   - {item.product_name}: {item.quantity}x ${item.unit_price:.2f}")
    
    # Get total
    total = get_cart_total(test_user_id)
    print(f"✅ Cart total: ${total:.2f}")
    
    # Get summary
    summary = get_cart_summary(test_user_id)
    print(f"✅ Cart summary:\n{summary}")
    
except Exception as e:
    print(f"❌ Cart management failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Stripe configuration check
print("\n" + "=" * 50)
print("TEST 5: Stripe Configuration")
print("=" * 50)

stripe_secret = os.getenv('STRIPE_SECRET_KEY', '')
stripe_public = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
stripe_webhook = os.getenv('STRIPE_WEBHOOK_SECRET', '')

if stripe_secret and stripe_secret.startswith('sk_'):
    print(f"✅ STRIPE_SECRET_KEY configured: {stripe_secret[:20]}...")
else:
    print("⚠️ STRIPE_SECRET_KEY not properly configured (needed for production)")

if stripe_public and stripe_public.startswith('pk_'):
    print(f"✅ STRIPE_PUBLISHABLE_KEY configured: {stripe_public[:20]}...")
else:
    print("⚠️ STRIPE_PUBLISHABLE_KEY not properly configured (needed for production)")

if stripe_webhook and stripe_webhook.startswith('whsec_'):
    print(f"✅ STRIPE_WEBHOOK_SECRET configured: {stripe_webhook[:20]}...")
else:
    print("⚠️ STRIPE_WEBHOOK_SECRET not configured (needed for webhook handling)")

# Test 6: Checkout session creation (mock)
print("\n" + "=" * 50)
print("TEST 6: Checkout Session Creation")
print("=" * 50)

if stripe_secret:
    try:
        import stripe
        stripe.api_key = stripe_secret
        
        # Create test line items
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Smartwatch X'},
                    'unit_amount': 29900  # $299.00
                },
                'quantity': 1
            },
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Wireless Earbuds Pro'},
                    'unit_amount': 9900  # $99.00
                },
                'quantity': 2
            }
        ]
        
        result = create_checkout_session(
            user_id=test_user_id,
            line_items=line_items,
            success_url='http://localhost:5000/api/payment-success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5000/api/payment-cancel'
        )
        
        if result and result.get('url'):
            print(f"✅ Checkout session created!")
            print(f"   Session ID: {result.get('session_id')}")
            print(f"   Checkout URL: {result.get('url')}")
        else:
            print(f"⚠️ Could not create checkout session: {result}")
    
    except Exception as e:
        print(f"⚠️ Checkout session creation failed: {e}")
        print("   (This may be expected in test mode)")
else:
    print("⚠️ Skipping checkout test - STRIPE_SECRET_KEY not configured")

# Test 7: Database models
print("\n" + "=" * 50)
print("TEST 7: Database Models Check")
print("=" * 50)

try:
    session = get_session()
    
    # Check tables exist
    from sqlalchemy import inspect
    inspector = inspect(session.get_bind())
    tables = inspector.get_table_names()
    
    required_tables = ['users', 'payment_intents', 'orders', 'cart_items']
    for table in required_tables:
        if table in tables:
            print(f"✅ Table '{table}' exists")
        else:
            print(f"❌ Table '{table}' missing")
    
    session.close()
except Exception as e:
    print(f"❌ Model check failed: {e}")

# Test 8: Cleanup
print("\n" + "=" * 50)
print("TEST 8: Cleanup")
print("=" * 50)

try:
    clear_cart(test_user_id)
    print("✅ Cart cleared")
except Exception as e:
    print(f"⚠️ Cleanup warning: {e}")

print("\n" + "=" * 50)
print("STRIPE INTEGRATION TESTS COMPLETE")
print("=" * 50)
print("\n📝 Next steps:")
print("1. Configure STRIPE_SECRET_KEY in .env")
print("2. Configure STRIPE_PUBLISHABLE_KEY in .env")
print("3. Run: python run.py")
print("4. Test cart flow via Telegram bot")
print("5. Deploy webhook handler for Stripe callbacks")
