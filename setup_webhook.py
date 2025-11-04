"""
Script to set up Telegram webhook after deploying to Vercel
Run this ONCE after deploying: python setup_webhook.py
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
VERCEL_URL = input("Enter your Vercel deployment URL (e.g., https://your-project.vercel.app): ").strip()

if not VERCEL_URL:
    print("❌ Please provide your Vercel URL!")
    exit(1)

if not VERCEL_URL.startswith('http'):
    VERCEL_URL = 'https://' + VERCEL_URL

# Remove trailing slash
VERCEL_URL = VERCEL_URL.rstrip('/')

webhook_url = f"{VERCEL_URL}/api/webhook"

print(f"\n🔧 Setting webhook to: {webhook_url}")

# Set the webhook
response = requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
    json={'url': webhook_url}
)

result = response.json()

if result.get('ok'):
    print("✅ Webhook set successfully!")
    print(f"   Webhook URL: {webhook_url}")
    print("\n🎉 Your bot is now deployed on Vercel!")
    print("   Try sending a message to your bot on Telegram!")
else:
    print("❌ Error setting webhook:")
    print(f"   {result}")
