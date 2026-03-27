import requests

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.model = settings.OLLAMA_MODEL

    def generate(self, question: str, context: list) -> str:
        context_text = "\n".join(context)
        prompt = (
            "Answer the question using the context below.\n\n"
            f"Context:\n{context_text}\n\n"
            f"Question:\n{question}"
        )

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            return data["response"]
        except (KeyError, ValueError, requests.RequestException):
            if context_text:
                return f"Ollama is unavailable right now. Relevant context:\n{context_text}"

            return "Ollama is unavailable right now, and no relevant context was found."
