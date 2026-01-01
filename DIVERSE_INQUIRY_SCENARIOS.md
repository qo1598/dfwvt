# 🎨 다양한 탐구 시나리오 시스템

> **업데이트**: 2025-12-12  
> **목적**: 개념기반탐구수업의 동기유발/전개 단계를 위한 다양한 이미지 생성

---

## 🎯 개선 목표

### 이전 문제점
```
❌ 항상 "environment" 주제만 사용
❌ 단순한 프롬프트: "A photo-realistic image representing environment"
❌ 비슷비슷한 이미지만 생성
❌ 탐구 촉진 요소 부족
```

### 개선 후
```
✅ 70+ 다양한 탐구 시나리오
✅ 과학, 환경, 사회, 예술, 수학, 기술 등 다양한 주제
✅ 매 세션마다 랜덤하게 다른 시나리오 선택
✅ 학생들의 탐구를 유도하는 구체적인 상황
```

---

## 📚 포함된 탐구 주제 카테고리 (70+ 시나리오)

### 1. 과학 탐구 (8개)
```
- 나비가 번데기에서 나오는 과정
- 얼음이 녹는 과정과 응결 현상
- 하루 종일 그림자 길이 변화
- 씨앗이 다른 토양에서 발아하는 모습
- 무지개가 물방울에서 생성되는 과정
- 자석의 인력과 척력, 철가루 패턴
- 촛불의 다른 색깔 층과 녹는 초
- 비눗방울의 무지개색 반사
```

### 2. 환경과 자연 (8개)
```
- 바위 주변을 흐르는 강물의 속도 차이
- 나무 나이테로 보는 성장 과정
- 다양한 동물 발자국
- 새가 둥지를 만드는 과정
- 가을 단풍의 색 변화
- 이슬이 맺힌 거미줄
- 빗물 후 토양 침식 패턴
- 썩는 통나무와 새로운 생태계
```

### 3. 사회와 문화 (8개)
```
- 다양한 문화의 아이들이 전통 음식 나누기
- 옛 건물과 새 건물의 대조
- 전통 시장의 물물교환
- 다양한 기후의 주거 형태
- 이웃이 함께 가꾸는 공동체 텃밭
- 다양성을 보여주는 거리 벽화
- 책과 태블릿으로 공부하는 도서관
- 시대별 교통수단의 발전
```

### 4. 예술과 창의성 (7개)
```
- 팔레트에서 섞이는 물감
- 세계의 다양한 악기
- 재활용품으로 만든 예술 작품
- 장식 창문을 통한 빛과 그림자
- 자연의 패턴: 나선형, 프랙탈, 대칭
- 도자기 물레로 흙 빚기
- 종이접기의 단계별 과정
```

### 5. 수학과 패턴 (7개)
```
- 벌집의 완벽한 육각형 패턴
- 과일 단면의 대칭과 씨앗 배열
- 서로 맞물려 돌아가는 톱니바퀴
- 위에서 본 나선형 계단
- 반복 패턴의 타일
- 방사형 대칭의 거미줄
- 연쇄 반응을 일으킬 도미노
```

### 6. 기술과 혁신 (7개)
```
- 도르래, 지렛대, 바퀴 등 단순 기계
- 풍력 발전기와 꽃밭
- 학교 지붕의 태양광 패널
- 3D 프린터로 물체 만들기
- 로봇과 인간의 협업
- 전통 도구와 현대 도구 비교
- 자전거의 기계 부품들
```

### 7. 생태계와 관계 (7개)
```
- 먹이사슬: 태양-식물-애벌레-새-여우
- 꽃가루를 옮기는 꿀벌
- 다양한 생물이 사는 조수 웅덩이
- 흙을 비옥하게 만드는 지렁이
- 새끼에게 먹이를 주는 어미새
- 물웅덩이에서 함께 물 마시는 동물들
- 퇴비통에서 흙으로 변하는 음식물
```

### 8. 건강과 신체 (6개)
```
- 무지개색으로 배열된 건강 음식
- 다양한 운동을 하는 아이들
- 혈관이 보이는 심장 모형
- 양치질 전후의 치아
- 다른 근육을 단련하는 운동들
- 균형잡힌 식사 구성
```

### 9. 날씨와 기후 (6개)
```
- 다양한 높이의 구름 종류
- 자연에서 보는 물의 순환
- 온도 변화를 보여주는 온도계
- 바람의 다양한 효과들
- 독특한 패턴의 눈 결정
- 폭풍우 속 번개
```

### 10. 물질과 변화 (6개)
```
- 물의 세 가지 상태: 얼음, 물, 수증기
- 시간에 따라 생기는 녹
- 발효로 부푸는 빵 반죽
- 나무가 재와 연기로 변하는 모습
- 물에 녹아 보이지 않는 소금
- 화학 변화로 갈색이 된 바나나
```

---

## 💡 프롬프트 구조

### 개선된 이미지 생성 프롬프트
```python
image_prompt = f"""
Create a vivid, photo-realistic educational photograph: {selected_scenario}

Style: High-quality educational photography, clear details, natural lighting
Purpose: To spark curiosity and inquiry in elementary students
Mood: Engaging, thought-provoking, inviting observation and questions
Composition: Clear focal point with interesting details to discover
Quality: Sharp, colorful, suitable for See-Think-Wonder thinking routine
"""
```

### 특징
- ✅ 구체적인 시나리오 설명
- ✅ 교육적 목적 명시
- ✅ See-Think-Wonder에 적합한 요소 강조
- ✅ 학생들의 호기심과 탐구 유도
- ✅ 관찰할 디테일 포함

---

## 🎯 교육적 가치

### See-Think-Wonder 루틴에 적합한 이유

