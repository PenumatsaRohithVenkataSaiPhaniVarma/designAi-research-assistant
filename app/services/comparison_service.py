import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from config.settings import GEMINI_API_KEY
from app.services.text_extractor import extract_text

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")


def compare_documents(document1, document2, documents):
    """
    Compare two uploaded documents without using ChromaDB.
    """

    file1 = None
    file2 = None

    for doc in documents:

        if doc["filename"] == document1:
            file1 = doc

        elif doc["filename"] == document2:
            file2 = doc

    if not file1 or not file2:
        return "⚠ One or both selected documents could not be found."

    text1 = extract_text(file1["filepath"])
    text2 = extract_text(file2["filepath"])

    prompt = f"""
You are an AI Research Assistant.

Compare these two documents.

Document 1:
{document1}

{text1}

------------------------------------

Document 2:
{document2}

{text2}

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

    except Exception as e:
        print(e)
        return "⚠ An unexpected error occurred."