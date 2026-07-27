from app.services.chat_service import generate_answer
from app.vector_db.chroma_manager import search_documents

results = search_documents(question)

context = "\n".join(results["documents"][0])

answer = generate_answer(question, context)


print(answer)