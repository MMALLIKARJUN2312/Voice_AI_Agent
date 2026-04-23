# Real-Time Multilingual Voice Agent for Clinical Appointment Booking

---

## Overview

VoiceCare AI is a **production-grade real-time multilingual voice AI agent** that enables users to:

-- Book, reschedule, and cancel appointments via voice
-- Communicate in **English, Hindi, and Tamil**
-- Maintain **contextual memory (session + persistent)**
-- Handle **outbound campaigns (reminders, follow-ups)**
-- Operate with **low latency (<450ms target)**

---

## Architecture Overview

```
User Voice
   ↓
Speech-to-Text (Whisper)
   ↓
Language Detection
   ↓
Gemini LLM Agent (Tool Calling)
   ↓
Tool Router
   ↓
Scheduler Engine (Validation + Booking)
   ↓
Memory (Redis + PostgreSQL)
   ↓
Text Response
   ↓
Text-to-Speech
   ↓
Audio Output
```

---

## Project Structure

```
voice-ai-agent/
│
├── backend/
│   ├── api/
│   ├── controllers/
│   └── routes/
│
├── agent/
│   ├── prompt/
│   ├── reasoning/
│   └── tools/
│
├── memory/
│   ├── session_memory/
│   └── persistent_memory/
│
├── services/
│   ├── speech_to_text/
│   ├── text_to_speech/
│   └── language_detection/
│
├── scheduler/
│   └── appointment_engine/
│
├── docs/
│   └── architecture.png
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Tech Stack

| Layer            | Technology                   |
| ---------------- | ---------------------------- |
| Backend          | FastAPI                      |
| LLM              | Gemini (google-generativeai) |
| STT              | Whisper                      |
| TTS              | Custom / Extendable          |
| Memory           | Redis                        |
| Database         | PostgreSQL                   |
| Realtime         | WebSockets                   |
| Containerization | Docker                       |

---

## Setup Instructions

### Clone Repository

```bash
git clone <your-repo-url>
cd voice-ai-agent
```

---

### Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
REDIS_HOST=localhost
POSTGRES_URL=postgresql://user:password@localhost/db
```

---

### Run Server

```bash
uvicorn backend.api.server:app --reload
```

---

## Docker Setup (Production)

### Build & Run

```bash
docker compose up --build
```

---

### Services

| Service    | Port |
| ---------- | ---- |
| API        | 8000 |
| Redis      | 6379 |
| PostgreSQL | 5432 |

---

## API Endpoints

### Voice Processing

```http
POST /voice/process
```

#### Request

```json
{
  "audio": "book appointment tomorrow at 10:00"
}
```

#### Response

```json
{
  "text": {
    "response": "Appointment booked at 10:00"
  },
  "audio": "[AUDIO-en] Appointment booked at 10:00",
  "latency_ms": 320
}
```

---

### Appointment Booking

```http
POST /appointment/book
```

---

## Agent Design

-- Gemini LLM with **tool-calling architecture**
-- Strict JSON prompting
-- Regex-based JSON extraction
-- Fallback parser for robustness

---

## Memory Design

### Session Memory (Redis)

-- Stores conversation context
-- TTL-based cleanup

### Persistent Memory (PostgreSQL)

-- Stores user history
-- Appointment records

---

## Scheduling & Validation

System prevents:

-- Double booking
-- Past-time booking
-- Invalid doctor selection

Example:

```python
if appointment_time < current_time:
    reject
```

---

## Latency Breakdown

| Stage          | Time         |
| -------------- | ------------ |
| STT            | ~120 ms      |
| Agent (Gemini) | ~200 ms      |
| TTS            | ~100 ms      |
| **Total**      | **< 450 ms** |

---

## Error Handling

### LLM Failure

```json
"I'm having trouble processing that request"
```

---

### Scheduling Conflict

```json
"Slot already booked. Available slots are 2 PM and 4 PM."
```

---

## Testing (Postman)

### Test Cases

| Scenario         | Expected Result |
| ---------------- | --------------- |
| Book appointment | Success         |
| Cancel           | Removed         |
| Reschedule       | Updated         |
| Hindi input      | Works           |
| Tamil input      | Works           |
| Invalid slot     | Rejected        |

---

## Logging & Metrics

-- Latency tracking per request
-- Structured logging using `loguru`
-- Debuggable LLM outputs

---

## Submission Deliverables

-- GitHub Repository
-- Working API
-- README.md
-- Architecture Diagram
-- Loom Demo (≤ 3 min)

---

## Key Highlights

-- Real-time voice AI pipeline
-- Gemini-powered agent with tool orchestration
-- Context-aware memory system
-- Robust error handling
-- Production-ready Docker deployment

---

## Limitations

-- Streaming STT can be improved
-- TTS is currently mocked
-- Gemini JSON output needs strict validation

---

## Future Improvements

-- Real-time streaming audio (chunk-based STT)
-- Barge-in interruption handling
-- Campaign scheduler with queues
-- Frontend voice interface

---
