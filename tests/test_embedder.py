import pytest

# Skip this whole file if sentence-transformers isn't installed
pytest.importorskip("sentence_transformers")

from docparseai.embeddings.embedder import Embedder

class TestEmbedder:
    def test_single_text_embedding(self):
        embedder = Embedder()
        vecs = embedder.embed("This is a test.")
        assert isinstance(vecs, list)
        assert isinstance(vecs[0], list)
        assert len(vecs[0]) > 0

    def test_batch_text_embedding(self):
        embedder = Embedder()
        inputs = ["First sentence.", "Second sentence."]
        vecs = embedder.embed(inputs)
        assert len(vecs) == 2
        assert all(isinstance(v, list) for v in vecs)
