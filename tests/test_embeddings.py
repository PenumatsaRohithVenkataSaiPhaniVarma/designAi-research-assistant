from app.services.embedding_service import generate_embeddings

chunks = [
    "Nmap is a network scanning tool.",
    "SQL Injection is a web application attack."
]

embeddings = generate_embeddings(chunks)

print(f"Total Embeddings: {len(embeddings)}")
print(f"Embedding Dimension: {len(embeddings[0])}")
print(embeddings[0][:10])  # Show first 10 numbers