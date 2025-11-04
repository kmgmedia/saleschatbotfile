import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Dry-run detection
DRY_RUN = ("--dry-run" in sys.argv) or os.getenv("DRY_RUN") == "1"

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

if DRY_RUN:
    logger.info("-- DRY-RUN: telegram bot will not import telegram/network libs --")
    if not TOKEN:
        logger.info("(dry-run) TELEGRAM_TOKEN not set — this is OK for dry-run")
    logger.info("Simulated bot: will respond to /start with a friendly greeting.")
    sys.exit(0)

# Normal mode: import telegram libs and run
try:
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
except Exception as e:
    logger.exception("ERROR: Failed to import telegram libraries: %s", e)
    logger.error("Make sure python-telegram-bot is installed and compatible with your Python version.")
    sys.exit(1)

async def start(update: Update, context):
    logger.info("Received /start from %s", update.effective_user.id if update.effective_user else 'unknown')
    await update.message.reply_text("Hey there 👋 I'm your AI assistant!")

if not TOKEN:
    logger.error("ERROR: TELEGRAM_TOKEN is not set. Please set it in your environment or in a .env file.")
    sys.exit(1)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

logger.info("Bot started (token prefix: %s)", (TOKEN[:6] + '***') if TOKEN else '(none)')

# Try to import the ecommerce chatbot implementation from the sibling folder
import importlib.machinery
import importlib.util

def load_chatbot_module():
    base = os.path.dirname(__file__)
    main_path = os.path.normpath(os.path.join(base, "..", "ecommerce-chatbot", "main.py"))
    if not os.path.exists(main_path):
        logger.warning("chatbot main not found at %s; message handling will be disabled.", main_path)
        return None
    loader = importlib.machinery.SourceFileLoader("ec_main", main_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    try:
        # Ensure the imported chatbot runs in dry-run mode so it doesn't require
        # OpenAI/langchain or env vars. Temporarily set DRY_RUN in os.environ
        prev_dry = os.environ.get("DRY_RUN")
        os.environ["DRY_RUN"] = "1"
        try:
            loader.exec_module(module)
        finally:
            # restore previous value
            if prev_dry is None:
                os.environ.pop("DRY_RUN", None)
            else:
                os.environ["DRY_RUN"] = prev_dry
    except SystemExit:
        # main.py may call sys.exit if env vars missing — treat as not available
        logger.warning("chatbot main exited during import (likely missing deps or env vars).")
        return None
    except Exception as e:
        logger.exception("failed to import chatbot main: %s", e)
        return None
    return module

ec = load_chatbot_module()
if ec:
    logger.info("Chatbot backend imported successfully; chatbot_response available: %s", hasattr(ec, 'chatbot_response'))
else:
    logger.warning("Chatbot backend not available; messages will receive a fallback reply.")

async def handle_message(update: Update, context):
    try:
        text = update.message.text
        logger.info("Received message from %s: %s", update.effective_user.username if update.effective_user else 'unknown', text)
        if not ec or not hasattr(ec, "chatbot_response"):
            await update.message.reply_text("Sorry, the chatbot backend is not available right now.")
            return
        # Run the potentially blocking chatbot_response in a thread pool
        loop = asyncio.get_event_loop()
        reply = await loop.run_in_executor(None, ec.chatbot_response, text)
        await update.message.reply_text(reply)
    except Exception:
        logger.exception("Error while handling message")
        try:
            await update.message.reply_text("Sorry, an error occurred while processing your message.")
        except Exception:
            logger.exception("Failed to send error reply to the user")

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    asyncio.run(app.run_polling())

