from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pathlib import Path
import pandas as pd
import config


def load_pdfs(directory: Path) -> list[Document]:
    docs = []
    for path in directory.rglob("*.pdf"):
        loader = PyPDFLoader(str(path))
        pages = loader.load()
        for page in pages:
            page.metadata["source"] = path.name
            page.metadata["category"] = path.parent.name
        docs.extend(pages)
    return docs


def load_csvs(directory: Path) -> list[Document]:
    docs = []
    block_size = 20
    for path in directory.rglob("*.csv"):
        df = pd.read_csv(path)
        for i in range(0, len(df), block_size):
            content = df.iloc[i : i + block_size].to_string(index=False)
            docs.append(Document(page_content=content, metadata={"source": path.name, "category": path.parent.name}))
    return docs


def load_all_documents() -> list[Document]:
    pdfs = load_pdfs(config.DOCUMENTS_PATH)
    csvs = load_csvs(config.DOCUMENTS_PATH)
    print(f"Documentos cargados: {len(pdfs)} páginas PDF, {len(csvs)} bloques CSV")
    return pdfs + csvs
