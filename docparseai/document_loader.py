"""
document_loader.py

This module provides a lightweight and extensible interface for loading plain text
from supported document formats: PDF, DOCX, and TXT. It abstracts file-type handling
and text extraction into a unified API.

Dependencies:
    - PyMuPDF (fitz): For PDF parsing.
    - python-docx: For reading DOCX files.
    - chardet: For automatic encoding detection in TXT files.

Usage:
    from document_loader import DocumentLoader

    content = DocumentLoader.load("example.pdf")
"""

import os
import fitz  # PyMuPDF
import docx
import chardet


class DocumentLoader:
    """
    Unified document loader for extracting plain text from common formats.

    Supported formats:
        - PDF (.pdf)
        - DOCX (.docx)
        - Plain text (.txt)

    Methods:
        - load(file_path): Dispatches to the appropriate parser based on file extension.
    """

    SUPPORTED_FORMATS = ('.pdf', '.docx', '.txt')

    @staticmethod
    def load(file_path: str) -> str:
        """
        Load text content from a document.

        Args:
            file_path (str): Absolute or relative path to the document file.

        Returns:
            str: Extracted plain text content.

        Raises:
            FileNotFoundError: If the file does not exist or cannot be read.
            ValueError: If the file extension is unsupported.
            UnicodeDecodeError: If text encoding cannot be correctly determined (for .txt).
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return DocumentLoader._load_pdf(file_path)
        elif ext == '.docx':
            return DocumentLoader._load_docx(file_path)
        elif ext == '.txt':
            return DocumentLoader._load_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    @staticmethod
    def _load_pdf(file_path: str) -> str:
        """
        Extract text from a PDF file using PyMuPDF.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            str: Extracted text from all pages concatenated by newline.

        Raises:
            FileNotFoundError: If the PDF file is not found or unreadable.
        """
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text

    @staticmethod
    def _load_docx(file_path: str) -> str:
        """
        Extract text from a DOCX file using python-docx.

        Args:
            file_path (str): Path to the DOCX file.

        Returns:
            str: Concatenated paragraph text separated by newline.

        Raises:
            Exception: If the DOCX file cannot be read or parsed.
        """
        doc = docx.Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)

    @staticmethod
    def _load_txt(file_path: str) -> str:
        """
        Extract text from a plain text file with automatic encoding detection.

        Args:
            file_path (str): Path to the TXT file.

        Returns:
            str: Cleaned plain text string.

        Raises:
            UnicodeDecodeError: If encoding detection fails or decoding fails.
        """
        with open(file_path, 'rb') as f:
            raw = f.read()
            encoding = chardet.detect(raw)['encoding']
        return raw.decode(encoding).strip()
