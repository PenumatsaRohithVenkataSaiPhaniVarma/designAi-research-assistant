from app.tensorflow.predict import predict_category


def classify_document(text):
    """
    Predict document category using already extracted text.
    """

    category = predict_category(text)

    return {
        "category": category
    }