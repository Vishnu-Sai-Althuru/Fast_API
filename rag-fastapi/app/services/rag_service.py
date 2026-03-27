from pathlib import Path

from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_db import VectorDB


DOCUMENTS_PATH = Path(__file__).resolve().parent.parent / "data" / "documents.txt"


class RAGService:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_db = VectorDB(self.embedder)
        self.llm = LLMService()

        with DOCUMENTS_PATH.open(encoding="utf-8") as file:
            docs = [line.strip() for line in file if line.strip()]

        self.vector_db.build_index(docs)

    def process_query(self, question: str) -> str:
        context = self.vector_db.search(question)
        return self.llm.generate(question, context)
