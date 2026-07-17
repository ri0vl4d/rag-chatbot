"""Smoke tests — verify loader, splitter, and vector store work end-to-end.

These tests do NOT hit NVIDIA NIM (no API key required). They cover only the
retrieval half of the pipeline.
"""
import tempfile
from pathlib import Path

import pytest

from app.rag.loader import load_markdown_files
from app.rag.splitter import split_documents
from app.rag.vectorstore import build_vectorstore


SAMPLE_MD = """# Sample Doc

## Section A
The Eiffel Tower is located in Paris, France. It was completed in 1889.

## Section B
The Great Wall of China stretches over 21,000 kilometers.

## Section C
Photosynthesis converts sunlight into chemical energy in plants.
"""


@pytest.fixture
def temp_data_dir():
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "sample.md").write_text(SAMPLE_MD, encoding="utf-8")
        yield td


def test_loader_reads_markdown(temp_data_dir):
    docs = load_markdown_files(temp_data_dir)
    assert len(docs) == 1
    assert "Eiffel Tower" in docs[0].page_content
    assert docs[0].metadata["source"] == "sample.md"


def test_splitter_creates_chunks(temp_data_dir):
    docs = load_markdown_files(temp_data_dir)
    chunks = split_documents(docs, chunk_size=100, chunk_overlap=20)
    assert len(chunks) >= 2
    assert all("chunk_id" in c.metadata for c in chunks)


def test_vectorstore_retrieves_relevant_chunk(temp_data_dir):
    docs = load_markdown_files(temp_data_dir)
    chunks = split_documents(docs, chunk_size=200, chunk_overlap=40)
    vs = build_vectorstore(chunks, "sentence-transformers/all-MiniLM-L6-v2")
    results = vs.similarity_search("Where is the Eiffel Tower?", k=1)
    assert len(results) == 1
    assert "Paris" in results[0].page_content
