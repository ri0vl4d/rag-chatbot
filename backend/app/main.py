import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

IST = timezone(timedelta(hours=5, minutes=30))

from app.config import settings
from app.rag.chain import answer_question, build_llm
from app.rag.loader import load_markdown_files
from app.rag.splitter import split_documents
from app.rag.vectorstore import build_vectorstore
from app.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    ReindexResponse,
    Source,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("rag")


class AppState:
    vectorstore = None
    llm = None
    chunk_count = 0
    file_count = 0


state = AppState()


def index_corpus() -> tuple[int, int]:
    """(Re)build the FAISS index from data/. Returns (files, chunks)."""
    docs = load_markdown_files(settings.data_dir)
    if not docs:
        logger.warning(
            "No .md files found in %s — /api/chat will return 503 until you add some.",
            settings.data_dir,
        )
        state.vectorstore = None
        state.chunk_count = 0
        state.file_count = 0
        return 0, 0

    chunks = split_documents(docs, settings.chunk_size, settings.chunk_overlap)
    state.vectorstore = build_vectorstore(chunks, settings.embedding_model)
    state.chunk_count = len(chunks)
    state.file_count = len(docs)
    logger.info("Indexed %d chunks from %d file(s).", len(chunks), len(docs))
    return len(docs), len(chunks)


async def self_ping_loop() -> None:
    """Ping configured URLs every interval, only within the IST active window."""
    urls = settings.self_ping_url_list
    if not urls:
        logger.info("Self-ping disabled (SELF_PING_URLS not set).")
        return
    start_h = settings.self_ping_start_hour_ist
    end_h = settings.self_ping_end_hour_ist
    logger.info(
        "Self-ping active %02d:00–%02d:00 IST every %ds for %d URL(s).",
        start_h, end_h, settings.self_ping_interval_seconds, len(urls),
    )
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            try:
                now_ist = datetime.now(IST)
                h = now_ist.hour
                in_window = (start_h <= h < end_h) if start_h < end_h else (h >= start_h or h < end_h)
                if in_window:
                    for url in urls:
                        try:
                            r = await client.get(url)
                            logger.info("Self-ping %s -> %d", url, r.status_code)
                        except Exception as e:
                            logger.warning("Self-ping %s failed: %s", url, e)
                await asyncio.sleep(settings.self_ping_interval_seconds)
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Self-ping loop error")
                await asyncio.sleep(settings.self_ping_interval_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up — building index and LLM client.")
    index_corpus()
    if settings.nvidia_api_key and settings.nvidia_api_key != "nvapi-REPLACE_ME":
        state.llm = build_llm(
            api_key=settings.nvidia_api_key,
            model=settings.nvidia_model,
            base_url=settings.nvidia_base_url,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )
        logger.info("NVIDIA NIM client ready: %s", settings.nvidia_model)
    else:
        logger.warning("NVIDIA_API_KEY missing — /api/chat will return 503 until set.")
    ping_task = asyncio.create_task(self_ping_loop())
    yield
    ping_task.cancel()
    logger.info("Shutting down.")


app = FastAPI(title="RAG Chatbot", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        indexed_chunks=state.chunk_count,
        model=settings.nvidia_model,
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if state.vectorstore is None:
        raise HTTPException(status_code=503, detail="Index is empty. Add .md files to data/ and reindex.")
    if state.llm is None:
        raise HTTPException(status_code=503, detail="LLM not configured. Set NVIDIA_API_KEY.")

    try:
        answer, docs = await answer_question(
            question=req.question,
            vectorstore=state.vectorstore,
            llm=state.llm,
            k=settings.retriever_k,
        )
    except Exception as e:
        logger.exception("Chat pipeline failed")
        raise HTTPException(status_code=500, detail=f"Chat failed: {e!s}") from e

    sources = [
        Source(
            content=d.page_content,
            source=d.metadata.get("source", "unknown"),
            chunk_id=d.metadata.get("chunk_id"),
        )
        for d in docs
    ]
    return ChatResponse(answer=answer, sources=sources)


def _require_token(authorization: str | None = Header(default=None)) -> None:
    expected = f"Bearer {settings.reindex_token}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/api/reindex", response_model=ReindexResponse, dependencies=[Depends(_require_token)])
async def reindex():
    files, chunks = index_corpus()
    return ReindexResponse(status="ok", files=files, chunks=chunks)
