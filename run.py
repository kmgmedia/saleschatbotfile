#!/usr/bin/env python
"""
Simple Flask app runner for development
"""
import sys
import os

# Ensure api directory is in path
api_dir = os.path.join(os.path.dirname(__file__), 'api')
sys.path.insert(0, api_dir)
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == '__main__':
    # Import after path is properly set
    from webhook import app
    
    print("🚀 Starting Flask server...")
    print("📊 Dashboard: http://localhost:5000/static/dashboard.html")
    print("🤖 Bot webhook: http://localhost:5000/webhook")
    print("\nPress Ctrl+C to stop server\n")
    
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
