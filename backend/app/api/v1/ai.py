from fastapi import APIRouter
from pydantic import BaseModel

from ...services.ai_service import extract_fields_from_document

router = APIRouter()

class ExtractRequest(BaseModel):
    document_url: str

@router.post("/extract")
async def extract(payload: ExtractRequest):
    # Stub: AI service returns mocked fields
    data = await extract_fields_from_document(payload.document_url)
    return {"fields": data}
