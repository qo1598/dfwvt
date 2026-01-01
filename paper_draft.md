# 데이터 플라이휠을 활용한 사고루틴 평가를 위한 AI 모델 개선 시스템 구축
## Building an AI Model Improvement System for Thinking Routine Assessment using Data Flywheel

### 초록 (Abstract)
본 연구는 개념기반탐구수업(Concept-Based Inquiry)에서 학생들의 사고 확장을 돕기 위해 사용되는 'See-Think-Wonder(STW)' 사고 루틴에 대한 교사의 평가 부담을 줄이고, 개인화된 피드백을 제공하기 위한 **휴먼인더루프(HITL)** 기반의 AI 평가 시스템을 제안한다. 특히, 단순히 일회성 피드백을 제공하는 것에 그치지 않고, **데이터 플라이휠(Data Flywheel)** 구조를 적용하여 축적된 평가 데이터를 기반으로 AI 모델의 성능을 지속적으로 향상시킬 수 있는 시스템 아키텍처를 설계하였다. 제안하는 시스템은 **AI 기반 평가**의 신뢰도를 높이기 위해 다양한 LLM(Gemini, GPT-4o 등)을 활용하고, 이를 교사가 비교 평가하는 과정을 통해 데이터의 선순환을 유도한다.

**핵심어**: 데이터 플라이휠, 휴먼인더루프(HITL), 개념기반탐구, 사고루틴, AI 기반 평가

---

### 1. 서론 (Introduction)

#### 1.1 연구 배경 및 필요성
미래 교육 현장에서는 단순 지식 습득을 넘어 개념적 이해와 비판적 사고를 함양하는 개념기반탐구수업(Concept-Based Inquiry)의 중요성이 강조되고 있다. 이러한 수업의 일환으로 학습자의 관찰력과 사고력을 키우기 위해 'See-Think-Wonder(STW)'와 같은 사고 루틴이 널리 활용된다. 그러나 다수 학생의 서술형 응답에 대해 교사가 일일이 개별화된 피드백을 제공하는 것은 물리적인 시간과 노력의 한계가 존재한다. 이에 생성형 AI(LLM)를 활용한 자동 피드백 시스템의 필요성이 대두되었으나, 기존 단일 모델 기반 시스템은 교육적 맥락에 맞는 피드백의 정확성과 일관성을 보장하기 어렵다는 한계가 있었다.

#### 1.2 연구 목적
본 연구는 이러한 문제를 해결하기 위해 **데이터 플라이휠(Data Flywheel)** 개념을 도입한 AI 모델 개선 시스템을 제안한다. 사용자가 서비스를 사용할수록 양질의 데이터가 축적되고, 이를 통해 서비스가 개선되어 더 많은 사용자를 유입시키는 선순환 구조를 구축함으로써, 교육 현장에 최적화된 STW 피드백 AI 모델을 개발하는 것을 목표로 한다.

### 2. 관련 연구 (Related Works)

#### 2.1 개념기반탐구와 See-Think-Wonder
See-Think-Wonder는 하버드대학교 Project Zero에서 개발한 사고 루틴으로, 시각적 자극을 통해 관찰(See), 해석(Think), 호기심(Wonder)을 연결하여 학습자의 사고를 심화시키는 학습 전략이다. 이는 AI가 시각적 정보와 텍스트 정보를 결합하여 처리하는 멀티모달(Multi-modal) 능력과 교육적 피드백 생성 능력을 검증하기에 적합한 도메인이다.

#### 2.2 LLM 기반 교육 평가 시스템
최근 GPT-4, Claude 3 등 고성능 LLM의 등장으로 자동 에세이 채점 및 피드백 생성 연구가 활발하다. 그러나 범용 모델은 특정 교육적 의도나 학습자 수준(페르소나)을 고려한 세밀한 피드백 제공에는 여전히 한계를 보이며, 이를 개선하기 위한 지속적인 인간-AI 상호작용(HITL) 기반의 데이터 수집 시스템이 요구된다.

### 3. 시스템 설계 (System Design)

#### 3.1 전체 아키텍처
본 시스템은 크게 입력(Input), 처리(Processing), 평가(Evaluation), 데이터(Data)의 4개 계층으로 구성된다.

