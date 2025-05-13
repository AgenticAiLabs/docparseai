import pytest
from docparseai.faiss_store import FAISSStore

class TestFAISSStore:
    def test_index_and_query(self):
        chunks = ["chunk one", "chunk two", "chunk three"]
        embeddings = [[0.1, 0.2, 0.3], [0.2, 0.1, 0.4], [0.3, 0.2, 0.1]]

        store = FAISSStore().from_embeddings(chunks, embeddings)
        query = [0.1, 0.2, 0.3]
        results = store.query(query, top_k=2)

        assert len(results) == 2
        assert isinstance(results[0], tuple)
        assert results[0][0] in chunks
