import pytest
from rag.loader import load_all_documents
from rag.embeddings import iniciar_indice
from rag.retriever import retrieve, format_context


@pytest.fixture(scope="module")
def index():
    return iniciar_indice(load_all_documents())


def test_retrieve_returns_list(index):
    results = retrieve(index, "información general")
    assert isinstance(results, list)


def test_retrieve_limite_k(index):
    results = retrieve(index, "información general", k=3)
    assert len(results) <= 3


def test_formato_string(index):
    docs = retrieve(index, "información general")
    ctx = format_context(docs)
    assert isinstance(ctx, str)
    assert len(ctx) > 0


def test_formato_incluye_source(index):
    docs = retrieve(index, "información general")
    ctx = format_context(docs)
    assert "(" in ctx
