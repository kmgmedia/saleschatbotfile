"""
Test telegram bot backend loading
"""
import os
import sys

# Ensure we're at project root
sys.path.insert(0, r'C:\Users\DELL\Desktop\saleschatbotfile')

# Import with DRY_RUN to avoid telegram libs
os.environ["DRY_RUN"] = "1"

print("Testing chatbot backend import from telegram bot...")
print("=" * 60)

# Manually run the load_chatbot_module logic
import importlib.machinery
import importlib.util

base = r'C:\Users\DELL\Desktop\saleschatbotfile\telegram_bot_project'
main_path = os.path.normpath(os.path.join(base, "..", "ecommerce-chatbot", "main.py"))

print(f"Looking for main.py at: {main_path}")
print(f"File exists: {os.path.exists(main_path)}")

if os.path.exists(main_path):
    loader = importlib.machinery.SourceFileLoader("ec_main", main_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    
    # Set DRY_RUN before import
    prev_dry = os.environ.get("DRY_RUN")
    os.environ["DRY_RUN"] = "1"
    
    try:
        loader.exec_module(module)
        print("✅ Module imported successfully!")
        print(f"Has chatbot_response: {hasattr(module, 'chatbot_response')}")
        
        if hasattr(module, 'chatbot_response'):
            # Test it
            test_msg = "Hello, I need help finding products"
            response = module.chatbot_response(test_msg)
            print(f"\nTest message: {test_msg}")
            print(f"Response: {response}")
            print("\n✅ Chatbot backend is working!")
        else:
            print("❌ chatbot_response not found")
    except SystemExit as e:
        print(f"❌ Module called sys.exit: {e}")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if prev_dry is None:
            os.environ.pop("DRY_RUN", None)
        else:
            os.environ["DRY_RUN"] = prev_dry
