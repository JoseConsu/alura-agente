import sys
import os

sys.path.insert(0, "backend")
os.environ.setdefault("DOCUMENTS_PATH", "documents")
os.environ.setdefault("FAISS_INDEX_PATH", "/tmp/faiss_index")
os.environ.setdefault("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

import streamlit as st
from rag.loader import load_all_documents
from rag.embeddings import iniciar_indice
from agent.graph import build_graph
from models.factory import crear_llm
import index_store

st.set_page_config(
    page_title="Santos Pegasus Agente",
    page_icon="🤖",
    layout="centered",
)

st.title("Santos Pegasus Agente")
st.caption("Asistente de documentacion interna · Santos Pegasus Soluciones")


@st.cache_resource(show_spinner="Cargando documentos e indice...")
def cargar_agente():
    docs = load_all_documents()
    index_store.index = iniciar_indice(docs)
    llm = crear_llm()
    return build_graph(llm, index_store.index)


agent = cargar_agente()

if "historial" not in st.session_state:
    st.session_state.historial = []

for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("source") and msg["role"] == "assistant":
            st.caption(f"Fuente: {msg['source']}")

if pregunta := st.chat_input("Hace una pregunta sobre la documentacion..."):
    st.session_state.historial.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.write(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Buscando..."):
            mensajes_input = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.historial
            ]
            result = agent.invoke({"messages": mensajes_input})
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
                    b.get("text", "") if isinstance(b, dict) else str(b)
                    for b in response
                )

            st.write(response)
            if source:
                st.caption(f"Fuente: {source}")

    st.session_state.historial.append({
        "role": "assistant",
        "content": response,
        "source": source,
    })
