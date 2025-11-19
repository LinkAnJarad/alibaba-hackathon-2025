import os
import base64
from typing import Dict
from openai import OpenAI
from ..core.config import settings


def get_qwen_client() -> OpenAI:
    """Get OpenAI client configured for Qwen API."""
    return OpenAI(
        api_key=settings.QWEN_API_KEY,
        base_url=settings.QWEN_API_ENDPOINT or "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )


def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def extract_fields_from_document(document_url: str) -> Dict:
    """
    Extract fields from a document using Qwen VL.
    For local files, pass absolute path. For remote, pass URL.
    """
    # Check if it's a local file or URL
    if document_url.startswith("http://") or document_url.startswith("https://"):
        # Remote image URL
        image_content = {"type": "image_url", "image_url": {"url": document_url}}
    else:
        # Local file - encode to base64
        if not os.path.exists(document_url):
            return {"error": f"File not found: {document_url}"}
        
        # Determine MIME type
        ext = os.path.splitext(document_url)[1].lower()
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        mime_type = mime_map.get(ext, "image/jpeg")
        
        base64_image = encode_image_to_base64(document_url)
        image_content = {
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
        }
    
    try:
        client = get_qwen_client()
        
        # Create extraction prompt
        prompt = """Extract all information from this document. 
        Focus on:
        - Full name
        - ID number
        - Date of birth
        - Address
        - Sex/Gender
        - Any other relevant personal information
        
        Return the information in JSON format with keys: full_name, id_number, date_of_birth, address, sex, and any other fields you find.
        If a field is not present, use null."""
        
        completion = client.chat.completions.create(
            model="qwen-vl-max",  # Using qwen-vl-max for better accuracy; can use qwen-vl-plus or qwen3-vl-flash
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        image_content
                    ]
                }
            ],
            temperature=0.1,  # Low temperature for consistent extraction
        )
        
        # Parse response
        response_text = completion.choices[0].message.content
        
        # Try to extract JSON from response
        import json
        import re
        
        # Look for JSON in code blocks or raw JSON
        json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', response_text, re.DOTALL)
        if json_match:
            extracted_data = json.loads(json_match.group(1))
        else:
            # Try to parse as raw JSON
            try:
                extracted_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: return the raw text
                extracted_data = {"raw_text": response_text}
        
        return extracted_data
        
    except Exception as e:
        return {"error": str(e)}
