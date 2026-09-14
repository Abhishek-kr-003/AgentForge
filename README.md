# 🤖 AgentForge

AgentForge is an AI-powered coding assistant that uses **Google Gemini** and tool calling to inspect and understand software projects.

Instead of only generating text, the agent can interact with project files, choose the appropriate tool, inspect the results, and use multiple tools before providing an answer.

## ✨ Features

- 🧠 Gemini-powered AI agent
- 🔧 Function/tool calling
- 📁 Project file listing
- 📖 File content reading
- 🔍 Source code searching
- 🔄 Multi-step tool chaining
- 🔐 Basic filesystem access protection
- ⚡ React + FastAPI full-stack architecture

### Available Tools

| Tool | Purpose |
|---|---|
| `list_files()` | Lists relevant files in the project |
| `read_file()` | Reads a specific project file |
| `search_code()` | Searches source code for a given text |

## 🏗️ Architecture

```text
React Frontend
      ↓
   FastAPI
      ↓
 Gemini Agent
      ↓
 ┌────┼──────────────┐
 ↓    ↓              ↓
List Read         Search
Files File         Code
 └────┼──────────────┘
      ↓
 Tool Result
      ↓
    Gemini
      ↓
 Final Answer
```

The agent can also chain multiple tools when necessary:

```text
User Request
     ↓
Gemini
     ↓
search_code()
     ↓
Gemini
     ↓
read_file()
     ↓
Gemini
     ↓
Final Answer
```

## 🛠️ Tech Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- Pydantic

**AI**
- Google Gemini API
- Google GenAI Python SDK
- Function Calling

## 📁 Project Structure

```text
AgentForge/
├── backend/
│   ├── main.py
│   ├── services/
│   │   └── gemini.py
│   └── tools/
│       └── filesystem.py
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── main.jsx
│
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AgentForge
```

### 2. Set up the backend

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install fastapi uvicorn python-dotenv google-genai
```

Create:

```text
backend/.env
```

and add:

```env
GEMINI_API_KEY=your_api_key_here
```

**Never commit your API key to GitHub.**

### 3. Start the backend

From the project root:

```bash
fastapi dev backend/main.py
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 🔐 Security

AgentForge protects sensitive and unnecessary files from filesystem tools, including:

- `.env`
- `.venv`
- `node_modules`
- `.git`
- `__pycache__`
- `dist`
- `build`

File access is also restricted to the configured project directory.

## 🗺️ Roadmap

Future improvements include:

- [ ] Streaming responses
- [ ] More coding tools
- [ ] Code modification capabilities
- [ ] Safer terminal execution
- [ ] Better conversation history
- [ ] Project indexing and RAG
- [ ] Improved chat interface
- [ ] Deployment

## 👨‍💻 About

AgentForge is a hands-on project for exploring **AI agents, tool calling, software project understanding, and full-stack AI application development**.