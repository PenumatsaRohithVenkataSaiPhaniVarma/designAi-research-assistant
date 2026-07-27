import fitz  # PyMuPDF
from docx import Document


def extract_text(file_path):
    """
    Extract text from PDF, DOCX, or TXT files.
    """

    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx(file_path)

    elif file_path.endswith(".txt"):
        return extract_txt(file_path)

    else:
        raise ValueError("Unsupported file type")


def extract_pdf(file_path):
    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def extract_docx(file_path):
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()