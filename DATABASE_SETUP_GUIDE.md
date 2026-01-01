# 📊 Database Persistence & Analytics Setup Guide

## 🎯 Overview

This guide helps you set up the new **PostgreSQL database persistence layer** and analytics system for your sales bot. This allows the bot to remember users across sessions and track detailed performance metrics.

---

## 🚀 Quick Start (5 minutes)

### 1. **Set Up PostgreSQL Database**

#### Option A: Use Vercel Postgres (Recommended for Production)

1. Go to https://vercel.com/storage/postgres
2. Create a new PostgreSQL database
3. Copy the **Postgres Connection String** (looks like `postgresql://...`)
4. Add to your `.env`:
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

#### Option B: Local Development (SQLite)

1. Your bot will automatically create SQLite if DATABASE_URL is not set
2. Or explicitly set:
   ```
   DATABASE_URL=sqlite:///./saleschatbot.db
   ```

### 2. **Initialize Database Tables**

```bash
# In your project directory
python -m pip install -r requirements.txt

# Run database initialization
python api/manage_db.py init
```

You should see: `✅ Database initialized successfully!`

### 3. **Add Admin Key to .env**

```
ADMIN_API_KEY=your-super-secret-key-here-change-this
```

### 4. **Deploy & Access Dashboard**

After deployment, go to:

```
https://your-bot-domain/static/dashboard.html
```

Enter your ADMIN_API_KEY to view analytics!

---

## 📁 New Files Added

```
api/
├── models.py                 ← Database schema definitions
├── database.py              ← Connection manager & utilities
├── database_memory.py       ← LangChain memory integration
├── analytics.py             ← Analytics tracking functions
├── admin_routes.py          ← Admin dashboard API endpoints
└── manage_db.py             ← Database management CLI

static/
└── dashboard.html           ← Analytics dashboard UI
```

---

## 🔧 Environment Variables

Add these to your `.env` file:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/saleschatbot

# Admin Dashboard Security
ADMIN_API_KEY=super-secret-admin-key

# Existing variables (unchanged)
GOOGLE_API_KEY=your-google-api-key
TELEGRAM_TOKEN=your-telegram-token
```

---

## 📊 What Gets Tracked

### User Data

- User ID, username, first name
- Total messages, conversations, purchases
- Total spent, last active time
- Preferred products

### Conversations

- Complete message history (user + bot)
- Current product discussed
- Detected emotion (frustration, urgency, etc.)
- User intent (price, buy, specs, compare)

### Analytics Events

- `message` - User sent a message
- `button_click` - User clicked a button
- `product_view` - User viewed a product
- `purchase` - User made a purchase

### Product Interactions

- Views per product
- Price inquiries
- Spec inquiries
- Purchase attempts

---

## 📈 Analytics Dashboard

Access at: `https://your-domain/static/dashboard.html`

**Key Metrics:**

- 📊 Conversion Rate (%)
- 💰 Total Revenue ($)
- 📦 Top Products
- 🔄 Conversion Funnel
  - Greeting → Browsing → Consideration → Purchase
- 👥 Active Users
- ⏱️ Average Order Value

**Admin API Endpoints:**

```
GET  /admin/dashboard                 - Full dashboard data
GET  /admin/analytics/conversion      - Conversion rate
GET  /admin/analytics/products        - Top products
GET  /admin/analytics/funnel          - Funnel breakdown
GET  /admin/users                     - User list (paginated)
GET  /admin/users/<user_id>           - User details
GET  /admin/analytics/events          - Recent events
GET  /admin/health                    - Health check
```

Query Parameter: `?api_key=YOUR_ADMIN_API_KEY`

---

## 🔄 Using Persistent Memory

The bot now remembers users automatically:

```python
from database_memory import get_user_memory, get_user_context_manager

# Get user's conversation memory
memory = get_user_memory(user_id)

# Add messages (automatically saved to DB)
memory.add_user_message("Tell me about the smartwatch")
memory.add_ai_message("The Smartwatch X is great!")

# Get context for prompt
context = memory.get_context()
# Output: "Previous conversation:\nUser: Tell me about...\nAssistant: The Smartwatch X..."

# Get context manager for product tracking
context_mgr = get_user_context_manager(user_id)
context_mgr.set_context(product="Smartwatch X", emotion="interest", intent="buy")
context_mgr.save_interaction(user_msg, bot_msg)
```

---

## 📊 Tracking Analytics

```python
from analytics import (
    log_user_message, log_button_click,
    log_product_view, log_purchase
)

# Log user message
log_user_message(user_id=123, product="Smartwatch", emotion="positive")

# Log button click
log_button_click(user_id=123, button_type="price", product="Smartwatch")

# Log product view
log_product_view(user_id=123, product="Smartwatch")

# Log purchase
log_purchase(user_id=123, product="Smartwatch", price=59.99)
```

---

## 🛠️ Database Management Commands

```bash
# Initialize database
python api/manage_db.py init

# Check database connection
python api/manage_db.py check

# View database statistics
python api/manage_db.py stats

# Reset database (WARNING: Deletes all data!)
python api/manage_db.py reset
```

---

## 🚨 Migration from In-Memory to Database

If you have an existing bot with in-memory user data:

1. **Backup your data** (export conversation_handler.user_conversations if needed)
2. **Initialize database**: `python api/manage_db.py init`
3. **Update webhook.py** to use new database functions
4. **Redeploy** your bot

The database will start fresh with new user interactions from this point forward.

---

## 🔐 Security Best Practices

1. **Change ADMIN_API_KEY**: Use a strong, random key

   ```bash
   # Generate random key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Database Password**: Use strong password for PostgreSQL

3. **HTTPS Only**: Always use HTTPS for dashboard access

4. **Rate Limiting**: Consider adding rate limits to admin endpoints

---

## 📱 Integration with Existing Bot

The database layer integrates seamlessly:

1. **Old code still works**: Existing response functions are unchanged
2. **Automatic user creation**: New users are added to DB automatically
3. **Memory bridges**: Persistent memory replaces in-memory storage

No breaking changes to existing functionality!

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'psycopg2'"

```bash
pip install psycopg2-binary
```

### "Cannot connect to database"

- Check DATABASE_URL in .env
- For PostgreSQL, ensure password/host is correct
- For local dev, use SQLite (no setup needed)

### "Admin key unauthorized"

- Verify ADMIN_API_KEY matches in .env and dashboard
- Keys are case-sensitive

### "Database is locked" (SQLite)

- Only one process can write at a time
- Use PostgreSQL for production with multiple workers

---

## 📚 Next Steps

1. ✅ Set up database (this guide)
2. ⬜ Update webhook.py to log analytics (see next section)
3. ⬜ Update conversation_handler.py to use persistent memory
4. ⬜ Test with sample conversations
5. ⬜ Monitor dashboard.html

---

## 📖 API Documentation

See `admin_routes.py` for complete REST API documentation.

---

**Questions?** Check the database modules:

- `models.py` - Database schema
- `database.py` - Connection & utilities
- `analytics.py` - Tracking functions
- `database_memory.py` - Memory integration
