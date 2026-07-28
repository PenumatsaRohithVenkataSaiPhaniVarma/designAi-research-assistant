import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from config.settings import GEMINI_API_KEY

from app.utils.text_chunker import chunk_text
from app.services.embedding_service import generate_embeddings
from app.vector_db.chroma_manager import (
    clear_database,
    store_document,
    search_documents,
)
from app.services.text_extractor import extract_text

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")


def build_vector_database(documents):
    """
    Build ChromaDB only when Ask AI is pressed.
    """

    clear_database()

    for doc in documents:

        text = extract_text(doc["filepath"])

        chunks = chunk_text(text)

        embeddings = generate_embeddings(chunks)

        store_document(
            document_name=doc["metadata"]["filename"],
            chunks=chunks,
            embeddings=embeddings,
        )


def generate_answer(question, context, history):

    conversation = ""

    for chat in history:

        conversation += f"""
User: {chat['question']}
Assistant: {chat['answer']}
"""

    prompt = f"""
You are an AI Research Assistant.

Use previous conversation if needed.

Only answer from the document.

If the answer isn't found say:

I couldn't find that information in the uploaded documents.

Conversation:
{conversation}

Context:
{context}

Question:
{question}
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except ResourceExhausted:

        return "Gemini quota exceeded."

    except Exception as e:

        print(e)

        return "Unexpected error."


def ask_document(question, history, documents):

    build_vector_database(documents)

    results = search_documents(question)

    if not results["documents"] or not results["documents"][0]:

        return {
            "question": question,
            "answer": "I couldn't find that information in the uploaded documents.",
            "sources": [],
            "show_sources": False,
        }

    docs = results["documents"][0]

    context = "\n\n".join(docs)

    answer = generate_answer(question, context, history)

    metadatas = results["metadatas"][0]

    unique_sources = []

    seen = set()

    for metadata in metadatas:

        if metadata["document"] not in seen:

            seen.add(metadata["document"])

            unique_sources.append(metadata["document"])

    return {
        "question": question,
        "answer": answer,
        "sources": unique_sources,
        "show_sources": len(unique_sources) > 0,
    }