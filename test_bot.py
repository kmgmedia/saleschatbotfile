"""
Test script for memory-based personalization and inline keyboard features
"""

# Add api directory to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from conversation_handler import (
    handle_user_input,
    get_user_memory,
    reset_conversation,
    get_product_spec,
    get_random_intro
)
from inline_keyboard import (
    product_buttons,
    handle_button_callback,
    get_product_list_keyboard
)

def test_memory_recall():
    """Test memory-based conversation recall"""
    print("\n" + "="*60)
    print("TEST 1: Memory-Based Recall")
    print("="*60)
    
    user_id = 12345
    
    # User asks about smartwatch
    print("\n👤 User (12345): Tell me about the smartwatch")
    response = handle_user_input("Tell me about the smartwatch", user_id)
    print(f"🤖 Bot: {response}\n")
    
    # User asks about something else but then wants to recall
    print("👤 User (12345): What was that product again?")
    response = handle_user_input("What was that product again?", user_id)
    print(f"🤖 Bot: {response}\n")
    
    # Check memory
    memory = get_user_memory(user_id)
    print(f"📝 Memory Check - Last Product: {memory['last_product']}")
    print(f"📝 Conversation History Length: {len(memory['conversation_history'])}")
    

def test_multi_user_memory():
    """Test that different users have separate memories"""
    print("\n" + "="*60)
    print("TEST 2: Multi-User Separate Memory")
    print("="*60)
    
    user1 = 11111
    user2 = 22222
    
    # User 1 asks about smartwatch
    print("\n👤 User 1: I want a smartwatch")
    response1 = handle_user_input("I want a smartwatch", user1)
    print(f"🤖 Bot to User 1: {response1[:100]}...\n")
    
    # User 2 asks about earbuds
    print("👤 User 2: Tell me about earbuds")
    response2 = handle_user_input("Tell me about earbuds", user2)
    print(f"🤖 Bot to User 2: {response2[:100]}...\n")
    
    # User 1 asks "how much" - should reference smartwatch
    print("👤 User 1: How much does it cost?")
    response1_price = handle_user_input("How much does it cost?", user1)
    print(f"🤖 Bot to User 1: {response1_price}\n")
    
    # User 2 asks "how much" - should reference earbuds
    print("👤 User 2: How much?")
    response2_price = handle_user_input("How much?", user2)
    print(f"🤖 Bot to User 2: {response2_price}\n")
    
    # Verify memories are separate
    mem1 = get_user_memory(user1)
    mem2 = get_user_memory(user2)
    print(f"✅ User 1 Last Product: {mem1['last_product']}")
    print(f"✅ User 2 Last Product: {mem2['last_product']}")
    print(f"✅ Memories are separate: {mem1['last_product'] != mem2['last_product']}")


def test_inline_keyboards():
    """Test inline keyboard generation"""
    print("\n" + "="*60)
    print("TEST 3: Inline Keyboard Buttons")
    print("="*60)
    
    # Generate product buttons
    product = "Smartwatch X"
    buttons = product_buttons(product)
    
    print(f"\n📱 Inline Keyboard for '{product}':")
    print(f"   Structure: {len(buttons['inline_keyboard'])} rows")
    for i, row in enumerate(buttons['inline_keyboard']):
        print(f"   Row {i+1}: {[btn['text'] for btn in row]}")
    
    # Generate product list keyboard
    list_keyboard = get_product_list_keyboard()
    print(f"\n📱 Product List Keyboard:")
    print(f"   Structure: {len(list_keyboard['inline_keyboard'])} rows")
    for i, row in enumerate(list_keyboard['inline_keyboard']):
        print(f"   Row {i+1}: {[btn['text'] for btn in row]}")


def test_button_callbacks():
    """Test button callback handling"""
    print("\n" + "="*60)
    print("TEST 4: Button Callback Handling")
    print("="*60)
    
    user_id = 99999
    product = "Wireless Earbuds Pro"
    
    # First, set up conversation context
    handle_user_input(f"Tell me about {product}", user_id)
    
    # Test "See Price" button
    print(f"\n🖱️ User clicks: '💰 See Price' on {product}")
    response = handle_button_callback(f"price:{product}", user_id)
    print(f"🤖 Bot response: {response['text']}")
    print(f"   Has buttons: {response.get('reply_markup') is not None}\n")
    
    # Test "See Specs" button
    print(f"🖱️ User clicks: '📋 See Specs' on {product}")
    response = handle_button_callback(f"specs:{product}", user_id)
    print(f"🤖 Bot response: {response['text']}")
    print(f"   Has buttons: {response.get('reply_markup') is not None}\n")
    
    # Test "Buy Now" button
    print(f"🖱️ User clicks: '🛒 Buy Now' on {product}")
    response = handle_button_callback(f"buy:{product}", user_id)
    print(f"🤖 Bot response: {response['text'][:150]}...")
    print(f"   Has buttons: {response.get('reply_markup') is not None}\n")
    
    # Test "Back" button
    print(f"🖱️ User clicks: '🏠 Back to Products'")
    response = handle_button_callback("back", user_id)
    print(f"🤖 Bot response: {response['text']}")
    print(f"   Has buttons: {response.get('reply_markup') is not None}")
    
    # Verify memory was reset
    memory = get_user_memory(user_id)
    print(f"   Memory cleared: {memory['last_product'] is None}")


def test_product_specs():
    """Test product specification retrieval"""
    print("\n" + "="*60)
    print("TEST 5: Product Specifications")
    print("="*60)
    
    products = ["Smartwatch X", "4K Action Camera", "VR Headset Max"]
    
    for product in products:
        spec = get_product_spec(product)
        print(f"\n📋 {product}:")
        print(f"   {spec}")


def test_randomized_intros():
    """Test randomized product introductions"""
    print("\n" + "="*60)
    print("TEST 6: Randomized Introductions")
    print("="*60)
    
    product = "Bluetooth Speaker Mini"
    print(f"\n🎲 Generating 5 random intros for '{product}':\n")
    
    for i in range(5):
        intro = get_random_intro(product)
        print(f"   {i+1}. {intro}")


def test_conversation_flow_with_memory():
    """Test complete conversation flow with memory"""
    print("\n" + "="*60)
    print("TEST 7: Complete Conversation Flow with Memory")
    print("="*60)
    
    user_id = 55555
    
    # Conversation sequence
    messages = [
        "I'm interested in fitness gear",
        "Tell me about the fitness band",
        "How much does it cost?",
        "I'll think about it",
        "Actually, show me what we were talking about",
        "I want to buy it"
    ]
    
    print(f"\n💬 Conversation with User {user_id}:\n")
    
    for msg in messages:
        print(f"👤 User: {msg}")
        response = handle_user_input(msg, user_id)
        print(f"🤖 Bot: {response}\n")
    
    # Show final memory state
    memory = get_user_memory(user_id)
    print(f"📝 Final Memory State:")
    print(f"   Last Product: {memory['last_product']}")
    print(f"   Conversation Length: {len(memory['conversation_history'])}")


if __name__ == "__main__":
    print("\n")
    print("🧪 TESTING MEMORY-BASED PERSONALIZATION & INLINE KEYBOARDS")
    print("="*60)
    
    test_memory_recall()
    test_multi_user_memory()
    test_inline_keyboards()
    test_button_callbacks()
    test_product_specs()
    test_randomized_intros()
    test_conversation_flow_with_memory()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60 + "\n")
