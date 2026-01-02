from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from supabase import create_client, Client

# Enable CORS for frontend
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(override=True)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000", # Just in case
        "https://dfwvt.vercel.app",  # Production Vercel App
        "https://dfwvt-frontend.vercel.app" # Alternate Vercel Domain format
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from genai_client import GenAIClient
from simulator import Simulator
from feedback_engine import FeedbackEngine
from pydantic import BaseModel
from typing import Dict, Any
import random

genai_client = GenAIClient()
simulator = Simulator()
feedback_engine = FeedbackEngine()

class FeedbackRequest(BaseModel):
    student_response: Dict[str, str]
    stage: str

# 개념기반탐구수업을 위한 다양한 탐구 주제 시나리오
INQUIRY_SCENARIOS = [
    # 1. 자연의 신비와 생태계 (Nature's Mysteries & Ecosystems)
    "A close-up of a spider web covered in morning dew, capturing a small insect, with the spider approaching",
    "A cross-section of an ant colony underground showing queen, workers, and larvae in different chambers",
    "A hermit crab using a colorful discarded plastic bottle cap as its shell on a sandy beach",
    "Time-lapse style image showing a seedling pushing through cracked asphalt in a city street",
    "A chameleon changing colors to match a vibrant tropical flower, halfway through the transformation",
    "A large dead whale on the ocean floor (Whale Fall) becoming a feast for crabs, worms, and other deep-sea creatures",
    "A Venus flytrap capturing a fly, showing the trigger hairs and the closing mechanism",
    "Symbiosis: A small bird cleaning the teeth of a crocodile with its mouth open wide",

    # 2. 인간과 환경 (Human Impact & Environment)
    "A solitary polar bear standing on a small, melting iceberg in a vast blue ocean",
    "A forest after a wildfire, showing green sprouts emerging from blackened soil (regeneration)",
    "A beach cleanup scene showing piles of plastic waste sorted by color, with animals nearby",
    "A futuristic vertical garden skyscraper in a dense smoggy city, acting as a 'green lung'",
    "A turtle swimming in the ocean mistaking a floating plastic bag for a jellyfish",
    "Traditional rice terraces on a steep mountain side, showing ancient farming engineering",
    "A drone pollinating a field of sunflowers because real bees are absent",
    "A massive dam holding back a river, showing the difference in water levels and ecosystem on both sides",

    # 3. 과학적 현상과 원리 (Scientific Phenomena)
    "A glass of water freezing in real-time, showing ice crystals forming from the edges inward",
    "A prism splitting a beam of white light into a rainbow in a dark room with dust motes visible",
    "Iron filings forming distinct magnetic field lines around a bar magnet on a white paper",
    "A volcano erupting with lightning strikes visible within the ash cloud (volcanic lightning)",
    "A magnified snowflake showing intricate, perfect hexagonal symmetry on a dark wool glove",
    "A balloon sticking to a cat's fur due to static electricity, with fur standing up",
    "The Milky Way galaxy visible clearly above a light-polluted city skyline (contrast)",
    "A rusty bicycle chain next to a shiny new one, showing oxidation and wear over time",

    # 4. 사회와 문화, 역사 (Society, Culture & History)
    "A split image showing a classroom from 100 years ago vs. a modern VR-based classroom",
    "People from diverse cultures holding hands, showing detailed traditional clothing and henna/tattoos",
    "An abandoned amusement park reclaimed by nature, with vines growing over a rollercoaster",
    "A busy traditional market in a developing country with spices, livestock, and modern smartphones visible",
    "A child in a remote village reading a book by the light of a solar-powered lamp",
    "Ancient cave paintings showing animals, next to a modern graffiti artist's work on a city wall",
    "Robots working alongside humans on a car assembly line, showing cooperation",

    # 5. 의외성과 호기심 자극 (Ambiguity & Curiosity)
    "An old door standing alone in the middle of a meadow, not attached to any building",
    "A library where books are flying off the shelves like birds (magical realism/metaphor)",
    "A giant footprint in the mud that doesn't match any known animal, with researchers measuring it",
    "A clock melting over a tree branch (inspired by Dali) but in a realistic photo style",
    "A ladder reaching up into the clouds with no visible top",
    "A fishbowl with the ocean inside it, sitting on a dry desert dune",
    "Shadows of people on a wall that are doing something different than the people casting them"
]

@app.get("/")
def read_root():
    return {"message": "Data Flywheel Pilot Backend is running!"}

