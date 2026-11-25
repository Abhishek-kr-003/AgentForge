
from backend.database import Base, engine
from backend.models import Conversation, Message

# Create tables that do not already exist
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
