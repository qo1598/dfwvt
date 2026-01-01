"""
Quick test script to verify Gemini API connection
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("[TEST] Testing Gemini API...")
print(f"API Key exists: {bool(os.environ.get('GOOGLE_API_KEY'))}")

try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # List available models
    print("\n[MODELS] Available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
    
    # Test simple generation
    print("\n[GENERATE] Testing simple generation...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello' in Korean")
    print(f"[SUCCESS] Response: {response.text}")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

