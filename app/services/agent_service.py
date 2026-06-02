from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import get_settings

settings = get_settings()

# LLM via OpenRouter con cliente OpenAI
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",        # cambia el modelo según necesites
    openai_api_key=settings.OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
)

SYSTEM_PROMPT = """Eres un asistente útil que puede consultar y operar 
sobre una base de datos PostgreSQL. Responde siempre en español y de forma concisa."""


def process_message(phone: str, text: str, db: Session) -> str:
    """
    Recibe el mensaje del usuario, consulta la DB si es necesario
    y devuelve la respuesta del agente.
    """
    # Ejemplo: puedes pasar contexto de la DB al agente
    # context = db.execute(text("SELECT ...")).fetchall()

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=text),
    ]

    response = llm.invoke(messages)
    return response.content
