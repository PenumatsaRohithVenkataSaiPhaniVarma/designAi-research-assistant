from app.vector_db.chroma_manager import search_documents

results = search_documents("What is SQL Injection?")

print(results["documents"])