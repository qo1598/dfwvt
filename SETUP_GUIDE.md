# Data Flywheel Platform - 설정 가이드 🚀

## 📋 설치 완료 상태

✅ **백엔드 의존성**: 모두 설치됨  
✅ **프론트엔드 의존성**: 모두 설치됨  
✅ **백엔드 서버**: 정상 실행 중 (http://localhost:8000)  
✅ **프론트엔드 서버**: 정상 실행 중 (http://localhost:5173)  

---

## ⚠️ 환경 변수 설정 필요

백엔드가 정상적으로 작동하려면 `backend/.env` 파일에 API 키를 설정해야 합니다.

### 1️⃣ backend/.env 파일 생성

`backend` 폴더에 `.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
# Access Control
ACCESS_CODE=PILOT2025

# Google Cloud (Imagen 3 이미지 생성용)
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI (GPT-4o, GPT-4o-mini 피드백 생성용)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (Claude 3.5 Sonnet 피드백 생성용)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Supabase (데이터베이스)
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

---

## 🔑 API 키 발급 방법

### Google Cloud (Imagen 3)
1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. "Create API Key" 클릭
3. 생성된 키를 `GOOGLE_API_KEY`에 입력
4. **중요**: Generative AI API 활성화 필요

### OpenAI (GPT-4o / GPT-4o-mini)
1. [OpenAI Platform](https://platform.openai.com/api-keys) 접속
2. "Create new secret key" 클릭
3. 생성된 키를 `OPENAI_API_KEY`에 입력
4. **비용**: GPT-4o는 유료, GPT-4o-mini는 저렴

### Anthropic (Claude 3.5 Sonnet)
1. [Anthropic Console](https://console.anthropic.com/) 접속
2. API Keys → "Create Key" 클릭
3. 생성된 키를 `ANTHROPIC_API_KEY`에 입력

### Supabase (데이터베이스)
1. [Supabase Dashboard](https://supabase.com/dashboard) 접속
2. 새 프로젝트 생성
3. Settings → API에서 URL과 anon/public 키 복사
4. `SUPABASE_URL`과 `SUPABASE_KEY`에 입력

---

## 🧪 테스트 방법

### 1. 환경 변수 설정 후 백엔드 재시작

```powershell
# 현재 실행 중인 서버 종료 (Ctrl+C)
cd backend
python -m uvicorn main:app --reload
```

### 2. API 테스트

```powershell
# 루트 엔드포인트 테스트
Invoke-WebRequest -Uri http://localhost:8000/ -UseBasicParsing

# 세션 생성 테스트 (환경 변수 설정 후)
$headers = @{'x-access-code' = 'PILOT2025'}
Invoke-WebRequest -Uri 'http://localhost:8000/generate-session?topic=environment' -Headers $headers -Method GET -UseBasicParsing
```

### 3. 프론트엔드 접속

브라우저에서 http://localhost:5173 접속

---

## 🎯 최소 요구사항

전체 플랫폼을 실행하려면 **최소한 다음이 필요**합니다:

1. ✅ **OPENAI_API_KEY** (필수) - GPT-4o, GPT-4o-mini 사용
2. ✅ **GOOGLE_API_KEY** (필수) - Imagen 3 이미지 생성
3. ⚠️ **ANTHROPIC_API_KEY** (선택) - Claude 피드백 (없어도 GPT만으로 작동 가능)
4. ⚠️ **SUPABASE_URL/KEY** (선택) - 현재 코드에서는 연결만 하고 실제 저장은 안 함

---

## 🔧 비용 절감 옵션

### OpenAI만 사용하고 싶다면?

`backend/feedback_engine.py`를 수정하여 Claude를 제거할 수 있습니다:

```python
# 3개 모델 대신 2개만 사용
tasks = [
    self._get_openai_feedback(base_system_prompt, user_prompt, model="gpt-4o"),
    self._get_gpt4o_mini_feedback(base_system_prompt, user_prompt)
]
```

### 이미지 생성을 건너뛰고 싶다면?

`backend/genai_client.py`의 `generate_image` 메서드를 수정하여 항상 placeholder를 반환하도록 할 수 있습니다.

---

## 📊 현재 수정 완료 사항

| 항목 | 상태 | 설명 |
|------|------|------|
| 이미지 생성 | ✅ 수정 | Imagen 3.0 사용 |
| Claude 404 오류 | ✅ 수정 | 최신 모델 ID로 업데이트 |
| Gemma 오류 | ✅ 수정 | GPT-4o-mini로 대체 |
| 학생 응답 품질 | ✅ 개선 | 프롬프트 강화 |
| 의존성 | ✅ 최적화 | HuggingFace 제거 |

자세한 내용은 `FIXES_APPLIED.md`를 참고하세요.

---

## ❓ 문제 해결

### "Internal Server Error" 발생 시
→ `backend/.env` 파일에 API 키가 제대로 설정되었는지 확인

### 이미지 생성 실패 시
→ `GOOGLE_API_KEY` 권한 확인 및 Generative AI API 활성화 확인

### Claude 404 오류 시
→ `ANTHROPIC_API_KEY` 유효성 확인 및 모델 접근 권한 확인

---

## 🎉 모든 준비 완료!

환경 변수만 설정하면 바로 사용할 수 있습니다! 🚀

질문이 있으시면 언제든지 문의하세요.


