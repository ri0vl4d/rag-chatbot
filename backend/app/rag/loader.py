from pathlib import Path
from langchain_core.documents import Document


def load_markdown_files(data_dir: str) -> list[Document]:
    """Load every .md file under data_dir into LangChain Documents.

    Each Document is tagged with metadata.source = filename so we can cite it later.
    """
    base = Path(data_dir)
    if not base.exists():
        return []

    docs: list[Document] = []
    for md_path in sorted(base.rglob("*.md")):
        text = md_path.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            continue
        docs.append(
            Document(
                page_content=text,
                metadata={"source": md_path.name, "path": str(md_path.relative_to(base))},
            )
        )
    return docs
