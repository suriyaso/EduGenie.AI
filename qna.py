import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def answer_question(
	question: str,
	level: str = "beginner"
):

	api_key = os.getenv("GEMINI_API_KEY")

	if not api_key:
		return (
			"Gemini API key is not configured. "
			"Please add GEMINI_API_KEY to your .env file."
		)

	prompt = f"""
You are an expert educational tutor.

Answer the following question for a {level} learner.

Question:
{question}

Use simple English, explain the reasoning clearly, and include an example
when it helps understanding.
"""

	try:
		client = genai.Client(api_key=api_key)
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
