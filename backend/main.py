
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.routes.conversations import router as conversations_router



BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")
from backend.services.gemini import run_agent

# Project configuration
PROJECT_PATH = Path(
    os.getenv("AGENTFORGE_PROJECT_PATH", str(PROJECT_ROOT))
).resolve()

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)


# Request models
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    messages: list[Message] = Field(default_factory=list)


# Initialize FastAPI
app = FastAPI(
    title="AgentForge API",
    description="AI-powered Software Engineering Agent",
    version="1.0.0",
)
app.include_router(conversations_router) 


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "AgentForge backend is running",
        "status": "healthy",
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project_directory_exists": PROJECT_PATH.is_dir(),
    }


# Chat endpoint
@app.post("/api/chat")
def chat(request: ChatRequest):

    print("CHAT REQUEST RECEIVED")
    print("Message:", request.message)

    if not PROJECT_PATH.exists() or not PROJECT_PATH.is_dir():
        raise HTTPException(
            status_code=500,
            detail="Configured project directory does not exist.",
        )

    try:
        answer = run_agent(
            request.message,
            str(PROJECT_PATH),
            request.messages,
        )

        print("AGENT RESPONSE:", answer)

        return {
            "message": answer,
        }

    except Exception as error:
        print(f"Agent execution error: {error}")

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request.",
        )
