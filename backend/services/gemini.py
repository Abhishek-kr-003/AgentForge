import os
import time

from google.genai import errors
from dotenv import load_dotenv
from google import genai
from google.genai import types
from backend.tools.filesystem import search_code, list_files, read_file

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

list_files_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="list_files",
            description=(
                "List all relevant files in the project."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
        )
    ]
)

read_file_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="read_file",
            description=(
                "Read the contents of a specific file in the project."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": (
                            "Path of the file relative to the project directory."
                        )
                    }
                },
                "required": ["file_path"],
            },
        )
    ]
)

search_code_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_code",
            description=(
                "Search the project source code for a text string. "
                "Returns matching files, line numbers, and matching lines."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to search for in the project."
                    }
                },
                "required": ["query"],
            },
        )
    ]
)

tools = [
    list_files_tool, 
    read_file_tool, 
    search_code_tool,
]            
               


def generate_response(message: str) -> str:
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=message,
            )
            return response.text

        except errors.ServerError as error:
           print(f"Gemini server error: {error}")
           if attempt == max_retries - 1:
            raise
           time.sleep(2)


def execute_tool(function_call, project_path: str):
    if function_call.name == "list_files":
        return list_files(project_path)

    if function_call.name == "read_file":
        file_path = function_call.args["file_path"]
        return read_file(project_path, file_path)

    if function_call.name == "search_code":
        query = function_call.args["query"]

        return search_code(
            project_path, 
            query
        )

    

    raise ValueError(
       f"Unknown tool: {function_call.name}"
    )


def run_agent(message: str, project_path: str):

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=message
                )
            ],
        )
    ]

    while True:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config={
                "tools": tools
            },
        )
        print("Gemini response received")

        if not response.function_calls:
            return response.text

        tool_parts = []

        for function_call in response.function_calls:
            print("Function:", function_call.name)
            print("Arguments:", function_call.args)

            result = execute_tool(
                function_call,
                project_path
            )
            

            print("Tool result:")
            print(result)

            tool_parts.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response={
                        "result": result
                    },
                )
            )

        contents.append(
            types.Content(
                role="model",
                parts=response.candidates[0].content.parts,
            )
        )

        contents.append(
            types.Content(
                role="user",
                parts=tool_parts,
            )
        )

if __name__ == "__main__":
    project_path = r"C:\Users\LOQ\OneDrive\Desktop\AgentForge"

    answer = run_agent(
    "Find the file that contains the FastAPI backend and then read that file and explain how the backend works.",
    project_path
)

print("\nFinal answer:")
print(answer)