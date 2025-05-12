\"""File utility functions for DocParseAI.

This module provides utility functions for working with files,
such as file type detection and validation.
"""

from pathlib import Path
from typing import Optional, Set, Union
import mimetypes
import os

# Initialize mimetypes
mimetypes.init()

# Define supported file formats by category
SUPPORTED_FORMATS = {
    "pdf": {".pdf"},
    "word": {".doc", ".docx"},
    "image": {".jpg", ".jpeg", ".png", ".tiff", ".bmp"},
    "text": {".txt", ".md", ".csv"},
}

# Flatten the supported formats for quick lookup
ALL_SUPPORTED_FORMATS: Set[str] = set()
for formats in SUPPORTED_FORMATS.values():
    ALL_SUPPORTED_FORMATS.update(formats)


def get_file_type(file_path: Union[str, Path]) -> Optional[str]:
    """Determine the type of a file based on its extension.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        str: The file type category ("pdf", "word", "image", "text", or None if not recognized).
        
    Raises:
        ValueError: If file_path is None or empty.
    """
    if not file_path:
        raise ValueError("File path cannot be None or empty")
        
    file_path = Path(file_path)
    file_ext = file_path.suffix.lower()
    
    for file_type, extensions in SUPPORTED_FORMATS.items():
        if file_ext in extensions:
            return file_type
    
    return None


def is_supported_format(file_path: Union[str, Path]) -> bool:
    """Check if a file format is supported by DocParseAI.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        bool: True if the file format is supported, False otherwise.
        
    Raises:
        ValueError: If file_path is None or empty.
    """
    if not file_path:
        raise ValueError("File path cannot be None or empty")
        
    file_path = Path(file_path)
    file_ext = file_path.suffix.lower()
    
    return file_ext in ALL_SUPPORTED_FORMATS


def get_mime_type(file_path: Union[str, Path]) -> str:
    """Get the MIME type of a file.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        str: The MIME type of the file, or 'application/octet-stream' if unknown.
        
    Raises:
        ValueError: If file_path is None or empty.
        FileNotFoundError: If the file doesn't exist.
    """
    if not file_path:
        raise ValueError("File path cannot be None or empty")
        
    path_obj = Path(file_path)
    
    if not path_obj.exists():
        raise FileNotFoundError(f"File not found: {path_obj}")
        
    file_path = str(path_obj)
    mime_type, _ = mimetypes.guess_type(file_path)
    
    return mime_type or 'application/octet-stream'


def get_file_size(file_path: Union[str, Path]) -> int:
    """Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        int: The size of the file in bytes.
        
    Raises:
        ValueError: If file_path is None or empty.
        FileNotFoundError: If the file doesn't exist.
    """
    if not file_path:
        raise ValueError("File path cannot be None or empty")
        
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return file_path.stat().st_size