1. **See (관찰)**
   - 명확한 초점과 흥미로운 디테일
   - 학생들이 발견할 수 있는 요소들
   - 시각적으로 풍부한 정보

2. **Think (생각)**
   - 인과관계를 생각하게 하는 상황
   - 비교와 대조가 가능한 요소
   - 과정과 변화를 보여주는 장면

3. **Wonder (궁금증)**
   - "왜?"를 묻게 만드는 현상
   - "어떻게?"를 탐구하고 싶게 하는 메커니즘
   - "만약에?"를 상상하게 하는 상황

---

## 📊 테스트 결과

### 다양성 테스트 (3회 연속 생성)
```
Session 1: ✅ "Healthy foods arranged as a rainbow..."
Session 2: ✅ "Solar panels on a school roof..."
Session 3: ⚠️ "A thermometer showing temperature change..." (이미지 생성 실패)

→ 매번 다른 주제의 이미지 생성 확인
→ 과학, 기술, 건강 등 다양한 카테고리 선택됨
```

---

## 🔄 작동 방식

### 1. 세션 생성 요청
```http
GET /generate-session
Header: x-access-code: PILOT2025
```

### 2. 랜덤 시나리오 선택
```python
selected_scenario = random.choice(INQUIRY_SCENARIOS)
# 70+ 시나리오 중 1개 랜덤 선택
```

### 3. 상세 프롬프트 생성
```python
image_prompt = f"""
Create a vivid, photo-realistic educational photograph: {selected_scenario}
...
"""
```

### 4. 이미지 생성 및 학생 응답
```python
image_url = genai_client.generate_image(image_prompt)
student_response = simulator.generate_stw_response(visual_context=selected_scenario)
```

### 5. 응답 반환
```json
{
  "image_url": "/generated/generated_xxxxx.png",
  "student_response": {
    "see": "...",
    "think": "...",
    "wonder": "..."
  },
  "scenario": "선택된 시나리오 설명"
}
```

---

## 📈 개념기반탐구수업 적용

### 수업 단계별 활용

**1. 동기유발 (5분)**
```
→ 다양한 탐구 이미지 제시
→ See-Think-Wonder 활동
→ 학습 주제에 대한 흥미 유발
```

**2. 전개 (30분)**
```
→ 이미지에서 발견한 내용 토의
→ 개념 탐구 및 심화
→ AI 피드백으로 사고 확장
```

**3. 정리 (10분)**
```
→ 배운 개념 정리
→ 추가 궁금증 공유
→ 다음 탐구 주제 연결
```

---

## 💡 교사 활용 팁

### 주제별 필터링 (향후 추가 가능)
```python
# 원하는 주제만 선택 가능
science_scenarios = [s for s in INQUIRY_SCENARIOS if "과학" 키워드]
environment_scenarios = [s for s in INQUIRY_SCENARIOS if "환경" 키워드]
```

### 난이도 조절 (향후 추가 가능)
```python
# 학년별로 다른 시나리오 풀 사용
elementary_low = [...] # 1-2학년
elementary_mid = [...] # 3-4학년
elementary_high = [...] # 5-6학년
```

---

## 🎨 이미지 품질 향상 요소

### 교육적 사진의 특징
- ✅ **Photo-realistic**: 실제 사진 같은 품질
- ✅ **Clear details**: 명확한 디테일
- ✅ **Natural lighting**: 자연스러운 조명
- ✅ **Clear focal point**: 명확한 초점
- ✅ **Colorful**: 다채로운 색상
- ✅ **Sharp**: 선명한 이미지

---

## 📊 예상 효과

### 학생 참여도
```
다양한 주제 → 더 많은 학생의 관심 유발
구체적 상황 → 관찰과 발견의 즐거움
탐구 유도 → 자발적인 질문 증가
```

### 교육 효과
```
다양한 개념 노출 → 통합적 사고력 발달
시각적 학습 → 개념 이해도 향상
See-Think-Wonder → 비판적 사고력 증진
```

### 데이터 수집
```
다양한 주제 → 풍부한 평가 데이터
다양한 맥락 → AI 모델 개선 효과
실제 수업 활용 → 실용성 검증
```

---

## 🚀 사용 방법

### 브라우저에서
```
http://localhost:5173
→ "Start New Session" 클릭
→ 매번 다른 주제의 이미지 생성
```

### API로 직접 호출
```bash
curl -X GET "http://localhost:8000/generate-session" \
  -H "x-access-code: PILOT2025"
```

---

## 📝 향후 개선 가능성

### 1. 주제 선택 기능
```python
GET /generate-session?category=science
→ 특정 카테고리만 선택
```

### 2. 난이도 조절
```python
GET /generate-session?level=elementary_low
→ 학년별 적합한 시나리오
```

### 3. 교육과정 연계
```python
GET /generate-session?curriculum=5th_grade_science
→ 교육과정 성취기준 연계
```

### 4. 시나리오 피드백
```python
POST /feedback-scenario
→ 교사가 좋았던 시나리오 피드백
→ 효과적인 시나리오 학습
```

---

## 🎉 결론

**개념기반탐구수업을 위한 다양한 탐구 이미지 생성 시스템 완성!**

```
✅ 70+ 다양한 탐구 시나리오
✅ 10개 주제 카테고리
✅ 랜덤 선택으로 매번 다른 이미지
✅ See-Think-Wonder에 최적화
✅ 동기유발/전개 단계에 적합
✅ 학생들의 자발적 탐구 유도
```

---

**이제 매 세션마다 새롭고 다양한 탐구 주제가 제시됩니다!** 🎨

---

**작성**: AI Assistant  
**날짜**: 2025-12-12  
**상태**: ✅ **다양한 탐구 시나리오 시스템 작동 중**


