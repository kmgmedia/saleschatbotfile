"""
Analytics Module - Real-time Metrics and Performance Tracking
Tracks user behavior, conversion funnels, and bot performance
"""
import sys
from datetime import datetime, timedelta

try:
    from .database import get_session, track_analytics, track_product_view
    from .models import Analytics, User, ProductView, Conversation
except ImportError:
    from database import get_session, track_analytics, track_product_view
    from models import Analytics, User, ProductView, Conversation

# Analytics event types
EVENTS = {
    'MESSAGE': 'message',
    'BUTTON_CLICK': 'button_click',
    'PRODUCT_VIEW': 'product_view',
    'PURCHASE': 'purchase',
    'ERROR': 'error',
    'SENTIMENT': 'sentiment'
}

# Funnel stages
FUNNEL_STAGES = {
    'GREETING': 'greeting',
    'BROWSING': 'browsing',
    'CONSIDERATION': 'consideration',
    'PURCHASE': 'purchase'
}


def log_user_message(user_id: int, product: str = None, emotion: str = None):
    """
    Log user message analytics
    
    Args:
        user_id: Telegram user ID
        product: Product mentioned
        emotion: Detected emotion
    """
    try:
        event_data = {
            'product': product,
            'emotion': emotion,
            'timestamp': datetime.utcnow().isoformat()
        }
        track_analytics(
            user_id=user_id,
            event_type=EVENTS['MESSAGE'],
            event_data=event_data,
            product_viewed=product
        )
        
        # Update user total messages
        session = get_session()
        try:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.total_messages += 1
                if product:
                    user.last_viewed_product = product
                session.commit()
        finally:
            session.close()
            
    except Exception as e:
        print(f"Analytics error (log_user_message): {e}", file=sys.stderr)


def log_button_click(user_id: int, button_type: str, product: str = None, button_data: dict = None):
    """
    Log button click analytics
    
    Args:
        user_id: Telegram user ID
        button_type: Type of button (price, specs, buy, compare)
        product: Product name
        button_data: Additional button data
    """
    try:
        event_data = {
            'button_type': button_type,
            'product': product,
            'timestamp': datetime.utcnow().isoformat()
        }
        if button_data:
            event_data.update(button_data)
        
        track_analytics(
            user_id=user_id,
            event_type=EVENTS['BUTTON_CLICK'],
            event_data=event_data,
            product_viewed=product
        )
        
        # Track specific product interaction
        if product and button_type in ['price', 'specs', 'buy']:
            track_product_view(user_id, product, view_type=button_type)
            
    except Exception as e:
        print(f"Analytics error (log_button_click): {e}", file=sys.stderr)


def log_product_view(user_id: int, product: str):
    """
    Log product view
    
    Args:
        user_id: Telegram user ID
        product: Product name
    """
    try:
        track_product_view(user_id, product, view_type='general')
        track_analytics(
            user_id=user_id,
            event_type=EVENTS['PRODUCT_VIEW'],
            product_viewed=product,
            event_data={'timestamp': datetime.utcnow().isoformat()}
        )
    except Exception as e:
        print(f"Analytics error (log_product_view): {e}", file=sys.stderr)


