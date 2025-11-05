"""
Test natural conversation handler
"""
import sys
sys.path.append('api')

from conversation_handler import handle_user_input, reset_conversation

print("=" * 70)
print("TESTING NATURAL CONVERSATION SYSTEM")
print("=" * 70)

# Test conversation flow
test_conversation = [
    "I'm interested in the smartwatch",
    "Is it waterproof?",
    "How much does it cost?",
    "That sounds good, I want to buy it",
    "Tell me about wireless earbuds",
    "What's the battery life?",
    "Can I return it if I don't like it?",
]

print("\n🗣️ SIMULATED CONVERSATION:\n")
for user_msg in test_conversation:
    print(f"👤 User: {user_msg}")
    bot_response = handle_user_input(user_msg)
    print(f"🤖 Bot: {bot_response}\n")
    print("-" * 70 + "\n")

# Test product switching
print("\n" + "=" * 70)
print("TESTING PRODUCT SWITCHING")
print("=" * 70 + "\n")

reset_conversation()

switch_test = [
    "Show me the power bank",
    "How long does it last?",
    "Actually, tell me about the drone instead",
    "Can it avoid obstacles?",
]

for user_msg in switch_test:
    print(f"👤 User: {user_msg}")
    bot_response = handle_user_input(user_msg)
    print(f"🤖 Bot: {bot_response}\n")
    print("-" * 70 + "\n")
