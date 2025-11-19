import os
import tempfile
from typing import Dict, List, Any
from pathlib import Path
from PyPDFForm import PdfWrapper


def get_pdf_form_fields(pdf_path: str) -> List[str]:
    """
    Get all fillable field names from a PDF form.
    
    Args:
        pdf_path: Path to the PDF form
    
    Returns:
        List of field names
    """
    try:
        form = PdfWrapper(pdf_path)
        schema = form.schema
        
        # schema is a dict like {'type': 'object', 'properties': {'field1': {...}, 'field2': {...}}}
        # Extract only the field names from the 'properties' key
        if schema and isinstance(schema, dict):
            if 'properties' in schema:
                # Extract field names from the properties dict
                return list(schema['properties'].keys())
            else:
                # Fallback: if schema is just a dict of fields
                return list(schema.keys())
        
        return []
    except Exception as e:
        raise ValueError(f"Failed to read PDF form fields: {str(e)}")


def fill_pdf_form(
    pdf_template_path: str,
    field_data: Dict[str, Any],
    output_path: str = None
) -> str:
    """
    Fill a PDF form with provided data using PyPDFForm.
    
    Args:
        pdf_template_path: Path to the PDF template
        field_data: Dictionary of {field_name: value} to fill
        output_path: Optional path for output PDF. If None, creates temp file.
    
    Returns:
        Path to the filled PDF file
    """
    try:
        # Load the PDF form
        form = PdfWrapper(pdf_template_path)
        
        # Fill the form
        # PyPDFForm expects a dict with field names as keys
        form.fill(field_data)
        
        # Generate output path if not provided
        if output_path is None:
            suffix = Path(pdf_template_path).suffix or ".pdf"
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            output_path = temp_file.name
            temp_file.close()
        
        # Read the filled PDF bytes
        filled_pdf_bytes = bytes(form.read())
        
        # Write to output file
        with open(output_path, 'wb') as f:
            f.write(filled_pdf_bytes)
        
        return output_path
        
    except Exception as e:
        raise ValueError(f"Failed to fill PDF form: {str(e)}")


def validate_and_prepare_field_data(
    filled_fields: Dict[str, Any],
    form_fields: List[str]
) -> tuple[Dict[str, Any], List[str]]:
    """
    Validate filled fields against form fields and identify missing required fields.
    
    Args:
        filled_fields: Dictionary of filled field data
        form_fields: List of all form field names
    
    Returns:
        Tuple of (valid_field_data, missing_fields)
    """
    valid_data = {}
    missing_fields = []
    
    for field in form_fields:
        if field in filled_fields and filled_fields[field]:
            # Convert to string for PDF form
            valid_data[field] = str(filled_fields[field])
        else:
            missing_fields.append(field)
    
    return valid_data, missing_fields
