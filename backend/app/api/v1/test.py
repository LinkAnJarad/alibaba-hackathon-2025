from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, List

from ...services.ai_service import extract_fields_from_document
from ...services.pdf_form_service import get_pdf_form_fields, fill_pdf_form, validate_and_prepare_field_data
from ...services.pdf_mapping_service import map_extracted_data_to_form_fields

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


class AutoFillRequest(BaseModel):
    pdf_form_name: str  # Name of PDF form in test_data
    

class ManualFillRequest(BaseModel):
    pdf_form_name: str
    manual_fields: Dict[str, Any]


@router.post("/test/pdf/get-fields")
async def get_pdf_fields(payload: AutoFillRequest):
    """
    Get all fillable fields from a PDF form.
    """
    backend_root = Path(__file__).parent.parent.parent.parent
    test_data_dir = backend_root / "test_data"
    pdf_path = test_data_dir / payload.pdf_form_name
    
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"PDF form not found: {payload.pdf_form_name}")
    
    try:
        fields = get_pdf_form_fields(str(pdf_path))
        return {"fields": fields, "pdf_form": payload.pdf_form_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/pdf/auto-fill")
async def auto_fill_pdf(
    pdf_form: UploadFile = File(..., description="PDF form template"),
    document: UploadFile = File(..., description="Document image to extract data from")
):
    """
    Auto-fill a PDF form by:
    1. Extracting data from uploaded document image
    2. Getting PDF form fields
    3. Using AI to map extracted data to form fields
    4. Filling the PDF
    5. Returning filled PDF + missing fields for manual input
    """
    try:
        # Save uploaded files temporarily
        pdf_suffix = Path(pdf_form.filename or "form.pdf").suffix
        doc_suffix = Path(document.filename or "doc.jpg").suffix
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=pdf_suffix) as pdf_tmp:
            pdf_content = await pdf_form.read()
            pdf_tmp.write(pdf_content)
            pdf_tmp_path = pdf_tmp.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=doc_suffix) as doc_tmp:
            doc_content = await document.read()
            doc_tmp.write(doc_content)
            doc_tmp_path = doc_tmp.name
        
        # Step 1: Extract data from document
        extracted_data = await extract_fields_from_document(doc_tmp_path)
        
        if "error" in extracted_data:
            os.unlink(pdf_tmp_path)
            os.unlink(doc_tmp_path)
            raise HTTPException(status_code=500, detail=f"Extraction failed: {extracted_data['error']}")
        
        # Step 2: Get PDF form fields
        form_fields = get_pdf_form_fields(pdf_tmp_path)
        
        # Step 3: Use AI to map extracted data to form fields
        mapping_result = await map_extracted_data_to_form_fields(extracted_data, form_fields)
        
        filled_fields = mapping_result.get("filled_fields", {})
        missing_fields = mapping_result.get("missing_fields", [])
        mappings = mapping_result.get("mappings", [])
        
        # Step 4: Fill PDF (with whatever data we have)
        valid_data, _ = validate_and_prepare_field_data(filled_fields, form_fields)
        
        output_pdf_path = fill_pdf_form(pdf_tmp_path, valid_data)
        
        # Clean up temp files
        os.unlink(pdf_tmp_path)
        os.unlink(doc_tmp_path)
        
        # Return result with filled PDF path (stored temporarily)
        return {
            "filled_pdf_path": output_pdf_path,
            "extracted_data": extracted_data,
            "mappings": mappings,
            "filled_fields": filled_fields,
            "missing_fields": missing_fields,
            "message": f"PDF filled with {len(filled_fields)} fields. {len(missing_fields)} fields need manual input."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auto-fill failed: {str(e)}")


@router.post("/test/pdf/complete-fill")
async def complete_pdf_fill(payload: ManualFillRequest):
    """
    Complete PDF filling with manually provided fields.
    Used after auto-fill when some fields are missing.
    """
    backend_root = Path(__file__).parent.parent.parent.parent
    test_data_dir = backend_root / "test_data"
    pdf_path = test_data_dir / payload.pdf_form_name
    
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"PDF form not found: {payload.pdf_form_name}")
    
    try:
        # Fill PDF with manual fields
        output_pdf_path = fill_pdf_form(str(pdf_path), payload.manual_fields)
        
        return FileResponse(
            output_pdf_path,
            media_type="application/pdf",
            filename=f"filled_{payload.pdf_form_name}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test/pdf/download/{temp_filename}")
async def download_filled_pdf(temp_filename: str):
    """
    Download a temporarily stored filled PDF.
    """
    # For security, only allow files from temp directory
    temp_dir = Path(tempfile.gettempdir())
    file_path = temp_dir / temp_filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        str(file_path),
        media_type="application/pdf",
        filename=f"filled_form.pdf"
    )
