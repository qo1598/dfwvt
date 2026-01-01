"""
Feedback Engine for Multi-LLM Comparison

Uses three LLMs:
1. GPT-4o (OpenAI)
2. Claude Sonnet 4 (Anthropic)
3. Gemma 3 4B (NVIDIA NIM API)
"""
import os
import asyncio
from typing import List, Dict
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import aiohttp

class FeedbackEngine:
    def __init__(self):
        # 1. OpenAI (GPT-4o)
        self.openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # 2. Anthropic (Claude Sonnet 4)
        # Explicitly pass API key to avoid authentication issues
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        if not anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        self.anthropic_client = AsyncAnthropic(api_key=anthropic_key)
        self.claude_model = "claude-sonnet-4-20250514"
        
        # 3. NVIDIA NIM API (Gemma 3 4B)
        print("[INFO] Initializing NVIDIA NIM API for Gemma 3...")
        self.nvidia_api_key = os.environ.get("NVIDIA_API_KEY")
        if not self.nvidia_api_key:
            print("[WARN] NVIDIA_API_KEY not set, Gemma 3 will not be available")
        self.nvidia_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.gemma_model = "google/gemma-3n-e4b-it"
        print(f"[OK] NVIDIA NIM API initialized with model: {self.gemma_model}")

    async def _get_openai_feedback(self, system_prompt: str, user_prompt: str, model: str = "gpt-4o") -> str:
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[ERROR] OpenAI {model}: {str(e)}"

    async def _get_anthropic_feedback(self, system_prompt: str, user_prompt: str) -> str:
        """
        Uses Claude Sonnet 4 (latest version as of May 2025).
        Reference: https://console.anthropic.com/docs/en/get-started
        """
        try:
            response = await self.anthropic_client.messages.create(
                model=self.claude_model,  # claude-sonnet-4-20250514
                max_tokens=300,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"[ERROR] Claude Sonnet 4: {str(e)}"

    async def _get_gemma_feedback(self, system_prompt: str, user_prompt: str) -> str:
        """
        Uses Gemma 3 4B via NVIDIA NIM API.
        Reference: https://docs.api.nvidia.com/nim/reference/google-gemma-3n-e4b-it
        """
        if not self.nvidia_api_key:
            return "[ERROR] Gemma 3: NVIDIA_API_KEY not set"
        
        try:
            headers = {
                "Authorization": f"Bearer {self.nvidia_api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.gemma_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.9,
                "stream": False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.nvidia_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        return f"[ERROR] Gemma 3 (NVIDIA): HTTP {response.status} - {error_text}"
                        
        except asyncio.TimeoutError:
            return "[ERROR] Gemma 3 (NVIDIA): Request timeout"
        except Exception as e:
            return f"[ERROR] Gemma 3 (NVIDIA): {str(e)}"

    async def generate_feedback_for_stage(self, student_response: Dict, stage: str) -> List[Dict]:
        """
        Generates feedback from GPT-4o, Claude Sonnet 4, and Gemma in parallel.
        Uses ultra-minimal prompt to extract pure model capabilities without any guidance.
        """
        student_text = student_response.get(stage, "")
        
        # 극도로 간소화된 프롬프트 - 모델 자체의 판단만 활용
        base_system_prompt = "교사"
        user_prompt = f"""학생 답변: "{student_text}"

피드백(2-3문장):"""
        
        tasks = [
            self._get_openai_feedback(base_system_prompt, user_prompt, model="gpt-4o"),
            self._get_anthropic_feedback(base_system_prompt, user_prompt),
            self._get_gemma_feedback(base_system_prompt, user_prompt)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return [
            {
                "model_id": "gpt-4o",
                "model_name": "GPT-4o (OpenAI)",
                "feedback_text": results[0]
            },
            {
                "model_id": "claude-sonnet-4",
                "model_name": "Claude Sonnet 4 (Anthropic)",
                "feedback_text": results[1]
            },
            {
                "model_id": "gemma-3-4b",
                "model_name": "Gemma 3 4B (NVIDIA NIM)",
                "feedback_text": results[2]
            }
        ]
