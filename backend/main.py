from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

#from services.gemini import generate_response  for generating responses using Gemini API
from backend.services.gemini import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "AgentForge backend is running"}


@app.post("/api/chat")
def chat(request: ChatRequest):
    project_path = r"C:\Users\LOQ\OneDrive\Desktop\AgentForge"
    answer = run_agent(
        request.message,
        project_path
    )

    return {
        "message": answer
    }