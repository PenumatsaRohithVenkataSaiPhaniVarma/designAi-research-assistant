import os
import pickle

import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import LabelEncoder

# -------------------------
# Load Dataset
# -------------------------

data = pd.read_csv("data/training_data.csv")

texts = data["text"].astype(str).tolist()
labels = data["category"].tolist()

print(f"Loaded {len(texts)} documents.")

# -------------------------
# Encode Labels
# -------------------------

label_encoder = LabelEncoder()

encoded_labels = label_encoder.fit_transform(labels)

print("\nCategories:")

for index, label in enumerate(label_encoder.classes_):
    print(f"{index} -> {label}")

# -------------------------
# Text Vectorization
# -------------------------

MAX_WORDS = 10000
MAX_SEQUENCE_LENGTH = 500

vectorizer = tf.keras.layers.TextVectorization(
    max_tokens=MAX_WORDS,
    output_mode="int",
    output_sequence_length=MAX_SEQUENCE_LENGTH
)

# Learn the vocabulary
vectorizer.adapt(texts)

print("\nText vectorizer created successfully.")
print(f"Vocabulary Size: {len(vectorizer.get_vocabulary())}")

# -------------------------
# Convert Text to Sequences
# -------------------------

X = vectorizer(tf.constant(texts))

print("\nText converted into sequences.")
print("Shape:", X.shape)

# -------------------------
# Build Neural Network
# -------------------------

model = tf.keras.Sequential([
    tf.keras.Input(shape=(MAX_SEQUENCE_LENGTH,)),
    tf.keras.layers.Embedding(
        input_dim=MAX_WORDS,
        output_dim=64
    ),

    tf.keras.layers.GlobalAveragePooling1D(),

    tf.keras.layers.Dense(
        64,
        activation="relu"
    ),

    tf.keras.layers.Dense(
        len(label_encoder.classes_),
        activation="softmax"
    )
])


print("\nModel created successfully.")
model.summary()

# -------------------------
# Compile Model
# -------------------------

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("\nModel compiled successfully.")

# -------------------------
# Train Model
# -------------------------

history = model.fit(
    X,
    encoded_labels,
    epochs=20,
    batch_size=2,
    verbose=1
)

print("\nTraining completed successfully.")

# -------------------------
# Save Label Encoder
# -------------------------

SAVE_FOLDER = "app/tensorflow/saved_model"

os.makedirs(SAVE_FOLDER, exist_ok=True)

with open(os.path.join(SAVE_FOLDER, "label_encoder.pkl"), "wb") as file:
    pickle.dump(label_encoder, file)

print("\nLabel encoder saved successfully.")

# -------------------------
# Save TensorFlow Model
# -------------------------

MODEL_PATH = os.path.join(SAVE_FOLDER, "document_classifier.keras")

model.save(MODEL_PATH)

print("\nTensorFlow model saved successfully.")
print(f"Saved at: {MODEL_PATH}")