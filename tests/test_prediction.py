from app.tensorflow.predict import predict_category

sample = """
Nmap is a network scanner used for penetration testing
and vulnerability assessment.
"""

print(predict_category(sample))