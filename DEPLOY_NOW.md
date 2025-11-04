# 🚀 Quick Vercel Deployment Guide

## Follow These Steps in Order:

### Step 1: Login to Vercel
```powershell
vercel login
```
- Choose your preferred login method (GitHub, Email, etc.)
- Complete authentication in browser

### Step 2: Deploy Your Bot
```powershell
cd C:\Users\DELL\Desktop\saleschatbotfile
vercel
```

**Answer the prompts:**
- "Set up and deploy?" → **Y** (Yes)
- "Which scope?" → Select your account
- "Link to existing project?" → **N** (No)
- "What's your project's name?" → **shopbot** (or any name)
- "In which directory is your code located?" → **./** (just press Enter)
- Vercel will detect settings and deploy!

### Step 3: Add Environment Variables

After deployment completes:

**Option A: Using CLI**
```powershell
vercel env add TELEGRAM_TOKEN
```
Paste your bot token when prompted

```powershell
vercel env add OPENAI_API_KEY
```
Paste your OpenAI key when prompted

**Option B: Using Dashboard**
1. Copy the URL Vercel gives you (like `https://shopbot-abc123.vercel.app`)
2. Go to that URL in browser → Click "Dashboard"
3. Settings → Environment Variables
4. Add:
   - `TELEGRAM_TOKEN` = your bot token
   - `OPENAI_API_KEY` = your OpenAI key

### Step 4: Redeploy (to apply environment variables)
```powershell
vercel --prod
```

### Step 5: Connect Telegram to Vercel
```powershell
python setup_webhook.py
```
- Enter your Vercel URL (the one that ends with `.vercel.app`)
- Script will connect Telegram to your deployed bot

### Step 6: Test!
1. Open Telegram
2. Find your bot
3. Send "Hi!"
4. Bot should respond instantly! 🎉

---

## 🎯 Your Vercel URL

After running `vercel`, you'll get a URL like:
```
https://shopbot-abc123.vercel.app
```

**Save this URL!** You need it for Step 5.

---

## ✅ What to Expect

When deployment succeeds, you'll see:
```
✅ Production: https://your-bot.vercel.app [copied to clipboard]
```

Copy that URL and use it in `setup_webhook.py`!

---

## 🆘 Troubleshooting

**"Command not found: vercel"**
- Close and reopen PowerShell
- Or use: `npx vercel` instead

**"Missing environment variables"**
- Make sure to add them in Step 3
- Redeploy after adding (Step 4)

**Bot doesn't respond**
- Check you ran `setup_webhook.py` with correct URL
- Make sure local bot is stopped (not running `bot.py`)

---

Ready? Start with **Step 1** above! 🚀
