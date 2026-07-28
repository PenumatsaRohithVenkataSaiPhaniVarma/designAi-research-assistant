from app.services.file_service import save_uploaded_file
from app.services.text_extractor import extract_text
from app.services.document_analyzer import analyze_document
from app.services.summarizer_service import summarize_text


def process_document(file):
    """
    Lightweight upload pipeline.
    """

    filename, filepath = save_uploaded_file(file)

    text = extract_text(filepath)

    summary = summarize_text(text)

    metadata = analyze_document(filepath, text)

    return {
        "filename": filename,
        "filepath": filepath,
        "text": text,
        "summary": summary,
        "metadata": metadata
    }