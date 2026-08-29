import os
import time

from google.genai import errors
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


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

