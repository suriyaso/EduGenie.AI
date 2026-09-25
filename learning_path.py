import os

from google import genai


def load_env_file():
    """Load simple KEY=VALUE entries from a local .env file."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")

    if not os.path.isfile(env_path):
        return

    with open(env_path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            os.environ.setdefault(key, value)


load_env_file()


def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


def get_learning_recommendations(
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
You are EduGenie, a personalized learning-path assistant.

Create a structured learning path for:

Topic:
{topic}

Current learner level:
{level}

Create a path containing:

1. Beginner stage
2. Intermediate stage
3. Advanced stage
4. Suggested timeline
5. Practice activities
6. Revision strategy
7. Project ideas
8. Recommended types of resources

For every stage include:

- Topics to learn
- What the student should understand
- Practice tasks
- Suggested learning resources

Do not invent specific URLs.

Make the plan practical and easy to follow.
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