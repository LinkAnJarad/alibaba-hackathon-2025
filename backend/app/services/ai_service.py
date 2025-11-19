from typing import Dict

async def extract_fields_from_document(document_url: str) -> Dict:
    # Stub: pretend to call Qwen OCR + QwenVL + Qwen2.5
    # Return common barangay form fields as example
    return {
        "full_name": "Juan Dela Cruz",
        "address": "123 Mabuhay St, Brgy. 1",
        "date_of_birth": "1990-01-01",
        "purpose": "Barangay Clearance",
        "id_number": "ID-123456",
    }
