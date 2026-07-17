from typing import Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    history: list[Message] = Field(default_factory=list)


class Source(BaseModel):
    content: str
    source: str
    chunk_id: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


class HealthResponse(BaseModel):
    status: str
    indexed_chunks: int
    model: str


class ReindexResponse(BaseModel):
    status: str
    files: int
    chunks: int
