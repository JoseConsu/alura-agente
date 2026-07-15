from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_community.tools import DuckDuckGoSearchRun
from rag.retriever import retrieve, format_context


def make_search_docs_tool(index: FAISS):
    @tool
    def search_documents(query: str, category: str | None = None) -> str:
        """Busca en los documentos internos. Filtra por category si se especifica."""
        docs = retrieve(index, query, category=category)
        if not docs:
            return "No encontré información relevante en los documentos.\n__source__:docs"
        sources = list({d.metadata.get("source", "docs") for d in docs})
        return format_context(docs) + f"\n__source__:{sources[0]}"

    return search_documents


def make_web_search_tool():
    ddg = DuckDuckGoSearchRun()

    @tool
    def web_search(query: str) -> str:
        """Busca en internet cuando los documentos internos no tienen la respuesta."""
        result = ddg.run(query)
        return result + "\n__source__:web"

    return web_search
