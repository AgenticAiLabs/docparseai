# test_text_splitter.py
from docparseai.utils.text_splitter import TextSplitter

text = """This is the first sentence. This is the second sentence. This is the third sentence. 
          Here comes the fourth sentence. And the fifth one is here."""

chunks = TextSplitter.split(text, chunk_size=50, overlap=20, method="sentence")
print("Sentence-based chunks:")
for idx, chunk in enumerate(chunks, 1):
    print(f"Chunk {idx}: {chunk}")

chunks_token = TextSplitter.split(text, chunk_size=10, overlap=5, method="token")
print("\nToken-based chunks:")
for idx, chunk in enumerate(chunks_token, 1):
    print(f"Chunk {idx}: {chunk}")
