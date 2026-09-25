import os
import importlib

try:
    load_dotenv = importlib.import_module("dotenv").load_dotenv
except ImportError:
    def load_dotenv():
        """Allow the module to run when python-dotenv is not installed."""
        return False

from google import genai

load_dotenv()


def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


def explain_topic(
    topic: str,
    level: str = "beginner"
):

    client = get_client()

    if client is None:

        return (
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY to your .env file."
        )

    prompt = f"""
You are an expert educational tutor.

Explain the following topic to a {level} learner.

Topic:
{topic}

Use this structure:

1. Simple definition
2. Step-by-step explanation
3. Real-world example
4. Important points
5. Short recap

Rules:

- Use simple English.
- Avoid unnecessary technical language.
- Make the explanation easy for a student to understand.
- Do not assume advanced prior knowledge.
"""

    try:

        model_name = os.getenv("GEMINI_MODEL") or "gemini-3.6-flash"
        if model_name == "gemini-2.5-flash":
            model_name = "gemini-3.6-flash"

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        return response.text.strip()

    except Exception as error:

        return f"Gemini API error: {error}"