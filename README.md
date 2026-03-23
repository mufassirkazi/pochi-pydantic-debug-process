# AI Image Generator

A full-stack AI image generator powered by **OpenAI DALL·E 3**, **FastAPI**, and **Pydantic Logfire**.

```
pochi-pydantic-demo/
├── backend/
│   ├── main.py          # FastAPI app + /generate endpoint
│   ├── models.py        # Pydantic request/response models
│   └── requirements.txt
├── frontend/
│   └── index.html       # Single-page UI (no build step)
├── .env.example
└── README.md
```

---

## Quick Start

### 1 — Backend

```bash
cd backend

# Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
cp ../.env.example .env
# Edit .env and add your OPENAI_API_KEY

# Authenticate Logfire (first time only)
logfire auth

# Start the server
uvicorn main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**.  
Interactive docs: **http://localhost:8000/docs**

### 2 — Frontend

Open `frontend/index.html` directly in your browser — no build step required.

> Make sure the backend is running on port 8000 before generating images.

---

## API

### `POST /generate`

**Request body**
```json
{ "prompt": "A futuristic city skyline at sunset" }
```

**Response**
```json
{
  "image_url": "https://oaidalleapiprodscus.blob.core.windows.net/...",
  "prompt": "A futuristic city skyline at sunset",
  "response_time_ms": 8423.5
}
```

---

## Observability — Pydantic Logfire

Every request is instrumented with structured spans and logs:

| Field               | Description                              |
|---------------------|------------------------------------------|
| `prompt`            | The user-supplied text prompt            |
| `response_status`   | `"success"` or error details             |
| `image_url_exists`  | `true` / `false`                         |
| `response_time_ms`  | End-to-end latency in milliseconds       |

View traces in the [Logfire dashboard](https://logfire.pydantic.dev).

---

## Environment Variables

| Variable         | Required | Description                     |
|------------------|----------|---------------------------------|
| `OPENAI_API_KEY` | ✅        | Your OpenAI API key             |
