from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import tempfile
from pathlib import Path

from ...services.ai_service import extract_fields_from_document

router = APIRouter()


class TestExtractRequest(BaseModel):
    test_file: str  # Name of test file in test_data directory


@router.post("/test/extract-upload")
async def test_extract_upload(file: UploadFile = File(...)):
    """
    Test endpoint: Upload an image and extract fields using Qwen VL.
    """
    # Save uploaded file temporarily
    try:
        suffix = Path(file.filename or "upload.jpg").suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Extract fields
        fields = await extract_fields_from_document(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return {
            "filename": file.filename,
            "extracted_fields": fields
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.post("/test/extract-sample")
async def test_extract_sample(payload: TestExtractRequest):
    """
    Test endpoint: Extract from a sample file in test_data directory.
    """
    # Get absolute path to backend root
    from ...core.config import settings
    backend_root = Path(__file__).parent.parent.parent.parent
    test_data_dir = backend_root / "test_data"
    
    file_path = test_data_dir / payload.test_file
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Test file not found: {payload.test_file}. Available files: {[f.name for f in test_data_dir.iterdir() if f.is_file()]}"
        )
    
    # Extract fields
    fields = await extract_fields_from_document(str(file_path.absolute()))
    
    return {
        "test_file": payload.test_file,
        "extracted_fields": fields
    }


@router.get("/test/list-samples")
async def list_test_samples():
    """List available test sample files."""
    backend_root = Path(__file__).parent.parent.parent.parent
    test_data_dir = backend_root / "test_data"
    
    if not test_data_dir.exists():
        return {"samples": [], "message": "test_data directory not found"}
    
    samples = [
        {
            "name": f.name,
            "size": f.stat().st_size,
            "type": f.suffix
        }
        for f in test_data_dir.iterdir()
        if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.txt', '.gif', '.webp']
    ]
    
    return {"samples": samples}
