from fastapi import APIRouter, UploadFile, File
from .. import v1
from ...services.storage_service import upload_file_to_oss

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Stub: just pass to storage service which returns a mock URL
    url = await upload_file_to_oss(file)
    return {"filename": file.filename, "url": url}
