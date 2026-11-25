
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker


from collections.abc import Generator
from sqlalchemy.orm import Session

# Locate the root project directory
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent

# Load environment variables from the root .env file
load_dotenv(PROJECT_ROOT / ".env")

# Read database configuration
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    raise ValueError("Database configuration is incomplete. Check your root .env file.")

# Construct the database URL safely
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Create a factory for database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Base class for future database models
class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
