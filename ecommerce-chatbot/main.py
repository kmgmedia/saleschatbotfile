import os
import sys
import asyncio
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# --- Dry-run (optional testing mode) ---
DRY_RUN = ("--dry-run" in sys.argv) or os.getenv("DRY_RUN") == "1"

# Only check required env vars when NOT in dry-run mode
if not DRY_RUN and __name__ == "__main__":
    if not OPENAI_API_KEY:
        raise ValueError("Missing OpenAI API key in .env file")
    if not TELEGRAM_TOKEN:
        raise ValueError("Missing Telegram token in .env file")

# --- Imports ---
if not DRY_RUN:
    from langchain_core.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain.chains import LLMChain
    from telegram import Update
    from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
else:
    class PromptTemplate:
        def __init__(self, input_variables, template):
            self.input_variables = input_variables
            self.template = template
        def format(self, **kwargs):
            return self.template.format(**kwargs)

# --- Prompt setup ---
template = """
You are an enthusiastic and helpful eCommerce sales assistant named "ShopBot". Your goal is to help customers find the perfect products and have an amazing shopping experience.

Your personality:
- Friendly, warm, and welcoming
- Knowledgeable about products
- Excited to help customers
- Uses emojis occasionally to be engaging (but not excessively)
- Always positive and solution-oriented

Your responsibilities:
- Greet customers warmly when they first message
- Ask clarifying questions to understand their needs
- Recommend products based on their preferences
- Provide detailed product information when asked
- Highlight key features and benefits
- Create urgency with limited-time offers when appropriate
- Offer alternatives if a product isn't available
- Thank customers and invite them to ask more questions

Available Products:
1. **Smartwatch X** - $59 - Tracks steps, sleep, and heart rate. Perfect for fitness enthusiasts!
2. **Bluetooth Speaker Mini** - $29 - Crisp sound and 12h battery life. Great for music lovers on the go!
3. **Wireless Earbuds Pro** - $79 - Noise cancelling and waterproof. Ideal for workouts and commuting!
4. **Power Bank 20000mAh** - $300 - Fast-charging power bank with dual USB ports. Never run out of power!
5. **Smart Home Hub** - $450 - Control all your smart devices from one hub. Make your home smarter!
6. **4K Action Camera** - $850 - Capture stunning 4K videos with image stabilization. Perfect for adventures!

Communication style:
- Keep responses concise but informative (2-4 sentences)
- Use bullet points for product features
- End with a friendly question or call-to-action
- Be conversational and natural

User: {user_message}

ShopBot:"""

prompt = PromptTemplate(
    input_variables=["user_message"],
    template=template
)

# --- Chatbot setup ---
if not DRY_RUN:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    chatbot_chain = LLMChain(llm=llm, prompt=prompt)

    def chatbot_response(user_message):
        response = chatbot_chain.run(user_message)
        return response.strip()
