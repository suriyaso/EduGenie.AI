import os
import json
import re

from google import genai


def load_dotenv():
    """Load simple KEY=VALUE entries from the local .env file."""
    env_file_path = os.path.join(os.path.dirname(__file__), ".env")

    if not os.path.isfile(env_file_path):
        return

    with open(env_file_path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key.strip(), value)


load_dotenv()


def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


def clean_json_response(text: str):

    text = text.strip()

    # Remove Markdown JSON code blocks
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def validate_quiz(data):

    if not isinstance(data, dict):
        return False

    if "questions" not in data:
        return False

    questions = data["questions"]

    if not isinstance(questions, list):
        return False

    if len(questions) != 3:
        return False

    for question in questions:

        if not isinstance(question, dict):
            return False

        required_fields = [
            "question",
            "options",
            "answer",
            "explanation"
        ]

        for field in required_fields:

            if field not in question:
                return False

        if not isinstance(
            question["options"],
            list
        ):
            return False

        if len(question["options"]) != 4:
            return False

        if not isinstance(
            question["answer"],
            int
        ):
            return False

        if question["answer"] < 0 or \
           question["answer"] > 3:

            return False

    return True


def generate_quiz(
    text: str,
    level: str = "beginner"
):

    client = get_client()

    if client is None:

        return {
            "error": (
                "Gemini API key is not configured. "
                "Please add GEMINI_API_KEY to your .env file."
            )
        }

    prompt = f"""
You are an educational quiz generator.

Generate exactly THREE multiple-choice questions
from the following educational content.

Learner level:
{level}

Content:
{text}

Each question must have exactly FOUR options.

Return ONLY valid JSON.

Use exactly this format:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": 0,
      "explanation": "Explanation"
    }}
  ]
}}

Important:

- answer must be a zero-based number.
- 0 means Option A.
- 1 means Option B.
- 2 means Option C.
- 3 means Option D.
- Questions must be based on the supplied content.
- Make distractors plausible.
"""

    try:

        model_name = os.getenv("GEMINI_MODEL") or "gemini-3.6-flash"
        if model_name == "gemini-2.5-flash":
            model_name = "gemini-3.6-flash"

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        raw_response = response.text

        cleaned = clean_json_response(
            raw_response
        )

        data = json.loads(cleaned)

        if not validate_quiz(data):

            return {
                "error": "Invalid quiz structure returned by AI.",
                "raw": cleaned
            }

        return data

    except json.JSONDecodeError:

        return {
            "error": "AI returned invalid JSON.",
            "raw": raw_response
        }

    except Exception as error:

        return {
            "error": f"Quiz generation failed: {error}"
        }