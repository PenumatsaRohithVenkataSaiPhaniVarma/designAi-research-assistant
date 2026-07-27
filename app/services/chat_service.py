import google.generativeai as genai

from app.vector_db.chroma_manager import search_documents
from config.settings import GEMINI_API_KEY
from google.api_core.exceptions import ResourceExhausted

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")


def generate_answer(question, context, history):
    """
    Generate an answer using the retrieved document context.
    """

    conversation = ""

    for chat in history:

        conversation += f"""
User: {chat['question']}
Assistant: {chat['answer']}
"""

    prompt = f"""
You are an AI Research Assistant.

Use the previous conversation when answering follow-up questions.

Answer ONLY using the information provided below.

If the answer is not available in the context, reply:

"I couldn't find that information in the uploaded documents."

Previous Conversation:
{conversation}

Document Context:
{context}

Current Question:
{question}
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except ResourceExhausted:

        return "⚠ Gemini API quota exceeded. Please try again later."

    except Exception as e:

        print(e)

        return "⚠ An unexpected error occurred while generating the answer."
def ask_document(question,history):
    """
    Search the uploaded documents and generate an answer.
    """

    # Search ChromaDB
    results = search_documents(question)

    # Get retrieved text chunks
    if not results["documents"] or not results["documents"][0]:
        return {
            "question": question,
            "answer": "I couldn't find that information in the uploaded documents.",
            "sources": [],
            "show_sources": False
        }

    documents = results["documents"][0]

    # Combine into context
    context = "\n\n".join(documents)

    # Generate answer using previous conversation
    answer = generate_answer(question, context, history)
    if answer is None:
        answer = "Sorry, I couldn't generate an answer."

    # Get metadata
    metadatas = results.get("metadatas", [[]])[0]

    # Remove duplicate document names
    unique_sources = []
    seen = set()

    for metadata in metadatas:

        document = metadata["document"]

        if document not in seen:
            seen.add(document)
            unique_sources.append(document)

    # Hide sources when no answer is found
    if "I couldn't find that information in the uploaded documents." in answer:
        unique_sources = []
        show_sources = False
    else:
        show_sources = len(unique_sources) > 0

    return {
        "question": question,
        "answer": answer,
        "sources": unique_sources,
        "show_sources": show_sources
    }