@app.get("/generate-session")
def generate_session():
    # 랜덤하게 탐구 시나리오 선택
    selected_scenario = random.choice(INQUIRY_SCENARIOS)
    
    # 교육적 탐구를 유도하는 상세한 프롬프트 생성
    image_prompt = f"""
    Create a vivid, photo-realistic educational photograph: {selected_scenario}
    
    Style: High-quality educational photography, clear details, natural lighting
    Purpose: To spark curiosity and inquiry in elementary students
    Mood: Engaging, thought-provoking, inviting observation and questions
    Composition: Clear focal point with interesting details to discover
    Quality: Sharp, colorful, suitable for See-Think-Wonder thinking routine
    """
    
    print(f"[SESSION] Selected inquiry scenario: {selected_scenario}")
    image_url = genai_client.generate_image(image_prompt)
    
    # 학생 응답도 선택된 시나리오 기반으로 생성
    student_response = simulator.generate_stw_response(visual_context=selected_scenario)
    
    return {
        "image_url": image_url,
        "student_response": student_response,
        "scenario": selected_scenario  # 어떤 시나리오가 선택되었는지 반환
    }

@app.post("/generate-feedback")
async def generate_feedback(request: FeedbackRequest):
    feedbacks = await feedback_engine.generate_feedback_for_stage(
        student_response=request.student_response,
        stage=request.stage
    )
    return {"feedbacks": feedbacks}

# Data Flywheel Storage Implementation
class TeacherEval(BaseModel):
    score: int
    comment: str = ""

class ModelFeedback(BaseModel):
    model_id: str
    feedback_text: str

# 각 단계(See, Think, Wonder)별 평가 데이터 구조
class TeacherEval(BaseModel):
    score: int
    comment: str = ""
    feedback_text: str = "" # Added feedback text field

class SubmitRequest(BaseModel):
    session_id: str
    image_url: str
    student_response: Dict[str, str] # {see, think, wonder}
    scenario: str
    evaluations: Dict[str, Dict[str, Dict[str, Any]]] 
    # Structure: { 
    #   "See": { "gpt-4o": {score: 9, comment: "..", feedback_text: ".."}, ... },
    # }

@app.post("/submit-evaluation")
async def submit_evaluation(request: SubmitRequest):
    print(f"[DATA] Submitting session {request.session_id}")
    
    final_image_url = request.image_url

    # 0. Image Upload to Supabase Storage (Optional)
    # User requested to skip storage upload and use local URL/Path as data reference.
    # This is valid for Data Flywheel as 'scenario' text serves as the grounding context.
    
    # if request.image_url.startswith("/generated/"):
    #     try:
    #         filename = request.image_url.split("/")[-1]
    #         # ... upload logic ...
    #         # (Disabled for Local-Only Mode)
    #     except ...
    
    # Just use the incoming URL (local path) or Base64
    final_image_url = request.image_url
    
    # [FIX] Prevent saving massive Base64 strings to DB (causes 500 Error)
    if final_image_url and final_image_url.startswith("data:image"):
        print("[INFO] Base64 image detected. Replacing with placeholder for DB storage.")
        final_image_url = "(Base64 Image Data - Not Stored in DB to prevent payload overflow)"

    try:
        # 1. Save Session Data
        session_data = {
            "session_id": request.session_id,
            "scenario_text": request.scenario,
            "image_url": final_image_url, # Use the uploaded URL or original
            "student_response_see": request.student_response.get('see', ''),
            "student_response_think": request.student_response.get('think', ''),
            "student_response_wonder": request.student_response.get('wonder', '')
        }
        
        # Save to Supabase 'flywheel_sessions'
        supabase.table("flywheel_sessions").insert(session_data).execute()

        # 2. Save Evaluations
        eval_records = []
        
        for stage, models_evals in request.evaluations.items():
            if not models_evals: continue
            
            for model_id, eval_data in models_evals.items():
                # Safe casting for score
                raw_score = eval_data.get('score', 0)
                if raw_score is None:
                    raw_score = 0
                try:
                    score_val = int(raw_score)
                except (ValueError, TypeError):
                    score_val = 0

                record = {
                    "session_id": request.session_id,
                    "routine_step": stage.lower(),
                    "model_id": model_id,
                    "feedback_content": eval_data.get('feedback_text', 'No content provided'), 
                    "teacher_score": score_val,
                    "teacher_comment": eval_data.get('comment', '')
                }
                eval_records.append(record)
        
        print(f"[DEBUG] Prepared {len(eval_records)} evaluation records for insertion")
        
        if eval_records:
            try:
                response = supabase.table("flywheel_evaluations").insert(eval_records).execute()
                print(f"[SUCCESS] Saved {len(eval_records)} evaluation records. Response: {response}")
            except Exception as e:
                print(f"[ERROR] Failed to insert evaluations: {e}")
                # We do not re-raise immediately to avoid 500 if session was saved.
                # But partial failure is bad. Let's return warning.
                return {"status": "partial_success", "warning": f"Evaluations failed: {str(e)}", "image_url": final_image_url}
                
        return {"status": "success", "records_saved": len(eval_records), "image_url": final_image_url}

    except Exception as e:
        print(f"[ERROR] Submit failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
