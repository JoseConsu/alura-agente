from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from rag.retriever import retrieve, format_context


def make_search_docs_tool(index: FAISS):
    @tool
    def search_documents(query: str, category: str | None = None) -> str:
        """Busca en los documentos internos. Filtra por category si se especifica."""
        docs = retrieve(index, query, category=category)
        if not docs:
            return "No encontré información relevante en los documentos."
        sources = list({d.metadata.get("source", "docs") for d in docs})
        return format_context(docs) + f"\n__source__:{sources[0]}"

    return search_documents
