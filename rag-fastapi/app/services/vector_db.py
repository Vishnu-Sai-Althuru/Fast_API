import numpy as np


class VectorDB:
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.document_vectors = None
        self.documents = []

    def build_index(self, docs: list):
        self.documents = docs

        if not docs:
            self.document_vectors = np.empty((0, 0), dtype=np.float32)
            return

        vectors = [self.embedding_service.embed(doc) for doc in docs]
        self.document_vectors = np.asarray(vectors, dtype=np.float32)

    def search(self, query: str, k=2):
        if self.document_vectors is None or not self.documents:
            return []

        query_vector = np.asarray(self.embedding_service.embed(query), dtype=np.float32)
        distances = np.linalg.norm(self.document_vectors - query_vector, axis=1)
        limit = min(k, len(self.documents))
        top_indices = np.argsort(distances)[:limit]

        results = [self.documents[index] for index in top_indices]
        return results
