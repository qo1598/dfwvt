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
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from genai_client import GenAIClient
from simulator import Simulator
from feedback_engine import FeedbackEngine
from pydantic import BaseModel
from typing import Dict
import random

genai_client = GenAIClient()
simulator = Simulator()
feedback_engine = FeedbackEngine()

class FeedbackRequest(BaseModel):
    student_response: Dict[str, str]
    stage: str

# 개념기반탐구수업을 위한 다양한 탐구 주제 시나리오
INQUIRY_SCENARIOS = [
    # 과학 탐구
    "A butterfly emerging from its chrysalis on a flower in morning sunlight",
    "Ice cubes melting in a glass with condensation on the outside",
    "A shadow changing length throughout the day with the sun's position",
    "Seeds sprouting in different soil types with visible root systems",
    "A rainbow forming in water droplets from a garden hose",
    "Magnets attracting and repelling with iron filings showing field patterns",
    "A candle flame with different colored zones and melting wax",
    "Bubbles floating with swirling rainbow colors reflecting on their surface",
    
    # 환경과 자연
    "A river splitting around a large rock, showing different water speeds",
    "Tree rings visible on a cut log showing years of growth",
    "Footprints of different animals in mud near a watering hole",
    "A bird building a nest with various materials",
    "Leaves changing colors from green to red and yellow in autumn",
    "A spider web covered in morning dew drops sparkling in sunlight",
    "Erosion patterns in soil after rainfall on a hillside",
    "A decomposing log with mushrooms and insects creating new soil",
    
    # 사회와 문화
    "Children from different cultures sharing traditional foods at a table",
    "Old and new buildings standing side by side in a city street",
    "A traditional market with vendors and various goods being exchanged",
    "Different types of homes in various climates around the world",
    "A community garden where neighbors work together planting vegetables",
    "Street art mural being painted showing diverse people and cultures",
    "A library with students reading different types of books and tablets",
    "Different modes of transportation through history displayed together",
    
    # 예술과 창의성
    "Primary colors mixing on a palette creating secondary colors",
    "Musical instruments from around the world arranged in a circle",
    "Recycled materials transformed into creative art sculptures",
    "Light and shadow creating patterns through a decorative window",
    "Natural patterns: spirals in shells, fractals in ferns, symmetry in flowers",
    "A pottery wheel shaping clay into a vessel with hands visible",
    "Origami figures in various stages of folding from paper to final form",
    
    # 수학과 패턴
    "A honeycomb showing perfect hexagonal patterns with bees working",
    "Fruits cut in half revealing symmetrical patterns and seed arrangements",
    "Gears of different sizes interlocking and turning together",
    "A spiral staircase viewed from above showing mathematical curves",
    "Tiles arranged in repeating patterns with different shapes and colors",
    "A spider web showing radial and circular symmetry",
    "Dominoes arranged in a pattern about to create a chain reaction",
    
    # 기술과 혁신
    "Simple machines like pulleys, levers, and wheels working together",
    "A wind turbine generating power near a field of flowers",
    "Solar panels on a school roof with students observing nearby",
    "A 3D printer creating an object layer by layer",
    "Robots and humans working together in a collaborative space",
    "Traditional tools and modern tools displayed side by side for comparison",
    "A bicycle showing all its mechanical parts and how they connect",
    
    # 생태계와 관계
    "A food chain illustrated: sun, plant, caterpillar, bird, and fox",
    "Bees pollinating flowers with pollen visible on their legs",
    "A tide pool ecosystem with various sea creatures coexisting",
    "Earthworms aerating soil with cross-section view showing tunnels",
    "A bird feeding its chicks in a nest with parent bringing insects",
    "Different animals drinking from the same watering hole peacefully",
    "A compost bin showing food scraps transforming into rich soil",
    
    # 건강과 신체
    "Healthy foods arranged as a rainbow with different colored fruits and vegetables",
    "Children playing different sports showing various movements and teamwork",
    "A human heart model with blood vessels clearly visible and labeled",
    "Teeth before and after brushing showing the importance of hygiene",
    "Different exercises strengthening different muscle groups illustrated",
    "A balanced meal with portions of grains, proteins, vegetables and fruits",
    
    # 날씨와 기후
    "Different types of clouds in the sky at various heights",
    "The water cycle illustrated in nature: ocean, clouds, rain, river",
    "A thermometer showing temperature change from hot to cold",
    "Wind making different effects: moving leaves, flying kite, bending grass",
    "Snow crystals with unique patterns magnified showing their six-sided structure",
    "Lightning striking during a storm with dark clouds and rain",
    
    # 물질과 변화
    "Water in three states: ice, liquid water, and steam from boiling",
    "Rust forming on metal showing chemical change over time",
    "Bread dough rising in a bowl showing fermentation process",
    "A burning log showing solid wood turning to ash and smoke",
    "Salt dissolving in water becoming invisible solution",
    "A frozen banana that has turned brown showing chemical change"
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
