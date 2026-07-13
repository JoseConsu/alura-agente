from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import config


def cargar_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=config.EMBEDDINGS_MODEL)


def build_index(documents: list[Document]) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"{len(documents)} documentos → {len(chunks)} fragmentos")

    embeddings = cargar_embeddings()
    index = FAISS.from_documents(chunks, embeddings)

    config.FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)
    index.save_local(str(config.FAISS_INDEX_PATH))
    print(f"Índice guardado en {config.FAISS_INDEX_PATH}")
    return index


def load_index() -> FAISS:
    embeddings = cargar_embeddings()
    return FAISS.load_local(
        str(config.FAISS_INDEX_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def iniciar_indice(documents: list[Document]) -> FAISS:
    try:
        index = load_index()
        print("Índice cargado desde disco")
        return index
    except Exception:
        print("Construyendo índice...")
        return build_index(documents)
