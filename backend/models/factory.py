from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
import config


def crear_llm() -> BaseChatModel:
    return ChatGroq(
        model=config.GROQ_MODEL_NAME,
        api_key=config.GROQ_API_KEY,
        temperature=0.3,
    )
