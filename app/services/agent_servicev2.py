import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from langchain_community.agent_toolkits import create_sql_agent # kit de herramientes para ejecutar consultas SQL
from app.core.agent_conexion import db_for_agent
from langchain_core.messages import SystemMessage # para crear mensajes del sistema 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # para darle el promt al agente
from langchain_community.chat_message_histories import ChatMessageHistory # para crear un historial de mensajes
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)


prompt = ChatPromptTemplate.from_messages([
    ("""
     Eres un asesor de ventas llamado Aeron de la marca de ropa targaryen asesoras correcmente a nuestro clientes,
     eres muy cariñoso y simpatico. tienes acceso a la base de datos donde en la tabla productos podras 
     ver nuestra ropa disponible, solo te tiene permitido usar consultas select pero en la tabla ventas si tienes permitido insertar las ventas que hayas realizado
     """),
    MessagesPlaceholder(variable_name="history"),("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# inyeccion de la bd al agente

db_and_agent = create_sql_agent(
    llm=llm,
    db=db_for_agent,
    prompt=prompt,
    agent_type="openai-tools"
)

_historiales: dict[str, ChatMessageHistory] = {}

def get_historial(session_id: str) -> ChatMessageHistory:
    if session_id not in _historiales:
        _historiales[session_id] = ChatMessageHistory()
    return  _historiales[session_id]

agent = RunnableWithMessageHistory(
    runnable=db_and_agent,
    get_session_history=get_historial,
    input_messages_key="input",
    history_messages_key="history"
)

def process_message(phone: str, text: str) -> str:
    result = agent.invoke(
        {"input": text},
        config={"configurable": {"session_id": phone}}
    )
    
    return result["output"]