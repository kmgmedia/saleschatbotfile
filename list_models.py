"""
List available Gemini models for your API key
"""
import requests
import json

GOOGLE_API_KEY = "AIzaSyDQ2afqPxDw5FkSfkRTcolG2oIzXRJ6zJs"

print("🔍 Fetching available Gemini models...\n")

url = f'https://generativelanguage.googleapis.com/v1beta/models?key={GOOGLE_API_KEY}'

try:
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        
        print(f"✅ Found {len(models)} models:\n")
        
        for model in models:
            name = model.get('name', 'Unknown')
            display_name = model.get('displayName', 'No display name')
            supported_methods = model.get('supportedGenerationMethods', [])
            
            if 'generateContent' in supported_methods:
                print(f"✅ {name}")
                print(f"   Display: {display_name}")
                print(f"   Methods: {', '.join(supported_methods)}\n")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {str(e)}")
