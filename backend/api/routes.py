from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agent.graph import build_graph
from models.factory import crear_llm
import index_store


router = APIRouter()

errores_conocidos = [
    ("api_key_invalid", 401, "API key inválida."),
    ("invalid_api_key", 401, "API key inválida."),
    ("authentication_error", 401, "Error de autenticación con el proveedor LLM."),
    ("rate_limit_exceeded", 429, "Límite de solicitudes alcanzado. Intenta de nuevo en unos segundos."),
    ("request too large", 413, "La consulta es demasiado larga."),
    ("context_length_exceeded", 413, "La consulta supera el límite de contexto del modelo."),
]


def error_http(e: Exception) -> HTTPException:
    msg = str(e).lower()
    for patron, status, detalle in errores_conocidos:
        if patron in msg:
            return HTTPException(status_code=status, detail=detalle)
    return HTTPException(status_code=500, detail="Error interno del agente.")


class ChatRequest(BaseModel):
    query: str
    history: list[dict] = []


class ChatResponse(BaseModel):
    response: str
    source: str | None = None


@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    try:
        llm = crear_llm()
        agent = build_graph(llm, index_store.index)

        messages = body.history if body.history else [{"role": "user", "content": body.query}]
        result = agent.invoke({"messages": messages})
        mensajes = result["messages"]

        source = None
        for msg in reversed(mensajes):
            content = getattr(msg, "content", "") or ""
            if "__source__:" in content:
                source = content.split("__source__:")[-1].strip().split("\n")[0]
                break

        response = mensajes[-1].content
        if isinstance(response, list):
            response = " ".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in response
            )

        return ChatResponse(response=response, source=source)
    except HTTPException:
        raise
    except Exception as e:
        raise error_http(e)
