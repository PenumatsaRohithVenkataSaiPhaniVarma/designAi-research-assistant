import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import app.vector_db.chroma_manager as chroma_manager
from config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")


def compare_documents(document1, document2):

    # Retrieve all chunks of document 1
    result1 = chroma_manager.collection.get(
        where={"document": document1},
        include=["documents"]
    )

    # Retrieve all chunks of document 2
    result2 = chroma_manager.collection.get(
        where={"document": document2},
        include=["documents"]
    )

    context1 = "\n".join(result1["documents"])

    context2 = "\n".join(result2["documents"])

    prompt = f"""
You are an AI Research Assistant.

Compare these two documents.

Document 1:
{document1}

{context1}

------------------------------------

Document 2:
{document2}

{context2}

------------------------------------

Provide the comparison using these headings:

1. Purpose
2. Main Topics
3. Similarities
4. Differences
5. Key Takeaways

Keep the answer clear and easy to read.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except ResourceExhausted:

        return "⚠ Gemini API quota exceeded. Please wait a while and try again."