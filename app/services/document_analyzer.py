import os
import fitz  # PyMuPDF


def analyze_document(file_path, text):
    """
    Analyse an uploaded document and return useful metadata.
    """

    metadata = {
        "filename": os.path.basename(file_path),
        "extension": os.path.splitext(file_path)[1].lower(),
        "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
        "pages": get_page_count(file_path),
        "word_count": count_words(text),
        "character_count": len(text),
        "estimated_reading_time": estimate_reading_time(text)
    }

    return metadata


def get_page_count(file_path):
    """
    Return the number of pages in a PDF.
    """

    if file_path.endswith(".pdf"):
        pdf = fitz.open(file_path)
        pages = len(pdf)
        pdf.close()
        return pages

    return 1


def count_words(text):
    return len(text.split())


def estimate_reading_time(text):
    """
    Average reading speed = 200 words/minute.
    """

    words = count_words(text)

    minutes = max(1, round(words / 200))

    return f"{minutes}"