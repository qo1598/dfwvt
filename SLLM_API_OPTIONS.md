# 🚀 sLLM API 옵션 - 웹 배포용

> **목적**: 연구용 sLLM을 API로 빠르게 사용  
> **요구사항**: 온라인 배포, API 방식, 안정적

---

## 🎯 추천 옵션 (우선순위순)

### Option 1: HuggingFace Serverless Inference API ⭐⭐⭐ (최고 추천)

**개요**:
- HuggingFace의 무료/유료 Inference API
- Gemma, Llama, Mistral 등 다양한 sLLM 지원
- GPU 서버에서 실행되어 빠름

**장점**:
- ✅ **설정 간단**: API 키만 있으면 됨
- ✅ **배포 용이**: 서버리스, 인프라 관리 불필요
- ✅ **비용 효율**: 무료 티어 + 종량제
- ✅ **다양한 모델**: Gemma 2B, 7B, Llama 3.1 등
- ✅ **안정성**: HuggingFace 관리

**사용 가능 sLLM**:
- `google/gemma-2-2b-it` (2B - 매우 빠름)
- `google/gemma-2-9b-it` (9B - 균형)
- `meta-llama/Llama-3.2-3B-Instruct` (3B)
- `mistralai/Mistral-7B-Instruct-v0.3` (7B)

**코드 예시**:
```python
from huggingface_hub import InferenceClient

client = InferenceClient(token=os.environ.get("HUGGINGFACE_API_KEY"))

response = client.chat_completion(
    model="google/gemma-2-2b-it",  # sLLM
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    max_tokens=300,
    temperature=0.7
)
```

**비용**:
- 무료 티어: 매일 일정량 무료
- 유료: $0.06 / 1K tokens (GPT-4o보다 훨씬 저렴)

---

### Option 2: Together AI ⭐⭐⭐ (강력 추천)

**개요**:
- 오픈소스 LLM 전문 API 플랫폼
- 매우 빠른 추론 속도
- 다양한 sLLM 지원

**장점**:
- ✅ **매우 빠름**: 최적화된 추론
- ✅ **저렴한 비용**: sLLM은 거의 무료 수준
- ✅ **안정적**: 프로덕션 레벨
- ✅ **간단한 API**: OpenAI와 유사

**사용 가능 sLLM**:
- `meta-llama/Llama-3.2-3B-Instruct`
- `google/gemma-2-2b-it`
- `mistralai/Mistral-7B-Instruct-v0.3`

**코드 예시**:
```python
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

response = client.chat.completions.create(
    model="meta-llama/Llama-3.2-3B-Instruct",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    max_tokens=300,
    temperature=0.7
)
```

**비용**:
- Llama 3.2 3B: $0.06 / 1M tokens (매우 저렴!)
- Gemma 2 2B: $0.05 / 1M tokens

---

### Option 3: Groq API ⭐⭐⭐ (속도 최고)

**개요**:
- 초고속 LLM 추론 플랫폼
- LPU (Language Processing Unit) 사용
- 무료 티어 제공

**장점**:
- ✅ **초고속**: 600+ tokens/sec
- ✅ **무료 티어**: 하루 14,400 requests
- ✅ **안정적**: 엔터프라이즈급
- ✅ **OpenAI 호환**: 동일한 인터페이스

**사용 가능 sLLM**:
- `llama-3.2-3b-preview`
- `gemma-7b-it`
- `mixtral-8x7b-32768`

**코드 예시**:
```python
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.2-3b-preview",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    max_tokens=300,
    temperature=0.7
)
```

**비용**:
- 무료 티어: 14,400 requests/day
- 유료: $0.05 / 1M tokens

---

### Option 4: Replicate API ⭐⭐

**개요**:
- 다양한 ML 모델 호스팅 플랫폼
- Pay-per-use 모델

**장점**:
- ✅ **다양한 모델**: 수백 개 선택 가능
- ✅ **사용한 만큼 지불**
- ✅ **커뮤니티 모델**: 최신 모델 빠르게 추가

**사용 가능 sLLM**:
- Gemma 2B, 7B
- Llama 3.1 8B
- Mistral 7B

---

## 📊 비교표

| 플랫폼 | 모델 종류 | 속도 | 비용 | 무료 티어 | 안정성 | 추천도 |
|--------|----------|------|------|-----------|--------|--------|
| **HuggingFace** | 매우 다양 | 빠름 | 저렴 | ✅ | 높음 | ⭐⭐⭐ |
| **Together AI** | 다양 | 매우 빠름 | 매우 저렴 | ✅ | 높음 | ⭐⭐⭐ |
| **Groq** | 제한적 | 초고속 | 저렴 | ✅ 관대 | 높음 | ⭐⭐⭐ |
| **Replicate** | 매우 다양 | 보통 | 보통 | ❌ | 보통 | ⭐⭐ |

---

## 🎯 최종 추천

### 연구 목적 최적 조합:

**세 번째 모델로 사용할 sLLM**:

#### 추천 1: **Groq API + Llama 3.2 3B** (최고 추천)
```python
# 이유:
✅ 무료 티어 관대 (14,400 requests/day)
✅ 초고속 (연구 참여자 대기 시간 단축)
✅ OpenAI와 동일한 인터페이스 (코드 변경 최소)
✅ 안정적
✅ Llama 3.2 3B는 품질 우수한 sLLM
```