def log_purchase(user_id: int, product: str, price: float):
    """
    Log purchase event
    
    Args:
        user_id: Telegram user ID
        product: Product name
        price: Purchase price
    """
    try:
        track_analytics(
            user_id=user_id,
            event_type=EVENTS['PURCHASE'],
            product_viewed=product,
            is_conversion=True,
            conversion_value=price,
            event_data={
                'product': product,
                'price': price,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        
        # Update user purchase stats
        session = get_session()
        try:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.total_purchases += 1
                user.total_spent += price
                session.commit()
        finally:
            session.close()
            
    except Exception as e:
        print(f"Analytics error (log_purchase): {e}", file=sys.stderr)


def log_error(user_id: int, error_type: str, error_message: str):
    """
    Log error event
    
    Args:
        user_id: Telegram user ID
        error_type: Type of error
        error_message: Error message
    """
    try:
        track_analytics(
            user_id=user_id,
            event_type=EVENTS['ERROR'],
            event_data={
                'error_type': error_type,
                'error_message': error_message,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        print(f"Analytics error (log_error): {e}", file=sys.stderr)


def get_conversion_rate(days: int = 7) -> dict:
    """
    Get conversion rate over period
    
    Args:
        days: Number of days to analyze
    
    Returns:
        Dictionary with conversion metrics
    """
    session = get_session()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        total_events = session.query(Analytics)\
            .filter(Analytics.created_at >= cutoff_date)\
            .count()
        
        conversion_events = session.query(Analytics)\
            .filter(
                Analytics.created_at >= cutoff_date,
                Analytics.is_conversion == True
            )\
            .count()
        
        total_value = session.query(Analytics)\
            .filter(
                Analytics.created_at >= cutoff_date,
                Analytics.is_conversion == True
            )\
            .with_entities(__import__('sqlalchemy').func.sum(Analytics.conversion_value))\
            .scalar() or 0.0
        
        conversion_rate = (conversion_events / total_events * 100) if total_events > 0 else 0
        
        return {
            'period_days': days,
            'total_events': total_events,
            'conversion_events': conversion_events,
            'conversion_rate': round(conversion_rate, 2),
            'total_revenue': round(float(total_value), 2),
            'average_order_value': round(float(total_value) / conversion_events, 2) if conversion_events > 0 else 0
        }
    finally:
        session.close()


def get_top_products(limit: int = 10, days: int = 7) -> list:
    """
    Get top products by views
    
    Args:
        limit: Number of products to return
        days: Number of days to analyze
    
    Returns:
        List of top products with metrics
    """
    session = get_session()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        top_products = session.query(
            ProductView.product_name,
            __import__('sqlalchemy').func.sum(ProductView.views_count).label('total_views'),
            __import__('sqlalchemy').func.sum(ProductView.price_inquiries).label('price_inquiries'),
            __import__('sqlalchemy').func.sum(ProductView.purchase_attempts).label('purchase_attempts')
        )\
        .filter(ProductView.last_viewed_at >= cutoff_date)\
        .group_by(ProductView.product_name)\
        .order_by(__import__('sqlalchemy').func.sum(ProductView.views_count).desc())\
        .limit(limit)\
        .all()
        
        return [
            {
                'product_name': p[0],
                'total_views': p[1] or 0,
                'price_inquiries': p[2] or 0,
                'purchase_attempts': p[3] or 0,
                'interest_conversion': round((p[3] or 0) / (p[1] or 1) * 100, 2)
            }
            for p in top_products
        ]
    finally:
        session.close()


def get_user_engagement_score(user_id: int) -> float:
    """
    Calculate user engagement score (0-100)
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        Engagement score
    """
    session = get_session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            return 0.0
        
        # Score components
        message_score = min(user.total_messages / 100 * 30, 30)  # 0-30 points
        conversation_score = min(user.total_conversations / 10 * 30, 30)  # 0-30 points
        purchase_score = min(user.total_purchases * 10, 40)  # 0-40 points
        
        total_score = message_score + conversation_score + purchase_score
        
        return round(min(total_score, 100), 2)
    finally:
        session.close()


def get_funnel_analysis(days: int = 7) -> dict:
    """
    Analyze conversion funnel
    
    Args:
        days: Number of days to analyze
    
    Returns:
        Funnel stage breakdown
    """
    session = get_session()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Count users in each stage
        greeting_users = session.query(Analytics)\
            .filter(Analytics.created_at >= cutoff_date)\
            .distinct(Analytics.user_id)\
            .count()
        
        # Users who viewed products (browsing stage)
        browsing_users = session.query(Analytics)\
            .filter(
                Analytics.created_at >= cutoff_date,
                Analytics.product_viewed.isnot(None)
            )\
            .distinct(Analytics.user_id)\
            .count()
        
        # Users who inquired about pricing (consideration)
        consideration_users = session.query(Analytics)\
            .filter(
                Analytics.created_at >= cutoff_date,
                Analytics.event_type == 'button_click'
            )\
            .distinct(Analytics.user_id)\
            .count()
        
        # Users who made purchase
        purchase_users = session.query(Analytics)\
            .filter(
                Analytics.created_at >= cutoff_date,
                Analytics.is_conversion == True
            )\
            .distinct(Analytics.user_id)\
            .count()
        
        return {
            'greeting': greeting_users,
            'browsing': browsing_users,
            'browsing_conversion': round(browsing_users / greeting_users * 100, 2) if greeting_users > 0 else 0,
            'consideration': consideration_users,
            'consideration_conversion': round(consideration_users / browsing_users * 100, 2) if browsing_users > 0 else 0,
            'purchase': purchase_users,
            'purchase_conversion': round(purchase_users / consideration_users * 100, 2) if consideration_users > 0 else 0,
            'overall_conversion': round(purchase_users / greeting_users * 100, 2) if greeting_users > 0 else 0
        }
    finally:
        session.close()


def get_dashboard_summary(days: int = 7) -> dict:
    """
    Get comprehensive dashboard summary
    
    Args:
        days: Number of days to analyze
    
    Returns:
        Dictionary with all key metrics
    """
    return {
        'conversion_metrics': get_conversion_rate(days),
        'top_products': get_top_products(limit=5, days=days),
        'funnel_analysis': get_funnel_analysis(days),
        'generated_at': datetime.utcnow().isoformat()
    }
