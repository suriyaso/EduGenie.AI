import os
from pathlib import Path

from google import genai


def load_dotenv():
    """Load simple KEY=VALUE entries from the local .env file."""
    env_file = Path(__file__).with_name(".env")

    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        os.environ.setdefault(key, value)


load_dotenv()


def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


def summarize_text(
    text: str,
    level: str = "beginner"
):

    client = get_client()

    if client is None:

        return (
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY to your .env file."
        )

    prompt = f"""
You are an educational summarization assistant.

Summarize the following educational content.

Learner level:
{level}

Content:
{text}

Requirements:

- Keep the important information.
- Remove repetition.
- Use simple language.
- Use bullet points when appropriate.
- Preserve important facts and concepts.
- Make the summary useful for exam revision.
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