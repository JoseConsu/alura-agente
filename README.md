# Santos Pegasus Agente

Agente de IA conversacional que responde preguntas sobre la documentación interna de Santos Pegasus Soluciones. Construido con LangGraph y FAISS como parte del challenge final de Alura.

**Demo en vivo:** [https://alura-agente-rlc22qglkm69xxktauqdgz.streamlit.app](https://alura-agente-rlc22qglkm69xxktauqdgz.streamlit.app)

---

## Descripción

Cualquier persona del equipo puede hacer preguntas en lenguaje natural sobre los manuales y guías de la empresa. El agente utiliza RAG (Retrieval-Augmented Generation) para buscar en los documentos cargados y devuelve la respuesta con la fuente. Mantiene historial de conversación para preguntas de seguimiento.

Los documentos están organizados por categorías:

```
documents/
├── onboarding/    ← Manual de incorporación para nuevos desarrolladores
├── backend/       ← Guía de ingeniería back-end
├── frontend/      ← Guía de ingeniería front-end
├── incidentes/    ← Protocolo de respuesta a incidentes
└── arquitectura/  ← Arquitectura de microservicios
```

---

## Arquitectura

```
Usuario (Streamlit UI)
       │
       ▼
  app.py / POST /api/chat
       │
       ▼
LangGraph ReAct Agent (agent/graph.py)
       │
       └── search_documents ──► FAISS index (rag/retriever.py)
                                      │
                               HuggingFace Embeddings
                                      │
                               PDFs + CSVs en documents/
```

**Flujo por request:**
1. El agente recibe la pregunta (y el historial de la conversación si existe).
2. Llama a `search_documents` con la query y, cuando corresponde, filtra por categoría.
3. FAISS devuelve los chunks más relevantes con sus metadatos (nombre de archivo, categoría).
4. El LLM (Groq) sintetiza la respuesta a partir del contexto recuperado.

El índice FAISS se construye una vez en startup y se persiste en disco. En arranques posteriores se carga directamente sin reconstruir.

---

## Tecnologías

| Componente | Tecnología |
|---|---|
| UI | Streamlit |
| Backend | FastAPI + uvicorn |
| Orquestación de agente | LangGraph (`create_react_agent`) |
| LLM | Groq API — `llama-3.1-8b-instant` |
| Embeddings | HuggingFace — `paraphrase-multilingual-MiniLM-L12-v2` |
| Búsqueda vectorial | FAISS (local) |
| Carga de documentos | LangChain — `PyPDFLoader`, `CSVLoader` |
| Deploy | Streamlit Community Cloud |

---

## Instalación y ejecución local

**Requisitos:** Python 3.10+ y una API key de Groq (gratis en [console.groq.com](https://console.groq.com))

```bash
git clone https://github.com/JoseConsu/alura-agente.git
cd alura-agente

pip install -r requirements.txt

# Crear backend/.env con tu API key
echo "GROQ_API_KEY=tu_key_aqui" > backend/.env
```

Colocar los PDFs en las subcarpetas de `documents/` (una por categoría).

**Iniciar la interfaz web:**
```bash
streamlit run app.py
```

**O iniciar solo el API backend:**
```bash
cd backend
python main.py
```

El servidor queda en `http://localhost:8000`. La primera vez construye el índice FAISS (puede tardar unos minutos).

### Variables de entorno

```
GROQ_API_KEY        = (obligatoria)
GROQ_MODEL_NAME     = llama-3.1-8b-instant
DOCUMENTS_PATH      = ../documents
FAISS_INDEX_PATH    = ./faiss_index
EMBEDDINGS_MODEL    = sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
CHUNK_SIZE          = 300
CHUNK_OVERLAP       = 50
```

---

## Endpoint API

```
POST /api/chat
Content-Type: application/json

{
  "query": "¿Cuál es el proceso de onboarding para nuevos devs?",
  "history": []
}
```

Respuesta:
```json
{
  "response": "El proceso de onboarding de Santos Pegasus dura 3 semanas...",
  "source": "Manual de Onboarding.pdf"
}
```

---

## Ejemplos de preguntas

**Onboarding**
- ¿Qué herramientas necesito instalar en mi primera semana?
- ¿Cuánto dura el período de onboarding y qué cubre cada etapa?
- ¿Quién es el responsable de acompañar a los nuevos desarrolladores?

**Back-end**
- ¿Cuáles son los estándares de manejo de errores en la API REST?
- ¿Qué framework de testing usa el equipo de back-end?
- ¿Cómo se estructura un endpoint nuevo en el proyecto?

**Incidentes**
- ¿Qué pasos hay que seguir cuando cae un servicio en producción?
- ¿Cómo se estructura un post-mortem en Santos Pegasus?
- ¿Cuáles son los niveles de severidad de incidentes?

**Arquitectura**
- ¿Cómo se comunican los microservicios entre sí?
- ¿Qué servicio es el responsable de la autenticación?
- ¿Cuál es la estrategia de base de datos por servicio?

---

## Ejemplos de respuestas del agente

**Pregunta:** ¿Qué herramientas necesito instalar en mi primera semana?

**Respuesta:**
> Según el Manual de Onboarding de Santos Pegasus, en la primera semana debes instalar: Git, Docker, Node.js (versión LTS), Python 3.10+, el cliente de la VPN corporativa, y configurar acceso al repositorio interno. El equipo de DevOps te enviará las credenciales por correo el día de ingreso.
>
> *Fuente: Manual de Onboarding.pdf*

---

**Pregunta:** ¿Qué pasos hay que seguir cuando cae un servicio en producción?

**Respuesta:**
> El protocolo de respuesta a incidentes de Santos Pegasus establece los siguientes pasos: 1) Notificar al canal #incidentes de inmediato, 2) Asignar un Incident Commander del equipo de guardia, 3) Evaluar el nivel de severidad (P1 a P4), 4) Iniciar el bridge de comunicación si es P1 o P2, 5) Aplicar mitigación (rollback o hotfix), 6) Documentar la línea de tiempo, 7) Redactar el post-mortem dentro de las 48 horas siguientes.
>
> *Fuente: Protocolo de Respuesta a Incidentes.pdf*

---

## Deploy

La aplicación está desplegada en Streamlit Community Cloud.

**URL pública:** [https://alura-agente-rlc22qglkm69xxktauqdgz.streamlit.app](https://alura-agente-rlc22qglkm69xxktauqdgz.streamlit.app)

Para replicar el deploy en Streamlit Cloud:
1. Hacer fork del repositorio en GitHub.
2. Ir a [share.streamlit.io](https://share.streamlit.io) y conectar el repo.
3. Configurar el secreto `GROQ_API_KEY` en Settings → Secrets.
4. Streamlit Cloud instala las dependencias de `requirements.txt` automáticamente y ejecuta `app.py`.
