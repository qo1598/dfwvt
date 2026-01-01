# Data Flywheel - 사고 루틴 평가 플랫폼

> AI 기반 See-Think-Wonder 학생 응답 생성 및 다중 LLM 피드백 비교 시스템

## 📋 프로젝트 개요

이 플랫폼은 **개념기반탐구수업**을 위한 교육용 AI 시스템입니다. 학생의 **See-Think-Wonder (STW)** 사고 루틴 응답을 시뮬레이션하고, 여러 LLM 모델을 통해 교육적 피드백을 생성하여 비교할 수 있습니다.

### 주요 기능

- 🖼️ **AI 이미지 생성**: Gemini 2.5 Flash를 활용한 교육용 탐구 이미지 자동 생성
- 👨‍🎓 **학생 응답 시뮬레이션**: 다양한 탐구 시나리오에 대한 초등학생 수준 STW 응답 생성
- 🤖 **다중 LLM 피드백**: GPT-4o, Claude Sonnet 4, Gemma 3를 통한 피드백 비교
- 📊 **교육자 평가 인터페이스**: 생성된 피드백의 품질을 전문가가 평가할 수 있는 UI

---

## 🏗️ 기술 스택

### Backend
| 기술 | 용도 |
|------|------|
| **FastAPI** | REST API 서버 |
| **Supabase** | 데이터 저장 |
| **Google GenAI** | 이미지 생성 & 학생 응답 시뮬레이션 |
| **OpenAI** | GPT-4o 피드백 생성 |
| **Anthropic** | Claude Sonnet 4 피드백 생성 |
| **NVIDIA NIM** | Gemma 3 4B 피드백 생성 |

### Frontend
| 기술 | 용도 |
|------|------|
| **React 19** | UI 프레임워크 |
| **Vite 7** | 빌드 도구 |
| **TailwindCSS** | 스타일링 |
| **Axios** | HTTP 클라이언트 |

---

## 📁 프로젝트 구조

```
dfwvt/
├── backend/                    # FastAPI 백엔드
│   ├── main.py                 # API 엔드포인트 & 탐구 시나리오
│   ├── genai_client.py         # Gemini 이미지 생성 클라이언트
│   ├── simulator.py            # 학생 응답 시뮬레이터 (STW)
│   ├── feedback_engine.py      # 다중 LLM 피드백 엔진
│   ├── requirements.txt        # Python 의존성
│   └── .env                    # 환경 변수 (API 키)
│
├── frontend/                   # React 프론트엔드
│   ├── src/
│   │   ├── App.jsx             # 메인 앱 컴포넌트
│   │   ├── components/
│   │   │   ├── Step1_Context.jsx       # 맥락 제시 단계
│   │   │   ├── EvaluationStep.jsx      # 평가 단계 UI
│   │   │   └── AccessCodeModal.jsx     # 접근 코드 모달
│   │   └── index.css           # 스타일
│   ├── package.json            # Node 의존성
│   └── vite.config.js          # Vite 설정
│
├── data_schema.json            # 데이터 스키마 정의
└── 구상도.pptx                  # 프로젝트 구상 문서
```

---

## 🚀 실행 방법

### 1. 환경 변수 설정

`backend/.env` 파일을 생성하고 다음 API 키를 설정합니다:

```env
GOOGLE_API_KEY=your_google_api_key       # Gemini API용
OPENAI_API_KEY=your_openai_api_key       # GPT-4o용
ANTHROPIC_API_KEY=your_anthropic_key     # Claude용
NVIDIA_API_KEY=your_nvidia_api_key       # Gemma용 (NVIDIA NIM)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
ACCESS_CODE=PILOT2025
```

### 2. Backend 실행

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

프론트엔드: http://localhost:5173  
백엔드 API: http://localhost:8000

---

## 📡 API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| `GET` | `/` | 서버 상태 확인 |
| `GET` | `/generate-session` | 새 세션 생성 (이미지 + 학생 응답) |
| `POST` | `/generate-feedback` | 특정 단계의 LLM 피드백 생성 |

### `/generate-session` 응답 예시

```json
{
  "image_url": "/generated/generated_abc123.png",
  "student_response": {
    "see": "나비가 꽃 위에 앉아있어요.",
    "think": "나비가 꿀을 먹으러 온 것 같아요.",
    "wonder": "나비는 어떻게 꿀을 찾을까요?"
  },
  "scenario": "A butterfly emerging from its chrysalis..."
}
```

---

## 🎓 탐구 시나리오 카테고리

시스템에는 90개 이상의 다양한 탐구 시나리오가 내장되어 있습니다:

- **과학 탐구**: 나비 우화, 얼음 녹음, 그림자 변화 등
- **환경과 자연**: 나무 나이테, 침식 패턴, 생태계 등
- **사회와 문화**: 다문화 음식, 전통 시장, 교통수단 변화 등
- **예술과 창의성**: 색 혼합, 악기, 재활용 예술 등
- **수학과 패턴**: 벌집 육각형, 대칭, 기어 맞물림 등
- **기술과 혁신**: 풍력 발전, 3D 프린팅, 단순 기계 등

---

## ⚠️ 알려진 이슈

현재 해결이 필요한 문제들은 [ISSUES.md](./ISSUES.md)를 참조하세요.

---

## 📄 라이선스

Educational Use Only - 교육 목적으로만 사용 가능
