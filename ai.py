# ai.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


def call_openai_chat(message: str) -> str | None:
    """Send user message to OpenAI and return reply."""
    if not client:
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",   # lightweight & fast model
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("OpenAI error:", e)
        return None
