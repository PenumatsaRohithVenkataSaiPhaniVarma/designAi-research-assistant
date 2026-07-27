from app.tensorflow.preprocess import clean_text

sample = """
This IS an AI Research Paper 2026!!!
TensorFlow is AMAZING.
"""

print(clean_text(sample))