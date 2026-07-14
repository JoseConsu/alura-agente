from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def retrieve(index: FAISS, query: str, category: str | None = None, k: int = 5) -> list[Document]:
    if category:
        return index.similarity_search(query, k=k, filter={"category": category})
    return index.similarity_search(query, k=k)


def format_context(documents: list[Document]) -> str:
    parts = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "desconocido")
        category = doc.metadata.get("category", "")
        label = f"{source} [{category}]" if category else source
        parts.append(f"[{i}] ({label})\n{doc.page_content}")
    return "\n\n".join(parts)
