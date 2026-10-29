
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class Generator:
    def __init__(self, model="llama3.2:3b"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def generate(self, query, context):
        prompt = f"""
You are DocuGuard, an enterprise document intelligence assistant.

Answer the question using only the supplied document context.

Rules:
1. Do not invent facts.
2. If the answer is not supported by the context,
   say that the information is unavailable in the provided documents.
3. Keep the answer clear and concise.
4. Cite supporting sources using the source and page labels
   provided in the context.
5. Do not invent page numbers or citations.

Document context:
{context}

Question:
{query}

Answer:
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }

        request = Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urlopen(request, timeout=180) as response:
                result = json.loads(response.read().decode("utf-8"))

            return result["response"].strip()

        except HTTPError as error:
            raise RuntimeError(
                f"Ollama API returned HTTP {error.code}. "
                "Check that the model is available."
            ) from error

        except URLError as error:
            raise RuntimeError(
                "Cannot connect to Ollama. Open the Ollama app "
                "and make sure its local service is running."
            ) from error