1.  **입력층 (Stimulus Generator)**: Gemini 2.5 Flash 모델을 활용하여 과학, 환경, 예술 등 다양한 주제의 고품질 교육용 이미지를 동적으로 생성하여 학생에게 시각적 자극을 제공한다.
2.  **처리층 (Multi-LLM Feedback Engine)**: 학생의 응답에 대해 서로 다른 특성을 가진 3종의 LLM(GPT-4o, Claude 3.5 Sonnet, Gemma 3)이 동시에 피드백을 생성한다. 이는 단일 모델의 편향을 방지하고 상호 비교를 가능하게 한다.
3. **평가층 (Blind Evaluation Interface)**: **휴먼인더루프(HITL)** 전략의 핵심으로, 교사는 모델명을 모르는 상태(Blind)에서 각 피드백의 적절성을 비교 평가한다. 이 인간 피드백(RLHF) 과정은 모델 성능 개선의 기준점(Ground Truth)이 된다.
4.  **데이터층 (Data Flywheel Storage)**: Supabase를 활용하여 원본 이미지, 학생 응답, 생성된 피드백, 교사의 평가 데이터를 통합 저장한다. 이 데이터는 향후 교육 특화 sLLM(Small Large Language Model) 파인튜닝(Fine-tuning)을 위한 고품질 데이터셋이 된다.

#### 3.2 데이터 플라이휠 전략
"시나리오 생성 → 학생 응답(Simulator) → 피드백 생성 → 교사 평가 → 데이터 축적 → 모델 개선"으로 이어지는 순환 구조를 설계하였다. 초기 단계에는 실제 학생 데이터 부족 문제를 해결하기 위해 'Student Persona Simulator'를 개발하여 다양한 학습자 수준(문해력 상/중/하, 성향 등)을 반영한 가상 응답 데이터를 생성하여 콜드 스타트(Cold Start) 문제를 해결하였다.

### 4. 구현 (Implementation)

#### 4.1 핵심 모듈 구현
-   **Backend**: Python FastAPI를 기반으로 비동기(Async) 처리를 통해 다중 LLM API 호출의 지연 시간을 최소화하였다.
    -   `Simulator.py`: Gemini 2.5 Flash를 활용해 5학년 수준의 STW 응답을 생성하며, JSON 포맷을 강제하여 데이터 구조의 일관성을 유지하였다.
    -   `Feedback_engine.py`: OpenAI(GPT-4o), Anthropic(Claude), NVIDIA NIM(Gemma 3) API를 병렬로 호출하여 실시간으로 피드백을 수집한다.
-   **Frontend**: React와 Vite를 사용하여 빠르고 반응성 높은 UI를 구현하였다. 교사는 직관적인 인터페이스에서 3개의 피드백을 나란히 비교하고, 선택 및 수정할 수 있다.

#### 4.2 실험 및 결과
프로토타입 시스템을 통해 90여 개의 탐구 시나리오에 대한 테스트를 진행하였다. 초기 실험 결과, GPT-4o는 논리적 정합성이 우수하고, Claude 3.5 Sonnet은 교육적 어조와 공감 능력이 뛰어남을 확인하였다. Gemma 3(4B)와 같은 경량 모델은 속도 면에서 장점이 있으나 복잡한 추론에는 한계를 보였다. 이러한 비교 데이터는 향후 모델 앙상블(Ensemble) 전략 수립의 근거가 된다.

### 5. 결론 및 향후 과제 (Conclusion)
본 연구는 **데이터 플라이휠** 구조를 적용하여 지속적으로 성장하는 **AI 기반 평가** 시스템을 제안하였다. 이 시스템은 교사의 평가 업무를 효율화할 뿐만 아니라, 축적된 데이터를 바탕으로 교육 현장에 최적화된 자체 모델을 확보할 수 있는 기반을 제공한다. 향후 연구에서는 축적된 평가 데이터를 활용하여 온디바이스(On-device) 구동이 가능한 경량화된 교육 전용 sLLM을 개발하고, 실제 교실 환경에서의 효과성을 검증할 계획이다.

### 참고문헌 (References)
1. Project Zero. (2016). *Making Thinking Visible*. Harvard Graduate School of Education.
2. Levy, S. (2023). *Data Flywheels: The Secret to AI Success*. O'Reilly Media.
3. OpenAI. (2024). *GPT-4 Technical Report*.
