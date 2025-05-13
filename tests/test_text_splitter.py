import pytest
from docparseai.text_splitter import TextSplitter

SHORT_TEXT = "Hello world. This is a test."
LONG_TEXT = (
    "This is the first sentence. Here is the second one! "
    "Now the third sentence arrives? And yet, another sentence here. "
    "The fifth one goes on. Finally, a sixth sentence to test splitting."
)


class TestTextSplitter:
    def test_sentence_split_basic(self):
        chunks = TextSplitter.split(SHORT_TEXT, chunk_size=40, overlap=10, method="sentence")
        assert isinstance(chunks, list)
        assert all(isinstance(c, str) for c in chunks)
        assert len(chunks) >= 1

    def test_token_split_basic(self):
        chunks = TextSplitter.split(SHORT_TEXT, chunk_size=5, overlap=2, method="token")
        assert isinstance(chunks, list)
        assert all(isinstance(c, str) for c in chunks)
        assert len(chunks) >= 1

    def test_sentence_split_respects_chunk_size(self):
        chunks = TextSplitter.split(LONG_TEXT, chunk_size=50, overlap=10, method="sentence")
        assert all(len(c) <= 60 for c in chunks)  # some buffer allowed

    def test_token_split_respects_token_count(self):
        chunks = TextSplitter.split(LONG_TEXT, chunk_size=10, overlap=3, method="token")
        for chunk in chunks:
            num_tokens = len(chunk.split())
            assert 3 <= num_tokens <= 15  # allowing overlap variation

    def test_empty_text(self):
        chunks = TextSplitter.split("", chunk_size=50, method="sentence")
        assert chunks == []

    def test_invalid_method(self):
        with pytest.raises(ValueError):
            TextSplitter.split("Some text", chunk_size=10, method="word")

    def test_token_overlap_behavior(self):
        chunks = TextSplitter.split(LONG_TEXT, chunk_size=10, overlap=5, method="token")
        # Check that overlapping tokens are shared
        if len(chunks) >= 2:
            first_tokens = chunks[0].split()
            second_tokens = chunks[1].split()
            assert first_tokens[-5:] == second_tokens[:5]
