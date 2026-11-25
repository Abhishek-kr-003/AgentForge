
from backend.database import SessionLocal
from backend.services.chat_history import (
    create_conversation,
    add_message,
    get_conversations,
    get_conversation,
    delete_conversation,
)

db = SessionLocal()

try:
    # Create a conversation
    chat = create_conversation(db, "AgentForge Database Test")
    print("Created conversation:", chat.id)

    # Save two messages
    add_message(db, chat.id, "user", "Hello AgentForge!")

    add_message(
        db,
        chat.id,
        "assistant",
        "Hello! Database connection is working.",
    )

    # Retrieve all conversations
    chats = get_conversations(db)
    print("Total conversations:", len(chats))

    # Retrieve one conversation
    retrieved_chat = get_conversation(db, chat.id)

    print("Conversation:", retrieved_chat.title)

    for message in retrieved_chat.messages:
        print(message.role, ":", message.content)

    # Delete the test conversation
    deleted = delete_conversation(db, chat.id)
    print("Test conversation deleted:", deleted)

finally:
    db.close()
