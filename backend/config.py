from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")

DOCUMENTS_PATH: Path = Path(os.getenv("DOCUMENTS_PATH", "../documents")).resolve()
FAISS_INDEX_PATH: Path = Path(os.getenv("FAISS_INDEX_PATH", "./faiss_index")).resolve()
EMBEDDINGS_MODEL: str = os.getenv(
    "EMBEDDINGS_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 300))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 50))

HOST: str = os.getenv("HOST", "localhost")
PORT: int = int(os.getenv("PORT", 8000))

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY no está configurada en el archivo .env")

if not DOCUMENTS_PATH.exists():
    raise FileNotFoundError(f"La carpeta de documentos no existe: {DOCUMENTS_PATH}")
