"""
GenAI Client for Image Generation using Gemini 2.5 Flash
"""
import os
from google import genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv(override=True)

class GenAIClient:
    def __init__(self):
        # Using Gemini 2.5 Flash for image generation
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model = 'gemini-2.5-flash-image'

    def generate_image(self, prompt: str) -> str:
        """
        Generates an image from a prompt using Gemini 2.5 Flash.
        Returns the relative path to the saved image or a placeholder URL.
        """
        try:
            print(f"[IMAGE] Generating with Gemini 2.5 Flash: {prompt}")
            
            # Use Gemini 2.5 Flash for image generation
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt]
            )
            
            # Process response parts to find the image
            for part in response.parts:
                if part.text is not None:
                    print(f"[INFO] Model response text: {part.text[:100]}...")
                elif part.inline_data is not None:
                    # Deployment Friendly: Return Base64 directly
                    # Eliminated disk write to allow serverless deployment without storage bucket
                    import base64
                    
                    # 'part.inline_data.data' contains the raw bytes
                    image_bytes = part.inline_data.data
                    b64_string = base64.b64encode(image_bytes).decode('utf-8')
                    
                    # Construct data URL
                    data_url = f"data:image/png;base64,{b64_string}"
                    
                    print(f"[OK] Image generated as Base64 (Length: {len(data_url)})")
                    return data_url
            
            # If no image was generated
            print("[WARN] No image found in response parts")
            return "https://placehold.co/600x400/4f46e5/ffffff?text=No+Image+Generated"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[ERROR] Image generation failed: {e}")
            return "https://placehold.co/600x400/ef4444/ffffff?text=Image+Generation+Error"

if __name__ == "__main__":
    client = GenAIClient()
    print("GenAI Client Initialized with Gemini 2.5 Flash")
