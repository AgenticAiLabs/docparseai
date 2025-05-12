import faiss
import numpy as np
from typing import List, Tuple

class FAISSStore:
    def __init__(self):
        # Initialize the FAISS index and chunks list
        self.index = None
        self.chunks = []

    def from_embeddings(self, chunks: List[str], embeddings: List[List[float]]):
        """
        Creates a FAISS index from document chunks and their corresponding embeddings.

        Args:
            chunks (List[str]): List of document chunks (text data).
            embeddings (List[List[float]]): List of embeddings (vector representation of the document chunks).

        Returns:
            self: Returns the FAISSStore object, allowing method chaining.
        """
        # Store the chunks (text data)
        self.chunks = chunks
        
        # Get the dimension of the embeddings (should be the same for all embeddings)
        dimension = len(embeddings[0])  # The number of elements in each embedding vector
        
        # Create a FAISS index for L2 (Euclidean) distance computation
        # IndexFlatL2 is a basic, simple FAISS index for finding the nearest neighbors based on L2 distance
        self.index = faiss.IndexFlatL2(dimension)
        
        # Convert the embeddings into a numpy array and add them to the FAISS index
        # FAISS requires the embeddings to be in float32 format
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Return the FAISSStore object itself for chaining method calls
        return self

    def query(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Queries the FAISS index to retrieve the top-k closest document chunks based on the similarity to the query embedding.

        Args:
            query_embedding (List[float]): The embedding (vector representation) of the query text.
            top_k (int): The number of closest results to return (default is 5).

        Returns:
            List[Tuple[str, float]]: A list of tuples containing:
                - The document chunk (str)
                - The similarity score (float) based on L2 distance (lower is better)
        """
        # Check if the FAISS index exists; raise an error if not
        if not self.index:
            raise ValueError("Index is empty. Use from_embeddings() first to populate the index.")
        
        # Perform the nearest neighbor search on the FAISS index
        # `self.index.search()` returns:
        #   - D: Distances between the query and the top_k closest embeddings
        #   - I: Indices of the top_k closest embeddings in the index
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        
        # Create a list of tuples (document chunk, similarity score) from the results
        # D contains the distance (similarity), and I contains the indices of the closest chunks
        return [(self.chunks[i], float(D[0][j])) for j, i in enumerate(I[0])]
