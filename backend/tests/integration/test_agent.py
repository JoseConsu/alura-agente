import pytest
from agent.graph import build_graph
from rag.loader import load_all_documents
from rag.embeddings import iniciar_indice
from models.factory import crear_llm


@pytest.fixture(scope="module")
def agent():
    llm = crear_llm()
    index = iniciar_indice(load_all_documents())
    return build_graph(llm, index)


def get_response(agent, query: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    response = result["messages"][-1].content
    if isinstance(response, list):
        response = " ".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in response
        )
    return response


def test_agent_responds(agent):
    r = get_response(agent, "¿De qué tratan los documentos?")
    assert isinstance(r, str) and len(r) > 0


def test_agent_doc_query_not_empty(agent):
    r = get_response(agent, "Resume el contenido principal")
    assert len(r) > 20


def test_agent_falls_back_to_web(agent):
    r = get_response(agent, "¿Qué es la teoría de la relatividad de Einstein?")
    assert len(r) > 0
