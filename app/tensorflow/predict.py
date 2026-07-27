import os
import pickle

import tensorflow as tf

from app.tensorflow.preprocess import clean_text

# -------------------------
# Paths
# -------------------------

SAVE_FOLDER = "app/tensorflow/saved_model"

MODEL_PATH = os.path.join(SAVE_FOLDER, "document_classifier.keras")
LABEL_PATH = os.path.join(SAVE_FOLDER, "label_encoder.pkl")

# -------------------------
# Lazy-loaded resources
# -------------------------

model = None
label_encoder = None

# -------------------------
# Create Vectorizer
# -------------------------

MAX_WORDS = 10000
MAX_SEQUENCE_LENGTH = 500

vectorizer = tf.keras.layers.TextVectorization(
    max_tokens=MAX_WORDS,
    output_mode="int",
    output_sequence_length=MAX_SEQUENCE_LENGTH
)

# -------------------------
# Load Model Only When Needed
# -------------------------

def load_prediction_resources():
    global model, label_encoder

    if model is None:
        print("Loading TensorFlow model...")
        model = tf.keras.models.load_model(MODEL_PATH)

        with open(LABEL_PATH, "rb") as file:
            label_encoder = pickle.load(file)

        print("Prediction module loaded successfully.")

# -------------------------
# Prediction Function
# -------------------------

def predict_category(text):

    load_prediction_resources()

    text = clean_text(text)

    vectorizer.adapt([text])

    sequence = vectorizer(tf.constant([text]))

    prediction = model.predict(sequence, verbose=0)

    predicted_index = tf.argmax(prediction, axis=1).numpy()[0]

    category = label_encoder.inverse_transform([predicted_index])[0]

    return category