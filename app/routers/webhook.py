import requests
from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.schemas.whatsapp import WebhookPayload
from app.services.agent_servicev2 import process_message

router = APIRouter()
settings = get_settings()


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None,
):
    if hub_verify_token == settings.VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge)
    return PlainTextResponse(content="Token inválido", status_code=403)


@router.post("/webhook")
async def receive_message(
    request: Request,
    db: Session = Depends(get_db),
):
    body = await request.json()

    try:
        payload = WebhookPayload(**body)

        for entry in payload.entry:
            for change in entry.changes:
                messages = change.value.messages
                if not messages:
                    continue

                for message in messages:
                    if message.type != "text" or not message.text:
                        continue

                    phone = message.from_
                    text = message.text.body

                    print(f"[{phone}]: {text}")

                    response_text = process_message(phone, text)
                    _send_whatsapp_message(phone, response_text)

    except Exception as e:
        print("ERROR en webhook:", e)

    return {"status": "ok"}


def _send_whatsapp_message(phone: str, message: str):
    url = f"https://graph.facebook.com/v25.0/{settings.PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message},
    }

    response = requests.post(url, headers=headers, json=data)
    print("WhatsApp API:", response.text)
