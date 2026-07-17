from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def build_vectorstore(chunks: list[Document], embedding_model: str) -> FAISS:
    """Embed chunks with a lightweight ONNX model and index them in FAISS."""
    if not chunks:
        raise ValueError(
            "No chunks to index. Drop at least one .md file into the data/ directory."
        )
    embeddings = FastEmbedEmbeddings(model_name=embedding_model)
    return FAISS.from_documents(chunks, embeddings)
