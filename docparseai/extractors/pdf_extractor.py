\"""PDF document extractor for DocParseAI.

This module provides functionality to extract text, tables, and form fields
from PDF documents.
"""

import io
import os
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import warnings

# PDF processing libraries
try:
    import PyPDF2
    import pdfplumber
    import tabula
    import camelot
    from pdf2image import convert_from_path
    LIBRARIES_AVAILABLE = True
except ImportError:
    LIBRARIES_AVAILABLE = False
    warnings.warn(
        "One or more PDF processing libraries are not installed. "
        "Install required packages with: pip install -r requirements.txt"
    )


class PDFExtractor:
    """Extractor for PDF documents.
    
    This class provides methods to extract various types of content from PDF documents.
    
    Attributes:
        config (Dict): Configuration options for the PDF extractor.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize a new PDFExtractor instance.
        
        Args:
            config: Optional configuration dictionary for customizing extraction behavior.
        """
        self.config = config or {}
        
        if not LIBRARIES_AVAILABLE:
            warnings.warn(
                "PDF extraction functionality is limited because required libraries are not installed. "
                "Install required packages with: pip install -r requirements.txt"
            )
    
    def extract_text(self, pdf_path: Union[str, Path]) -> str:
        """Extract text content from a PDF document.
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            str: The extracted text content.
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            RuntimeError: If required libraries are not available.
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not LIBRARIES_AVAILABLE:
            raise RuntimeError("Required PDF processing libraries are not installed")
        
        extracted_text = ""
        
        # Method selection based on configuration
        extraction_method = self.config.get("text_extraction_method", "pdfplumber")
        
        try:
            if extraction_method == "pypdf2":
                # Extract text using PyPDF2
                with open(pdf_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        extracted_text += page.extract_text() + "\n\n"
            
            elif extraction_method == "pdfplumber":
                # Extract text using pdfplumber (better for maintaining layout)
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text is not None:
                            extracted_text += page_text + "\n\n"
                        else:
                            extracted_text += "\n\n"
            
            else:
                # Default to PyPDF2 if method not recognized
                with open(pdf_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        extracted_text += page.extract_text() + "\n\n"
        
        except Exception as e:
            # Fallback to alternative method if primary method fails
            try:
                with open(pdf_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        extracted_text += page.extract_text() + "\n\n"
            except Exception as fallback_error:
                raise RuntimeError(f"Failed to extract text: {str(e)}. Fallback also failed: {str(fallback_error)}")
        
        # Clean up the extracted text
        extracted_text = extracted_text.strip()
        
        return extracted_text
    
    def extract_tables(self, pdf_path: Union[str, Path]) -> List[Dict]:
        """Extract tables from a PDF document.
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            List[Dict]: List of extracted tables, where each table is represented as a dictionary
                       with keys for headers and data.
                       
        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            RuntimeError: If required libraries are not available.
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not LIBRARIES_AVAILABLE:
            raise RuntimeError("Required PDF processing libraries are not installed")
        
        tables = []
        
        # Method selection based on configuration
        extraction_method = self.config.get("table_extraction_method", "tabula")
        
        try:
            if extraction_method == "tabula":
                # Extract tables using tabula-py
                df_list = tabula.read_pdf(
                    str(pdf_path),
                    pages='all',
                    multiple_tables=True,
                    guess=True
                )
                
                for df in df_list:
                    if not df.empty:
                        headers = df.columns.tolist()
                        data = df.values.tolist()
                        tables.append({
                            "headers": headers,
                            "data": data
                        })
            
            elif extraction_method == "camelot":
                # Extract tables using camelot (often more accurate but slower)
                table_objects = camelot.read_pdf(
                    str(pdf_path),
                    pages='all',
                    flavor='lattice'  # or 'stream' depending on table type
                )
                
                for table in table_objects:
                    df = table.df
                    headers = df.iloc[0].tolist()
                    data = df.iloc[1:].values.tolist()
                    tables.append({
                        "headers": headers,
                        "data": data
                    })
            
            else:
                # Default to tabula if method not recognized
                df_list = tabula.read_pdf(
                    str(pdf_path),
                    pages='all',
                    multiple_tables=True
                )
                
                for df in df_list:
                    if not df.empty:
                        headers = df.columns.tolist()
                        data = df.values.tolist()
                        tables.append({
                            "headers": headers,
                            "data": data
                        })
        
        except Exception as e:
            # Fallback to alternative method if primary method fails
            try:
                # Try with different settings
                df_list = tabula.read_pdf(
                    str(pdf_path),
                    pages='all',
                    multiple_tables=True,
                    lattice=True  # Try with lattice mode
                )
                
                for df in df_list:
                    if not df.empty:
                        headers = df.columns.tolist()
                        data = df.values.tolist()
                        tables.append({
                            "headers": headers,
                            "data": data
                        })
            except Exception as fallback_error:
                raise RuntimeError(f"Failed to extract tables: {str(e)}. Fallback also failed: {str(fallback_error)}")
        
        return tables
    
    def extract_form_fields(self, pdf_path: Union[str, Path]) -> Dict:
        """Extract form fields from a PDF document.
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            Dict: Dictionary of extracted form fields, where keys are field names and values are field values.
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            RuntimeError: If required libraries are not available.
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not LIBRARIES_AVAILABLE:
            raise RuntimeError("Required PDF processing libraries are not installed")
        
        form_fields = {}
        
        try:
            # Extract form fields using PyPDF2
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                if reader.is_encrypted:
                    try:
                        # Try to decrypt with empty password
                        reader.decrypt('')
                    except:
                        # If decryption fails, we can't extract form fields
                        return {}
                
                # Get form fields
                form_fields = reader.get_form_text_fields() or {}
                
                # Get checkbox fields (if available in this version of PyPDF2)
                try:
                    checkbox_fields = reader.get_fields()
                    if checkbox_fields:
                        for field_name, field_value in checkbox_fields.items():
                            if field_name not in form_fields:
                                # Check if it's a checkbox by examining its value
                                if isinstance(field_value, dict) and '/AS' in field_value:
                                    checkbox_value = field_value['/AS'] != '/Off'
                                    form_fields[field_name] = checkbox_value
                except (AttributeError, KeyError):
                    # This version of PyPDF2 might not support this method
                    pass
        
        except Exception as e:
            # Log the error but return empty dict rather than failing
            warnings.warn(f"Failed to extract form fields: {str(e)}")
            return {}
        
        return form_fields
    
    def extract_metadata(self, pdf_path: Union[str, Path]) -> Dict:
        """Extract metadata from a PDF document.
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            Dict: Dictionary of extracted metadata such as author, creation date, etc.
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            RuntimeError: If required libraries are not available.
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not LIBRARIES_AVAILABLE:
            raise RuntimeError("Required PDF processing libraries are not installed")
        
        metadata = {}
        
        try:
            # Extract metadata using PyPDF2
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                
                # Get document info dictionary
                info = reader.metadata
                if info:
                    # Extract common metadata fields
                    for key in info:
                        # Clean up the key name (remove leading '/' if present)
                        clean_key = key[1:] if key.startswith('/') else key
                        metadata[clean_key.lower()] = info[key]
                
                # Add page count
                metadata['page_count'] = len(reader.pages)
                
                # Add file size
                metadata['file_size_bytes'] = os.path.getsize(pdf_path)
                
                # Add creation and modification dates in a standardized format if available
                if 'creationdate' in metadata:
                    # Try to parse and standardize the date format
                    try:
                        # This is a simplified approach - actual implementation would need more robust date parsing
                        raw_date = metadata['creationdate']
                        # Keep the raw date but remove D: prefix if present
                        if isinstance(raw_date, str) and raw_date.startswith('D:'):
                            metadata['creation_date'] = raw_date[2:]
                    except:
                        pass
        
        except Exception as e:
            # Log the error but return basic metadata rather than failing
            warnings.warn(f"Failed to extract complete metadata: {str(e)}")
            
            # Try to at least get page count
            try:
                with open(pdf_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    metadata['page_count'] = len(reader.pages)
            except:
                metadata['page_count'] = 0
        
        return metadata