#### 추천 2: **Together AI + Gemma 2 2B**
```python
# 이유:
✅ 매우 저렴 ($0.05 / 1M tokens)
✅ 빠른 속도
✅ Gemma는 연구에서 많이 사용됨
✅ 안정적
```

---

## 💻 구현 방법

### Groq API 적용 (권장)

**1. 라이브러리 설치**:
```bash
pip install groq
```

**2. 환경 변수 추가** (`.env`):
```env
GROQ_API_KEY=your_groq_api_key_here
```

**3. 코드 수정** (`feedback_engine.py`):
```python
from groq import Groq

class FeedbackEngine:
    def __init__(self):
        # ... 기존 코드 ...
        
        # 3. Groq (Llama 3.2 3B - sLLM)
        self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.sllm_model = "llama-3.2-3b-preview"
    
    async def _get_sllm_feedback(self, system_prompt: str, user_prompt: str) -> str:
        """
        Uses Llama 3.2 3B via Groq API (sLLM for research).
        Ultra-fast inference with free tier.
        """
        try:
            # Groq는 동기 API만 제공, executor 사용
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, 
                self._groq_sync_call, 
                system_prompt, 
                user_prompt
            )
        except Exception as e:
            return f"[ERROR] Llama 3.2 3B (Groq): {str(e)}"
    
    def _groq_sync_call(self, system_prompt: str, user_prompt: str) -> str:
        response = self.groq_client.chat.completions.create(
            model=self.sllm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
```

**4. 피드백 목록 업데이트**:
```python
tasks = [
    self._get_openai_feedback(base_system_prompt, user_prompt, model="gpt-4o"),
    self._get_anthropic_feedback(base_system_prompt, user_prompt),
    self._get_sllm_feedback(base_system_prompt, user_prompt)  # sLLM
]

return [
    {"model_id": "gpt-4o", "model_name": "GPT-4o (OpenAI)", ...},
    {"model_id": "claude-sonnet-4", "model_name": "Claude Sonnet 4 (Anthropic)", ...},
    {"model_id": "llama-3.2-3b", "model_name": "Llama 3.2 3B (sLLM)", ...}
]
```

---

## 📈 연구 목적 장점

### sLLM 포함의 연구적 가치:

1. **모델 크기 비교**:
   - Large (GPT-4o): 175B+
   - Large (Claude Sonnet 4): 100B+
   - **Small (Llama 3.2 3B): 3B** ⭐

2. **비용-성능 분석**:
   - 교육 피드백에서 sLLM 효과성 검증
   - Data Flywheel의 sLLM 개선 효과 측정

3. **실용성**:
   - 저비용 배포 가능성
   - 교육 현장 적용 가능성

4. **논문 기여**:
   - "sLLM도 적절한 피드백 제공 가능" 입증
   - Data Flywheel로 sLLM 성능 향상 측정

---

## 🚀 빠른 시작 가이드

### Step 1: API 키 발급
```
Groq (추천): https://console.groq.com
→ Sign up (무료)
→ API Keys → Create API Key
→ 복사
```

### Step 2: 환경 변수 설정
```bash
# backend/.env에 추가
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxx
```

### Step 3: 코드 적용
```bash
# 제가 수정해드릴 수 있습니다!
# 말씀만 해주세요.
```

### Step 4: 테스트
```bash
cd backend
python test_sllm.py  # 테스트 스크립트 생성
```

---

## 💰 예상 비용 (웹 배포 시)

### 세션당 비용 비교:

| 모델 | 역할 | 토큰/세션 | 비용/세션 |
|------|------|-----------|-----------|
| Gemini 2.5 Flash | 이미지 | - | $0.00-0.04 |
| GPT-4o | 피드백 #1 | ~500 | $0.02 |
| Claude Sonnet 4 | 피드백 #2 | ~500 | $0.015 |
| **Llama 3.2 3B (Groq)** | **피드백 #3** | **~500** | **$0.00003** ⭐ |
| Gemini 1.5 Flash | 학생 응답 | ~300 | $0.001 |
| **총계** | - | - | **$0.076** |

**Groq 무료 티어로는 하루 약 4,800 세션 가능!**

---

## ✅ 최종 추천

### 🎯 **Groq API + Llama 3.2 3B**

**이유**:
1. ✅ 무료 티어로 충분한 연구 가능
2. ✅ 초고속 (참여자 경험 개선)
3. ✅ API 방식 (배포 간단)
4. ✅ 안정적 (프로덕션 레벨)
5. ✅ Llama 3.2 3B는 성능 좋은 sLLM
6. ✅ OpenAI와 동일한 인터페이스

**연구 논문 기여**:
- "3B 파라미터 sLLM의 교육 피드백 품질 평가"
- "Data Flywheel을 통한 sLLM 성능 향상"
- "비용 효율적인 AI 교육 피드백 시스템"

---

## 🎊 결론

**지금 바로 적용 가능한 솔루션**:
- Groq API 키만 발급받으면 5분 만에 적용 가능
- 무료 티어로 전체 연구 진행 가능
- 웹 배포 시에도 매우 저렴한 비용

**말씀만 해주시면 바로 적용해드리겠습니다!**

---

**작성**: AI Assistant  
**날짜**: 2025-12-12  
**추천**: 🚀 Groq API + Llama 3.2 3B


