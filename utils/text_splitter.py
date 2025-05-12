import pandas as pd
import numpy as np
import re
from typing import List
import spacy

# Load spaCy model for tokenization
nlp = spacy.load("en_core_web_sm")

class TextSplitter:
    @staticmethod
    def split(text: str, chunk_size: int = 500, overlap: int = 50, method: str = "sentence") -> List[str]:
        """
        Splits the text into chunks using sentence or token-level chunking.
        
        Args:
            text (str): The input document text.
            chunk_size (int): The max size of each chunk (in characters).
            overlap (int): The number of overlapping characters between consecutive chunks.
            method (str): The method of chunking ("sentence" or "token").
        
        Returns:
            List[str]: A list of text chunks.
        """
        if not text.strip():
            return []

        if method == "sentence":
            return TextSplitter._split_by_sentence(text, chunk_size, overlap)
        elif method == "token":
            return TextSplitter._split_by_token(text, chunk_size, overlap)
        else:
            raise ValueError("Invalid method. Choose either 'sentence' or 'token'.")

    @staticmethod
    def _split_by_sentence(text: str, chunk_size: int, overlap: int) -> List[str]:
        """Splits text into chunks based on sentences"""
        sentences = re.split(r'(?<=[.!?]) +', text)  # Simple sentence split (not perfect, can be improved)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk:
            chunks.append(current_chunk.strip())  # Append the last chunk
        return chunks

    @staticmethod
    def _split_by_token(text: str, chunk_size: int, overlap: int) -> List[str]:
        """Splits text into chunks based on token count (using spaCy)"""
        doc = nlp(text)
        tokens = [token.text for token in doc]
        chunks = []
        current_chunk = []
        
        for token in tokens:
            if len(current_chunk) < chunk_size:
                current_chunk.append(token)
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = current_chunk[-overlap:] + [token]  # Keep overlap
                
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks
