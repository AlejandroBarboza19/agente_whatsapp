from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


@app.get("/")
async def home():
    return {"message": "Servidor funcionando"}


# VERIFICAR WEBHOOK
@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):

    if hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge)

    return PlainTextResponse(content="Token inválido", status_code=403)


# RECIBIR MENSAJES
@app.post("/webhook")
async def receive_message(request: Request):

    body = await request.json()

    print("MENSAJE RECIBIDO:")
    print(body)

    try:

        message = body["entry"][0]["changes"][0]["value"]["messages"][0]

        phone = message["from"]

        text = message["text"]["body"]

        print(f"Usuario: {phone}")
        print(f"Mensaje: {text}")

        send_whatsapp_message(
            phone,
            f"Hola 👋 perra  dijiste: {text}"
        )

    except Exception as e:
        print("ERROR:", e)

    return {"status": "ok"}


# ENVIAR MENSAJE
def send_whatsapp_message(phone, message):

    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    print(response.text)