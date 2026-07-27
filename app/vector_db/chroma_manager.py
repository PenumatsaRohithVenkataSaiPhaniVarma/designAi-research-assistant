import chromadb
from app.services.embedding_service import generate_embeddings

# Create a persistent database
client = chromadb.PersistentClient(path="app/vector_db/chroma_storage")

# Create (or load) a collection
collection = client.get_or_create_collection(
    name="research_documents"
)
def clear_database():
    """
    Clear all documents from ChromaDB before a new upload.
    """

    global collection

    try:
        client.delete_collection("research_documents")
    except:
        pass

    collection = client.get_or_create_collection(
        name="research_documents"
    )

def store_document(document_name, chunks, embeddings):
    """
    Store document chunks and embeddings in ChromaDB.
    """

    ids = [
        f"{document_name}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "document": document_name
        }
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )
def search_documents(query, top_k=5):
    """
    Search for the most relevant document chunks.
    """

    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results
