model = None


def get_model():
    global model

    if model is None:
        print("Loading SentenceTransformer...")

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


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

    embedding_model = get_model()

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings