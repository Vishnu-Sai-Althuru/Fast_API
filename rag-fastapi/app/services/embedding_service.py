from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", fallback_dimension: int = 16):
        self.model_name = model_name
        self.fallback_dimension = fallback_dimension
        self.model: Optional[SentenceTransformer] = None
        self.model_load_attempted = False

    def _get_model(self) -> Optional[SentenceTransformer]:
        if self.model is None and not self.model_load_attempted:
            self.model_load_attempted = True
            try:
                # Prefer a locally cached model so development remains stable offline.
                self.model = SentenceTransformer(self.model_name, local_files_only=True)
            except Exception:
                self.model = None
        return self.model

    def _fallback_embed(self, text: str) -> np.ndarray:
        vector = np.zeros(self.fallback_dimension, dtype=np.float32)

        for index, char in enumerate(text.lower()):
            vector[index % self.fallback_dimension] += float(ord(char))

        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm

        return vector

    def embed(self, text: str):
        model = self._get_model()
        if model is None:
            return self._fallback_embed(text)

        return np.asarray(model.encode(text), dtype=np.float32)
