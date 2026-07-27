from app.services.classifier_service import classify_document

result = classify_document(
    "app/uploads/Nmap_Complete_Guides.pdf"
)

print(result["category"])