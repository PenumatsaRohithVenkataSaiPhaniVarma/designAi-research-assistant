import chromadb
from app.services.embedding_service import generate_embeddings

client = None
collection = None


def get_collection():
    global client, collection

    if collection is None:
        client = chromadb.PersistentClient(
            path="app/vector_db/chroma_storage"
        )

        collection = client.get_or_create_collection(
            name="research_documents"
        )

    return collection


def clear_database():
    """
    Clear all documents from ChromaDB before a new upload.
    """

    global client, collection

    if client is None:
        client = chromadb.PersistentClient(
            path="app/vector_db/chroma_storage"
        )

    try:
        client.delete_collection("research_documents")
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name="research_documents"
    )


def store_document(document_name, chunks, embeddings):
    """
    Store document chunks and embeddings in ChromaDB.
    """

    collection = get_collection()

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

    collection = get_collection()

    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results