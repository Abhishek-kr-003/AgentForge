
from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        default="New Chat",
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )

    role: Mapped[str] = mapped_column(String(20))

    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages",
    )
