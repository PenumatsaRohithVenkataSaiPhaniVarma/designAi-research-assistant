def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks.

    Args:
        text (str): Extracted document text.
        chunk_size (int): Number of words per chunk.
        overlap (int): Number of overlapping words.

    Returns:
        list: List of text chunks.
    """

    if not text:
        return []

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks