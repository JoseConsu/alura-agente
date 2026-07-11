from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from rag.loader import load_all_documents
from rag.embeddings import iniciar_indice
import index_store
import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando servidor...")
    docs = load_all_documents()
    index_store.index = iniciar_indice(docs)
    print("Listo.")
    yield
    print("Cerrando servidor...")


app = FastAPI(title="Santos Pegasus Agent", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=True)
