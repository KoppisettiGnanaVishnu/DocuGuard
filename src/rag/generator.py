import os
from google import genai


class Generator:

    def __init__(self):

        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Please configure your Gemini API key."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(self, query, context):

        prompt = f"""
You are DocuGuard, an enterprise document intelligence assistant.

Answer the user's question using only the information
provided in the context.

Rules:
1. Do not invent facts that are absent from the context.
2. If the context does not contain enough information,
   clearly state that the information is unavailable
   in the provided documents.
3. Give a clear and concise answer.

Context:
{context}

Question:
{query}

Answer:
"""

        response = self.client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        answer = response.output_text

        return answer