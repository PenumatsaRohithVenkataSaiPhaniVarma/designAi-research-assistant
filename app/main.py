print("===== MAIN.PY STARTED =====")

from flask import Flask, render_template
print("Flask imported")

from app.api.upload import upload_bp
print("upload.py imported")

app = Flask(__name__)
print("Flask app created")

app.secret_key = "designai_research_assistant_2026"

app.register_blueprint(upload_bp)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)