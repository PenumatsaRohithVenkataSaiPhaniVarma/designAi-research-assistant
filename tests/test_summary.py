from app.services.summarizer_service import summarize_text

text = """
Artificial Intelligence is transforming modern cybersecurity.
Machine learning helps detect threats faster.
Organizations use AI to automate security monitoring.
Deep learning models can identify complex attack patterns.
"""

summary = summarize_text(text)

print(summary)