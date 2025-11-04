"""
Simple endpoint to see incoming Telegram updates
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def show_update():
    if request.method == 'POST':
        update = request.get_json()
        # Return the full update so we can see what Telegram is sending
        return jsonify({
            'received': True,
            'update': update
        })
    return jsonify({'status': 'Chat ID catcher ready'})
