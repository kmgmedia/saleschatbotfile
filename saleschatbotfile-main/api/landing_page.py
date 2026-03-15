"""
HTML landing page for the webhook
"""

def get_landing_page():
    """Return the HTML landing page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="15; url=https://t.me/Store_help_bot">
        <title>Alex - Your AI Tech Consultant</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: white;
                text-align: center;
                padding: 20px;
            }
            .container {
                max-width: 500px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            .logo {
                font-size: 80px;
                margin-bottom: 20px;
                animation: bounce 2s infinite;
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 700;
            }
            .tagline {
                font-size: 1.2em;
                opacity: 0.9;
                margin-bottom: 30px;
            }
            .status {
                background: rgba(255, 255, 255, 0.2);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 30px;
            }
            .status-indicator {
                display: inline-block;
                width: 10px;
                height: 10px;
                background: #4ade80;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            .btn {
                display: inline-block;
                background: white;
                color: #667eea;
                padding: 15px 40px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.1em;
                transition: transform 0.3s, box-shadow 0.3s;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            }
            .products {
                margin-top: 30px;
                font-size: 0.9em;
                opacity: 0.8;
            }
            .redirect-notice {
                margin-top: 20px;
                font-size: 0.9em;
                opacity: 0.7;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🤖</div>
            <h1>ShopBot</h1>
            <p class="tagline">Your AI Shopping Assistant</p>
            
            <div class="status">
                <span class="status-indicator"></span>
                <strong>Online & Ready to Help</strong>
            </div>
            
            <a href="https://t.me/Store_help_bot" class="btn">💬 Chat with Alex on Telegram</a>
            
            <div class="products">
                <p><strong>Featured Products:</strong></p>
                <p>🎧 Wireless Earbuds Pro • ⌚ Smartwatch X</p>
                <p>🔊 Bluetooth Speaker • 🔋 Power Bank</p>
                <p>🏠 Smart Home Hub • 📹 4K Camera</p>
            </div>
            
            <div class="redirect-notice">
                🔄 Redirecting to Telegram in 15 seconds...
            </div>
        </div>
    </body>
    </html>
    """
