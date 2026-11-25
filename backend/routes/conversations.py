
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.chat_history import (
    create_conversation,
    get_conversations,
    get_conversation,
    add_message,
    delete_conversation,
)
from backend.schemas import (
    ConversationCreate,
    ConversationResponse,
    ConversationDetail,
    MessageCreate,
    MessageResponse,
)

router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversations"],
)


# Create a conversation
@router.post("", response_model=ConversationResponse)
def create_new_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
):
    return create_conversation(db, data.title)


# Get all conversations
@router.get("", response_model=list[ConversationResponse])
def read_conversations(
    db: Session = Depends(get_db),
):
    return get_conversations(db)


# Get one conversation with its messages
@router.get("/{conversation_id}", response_model=ConversationDetail)
def read_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation = get_conversation(db, conversation_id)

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return conversation


# Add a message to a conversation
@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
)
def create_message(
    conversation_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
):
    message = add_message(
        db,
        conversation_id,
        data.role,
        data.content,
    )

    if not message:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return message


# Delete a conversation
@router.delete("/{conversation_id}")
def remove_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_conversation(db, conversation_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {"detail": "Conversation deleted successfully"}
