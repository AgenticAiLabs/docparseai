import os
import fitz  # PyMuPDF
import docx
import pandas as pd
import numpy as np
import chardet

class DocumentLoader:
    SUPPORTED_FORMATS = ('.pdf', '.docx', '.txt')

    @staticmethod
    def load(file_path: str) -> str:
        """Load document content from a supported file type"""
        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.pdf':
                return DocumentLoader._load_pdf(file_path)
            elif ext == '.docx':
                return DocumentLoader._load_docx(file_path)
            elif ext == '.txt':
                return DocumentLoader._load_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        except fitz.FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def _load_pdf(file_path: str) -> str:
        """Extract text from PDF using PyMuPDF"""

        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text

    @staticmethod
    def _load_docx(file_path: str) -> str:
        """Extract text from DOCX using python-docx"""

        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    @staticmethod
    def _load_txt(file_path: str) -> str:
        """Extract text from TXT file with encoding detection"""
        
        with open(file_path, 'rb') as f:
            raw = f.read()
            encoding = chardet.detect(raw)['encoding']
        return raw.decode(encoding).strip()
