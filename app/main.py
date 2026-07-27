from flask import Flask

print("MAIN STARTED")

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"