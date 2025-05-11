# test_loader.py
from docparseai.loaders.document_loader import DocumentLoader

doc = DocumentLoader.load("sample.pdf")
print(doc[:1000])  # Show first 1000 characters
