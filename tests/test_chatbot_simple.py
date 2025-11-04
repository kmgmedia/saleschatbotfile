"""
Quick test to verify the ecommerce chatbot works in dry-run mode
"""
import os
import sys

# Force dry-run mode
os.environ["DRY_RUN"] = "1"

# Add parent to path so we can import
sys.path.insert(0, r'C:\Users\DELL\Desktop\saleschatbotfile\ecommerce-chatbot')

# Import the chatbot
import main as chatbot

# Test the chatbot_response function
print("Testing chatbot_response function...")
print("=" * 50)

test_messages = [
    "Hi, what products do you have?",
    "I need waterproof earbuds",
    "Tell me about the smartwatch"
]

for msg in test_messages:
    print(f"\nUser: {msg}")
    response = chatbot.chatbot_response(msg)
    print(f"Bot: {response}")
    print("-" * 50)

print("\n✅ Chatbot test completed successfully!")
