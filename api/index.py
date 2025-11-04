from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'ShopBot Webhook Server is running!',
        'endpoints': {
            'webhook': '/api/webhook',
            'health': '/api/index'
        }
    })
