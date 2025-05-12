"""Core parsing functionality for DocParseAI.

This module contains the main DocParser class that serves as the entry point
for document parsing and extraction operations.
"""

from typing import Dict, List, Optional, Union
import os
from pathlib import Path
from docparseai.utils.file_utils import get_file_type, is_supported_format, get_file_size, get_mime_type


class ParseResult:
    """Container for document parsing results.
    
    Attributes:
        text (str): The extracted full text content of the document.
        tables (List[Dict]): List of tables extracted from the document.
        form_fields (Dict): Dictionary of form fields extracted from the document.
        metadata (Dict): Document metadata such as author, creation date, etc.
    """
    
    def __init__(self):
        self.text = ""
        self.tables = []
        self.form_fields = {}
        self.metadata = {}


class DocParser:
    """Main document parser class.
    
    This class provides methods to parse and extract data from various document formats.
    
    Attributes:
        config (Dict): Configuration options for the parser.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize a new DocParser instance.
        
        Args:
            config: Optional configuration dictionary for customizing parser behavior.
        """
        self.config = config or {}
    
    def parse(self, document_path: Union[str, Path]) -> ParseResult:
        """Parse a document and extract its content.
        
        Args:
            document_path: Path to the document file to parse.
            
        Returns:
            ParseResult: Object containing the extracted data.
            
        Raises:
            FileNotFoundError: If the document file doesn't exist.
            ValueError: If the document format is not supported.
        """
        document_path = Path(document_path)
        
        if not document_path.exists():
            raise FileNotFoundError(f"Document not found: {document_path}")
        
        # Check if the file format is supported
        if not is_supported_format(document_path):
            raise ValueError(f"Unsupported document format: {document_path.suffix.lower()}")
        
        # Get the file type
        file_type = get_file_type(document_path)
        
        result = ParseResult()
        
        # TODO: Implement actual parsing logic for different document types
        # This is a placeholder implementation
        if file_type == "pdf":
            result.text = f"[PDF content from {document_path}]"
        elif file_type == "word":
            result.text = f"[Word document content from {document_path}]"
        elif file_type == "image":
            result.text = f"[Image content from {document_path}]"
        elif file_type == "text":
            result.text = f"[Text content from {document_path}]"
        else:
            # This should not happen as we already checked if the format is supported
            raise ValueError(f"Unsupported document format: {document_path.suffix.lower()}")
        
        # Add metadata using file utility functions
        result.metadata = {
            "filename": document_path.name,
            "file_size": get_file_size(document_path),
            "file_type": file_type,
            "mime_type": get_mime_type(document_path)
        }
        
        return result
    
    def extract_text(self, document_path: Union[str, Path]) -> str:
        """Extract text content from a document.
        
        Args:
            document_path: Path to the document file.
            
        Returns:
            str: The extracted text content.
        """
        result = self.parse(document_path)
        return result.text
    
    def extract_tables(self, document_path: Union[str, Path]) -> List[Dict]:
        """Extract tables from a document.
        
        Args:
            document_path: Path to the document file.
            
        Returns:
            List[Dict]: List of extracted tables.
        """
        result = self.parse(document_path)
        return result.tables
    
    def extract_form_fields(self, document_path: Union[str, Path]) -> Dict:
        """Extract form fields from a document.
        
        Args:
            document_path: Path to the document file.
            
        Returns:
            Dict: Dictionary of extracted form fields.
        """
        result = self.parse(document_path)
        return result.form_fields