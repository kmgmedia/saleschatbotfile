"""Shopping cart management for users"""
from api.database import get_session
from api.models import CartItem, User
from api.product_data.utils import get_product_price
import logging

logger = logging.getLogger(__name__)


def add_to_cart(user_id, product_name, quantity=1):
    """Add item to user's shopping cart"""
    try:
        session = get_session()
        
        # Check if item already in cart
        existing = session.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_name == product_name
        ).first()
        
        price = get_product_price(product_name)
        if price is None:
            logger.warning(f"Product {product_name} not found for cart")
            return False
        
        if existing:
            existing.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_name=product_name,
                quantity=quantity,
                unit_price=price
            )
            session.add(cart_item)
        
        session.commit()
        logger.info(f"Added {quantity}x {product_name} to cart for user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        return False


def get_cart(user_id):
    """Retrieve user's shopping cart"""
    try:
        session = get_session()
        items = session.query(CartItem).filter(CartItem.user_id == user_id).all()
        return items if items else []
    except Exception as e:
        logger.error(f"Error retrieving cart: {e}")
        return []


def get_cart_total(user_id):
    """Calculate total cart value"""
    try:
        items = get_cart(user_id)
        total = sum(item.quantity * item.unit_price for item in items)
        return total
    except Exception as e:
        logger.error(f"Error calculating cart total: {e}")
        return 0


def get_cart_summary(user_id):
    """Get formatted cart summary for display"""
    items = get_cart(user_id)
    if not items:
        return "Your cart is empty."
    
    summary = "🛒 *Your Cart:*\n\n"
    for item in items:
        summary += f"• {item.product_name}\n  {item.quantity}x ${item.unit_price:.2f} = ${item.quantity * item.unit_price:.2f}\n"
    
    total = get_cart_total(user_id)
    summary += f"\n*Total: ${total:.2f}*"
    return summary


def remove_from_cart(user_id, product_name):
    """Remove item from cart"""
    try:
        session = get_session()
        session.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_name == product_name
        ).delete()
        session.commit()
        logger.info(f"Removed {product_name} from cart for user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error removing from cart: {e}")
        return False


def clear_cart(user_id):
    """Clear all items from user's cart"""
    try:
        session = get_session()
        session.query(CartItem).filter(CartItem.user_id == user_id).delete()
        session.commit()
        logger.info(f"Cleared cart for user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error clearing cart: {e}")
        return False


def update_quantity(user_id, product_name, quantity):
    """Update quantity of item in cart"""
    try:
        if quantity <= 0:
            return remove_from_cart(user_id, product_name)
        
        session = get_session()
        item = session.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_name == product_name
        ).first()
        
        if item:
            item.quantity = quantity
            session.commit()
            logger.info(f"Updated {product_name} quantity to {quantity} for user {user_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error updating quantity: {e}")
        return False
