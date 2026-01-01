# Data Flywheel Platform - 현재 문제점 정리

> 작성일: 2025-12-12

---

## 1. 이미지 생성 실패 ❌

| 항목 | 내용 |
|------|------|
| **파일** | `backend/genai_client.py` |
| **모델** | `gemini-2.5-flash-preview-05-20` |
| **증상** | "Gemini Generation Error" 표시 |
| **원인 추정** | API 권한, 모델 ID 오류, 또는 SDK 호환성 문제 |

### 확인 필요 사항
- [ ] Google Cloud Console에서 Generative AI API 활성화 여부
- [ ] `GOOGLE_API_KEY` 권한 확인
- [ ] `google-genai` 라이브러리 버전 확인

---

## 2. Claude 3.5 Sonnet 피드백 실패 ❌

| 항목 | 내용 |
|------|------|
| **파일** | `backend/feedback_engine.py` |
| **모델** | `claude-3-5-sonnet-20240620` |
| **증상** | 404 not_found_error |
| **원인 추정** | 모델 ID 만료 또는 API 키 권한 부족 |

### 확인 필요 사항
- [ ] Anthropic Console에서 사용 가능한 모델 목록 확인
- [ ] `ANTHROPIC_API_KEY` 유효성 확인
- [ ] 올바른 모델 ID로 교체 (예: `claude-3-sonnet-20240229`)

---

## 3. HuggingFace Gemma 피드백 실패 ❌

| 항목 | 내용 |
|------|------|
| **파일** | `backend/feedback_engine.py` |
| **모델** | `google/gemma-3-4b-it` |
| **증상** | `coroutine raised StopIteration` |
| **원인 추정** | HuggingFace 비동기 API 호출 문제 |

### 확인 필요 사항
- [ ] `HUGGINGFACE_API_KEY` 유효성 확인
- [ ] 모델 서버 가용성 확인
- [ ] 대체 모델 검토 (예: GPT-4o-mini)

---

## 4. 학생 응답 품질 저하 ⚠️

| 항목 | 내용 |
|------|------|
| **파일** | `backend/simulator.py` |
| **증상** | "잘 모르겠어요" 등 부실한 응답 |
| **원인** | 이미지 생성 실패로 시각적 맥락 부재 |

---

## 5. 환경 변수 점검 📋

**파일**: `backend/.env`

```env
GOOGLE_API_KEY=???       # Gemini/Imagen API용
OPENAI_API_KEY=???       # GPT-4o용 (작동 중 ✅)
ANTHROPIC_API_KEY=???    # Claude용 (404 오류)
HUGGINGFACE_API_KEY=???  # Gemma용 (StopIteration)
SUPABASE_URL=???
SUPABASE_KEY=???
ACCESS_CODE=PILOT2025
```

---

## 요약

| 기능 | 상태 | 우선순위 |
|------|------|----------|
| 이미지 생성 | ❌ 실패 | 🔴 높음 |
| GPT-4o 피드백 | ✅ 정상 | - |
| Claude 피드백 | ❌ 404 | 🔴 높음 |
| Gemma 피드백 | ❌ 오류 | 🟡 중간 |
| 학생 응답 품질 | ⚠️ 저하 | 🟡 중간 |

---

## 해결 방향 제안

1. **이미지 생성**: Imagen 3.0 (`imagen-3.0-generate-002`)으로 대체 검토
2. **Claude**: `claude-3-sonnet-20240229` 또는 `claude-3-haiku-20240307`로 변경
3. **Gemma**: GPT-4o-mini로 대체하여 안정성 확보
