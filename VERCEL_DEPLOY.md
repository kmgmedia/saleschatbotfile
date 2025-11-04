# 🚀 Deploying ShopBot to Vercel

## Step-by-Step Guide

### 1️⃣ Prerequisites

- Vercel account (sign up at [vercel.com](https://vercel.com))
- Your project already on GitHub (or ready to upload)

### 2️⃣ Deploy to Vercel

**Option A: Using Vercel CLI**

```powershell
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

**Option B: Using Vercel Dashboard**

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Click "Deploy"

### 3️⃣ Add Environment Variables

In Vercel Dashboard → Settings → Environment Variables, add:

| Name             | Value                          |
| ---------------- | ------------------------------ |
| `TELEGRAM_TOKEN` | Your bot token from @BotFather |
| `OPENAI_API_KEY` | Your OpenAI API key (optional) |

### 4️⃣ Set Up Webhook

After deployment, run this command locally:

```powershell
python setup_webhook.py
```

Enter your Vercel URL when prompted (e.g., `https://your-bot.vercel.app`)

### 5️⃣ Test Your Bot!

Send a message to your bot on Telegram - it should respond instantly! 🎉

---

## 🔧 Troubleshooting

**"Application Error"**

- Check Environment Variables are set correctly in Vercel
- Redeploy after adding variables

**Bot doesn't respond**

- Make sure webhook is set (run `setup_webhook.py` again)
- Check Vercel function logs in dashboard

**Import errors**

- The webhook uses DRY_RUN mode automatically
- No heavy dependencies needed

---

## ✅ What Changed?

- **Before:** Bot used polling (needs to run 24/7)
- **After:** Bot uses webhooks (Vercel calls your function when messages arrive)

This is much more efficient and works perfectly with Vercel's serverless model!

---

## 💡 Keep Local Bot Running

You can still run the bot locally for testing:

```powershell
cd telegram_bot_project
python bot.py
```

Just make sure to **stop the local bot** when using the webhook, or messages will be handled twice!

---

Need help? Check Vercel deployment logs in your dashboard!
