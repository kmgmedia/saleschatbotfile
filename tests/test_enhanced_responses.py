"""
Test enhanced chatbot responses
"""
import os
import sys

os.environ["DRY_RUN"] = "1"
sys.path.insert(0, r'C:\Users\DELL\Desktop\saleschatbotfile\ecommerce-chatbot')

import main as chatbot

print("🤖 Testing Enhanced ShopBot Responses")
print("=" * 60)

test_conversations = [
    "Hi there!",
    "What products do you have?",
    "I need good earbuds for the gym",
    "How much is the smartwatch?",
    "Tell me about the speaker",
    "I want to buy the earbuds",
    "Thanks for your help!",
]

for msg in test_conversations:
    print(f"\n👤 Customer: {msg}")
    response = chatbot.chatbot_response(msg)
    print(f"🤖 ShopBot: {response}")
    print("-" * 60)

print("\n✅ All test conversations completed!")
