from pydantic import BaseModel, Field
from typing import Optional, List


class TextMessage(BaseModel):
    body: str


class Message(BaseModel):
    id: str
    from_: str = Field(alias="from")
    timestamp: str
    type: str
    text: Optional[TextMessage] = None

    model_config = {"populate_by_name": True}


class Value(BaseModel):
    messaging_product: str
    messages: Optional[List[Message]] = None


class Change(BaseModel):
    value: Value
    field: str


class Entry(BaseModel):
    id: str
    changes: List[Change]


class WebhookPayload(BaseModel):
    object: str
    entry: List[Entry]
