# 🤖 Alex - Your AI Tech Consultant

**Meet Alex:** A 7-year veteran sales consultant powered by AI, helping customers find their perfect tech match through genuine conversation and expert guidance.

> **A 24/7 Telegram chatbot that helps customers find and buy your products!**

---

## 🚀 Quick Start

### 1. Get a Telegram Bot Token 📱

1. Open Telegram and search for **@BotFather**
2. Type `/newbot` and follow instructions
3. Save your TOKEN (looks like `123456789:ABCdef...`)

### 2. Get Google Gemini API Key 🔑

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create account → Create API Key → Create API key in new project
3. Save your key (starts with `AIza...`)

### 3. Add Your Keys 🗝️

Open `.env` file and add:

```
GOOGLE_API_KEY=AIza-your-key-here
TELEGRAM_TOKEN=123456789:your-token-here
```

### 4. Start the Bot! 🎬

```powershell
cd telegram_bot_project
python bot.py
```

**Done!** 🎉 Your bot is live!

---

## 💬 Try It Out

1. Search for your bot name in Telegram
2. Send: **"Hi!"**
3. Watch it respond! ✨

The bot will:

- 👋 Greet customers warmly
- 🛍️ Show products with prices
- 💬 Answer questions
- 🎯 Recommend items

---

## 🏗️ Architecture - How It Works

The bot uses an intelligent **Intent Classification System** that routes customer messages to the right handler:

```
User Message → Intent Classification (AI + Keyword Fallback)
                    ↓
            ┌───────┼───────┐
            ↓       ↓       ↓
        Purchase Support Upsell
            ↓       ↓       ↓
        (Cart)  (Help)  (Premium)
            ↓       ↓       ↓
            └───────┼───────┘
                    ↓
            Update & Store Context
                    ↓
            Send Response to Telegram
```

**View the complete flow diagram:** [INTENT_CLASSIFICATION_FLOW.html](INTENT_CLASSIFICATION_FLOW.html) (Open in browser for a professional architecture diagram)

**View the analytics system:** [CONVERSATION_ANALYTICS.html](CONVERSATION_ANALYTICS.html) (Real-time metrics, conversion tracking, intent distribution)

**View the recommendation engine:** [PRODUCT_RECOMMENDATION_OUTPUT.html](PRODUCT_RECOMMENDATION_OUTPUT.html) (Context-aware personalization pipeline)

### 🔄 Three Intent Routes:

- **💰 Purchase Flow** - Product browsing, pricing, cart management, checkout
- **🆘 Support Flow** - Issue logging, help content, solutions
- **📈 Upsell Flow** - Premium recommendations, add-on suggestions, upgrades

---

## 🛍️ Your Products

Current catalog:

| Product                   | Price | Details                      |
| ------------------------- | ----- | ---------------------------- |
| 🎧 Wireless Earbuds Pro   | $79   | Noise cancelling, waterproof |
| ⌚ Smartwatch X           | $59   | Fitness & sleep tracker      |
| 🔊 Bluetooth Speaker Mini | $29   | 12-hour battery              |

**To add products:** Edit `ecommerce-chatbot/data/products.json`

---

## 🎨 Customize

**Change bot personality:**  
Edit `ecommerce-chatbot/prompts/sales_prompt.txt`

**Test mode (free):**  
The bot runs in smart keyword mode automatically - no AI costs until you're ready!

---

## ❓ FAQ

**Need to code?** Nope! Just follow the steps above 👨‍🍳

**Cost?** Free! Google Gemini API has a generous free tier. No credit card needed for testing.

**What if it stops?** Run `python bot.py` again 🔄

**Buy feature?** Bot recommends products. You can add checkout links!

---

## 🎉 You're Ready!

Your AI sales assistant is working 24/7! Test it, customize it, and watch it help your customers.

**Real examples:**

- "What do you sell?" → ✅ Shows all products
- "How much is the smartwatch?" → ✅ Gives price
- "I want earbuds" → ✅ Recommends perfect match

Happy selling! 💰✨

---

\_Made with ❤️ for entrepreneurs_by Moruf Adebola
