from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel
from langchain_community.vectorstores import FAISS
from agent.tools import make_search_docs_tool


SYSTEM_PROMPT = """Eres el asistente interno de Santos Pegasus Soluciones.
Respondes preguntas del equipo de desarrollo usando exclusivamente la documentación interna de la empresa.

Siempre llama a search_documents antes de responder, nunca desde tu conocimiento propio.
Puedes usar el parámetro category para filtrar: 'onboarding' para temas de incorporación, 'backend' para guías de ingeniería back-end, 'frontend' para front-end, 'incidentes' para protocolos de respuesta a incidentes, y 'arquitectura' para microservicios.

Responde siempre en el mismo idioma que la pregunta. Si no encuentras nada relevante, dilo directamente."""


def build_graph(llm: BaseChatModel, index: FAISS):
    tools = [make_search_docs_tool(index)]
    return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
