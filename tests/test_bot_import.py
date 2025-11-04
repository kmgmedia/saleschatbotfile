"""
Test telegram bot integration with chatbot backend
"""
import os
import sys

# Set dry-run so we don't need telegram libs
os.environ["DRY_RUN"] = "1"

sys.path.insert(0, r'C:\Users\DELL\Desktop\saleschatbotfile')

# Try to import bot module
print("Importing telegram bot module...")
import telegram_bot_project.bot as bot_module

print("✅ Bot module imported successfully")
print("=" * 50)

# The bot runs in dry-run mode and exits, so this just confirms import works
