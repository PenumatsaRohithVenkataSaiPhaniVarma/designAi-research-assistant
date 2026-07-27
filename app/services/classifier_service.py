from app.services.text_extractor import extract_text
from app.tensorflow.predict import predict_category


def classify_document(file_path):
    """
    Extract text from the uploaded document
    and predict its category.
    """

    text = extract_text(file_path)

    category = predict_category(text)

    return {
        "category": category,
        "text": text
    }