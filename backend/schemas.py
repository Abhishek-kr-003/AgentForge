
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ConversationCreate(BaseModel):
    title: str = "New Chat"


class MessageCreate(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationDetail(ConversationResponse):
    messages: list[MessageResponse]
