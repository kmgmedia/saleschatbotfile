"""
Load prompts from the prompts/ folder
"""
import os
import sys

def load_prompt(filename):
    """Load prompt content from prompts folder"""
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error loading {filename}: {e}", file=sys.stderr)
        return ""

# Load all prompts at module initialization
SYSTEM_PROMPT = load_prompt('system_prompt.txt')
PRODUCTS_LIST = load_prompt('products.txt')
SALES_STYLE = load_prompt('sales_style.txt')

# Log prompt loading status
print(f"Prompts loaded - System: {len(SYSTEM_PROMPT)} chars, Products: {len(PRODUCTS_LIST)} chars", file=sys.stderr)
