"""Test if environment variables are loaded"""
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def test():
    token = os.getenv('TELEGRAM_TOKEN', '')
    openai = os.getenv('OPENAI_API_KEY', '')
    
    return jsonify({
        'telegram_token_loaded': bool(token),
        'telegram_prefix': token[:10] + '...' if token else 'NOT FOUND',
        'openai_loaded': bool(openai)
    })
