import re
from typing import List, Optional


class TextSplitter:
    @staticmethod
    def split(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50,
        method: str = "sentence",
        advanced: bool = False,
    ) -> List[str]:
        """
        Splits the text into chunks using sentence- or token-level chunking.

        Args:
            text (str): The input document text.
            chunk_size (int): Max number of tokens or characters per chunk.
            overlap (int): Overlap size between chunks.
            method (str): "sentence" or "token".
            advanced (bool): If True and method="token", use spaCy for tokenization.

        Returns:
            List[str]: A list of text chunks.
        """
        if not text.strip():
            return []

        if method == "sentence":
            return TextSplitter._split_by_sentence(text, chunk_size, overlap)
        elif method == "token":
            return TextSplitter._split_by_token(text, chunk_size, overlap, advanced)
        else:
            raise ValueError("Invalid method. Choose 'sentence' or 'token'.")

    @staticmethod
    def _split_by_sentence(text: str, chunk_size: int, overlap: int) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current_chunk = []

        for sentence in sentences:
            joined = " ".join(current_chunk + [sentence])
            if len(joined) <= chunk_size:
                current_chunk.append(sentence)
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    @staticmethod
    def _split_by_token(
        text: str, chunk_size: int, overlap: int, advanced: bool = False
    ) -> List[str]:
        if advanced:
            try:
                import spacy

                nlp = spacy.load("en_core_web_sm")
                tokens = [token.text for token in nlp(text)]
            except ImportError:
                raise ImportError(
                    "To use Advanced Token splitting, you need to install. Install with: pip install 'docparseai[advanced]'"
                )
            except OSError:
                raise OSError(
                    "spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm"
                )
        else:
            tokens = text.split()

        chunks = []
        i = 0
        while i < len(tokens):
            chunk = tokens[i : i + chunk_size]
            chunks.append(" ".join(chunk))
            i += chunk_size - overlap
        return chunks
