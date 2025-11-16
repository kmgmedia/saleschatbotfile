# 📁 Project Structure - Modular Architecture

## Your Clean, Separated Code Structure

```
saleschatbotfile/
├── api/
│   ├── webhook.py          ← Main entry point (Flask app & routes)
│   ├── gemini_handler.py   ← Google Gemini AI logic
│   ├── responses.py        ← Fallback keyword responses
│   ├── telegram_handler.py ← Telegram API interactions
│   ├── prompt_loader.py    ← Load prompts from files
│   └── landing_page.py     ← HTML landing page
├── prompts/
│   ├── system_prompt.txt   ← Bot personality
│   ├── products.txt        ← Product catalog
│   └── sales_style.txt     ← System role
└── ...

```

## 📝 What Each File Does

### `api/webhook.py` - Main Entry Point

- Flask application and routes
- Handles `/` GET request (landing page)
- Handles `/webhook` POST request (Telegram updates)
- **Edit this to**: Add new routes or change app configuration

### `api/responses.py` - Keyword Fallback Responses

- Contains `get_fallback_response()` function
- Keyword-based responses when Google Gemini is unavailable
- **Edit this to**: Add/modify product responses, greetings, FAQs

### `api/gemini_handler.py` - AI Intelligence (Google Gemini)

- Contains `get_response()` function
- Calls Google Gemini 2.5 Flash API with prompts
- Falls back to keyword responses on error
- **Edit this to**: Change AI model, temperature, max tokens

### `api/telegram_handler.py` - Telegram Integration

- `send_message()` - Send messages to users
- `process_update()` - Process incoming Telegram updates
- **Edit this to**: Add buttons, inline keyboards, media handling

### `api/prompt_loader.py` - Prompt Management

- Loads prompts from `prompts/` folder
- Exports: `SYSTEM_PROMPT`, `PRODUCTS_LIST`, `SALES_STYLE`
- **Edit this to**: Add new prompt files or change loading logic

### `api/landing_page.py` - Web Interface

- Returns HTML for the landing page
- **Edit this to**: Customize the website look and feel

### `prompts/` Folder - Easy Editing

- `system_prompt.txt` - Bot behavior and personality
- `products.txt` - Product catalog and descriptions
- `sales_style.txt` - Short system role description
- **Edit these to**: Change bot responses without touching code!

## 🎯 Common Tasks

###To add/edit product responses:

1. **For AI responses**: Edit `prompts/products.txt`
2. **For fallback responses**: Edit `api/responses.py`

### To change bot personality:

1. Edit `prompts/system_prompt.txt`

### To add new Telegram features (buttons, images, etc.):

1. Edit `api/telegram_handler.py`

### To change AI settings:

1. Edit `api/openai_handler.py` (model, temperature, etc.)

## 🚀 Deployment

After editing any file:

```bash
git add .
git commit -m "Update [what you changed]"
git push
vercel --prod
```

Your changes will be live in seconds!

---

**Note**: Currently the imports between modules need fixing for Vercel. Working on making this fully modular!
