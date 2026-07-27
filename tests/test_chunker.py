from app.utils.text_chunker import chunk_text

text = " ".join([f"word{i}" for i in range(1, 1201)])

chunks = chunk_text(text)

print(f"Total Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}")
    print(chunk[:120] + "...")