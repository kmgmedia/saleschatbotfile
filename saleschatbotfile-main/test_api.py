"""
Quick test to verify Google Gemini API is working with new key
"""
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Google Gemini API with new key"""
    
    print("\n🧪 Testing Google Gemini API...")
    print("=" * 50)
    
    # Get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in .env file!")
        return False
    
    print(f"✓ API Key found: {api_key[:20]}...")
    
    # Test with a simple prompt
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}'
    
    headers = {'Content-Type': 'application/json'}
    
    data = {
        'contents': [{
            'parts': [{
                'text': 'Say hello and introduce yourself as Alex, a friendly sales assistant!'
            }]
        }],
        'generationConfig': {
            'temperature': 0.7,
            'maxOutputTokens': 200
        }
    }
    
    try:
        print("\n📡 Sending request to Gemini API...")
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract response text
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0].get('content', {})
                parts = content.get('parts', [])
                
                if parts and len(parts) > 0:
                    reply = parts[0].get('text', '').strip()
                    
                    print("\n✅ SUCCESS! Google Gemini API is working!\n")
                    print("=" * 50)
                    print("🤖 Alex's Response:")
                    print("=" * 50)
                    print(reply)
                    print("=" * 50)
                    print("\n✨ Your new API key is working perfectly!")
                    print("\n🎯 Next step: Test on Telegram @Store_help_bot\n")
                    return True
                else:
                    print("\n❌ No text in response")
                    print(f"Response: {result}")
                    return False
            else:
                print("\n❌ No candidates in response")
                print(f"Response: {result}")
                return False
                
        elif response.status_code == 400:
            print("\n❌ Bad Request - Check API key format")
            print(f"Response: {response.text}")
            return False
            
        elif response.status_code == 403:
            print("\n❌ API Key Invalid or Restricted")
            print("   Make sure:")
            print("   1. API key is correct")
            print("   2. API key has Gemini API enabled")
            print(f"   Response: {response.text}")
            return False
            
        elif response.status_code == 404:
            print("\n❌ Model not found - Check model name")
            print(f"Response: {response.text}")
            return False
            
        else:
            print(f"\n❌ Unexpected error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n❌ Request timed out - Check internet connection")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    
    if success:
        print("\n🎉 All systems go! Your bot is ready to use Google Gemini!\n")
    else:
        print("\n⚠️  Fix the issues above and try again.\n")