else:
    def chatbot_response(user_message):
        # More realistic dry-run responses based on keywords
        msg_lower = user_message.lower()

        if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'start', 'hey are you available', 'sup', 'good morning', 'good afternoon', 'good evening', 'i need help']):
            return "👋 Hello! Welcome to ShopBot from KMGMedia Design & Technologies! I'm here to help you find amazing tech products. We have smartwatches, wireless earbuds, bluetooth speakers, power banks, smart home hubs, and 4K action cameras. What are you looking for today?"
        
        elif any(word in msg_lower for word in ['earbud', 'headphone', 'audio', 'music']):
            return "🎧 Great choice! I'd recommend our **Wireless Earbuds Pro** ($79):\n\n✅ Noise cancelling technology\n✅ Waterproof design\n✅ Perfect for workouts and commuting\n\nThey're one of our best-sellers! Would you like to know more about them?"
        
        elif any(word in msg_lower for word in ['watch', 'fitness', 'track', 'health']):
            return "⌚ Perfect! Our **Smartwatch X** ($59) is amazing:\n\n✅ Tracks steps, sleep & heart rate\n✅ Long battery life\n✅ Great for fitness enthusiasts\n\nIt's on sale right now! Interested in getting one?"
        
        elif any(word in msg_lower for word in ['speaker', 'sound', 'bluetooth']):
            return "🔊 Excellent! The **Bluetooth Speaker Mini** ($29) is perfect:\n\n✅ Crisp, clear sound\n✅ 12-hour battery life\n✅ Portable and lightweight\n\nGreat for parties or outdoor use! Want to order one?"
        
        elif any(word in msg_lower for word in ['power bank', 'powerbank', 'battery', 'charging']):
            return "🔋 Awesome! Our **Power Bank 20000mAh** ($300) is a game-changer:\n\n✅ Fast-charging technology\n✅ Dual USB ports\n✅ Charge multiple devices at once\n\nNever run out of power again! Interested?"
        
        elif any(word in msg_lower for word in ['smart home', 'home hub', 'hub', 'automation']):
            return "🏠 Fantastic! The **Smart Home Hub** ($450) is incredible:\n\n✅ Control all smart devices from one place\n✅ Works with lights, thermostats, security systems\n✅ Voice control compatible\n\nMake your home smarter today! Want to learn more?"
        
        elif any(word in msg_lower for word in ['camera', 'action camera', '4k', 'video', 'gopro']):
            return "📹 Perfect for adventures! Our **4K Action Camera** ($850) is top-notch:\n\n✅ Stunning 4K video quality\n✅ Professional image stabilization\n✅ Waterproof and rugged design\n\nCapture amazing moments! Ready to order?"
        
        elif any(word in msg_lower for word in ['price', 'cost', 'cheap', 'affordable']):
            return "💰 Here are our prices:\n\n🔸 Bluetooth Speaker Mini - **$29** (Best value!)\n🔸 Smartwatch X - **$59**\n🔸 Wireless Earbuds Pro - **$79**\n🔸 Power Bank 20000mAh - **$300**\n🔸 Smart Home Hub - **$450**\n🔸 4K Action Camera - **$850**\n\nFree shipping on orders over $100! Which one interests you?"
        
        elif any(word in msg_lower for word in ['all', 'products', 'what', 'show', 'available', 'catalog']):
            return "🛍️ Here's our complete catalog:\n\n1️⃣ **Smartwatch X** - $59\n   Track your fitness goals!\n\n2️⃣ **Bluetooth Speaker Mini** - $29\n   Amazing sound quality!\n\n3️⃣ **Wireless Earbuds Pro** - $79\n   Noise cancelling & waterproof!\n\n4️⃣ **Power Bank 20000mAh** - $300\n   Fast-charging power solution!\n\n5️⃣ **Smart Home Hub** - $450\n   Control your entire home!\n\n6️⃣ **4K Action Camera** - $850\n   Pro-level video capture!\n\nWhich one catches your eye? 😊"
        
        elif any(word in msg_lower for word in ['buy', 'order', 'purchase', 'get']):
            return "🎉 Awesome! To complete your order, please click the 'Buy Now' button or contact our sales team. We offer:\n\n✅ Free shipping\n✅ 30-day returns\n✅ 1-year warranty\n\nAnything else I can help you with?"
        
        elif any(word in msg_lower for word in ['thank', 'thanks']):
            return "You're very welcome! 😊 Feel free to ask if you need anything else. Happy shopping! 🛒"
        
        else:
            return f"I'm here to help! We have great tech products like smartwatches ($59), wireless earbuds ($79), bluetooth speakers ($29), power banks ($300), smart home hubs ($450), and 4K action cameras ($850). Could you tell me more about what you're looking for? 🤔"

# --- Telegram integration ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"💬 User: {user_message}")  # for your console log

    try:
        reply = chatbot_response(user_message)
        await update.message.reply_text(reply)
    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("⚠️ Oops! Something went wrong. Please try again.")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running and ready to chat!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
