from app.services.file_service import save_uploaded_file
from app.services.text_extractor import extract_text
from app.services.document_analyzer import analyze_document
from app.services.summarizer_service import summarize_text
from app.utils.text_chunker import chunk_text
from app.services.embedding_service import generate_embeddings
from app.vector_db.chroma_manager import store_document

def process_document(file):
    """
    Complete document processing pipeline.
    """

    # Save uploaded file
    filename, filepath = save_uploaded_file(file)

    # Extract text
    text = extract_text(filepath)

    # Generate summary
    summary = summarize_text(text)
    # Split text into chunks
    chunks = chunk_text(text)

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Store document in ChromaDB
    store_document(
        document_name=filename,
        chunks=chunks,
        embeddings=embeddings
    )

    metadata = analyze_document(filepath, text)

    return {
        "filename": filename,
        "filepath": filepath,
        "text": text,
        "summary": summary,
        "metadata": metadata
    }