import os
from dotenv import load_dotenv
from google import genai

# Load env variables
load_dotenv(override=True)

api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERROR: GOOGLE_API_KEY not found in environment.")
    exit(1)

print(f"🔑 API Key found: {api_key[:5]}...{api_key[-5:]}")
print("🔄 Testing access to 'gemini-2.5-flash-image'...")

try:
    client = genai.Client(api_key=api_key)
    
    # Simple generation test
    response = client.models.generate_content(
        model='gemini-2.5-flash-image',
        contents='Test'
    )
    print("✅ SUCCESS: Model accessed successfully!")
    print(f"📝 Response: {response.text if response.text else 'No text'}")

except Exception as e:
    print("\n❌ FAILED: Could not access model.")
    print(f"Error details: {e}")
    
    if "403" in str(e):
        print("\n[Analysis] 403 Forbidden: API 키는 유효하지만, 이 모델(Gemini 2.5)에 대한 사용 권한이 없습니다.")
    elif "404" in str(e):
        print("\n[Analysis] 404 Not Found: 모델명을 찾을 수 없습니다.")
    elif "400" in str(e):
        print("\n[Analysis] 400 Bad Request: 요청 형식이 잘못되었습니다.")
