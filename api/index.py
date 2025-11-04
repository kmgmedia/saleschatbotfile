from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'ok',
            'message': 'ShopBot Webhook Server is running!',
            'endpoints': {
                'webhook': '/api/webhook',
                'health': '/api/index'
            }
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return
