"""
Quick test script to verify Google Gemini API is working
"""
import requests

# Your Google API Key
GOOGLE_API_KEY = "AIzaSyDQ2afqPxDw5FkSfkRTcolG2oIzXRJ6zJs"

def test_gemini():
    """Test Google Gemini API"""
    
    print("🧪 Testing Google Gemini API...\n")
    
    # Simple test prompt
    test_message = "Hello! Tell me about smartwatches in a friendly way."
    
    # Using Gemini 2.5 Flash - fast and reliable
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}'
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        'contents': [{
            'parts': [{
                'text': f"You are Alex, a friendly 7-year sales expert. {test_message}"
            }]
        }],
        'generationConfig': {
            'temperature': 0.7,
            'maxOutputTokens': 1024,  # Increased for Gemini 2.5 thinking tokens
            'topP': 0.8,
            'topK': 40
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Full response: {result}\n")
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0].get('content', {})
                parts = content.get('parts', [])
                if parts and len(parts) > 0:
                    reply = parts[0].get('text', '').strip()
                    print(f"\n✅ SUCCESS! Gemini 2.5 Flash is working!\n")
                    print(f"📝 Response:\n{reply}\n")
                    return True
                else:
                    print(f"❌ No parts in content")
                    return False
            else:
                print(f"❌ No candidates in response")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini()
