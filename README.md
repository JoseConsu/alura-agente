# Santos Pegasus Agente

Agente de IA que responde preguntas sobre la documentación interna de Santos Pegasus Soluciones. Construido con FastAPI, LangGraph y FAISS como parte del challenge final de Alura.

## ¿Qué hace?

Cualquier persona del equipo puede hacer preguntas en lenguaje natural sobre los manuales y guías de la empresa. El agente busca en los documentos cargados y devuelve la respuesta con la fuente. Si no encuentra nada relevante, busca en internet como fallback.

## Arquitectura

```
POST /api/chat
     │
     ▼
FastAPI (api/routes.py)
     │
     ▼
LangGraph ReAct Agent (agent/graph.py)
     │
     ├── search_documents ──► FAISS index (rag/retriever.py)
     │                              │
     │                         documentos cargados en startup
     │                         (PDFs + CSVs de documents/)
     │
     └── web_search ──► DuckDuckGo (fallback)
```

El índice FAISS se construye una vez al arrancar el servidor y se guarda en disco. En arranques posteriores se carga desde `faiss_index/` sin necesidad de reconstruir.

Cada documento se carga con su categoría (`onboarding`, `backend`, `frontend`, `incidentes`, `arquitectura`) según la carpeta donde esté. La herramienta `search_documents` puede filtrar por categoría cuando la pregunta lo requiere.

## Tech stack

- Python 3.x
- FastAPI + uvicorn
- LangGraph (`create_react_agent`)
- Groq API — `llama-3.1-8b-instant`
- HuggingFace Embeddings — `paraphrase-multilingual-MiniLM-L12-v2`
- FAISS (búsqueda vectorial local)
- DuckDuckGo Search (fallback web)

## Requisitos

- Python 3.10+
- API key de Groq (gratis en [console.groq.com](https://console.groq.com))

## Instalación y ejecución local

```bash
git clone https://github.com/josedconsuegram/alura-agente.git
cd alura-agente/backend

pip install -r requirements.txt

cp .env.example .env
# editar .env y agregar GROQ_API_KEY
```

Colocar los PDFs en las subcarpetas de `documents/`:
```
documents/
├── onboarding/   ← Manual de incorporación
├── backend/      ← Guía de ingeniería back-end
├── frontend/     ← Guía de ingeniería front-end
├── incidentes/   ← Protocolo de respuesta a incidentes
└── arquitectura/ ← Arquitectura de microservicios
```

```bash
python main.py
```

El servidor queda en `http://localhost:8000`. La primera vez construye el índice FAISS (puede tardar unos minutos dependiendo del volumen de documentos).

## Endpoint

```
POST /api/chat
Content-Type: application/json

{
  "query": "¿Cuál es el proceso de onboarding para nuevos devs?",
  "history": []  // opcional, lista de mensajes anteriores
}
```

Respuesta:
```json
{
  "response": "El proceso de onboarding de Santos Pegasus dura 3 semanas...",
  "source": "Manual de Onboarding para Nuevos Desarrolladores.pdf"
}
```

## Ejemplos

**Onboarding**
> ¿Qué herramientas necesito instalar en mi primera semana?

> ¿Cuánto dura el período de onboarding y qué cubre cada etapa?

**Back-end**
> ¿Cuáles son los estándares de manejo de errores en la API REST?

> ¿Qué framework de testing usa el equipo de back-end?

**Incidentes**
> ¿Qué pasos hay que seguir cuando cae un servicio en producción?

> ¿Cómo se estructura un post-mortem en Santos Pegasus?

**Arquitectura**
> ¿Cómo se comunican los microservicios entre sí?

> ¿Qué servicio es el responsable de la autenticación?

## Deploy en OCI

La aplicación está desplegada en Oracle Cloud Infrastructure (Always Free tier).

**URL:** `http://<IP_OCI>:8000`

<!-- agregar screenshot o URL pública después del deploy -->

### Pasos para replicar el deploy

1. Crear instancia `VM.Standard.A1.Flex` (Ubuntu 22.04) en OCI
2. Abrir el puerto 8000 en el Security List de OCI y en el firewall del OS:
   ```bash
   sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
   sudo netfilter-persistent save
   ```
3. En la VM:
   ```bash
   sudo apt install -y python3-pip python3-venv git screen
   git clone https://github.com/josedconsuegram/alura-agente.git
   cd alura-agente/backend
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   # crear .env con HOST=0.0.0.0 y GROQ_API_KEY
   bash start.sh
   ```
4. Subir los PDFs via SCP:
   ```bash
   scp -i clave.pem -r documents/ ubuntu@<IP_OCI>:~/alura-agente/
   ```
