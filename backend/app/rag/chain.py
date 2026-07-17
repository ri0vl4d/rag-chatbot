from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA


SYSTEM_PROMPT = """You are a helpful assistant that answers questions strictly using the provided context.

Rules:
1. Base your answer ONLY on the context below. Do not use outside knowledge.
2. If the context does not contain the answer, reply exactly: "I don't know based on the provided documents."
3. Be concise and factual. Cite the source filenames inline like [source.md] when possible.
4. Do not invent, guess, or extrapolate.

Context:
{context}
"""

USER_PROMPT = "Question: {question}\n\nAnswer:"


def build_llm(api_key: str, model: str, base_url: str, temperature: float, max_tokens: int) -> ChatNVIDIA:
    return ChatNVIDIA(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def format_context(docs: list[Document]) -> str:
    parts = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        parts.append(f"[{src}]\n{d.page_content}")
    return "\n\n---\n\n".join(parts)


async def answer_question(
    question: str,
    vectorstore: FAISS,
    llm: ChatNVIDIA,
    k: int,
) -> tuple[str, list[Document]]:
    """Retrieve top-k chunks via MMR, then generate a grounded answer."""
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": max(k * 3, 12), "lambda_mult": 0.5},
    )
    docs = await retriever.ainvoke(question)
    context = format_context(docs)

    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("user", USER_PROMPT)]
    )
    chain = prompt | llm
    result = await chain.ainvoke({"context": context, "question": question})
    answer = result.content if hasattr(result, "content") else str(result)
    return answer, docs
