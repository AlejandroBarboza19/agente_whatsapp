from fastapi import FastAPI
from app.routers import webhook

app = FastAPI(title="Agente WhatsApp")

app.include_router(webhook.router)


@app.get("/")
async def home():
    return {"message": "Servidor funcionando"}
