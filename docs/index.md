
# docparseai: Document Parsing, Chunking, and Embedding

`docparseai` is an open-source Python package designed for document processing tasks. It enables parsing, chunking, embedding, and efficient retrieval of document chunks using **FAISS** for vector similarity search. Ideal for applications like document summarization, intelligent search engines, and semantic question answering.

---

## 📚 Table of Contents

- [Installation](#installation)
- [Modules](#modules)
  - [DocumentLoader](#1-documentloader)
  - [TextSplitter](#2-textsplitter)
  - [Embedder](#3-embedder)
  - [FAISSStore](#4-faissstore)
- [Full Workflow Example](#full-workflow-example)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)
- [Feedback / Issues](#feedback--issues)

---

## 🚀 Installation

Install `docparseai` via PyPI:

```bash
pip install docparseai
```

### Optional Dependency for Embeddings

To use `sentence-transformers` for semantic embeddings:

```bash
pip install docparseai[embedding]
```

---

## 🧩 Modules

### 1. `DocumentLoader`

Parses `.pdf`, `.docx`, and `.txt` into clean text.

```python
from docparseai.document_loader import DocumentLoader

text = DocumentLoader.load("file.pdf")
```

---

### 2. `TextSplitter`

Splits text into chunks. Supports sentence- and token-based methods.

```python
from docparseai.text_splitter import TextSplitter

chunks = TextSplitter.split(text, chunk_size=500, overlap=50)
```

---

### 3. `Embedder`

Uses `sentence-transformers` to generate dense embeddings. Defaults to `all-MiniLM-L6-v2`.

```python
from docparseai.embeddings.embedder import Embedder

embedder = Embedder()
embeddings = embedder.embed(chunks)
```

---

### 4. `FAISSStore`

Stores embeddings and enables semantic querying.

```python
from docparseai.vectorstore.faiss_store import FAISSStore

store = FAISSStore().from_embeddings(chunks, embeddings)
top_k_results = store.query(query_embedding, top_k=5)
```

---

## 🧪 Full Workflow Example

```python
from docparseai.document_loader import DocumentLoader
from docparseai.text_splitter import TextSplitter
from docparseai.embeddings.embedder import Embedder
from docparseai.vectorstore.faiss_store import FAISSStore

text = DocumentLoader.load("file.pdf")
chunks = TextSplitter.split(text, chunk_size=500, overlap=50)
embedder = Embedder()
embeddings = embedder.embed(chunks)
store = FAISSStore().from_embeddings(chunks, embeddings)

query = "What is this document about?"
query_embedding = embedder.embed(query)[0]
top_k_results = store.query(query_embedding, top_k=5)

for chunk, score in top_k_results:
    print(f"Chunk: {chunk} - Score: {score}")
```

---

## 📝 Notes

- **Embeddings are optional.** You can use basic functionality without installing `sentence-transformers`.
- **FAISS** provides fast, efficient similarity search via dense vectors.

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repo
2. Clone: `git clone https://github.com/your-username/docparseai.git`
3. Create a branch: `git checkout -b feature-name`
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature-name`
6. Open a Pull Request

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 📬 Feedback / Issues

Please [open an issue](https://github.com/your-username/docparseai/issues) or contact us directly.
