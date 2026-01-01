"""
GenAI Client for Image Generation using Gemini 2.5 Flash (Nano Banana)
Reference: https://ai.google.dev/gemini-api/docs/image-generation
"""
import os
import io
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

class GenAIClient:
    def __init__(self):
        # Using Gemini 2.5 Flash Image (aka Nano Banana) for image generation
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model = 'gemini-2.5-flash-image'

    def generate_image(self, prompt: str) -> str:
        """
        Generates an image from a prompt using Gemini 2.5 Flash Image (Nano Banana).
        Returns the relative path to the saved image or a placeholder URL.
        """
        try:
            print(f"[IMAGE] Generating with Gemini 2.5 Flash: {prompt}")
            
            # Use Gemini 2.5 Flash Image (Nano Banana) - exact API from documentation
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt]
            )
            
            # Process response parts to find the image
            for part in response.parts:
                if part.text is not None:
                    print(f"[INFO] Model response text: {part.text[:100]}...")
                elif part.inline_data is not None:
                    # Convert to PIL Image and save
                    image = part.as_image()
                    
                    filename = f"generated_{os.urandom(4).hex()}.png"
                    directory = os.path.join(os.path.dirname(__file__), "../frontend/public/generated")
                    os.makedirs(directory, exist_ok=True)
                    
                    filepath = os.path.join(directory, filename)
                    image.save(filepath)
                    
                    print(f"[OK] Image generated and saved to: {filepath}")
                    return f"/generated/{filename}"
            
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
