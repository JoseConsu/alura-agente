from langchain_core.documents import Document
from rag.loader import load_all_documents


def test_load_returns_list():
    docs = load_all_documents()
    assert isinstance(docs, list)


def test_tipo_documentos():
    docs = load_all_documents()
    assert all(isinstance(d, Document) for d in docs)


def test_metadata_source():
    docs = load_all_documents()
    for doc in docs:
        assert "source" in doc.metadata
        assert len(doc.metadata["source"]) > 0
