
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models import Conversation, Message


# 1. Create a new conversation
def create_conversation(
    db: Session,
    title: str = "New Chat",
):
    conversation = Conversation(title=title)

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


# 2. Retrieve all conversations
def get_conversations(db: Session):
    return (
        db.query(Conversation)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


# 3. Retrieve one conversation with its messages
def get_conversation(db: Session, conversation_id: int):
    return db.get(Conversation, conversation_id)


# 4. Save a message to a conversation
def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
):
    conversation = db.get(Conversation, conversation_id)

    if not conversation:
        return None

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    # Update the conversation's last activity time
    conversation.updated_at = func.now()

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


# 5. Delete a conversation
def delete_conversation(
    db: Session,
    conversation_id: int,
):
    conversation = db.get(Conversation, conversation_id)

    if not conversation:
        return False

    db.delete(conversation)
    db.commit()

    return True
