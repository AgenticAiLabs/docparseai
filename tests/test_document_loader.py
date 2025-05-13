import os
import pytest
from docparseai.document_loader import DocumentLoader

SUPPORTED_FILES = ["sample.txt", "sample.pdf", "sample.docx"]

class TestDocumentLoader:
    @pytest.mark.parametrize("filename", SUPPORTED_FILES)
    def test_load_supported_formats(self, test_files_path, filename):
        file_path = os.path.join(test_files_path, filename)
        content = DocumentLoader.load(file_path)
        assert isinstance(content, str)
        assert len(content.strip()) > 0

    def test_load_unsupported_format(self):
        with pytest.raises(ValueError):
            DocumentLoader.load("unsupported.xlsx")

    def test_load_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            DocumentLoader.load("nonexistent.pdf")
