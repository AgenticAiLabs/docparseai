
# docparseai: Document Parsing, Chunking, and Embedding

`docparseai` is an open-source Python package designed for document processing tasks. It enables parsing, chunking, embedding, and efficient retrieval of document chunks using **FAISS** for vector similarity search. This package is ideal for applications such as document summarization, search engines, and semantic queries.

## Installation

To install `docparseai` via **PyPI**:

```bash
pip install docparseai
```

### Optional Dependency for Embeddings

If you need the **embedding functionality** for document chunking (which uses `sentence-transformers` for advanced embeddings), install the package with optional dependencies:

```bash
pip install docparseai[embedding]
```

This will install the `sentence-transformers` dependency needed for embedding-based models.

---

## Modules

### 1. **DocumentLoader**

`DocumentLoader` parses various document formats such as PDF, DOCX, and TXT into clean text.

#### Usage:
```python
from docparseai.document_loader import DocumentLoader

# Load a document
text = DocumentLoader.load("file.pdf")
```

---

### 2. **TextSplitter**

`TextSplitter` splits the loaded document text into manageable chunks. The chunking can be based on sentence or token boundaries with configurable chunk size and overlap.

#### Usage:
```python
from docparseai.text_splitter import TextSplitter

# Split the document text into chunks
chunks = TextSplitter.split(text, chunk_size=500, overlap=50)
```

---

### 3. **Embedder**

`Embedder` generates dense vector embeddings for document chunks using **SentenceTransformers**. The default model is `all-MiniLM-L6-v2`, but you can provide your own model.

#### Usage (with optional dependency):
```python
from docparseai.embeddings.embedder import Embedder

# Generate embeddings for chunks
embedder = Embedder()  # By default, uses `all-MiniLM-L6-v2`
embeddings = embedder.embed(chunks)
```

---

### 4. **FAISSStore**

`FAISSStore` stores document chunk embeddings and allows fast similarity-based retrieval of top-k similar chunks for a given query.

#### Usage:
```python
from docparseai.vectorstore.faiss_store import FAISSStore

# Create a store from embeddings
store = FAISSStore().from_embeddings(chunks, embeddings)

# Query the store for top-k similar chunks
top_k_results = store.query(query_embedding, top_k=5)
```

---

## Full Workflow Example

```python
from docparseai.document_loader import DocumentLoader
from docparseai.text_splitter import TextSplitter
from docparseai.embeddings.embedder import Embedder
from docparseai.vectorstore.faiss_store import FAISSStore

# 1. Load document
text = DocumentLoader.load("file.pdf")

# 2. Split document into chunks
chunks = TextSplitter.split(text, chunk_size=500, overlap=50)

# 3. Generate embeddings for chunks
embedder = Embedder()
embeddings = embedder.embed(chunks)

# 4. Create FAISS store with embeddings
store = FAISSStore().from_embeddings(chunks, embeddings)

# 5. Query the store for similar chunks
query = "What is this document about?"
query_embedding = embedder.embed(query)[0]
top_k_results = store.query(query_embedding, top_k=5)

# Output results
for chunk, score in top_k_results:
    print(f"Chunk: {chunk} - Score: {score}")
```

## Notes

- **Optional Embeddings:** If you don’t need advanced embedding capabilities (e.g., for small or non-semantic tasks), you can run the package without installing `sentence-transformers`.
- **FAISS:** The **FAISS** indexing method allows you to efficiently store and retrieve vector-based data for similarity queries.


## Contributing

We welcome contributions! Feel free to submit issues or pull requests for bug fixes, enhancements, or new features.

### To contribute:

1. Fork the repository.
2. Clone your fork: `git clone https://github.com/your-username/docparseai.git`
3. Create a feature branch: `git checkout -b feature-name`
4. Commit your changes: `git commit -m "Add feature"`
5. Push to your fork: `git push origin feature-name`
6. Open a Pull Request


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


### Feedback / Issues

If you encounter any issues or have feedback, feel free to open an issue on GitHub or contact us directly.
