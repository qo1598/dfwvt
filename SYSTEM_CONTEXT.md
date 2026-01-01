# System Context: Data Flywheel for Thinking Routine Assessment

> **For AI Agents**: This document provides a **deep dive** into the Data Flywheel Verification Testbed (DFWVT). It details the logic, prompts, data schemas, and design philosophy required to fully understand the codebase.

## 1. Project Overview & Philosophy

### 1.1 Core Objective
The goal is to build an **autonomous educational feedback system** that improves itself via a **Data Flywheel**.
- **Problem**: Teachers cannot provide individual detailed feedback for every "See-Think-Wonder" (STW) response from students.
- **Solution**: Use LLMs to generate feedback.
- **Challenge**: Generic LLMs lack pedagogical nuance.
- **Approach**:
    1.  **Cold Start**: Simulate students (Gemini) to generate STW data.
    2.  **Blind Evaluation**: Teachers evaluate anonymized feedback from competing LLMs (GPT-4o, Claude, Gemma).
    3.  **Flywheel**: Teacher choices become "Golden Labels" to fine-tune a future sLLM.

### 1.2 "See-Think-Wonder" (STW) Domain
A thinking routine from Harvard Project Zero.
- **See**: Objective observation (Visual).
- **Think**: Interpretation/Inference (Cognitive).
- **Wonder**: Curiosity/Questions (Inquiry).

---

## 2. Technical Architecture Deep Dive

### 2.1 Backend (`/backend`) - FastAPI
The backbone of the system. Designed for **concurrency**.

#### `simulator.py`: Student Persona Logic
Uses **Gemini 2.5 Flash** to simulate a Korean elementary student.
- **Critical Prompt**:
    ```text
    Role: 5th grade student.
    Task: See-Think-Wonder.
    Constraints:
    - Use child-like tone (~해요).
    - No "I don't know".
    - Be creative.
    ```
- **Why?**: Guaranteed structured JSON output prevents parsing errors.

#### `feedback_engine.py`: The Arena
Manages the "Battle of Models".
- **Models**:
    - **GPT-4o** (OpenAI): The logic benchmark.
    - **Claude 3.5 Sonnet** (Anthropic): The empathy/nuance benchmark.
    - **Gemma 3 4B** (NVIDIA NIM): The on-device comparison target.
- **Prompt Strategy**:
    - Uses **Minimalist Prompting**: `Student said: "{text}". Feedback(2-3 sentences):`
    - **Reason**: We want to measure the *base capability* of the model to act as a teacher, without heavy instructed prompting (zero-shot).

#### `genai_client.py`: Visual Stimulus
- **Model**: `gemini-2.5-flash-image`.
- **Purpose**: Generates high-quality, inquiry-provoking images (e.g., "A butterfly emerging...").

### 2.2 Frontend (`/frontend`) - React 19
A Single Page Application (SPA) modeling a linear workflow.

#### State Machine (Steps)
The app flows through integer steps in `App.jsx`:
- **0 (Init)**: Fetch/restore session.
- **1 (Context)**: Show Image + Full STW Response.
- **2 (See)**: Evaluation UI for "See".
- **3 (Think)**: Evaluation UI for "Think".
- **4 (Wonder)**: Evaluation UI for "Wonder".
- **5 (Done)**: Completion & Thank you.

#### Blind Test UI (`EvaluationStep.jsx`)
- **Mechanism**:
    - Fetches 3 feedbacks via `POST /generate-feedback`.
    - Renders them in cards *without* model names.
    - **Inputs**: Score (0-10 slider), Comment (Textarea).
    - **Goal**: Unbiased RLHF (Reinforcement Learning from Human Feedback) data collection.

---

## 3. Data Schemas & API Contract

### 3.1 Session Generation (`GET /generate-session`)
Response:
```json
{
  "image_url": "/generated/img_29fa81.png",
  "student_response": {
    "see": "나비 날개가 젖어 보여요.",
    "think": "방금 번데기에서 나온 것 같아요.",
    "wonder": "날개가 마르는 데 얼마나 걸릴까요?"
  },
  "scenario": "A butterfly emerging from its chrysalis..."
}
```

### 3.2 Feedback Generation (`POST /generate-feedback`)
Request:
```json
{
  "student_response": { ... },
  "stage": "see"
}
```
Response:
```json
{
  "feedbacks": [
    {
      "model_id": "gpt-4o",
      "model_name": "GPT-4o (OpenAI)",
      "feedback_text": "관찰한 내용이 아주 구체적이네요! ..."
    },
    ...
  ]
}
```

---

## 4. Key Configurations (`.env`)
The system requires these keys to function:
| Key | Provider | Purpose |
|-----|----------|---------|
| `GOOGLE_API_KEY` | Google | Image & Student Sim |
| `OPENAI_API_KEY` | OpenAI | Feedback Candidate 1 |
| `ANTHROPIC_API_KEY` | Anthropic | Feedback Candidate 2 |
| `NVIDIA_API_KEY` | NVIDIA | Feedback Candidate 3 |
| `SUPABASE_URL` | Supabase | Data Storage (Flywheel) |

## 5. Troubleshooting Guide for AI
- **Image Generation Fails**: Usually safety filters. Check `genai_client.py` error logs.
- **Feedback "404"**: Claude API key often needs explicit model permissions.
- **Frontend Start**: If `npm run dev` fails, checks `node_modules`. Run `npm install` again.

## 6. Future Roadmap (The "Why")
This codebase is **Phase 1 (Data Collection)**.
- **Phase 2**: Train a Llama-3-8B adapter using the collected "High Score" feedbacks.
- **Phase 3**: Deploy the fine-tuned model to edge devices for classroom use.
