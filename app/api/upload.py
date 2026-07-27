from flask import Blueprint, jsonify, request, render_template, session
from app.services.classifier_service import classify_document
from app.services.chat_service import ask_document
from app.pipeline.ingest_pipeline import process_document
from app.services.comparison_service import compare_documents
from app.vector_db.chroma_manager import clear_database
from markdown import markdown


global chat_history

chat_history = []

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    clear_database()
    global chat_history
    chat_history = []

    # New upload = new conversation
    session["chat_history"] = []

    if "files" not in request.files:
        return jsonify({"error": "No files selected"}), 400

    files = request.files.getlist("files")

    if len(files) == 0:
        return jsonify({"error": "No files selected"}), 400

    all_results = []

    # Process every uploaded file
    for file in files:

        if file.filename == "":
            continue

        print("Processing:", file.filename)

        result = process_document(file)

        classification = classify_document(result["filepath"])

        all_results.append({
            "metadata": result["metadata"],
            "summary": result["summary"],
            "category": classification["category"]
        })

    # Save the first document in session (temporary)
    session["metadata"] = all_results[0]["metadata"]
    session["summary"] = all_results[0]["summary"]
    session["category"] = all_results[0]["category"]

    # Save all uploaded documents
    session["documents"] = [
        {
            "metadata": doc["metadata"],
            "summary": doc["summary"],
            "category": doc["category"]
        }
        for doc in all_results
    ]
    print("===== SAVED DOCUMENTS =====")
    print(session["documents"])

    return render_template(
        "result.html",

        metadata=all_results[0]["metadata"],
        summary=all_results[0]["summary"],
        category=all_results[0]["category"],
        documents=all_results
    )

@upload_bp.route("/ask", methods=["POST"])
def ask_ai():

    question = request.form.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    global chat_history

    history = chat_history

    result = ask_document(question, history)

    # Save the latest conversation
    history.append({
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"],
        "show_sources": result["show_sources"]
    })
    print(history)

    # Keep only the last 10 conversations
    history = history[-10:]

    chat_history = history
    print("===== SESSION DOCUMENTS =====")
    print(session.get("documents"))

    print("===== CHAT HISTORY =====")
    print(chat_history)

    return render_template(

        "result.html",

        metadata=session.get("metadata"),
        summary=session.get("summary"),
        category=session.get("category"),

        documents=session.get("documents"),

        history=history,

        question=result["question"],
        answer=result["answer"],
        sources=result["sources"],
        show_sources=result["show_sources"]
    )

@upload_bp.route("/compare", methods=["POST"])
def compare():

    document1 = request.form["document1"]
    document2 = request.form["document2"]


    if document1 == document2:
        comparison = "⚠ Please select two different documents."
    else:
        comparison = markdown(
                        compare_documents(document1, document2),
                        extensions=["tables"]
                    )
    return render_template(
        "result.html",

        metadata=session.get("metadata"),
        summary=session.get("summary"),
        category=session.get("category"),
        documents=session.get("documents", []),
        history=chat_history,
        comparison=comparison
    )