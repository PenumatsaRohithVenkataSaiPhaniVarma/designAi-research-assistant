import re


def summarize_text(text, max_sentences=3):
    """
    Generate a simple summary by returning
    the first few meaningful sentences.
    """

    if not text:
        return "No text available for summarization."

    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Remove empty sentences
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    if not sentences:
        return "No summary could be generated."

    summary = " ".join(sentences[:max_sentences])

    return summary