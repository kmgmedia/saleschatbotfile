"""
Test the smart recommendation system
"""
import sys
sys.path.append('api')

from product_catalog import get_smart_recommendation, detect_intent

# Test cases
test_messages = [
    "I want something to track my fitness",
    "I need good headphones for music",
    "Show me smart home products",
    "What do you have for gaming?",
    "I work from home, need office stuff",
    "Something for camping and travel",
]

print("=" * 60)
print("TESTING SMART RECOMMENDATION SYSTEM")
print("=" * 60)

for msg in test_messages:
    print(f"\n📝 User: {msg}")
    print(f"🎯 Detected Intent: {detect_intent(msg)}")
    print("\n🤖 Bot Response:")
    print(get_smart_recommendation(msg))
    print("\n" + "-" * 60)
