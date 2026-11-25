
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from backend.tools.filesystem import (
    search_code,
    list_files,
    read_file,
)


# ========================================
# ENVIRONMENT CONFIGURATION
# ========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load .env from AgentForge root directory
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your root .env file."
    )

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        api_version="v1beta"
    )
)
# ========================================
# AGENT CONFIGURATION
# ========================================

MODEL_NAME = "gemini-2.5-flash"

MAX_AGENT_ITERATIONS = 8
MAX_RETRIES = 3

RETRY_DELAY = 2


# ========================================
# LIST FILES TOOL
# ========================================

list_files_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="list_files",
            description=(
                "List all relevant files in the project. "
                "Use this when you need to discover the project's "
                "file structure or find available files."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
        )
    ]
)


# ========================================
# READ FILE TOOL
# ========================================

read_file_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="read_file",
            description=(
                "Read the contents of a specific file in the project. "
                "Use this when you already know which file you need "
                "to inspect."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": (
                            "Path of the file relative to the "
                            "project directory."
                        ),
                    }
                },
                "required": ["file_path"],
            },
        )
    ]
)


# ========================================
# SEARCH CODE TOOL
# ========================================

search_code_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_code",
            description=(
                "Search project source code for a text string. "
                "Returns matching files, line numbers, and lines. "
                "Use this to find functions, classes, variables, "
                "imports, or other code."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to search for.",
                    }
                },
                "required": ["query"],
            },
        )
    ]
)


# All tools available to Gemini
tools = [
    list_files_tool,
    read_file_tool,
    search_code_tool,
]


# ========================================
# TOOL EXECUTION
# ========================================

def execute_tool(function_call, project_path: str):

    if function_call.name == "list_files":
        return list_files(project_path)

    if function_call.name == "read_file":
        file_path = function_call.args["file_path"]
        return read_file(project_path, file_path)

    if function_call.name == "search_code":
        query = function_call.args["query"]
        return search_code(project_path, query)

    raise ValueError(
        f"Unknown tool: {function_call.name}"
    )


# ========================================
# GEMINI API WITH RETRIES
# ========================================

def generate_with_retry(contents):

    for attempt in range(MAX_RETRIES):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=tools,
                ),
            )

            return response

        except errors.ServerError as error:

            print(f"Gemini server error: {error}")

            if attempt == MAX_RETRIES - 1:
                raise

            wait_time = RETRY_DELAY * (2 ** attempt)

            print(
                f"Retrying in {wait_time} seconds... "
                f"Attempt {attempt + 2}/{MAX_RETRIES}"
            )

            time.sleep(wait_time)

    return None


# ========================================
# MAIN AGENT
# ========================================

def run_agent(
    message: str,
    project_path: str,
    messages,
):

    # Build conversation history
    contents = []

    for msg in messages:

        role = msg.role

        # Gemini uses "model" instead of "assistant"
        if role == "assistant":
            role = "model"

        contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=msg.content
                    )
                ],
            )
        )

    # Add current user message
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=message
                )
            ],
        )
    )

    # ====================================
    # AGENT EXECUTION LOOP
    # ====================================

    for iteration in range(MAX_AGENT_ITERATIONS):

        print(
            f"Agent iteration: "
            f"{iteration + 1}/{MAX_AGENT_ITERATIONS}"
        )

        try:

            response = generate_with_retry(contents)

        except errors.ServerError:

            return (
                "Gemini is temporarily unavailable due to "
                "high demand. Please try again in a few seconds."
            )

        except Exception as error:

            print(f"Gemini API error: {error}")

            return (
                "An error occurred while communicating "
                "with Gemini. Please try again."
            )

        # Check response
        if response is None or not response.candidates:

            return (
                "Gemini returned an empty response. "
                "Please try again."
            )

        print("Gemini response received")

        # Check whether Gemini wants to use tools
        function_calls = response.function_calls

        # No tool required: return final response
        if not function_calls:

            return (
                response.text
                or "Gemini could not generate a response."
            )

        tool_parts = []

        # Execute requested tools
        for function_call in function_calls:

            print("Function:", function_call.name)
            print("Arguments:", function_call.args)

            try:

                result = execute_tool(
                    function_call,
                    project_path,
                )

            except Exception as error:

                print(f"Tool execution error: {error}")

                result = {
                    "error": str(error),
                    "status": "failed",
                }

            print("Tool result:")
            print(result)

            tool_parts.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response={
                        "result": result,
                    },
                )
            )

        # Add Gemini's tool request to history
        contents.append(
            types.Content(
                role="model",
                parts=response.candidates[0].content.parts,
            )
        )

        # Add tool results to history
        contents.append(
            types.Content(
                role="user",
                parts=tool_parts,
            )
        )

    # Maximum iteration limit reached
    return (
        "The agent reached its maximum execution limit. "
        "Please try a more specific request."
    )
