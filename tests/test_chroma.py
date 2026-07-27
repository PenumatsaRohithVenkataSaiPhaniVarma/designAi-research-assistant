from app.services.embedding_service import generate_embeddings
from app.vector_db.chroma_manager import store_document

chunks = [
    "Nmap is a network scanning tool.",
    "SQL Injection is a web vulnerability."
]

embeddings = generate_embeddings(chunks)

store_document(
    "sample.pdf",
    chunks,
    embeddings
)

print("Stored successfully!")