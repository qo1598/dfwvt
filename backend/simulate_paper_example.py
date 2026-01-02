
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add backend directory to sys.path
sys.path.append(os.path.dirname(__file__))

from genai_client import GenAIClient
from simulator import Simulator
from feedback_engine import FeedbackEngine

# Load Environment Variables
load_dotenv(override=True)

async def run_simulation():
    print("--- [Paper Example Simulation Start] ---")
    
    # 1. Define Scenario (Environmental Pollution)
    scenario_text = "A photo of a sea turtle swimming underwater, approaching a floating plastic bag that resembles a jellyfish."
    print(f"\n[1. Scenario]: {scenario_text}")
    
    # 2. Generate Image
    print("\n[2. Generating Image...]")
    genai_client = GenAIClient()
    # Note: genai_client.generate_image now returns Base64 data URL
    image_url = genai_client.generate_image(scenario_text)
    print(f"Image Generated: {image_url[:50]}... (Base64 Truncated)")
    
    # 3. Generate Student Response (Persona: 12-year-old curious student)
    print("\n[3. Simulating Student Response...]")
    simulator = Simulator()
    # We pass a dummy 'image_url' because the simulator (GPT-4o) actually takes the text description 
    # or the image url. In the current implementation of `simulator.py`, let's check input.
    # It takes (visual_context).
    
    student_response = simulator.generate_stw_response(scenario_text)
    print(f"Student See: {student_response['see']}")
    print(f"Student Think: {student_response['think']}")
    print(f"Student Wonder: {student_response['wonder']}")
    
    # 4. Generate AI Feedbacks (Multi-LLM)
    print("\n[4. Generating Multi-LLM Feedbacks...]")
    feedback_engine = FeedbackEngine()
    
    # We will generate feedback for the 'Wonder' stage as the representative example
    target_stage = 'wonder'
    feedbacks = await feedback_engine.generate_feedback_for_stage(student_response, target_stage)
    
    print(f"\n--- [Results for Stage: {target_stage.upper()}] ---")
    for fb in feedbacks:
        print(f"\n[Model: {fb['model_id']}]")
        print(f"Feedback: {fb['feedback_text']}")
        
    print("\n--- [Simulation Complete] ---")

if __name__ == "__main__":
    asyncio.run(run_simulation())
