import os
import csv

from app.services.text_extractor import extract_text

# Paths
UPLOAD_FOLDER = "app/uploads"
LABELS_FILE = "data/document_labels.csv"
OUTPUT_FILE = "data/training_data.csv"

# Read labels
labels = {}

with open(LABELS_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        labels[row["filename"]] = row["category"]

# Create training dataset
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)
    writer.writerow(["text", "category"])

    for filename, category in labels.items():

        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if not os.path.exists(file_path):
            print(f"❌ File not found: {filename}")
            continue

        try:
            text = extract_text(file_path)

            if text.strip():
                writer.writerow([text, category])
                print(f"✅ Added: {filename}")

            else:
                print(f"⚠ No text found: {filename}")

        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

print("\nDataset created successfully!")