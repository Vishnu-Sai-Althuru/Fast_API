from pathlib import Path

from app.core.exceptions import InputValidationError, QueryProcessingError, ServiceUnavailableError
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_db import VectorDB


DOCUMENTS_PATH = Path(__file__).resolve().parent.parent / "data" / "documents.txt"


class RAGService:
    def __init__(self):
        try:
            self.embedder = EmbeddingService()
            self.vector_db = VectorDB(self.embedder)
            self.llm = LLMService()

            with DOCUMENTS_PATH.open(encoding="utf-8") as file:
                docs = [line.strip() for line in file if line.strip()]
        except OSError as exc:
            raise ServiceUnavailableError("RAG knowledge base is unavailable right now.") from exc
        except Exception as exc:
            raise ServiceUnavailableError("RAG service is unavailable right now.") from exc

        if not docs:
            raise ServiceUnavailableError("RAG knowledge base is empty right now.")

        try:
            self.vector_db.build_index(docs)
        except Exception as exc:
            raise ServiceUnavailableError("RAG service is unavailable right now.") from exc

    def process_query(self, question: str) -> str:
        normalized_question = question.strip()
        if not normalized_question:
            raise InputValidationError("Question cannot be empty.")

        try:
            context = self.vector_db.search(normalized_question)
            return self.llm.generate(normalized_question, context)
        except Exception as exc:
            raise QueryProcessingError("Unable to process the question right now.") from exc
