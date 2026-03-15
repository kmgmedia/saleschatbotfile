"""
Admin Routes - Analytics Dashboard API
Provides endpoints for analytics and monitoring
"""
import sys
from flask import Blueprint, jsonify, request
from datetime import datetime

try:
    from .database import get_session, get_user_stats
    from .models import User, Analytics, ProductView
    from .analytics import (
        get_conversion_rate, get_top_products, get_funnel_analysis,
        get_dashboard_summary
    )
except ImportError:
    from database import get_session, get_user_stats
    from models import User, Analytics, ProductView
    from analytics import (
        get_conversion_rate, get_top_products, get_funnel_analysis,
        get_dashboard_summary
    )

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def verify_admin_key(request_obj):
    """Verify admin API key"""
    import os
    admin_key = os.getenv('ADMIN_API_KEY', 'change-me-in-production')
    
    api_key = request_obj.headers.get('X-Admin-Key') or request_obj.args.get('api_key')
    
    return api_key == admin_key


@admin_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard summary"""
    if not verify_admin_key(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        days = request.args.get('days', 7, type=int)
        summary = get_dashboard_summary(days)
        
        return jsonify({
            'success': True,
            'data': summary,
            'period_days': days
        })
    except Exception as e:
        print(f"Dashboard error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/analytics/conversion', methods=['GET'])
def get_conversion():
    """Get conversion rate analytics"""
    if not verify_admin_key(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        days = request.args.get('days', 7, type=int)
        data = get_conversion_rate(days)
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/analytics/products', methods=['GET'])
def get_products():
    """Get top products analytics"""
    if not verify_admin_key(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 10, type=int)
        data = get_top_products(limit=limit, days=days)
        
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/analytics/funnel', methods=['GET'])
def get_funnel():
    """Get funnel analysis"""
    if not verify_admin_key(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        days = request.args.get('days', 7, type=int)
        data = get_funnel_analysis(days)
        
        return jsonify({
            'success': True,
            'data': data,
            'period_days': days
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users', methods=['GET'])
def get_users():
    """Get list of users with pagination"""
    if not verify_admin_key(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        session = get_session()
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        offset = (page - 1) * limit
        
        users = session.query(User)\
            .order_by(User.last_active.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        total = session.query(User).count()
        session.close()
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'user_id': u.user_id,
                    'username': u.username,
                    'first_name': u.first_name,
                    'total_messages': u.total_messages,
                    'total_purchases': u.total_purchases,
                    'total_spent': float(u.total_spent),
                    'created_at': u.created_at.isoformat(),
                    'last_active': u.last_active.isoformat()
                }
                for u in users
            ],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        })
    except Exception as e:
        print(f"Get users error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get detailed user statistics"""
    if not verify_admin_key(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        stats = get_user_stats(user_id)
        
        if not stats:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/analytics/events', methods=['GET'])
def get_events():
    """Get recent analytics events"""
    if not verify_admin_key(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        session = get_session()
        
        limit = request.args.get('limit', 50, type=int)
        event_type = request.args.get('type')
        
        query = session.query(Analytics).order_by(Analytics.created_at.desc())
        
        if event_type:
            query = query.filter(Analytics.event_type == event_type)
        
        events = query.limit(limit).all()
        session.close()
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'metric_id': e.metric_id,
                    'user_id': e.user_id,
                    'event_type': e.event_type,
                    'product_viewed': e.product_viewed,
                    'is_conversion': e.is_conversion,
                    'conversion_value': float(e.conversion_value) if e.conversion_value else None,
                    'created_at': e.created_at.isoformat()
                }
                for e in events
            ],
            'count': len(events)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/health', methods=['GET'])
def health():
    """Health check"""
    try:
        session = get_session()
        user_count = session.query(User).count()
        session.close()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database_connected': True,
            'total_users': user_count
        })
    except Exception as e:
        print(f"Health check error: {e}", file=sys.stderr)
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'database_connected': False
        }), 500
