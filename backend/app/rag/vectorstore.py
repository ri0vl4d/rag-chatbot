from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


def build_vectorstore(chunks: list[Document], embedding_model: str) -> FAISS:
    """Embed chunks with a local HuggingFace model and index them in FAISS."""
    if not chunks:
        raise ValueError(
            "No chunks to index. Drop at least one .md file into the data/ directory."
        )
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return FAISS.from_documents(chunks, embeddings)
