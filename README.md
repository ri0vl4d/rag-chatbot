# RAG Chatbot

A retrieval-augmented generation chatbot that answers questions grounded in your own markdown documents.

- **Backend**: Python 3.11 + FastAPI + LangChain
- **LLM**: NVIDIA NIM (free tier, OpenAI-compatible) — `meta/llama-3.1-8b-instruct` by default
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (local, no API key)
- **Vector store**: FAISS in-memory
- **Frontend**: React + Vite + TypeScript + TailwindCSS
- **Deploy**: Render (free web service + free static site)

---

## Project structure

```
rag-chatbot/
├── backend/          FastAPI + RAG pipeline
│   ├── app/          Source code
│   ├── data/         >>> DROP YOUR .md FILES HERE <<<
│   ├── tests/        Pytest smoke tests
│   └── requirements.txt
├── frontend/         React chat UI
├── render.yaml       One-click Render deployment
└── SAMPLE_QUESTIONS.md   Test questionnaire
```

---

## 1. Get a free NVIDIA API key

1. Go to https://build.nvidia.com and sign up (email only — no credit card).
2. Pick any model (e.g. `meta/llama-3.1-8b-instruct`) → **Get API Key** → copy `nvapi-...`.
3. Free tier gives 1,000 requests/month per model.

---

## 2. Local setup — Backend

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and paste your NVIDIA key. Then drop your markdown files into `backend\data\`.

Start the server:

```cmd
uvicorn app.main:app --reload
```

You should see logs like:

```
INFO rag: Indexed 42 chunks from 1 file(s).
INFO rag: NVIDIA NIM client ready: meta/llama-3.1-8b-instruct
```

Test it:

```cmd
curl -X POST http://localhost:8000/api/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What is this document about?\",\"history\":[]}"
```

Run tests:

```cmd
pytest tests\ -v
```

---

## 3. Local setup — Frontend

```cmd
cd frontend
npm install
copy .env.example .env
npm run dev
```

Open http://localhost:5173.

---

## 4. Deploy to Render

### Option A: One-click with render.yaml (recommended)

1. Push this repo to GitHub.
2. In Render dashboard → **New +** → **Blueprint** → connect the repo.
3. Render reads `render.yaml` and creates both services.
4. In the **backend** service settings, add these env vars manually (marked `sync: false`):
   - `NVIDIA_API_KEY` = your key
   - `ALLOWED_ORIGINS` = `https://<your-frontend-name>.onrender.com`
   - `REINDEX_TOKEN` = any random string
5. In the **frontend** service settings, add:
   - `VITE_API_URL` = `https://<your-backend-name>.onrender.com`
6. Trigger a redeploy of the frontend after the backend URL is known.

### Option B: Manual (two services)

**Backend** — New Web Service, Python:
- Root Directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Env vars: `NVIDIA_API_KEY`, `NVIDIA_MODEL`, `ALLOWED_ORIGINS`, `REINDEX_TOKEN`, `HF_HOME=/opt/render/.cache/huggingface`

**Frontend** — New Static Site:
- Root Directory: `frontend`
- Build: `npm ci && npm run build`
- Publish Directory: `dist`
- Env var: `VITE_API_URL=https://<backend>.onrender.com`

### Render free-tier caveats

- Services spin down after 15 min of inactivity → first request after idle takes ~30–60 seconds (embedding model loads into memory). Warn viewers.
- 512 MB RAM ceiling. MiniLM + FAISS + FastAPI fits comfortably for small corpora (<5 MB of markdown).

---

## 5. Adding or updating documents

1. Drop new `.md` files into `backend/data/`.
2. Locally: just restart uvicorn.
3. On Render: either redeploy, or hit `/api/reindex`:

```cmd
curl -X POST https://<backend>.onrender.com/api/reindex ^
  -H "Authorization: Bearer <REINDEX_TOKEN>"
```

---

## 6. Testing the RAG agent

See `SAMPLE_QUESTIONS.md` — a 14-question rubric covering direct retrieval, multi-chunk synthesis, hallucination guarding, and paraphrase robustness.

---

## API reference

| Method | Path            | Description                                       |
|--------|-----------------|---------------------------------------------------|
| GET    | `/health`       | Liveness + indexed chunk count + model            |
| POST   | `/api/chat`     | `{ question, history }` → `{ answer, sources }`   |
| POST   | `/api/reindex`  | Rebuild FAISS from `data/` (bearer token required)|

---

## Tuning knobs (`.env`)

| Variable          | Default | Effect                                              |
|-------------------|---------|-----------------------------------------------------|
| `CHUNK_SIZE`      | 800     | Larger = fewer, denser chunks. Try 1200 for prose.  |
| `CHUNK_OVERLAP`   | 120     | Higher = less boundary loss, more index size.       |
| `RETRIEVER_K`     | 4       | More chunks in context → better recall, more tokens.|
| `LLM_TEMPERATURE` | 0.2     | Lower = more deterministic. 0.0 for max grounding.  |
| `LLM_MAX_TOKENS`  | 1024    | Cap on answer length.                               |

---

## Troubleshooting

- **503 "Index is empty"** — drop at least one `.md` into `backend/data/` and restart.
- **503 "LLM not configured"** — `NVIDIA_API_KEY` is missing or still the placeholder.
- **CORS error in browser** — add your frontend URL to `ALLOWED_ORIGINS`.
- **Slow first response** — cold start; MiniLM is loading (~15s). Second request is fast.
