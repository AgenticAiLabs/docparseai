import faiss
import numpy as np
from typing import List, Tuple

class FAISSStore:
    def __init__(self):
        self.index = None
        self.chunks = []

    def from_embeddings(self, chunks: List[str], embeddings: List[List[float]]):
        self.chunks = chunks
        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        return self

    def query(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        if not self.index:
            raise ValueError("Index is empty. Use from_embeddings() first.")
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        return [(self.chunks[i], float(D[0][j])) for j, i in enumerate(I[0])]
