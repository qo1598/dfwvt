import json
import logging
import google.generativeai as genai
from pydantic import BaseModel
from typing import Optional, Dict

# Configure GenAI (assumes key is already loaded in env)
# If not, ensure main.py loads .env before importing this

class StudentPersona(BaseModel):
    name: str
    description: str
    literacy_level: str  # e.g., 'Low', 'Medium', 'High'
    tendency: str        # e.g., 'Creative', 'Analytical', 'Observant'

class StudentResponse(BaseModel):
    see: str
    think: str
    wonder: str

class Simulator:
    def __init__(self):
        # Using Gemini 2.5 Flash for speed as the student simulator
        self.model = genai.GenerativeModel('gemini-2.5-flash') 

    def _get_persona_prompt(self, persona: Optional[StudentPersona] = None) -> str:
        if not persona:
            # Default diverse persona generator prompt could go here, 
            # but for now we'll use a generic "Average 5th Grader"
            return "You are a 5th grade student."
        
        return f"""
        You are a student with the following characteristics:
        - Description: {persona.description}
        - Literacy Level: {persona.literacy_level}
        - Tendency: {persona.tendency}
        Act exactly like this student would. Do not sound too academic if the level is low.
        """

    def generate_stw_response(self, visual_context: str, persona: Optional[StudentPersona] = None) -> Dict[str, str]:
        """
        Generates a See-Think-Wonder response based on a text description of the visual.
        (In a full implementation, we would pass the actual image to Gemini Vision).
        
        Task: Perform the 'See-Think-Wonder' (STW) thinking routine.
        If the visual context provided is missing, abstract, or unclear, use your imagination to describe an interesting scene that might be there.
        Output must be a valid JSON object with keys: "see", "think", "wonder".
        
        Language: Korean (한국어).
        Tone: Child-like, simple sentences (e.g., "~해요", "~인 것 같아요").
        """
        
        system_prompt = self._get_persona_prompt(persona)
        
        # Enhanced prompt for better quality responses
        prompt = f"""
        당신은 5학년 학생입니다. 다음 주제에 대해 See-Think-Wonder 활동을 수행하세요.
        
        주제: {visual_context}
        
        중요한 규칙:
        1. 반드시 구체적이고 창의적인 내용을 작성하세요.
        2. "잘 모르겠어요" 같은 회피하는 답변은 금지입니다.
        3. 주제가 불명확하면 "미래 도시의 학교" 또는 "환경 보호" 주제로 상상해서 작성하세요.
        4. 각 항목은 최소 2문장 이상 작성하세요.
        5. 초등학생 말투로 자연스럽게 작성하세요 (~해요, ~것 같아요, ~인가봐요).
        
        JSON 형식으로 답변하세요:
        {{
          "see": "내가 관찰한 것 (구체적으로)",
          "think": "내가 생각한 것 (창의적으로)",
          "wonder": "내가 궁금한 것 (호기심 가득)"
        }}
        """
        
        try:
            response = self.model.generate_content(
                [system_prompt, prompt],
                generation_config={"response_mime_type": "application/json"}
            )
            # The model is configured to output JSON, so direct parsing should work.
            # Basic cleaning if model outputs markdown is no longer strictly needed but kept for robustness.
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "see": "잘 모르겠어요.",
                "think": "뭔가 복잡해보여요.",
                "wonder": "이게 뭘까요?",
                "error": "JSON Parsing Failed"
            }
        except Exception as e:
            print(f"Error generating student response: {e}")
            return {
                "see": "잘 모르겠어요.", 
                "think": "뭔가 복잡해보여요.", 
                "wonder": "이게 뭘까요?",
                "error": str(e)
            }
