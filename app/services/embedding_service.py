from sentence_transformers import SentenceTransformer


# Load the embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Generate embeddings for a list of text chunks.

    Args:
        chunks (list): List of text chunks.

    Returns:
        list: List of embedding vectors.
    """

    if not chunks:
        return []

    embeddings = model.encode(chunks, convert_to_numpy=True)

    return embeddings