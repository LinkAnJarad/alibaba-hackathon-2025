import json
import re
from typing import Dict, List, Any
from openai import OpenAI
from ..core.config import settings


def get_qwen_client() -> OpenAI:
    """Get OpenAI client configured for Qwen API."""
    return OpenAI(
        api_key=settings.QWEN_API_KEY,
        base_url=settings.QWEN_API_ENDPOINT or "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )


async def map_extracted_data_to_form_fields(
    extracted_data: Dict[str, Any],
    form_fields: List[str]
) -> Dict[str, Any]:
    """
    Use Qwen AI to intelligently map extracted document data to PDF form fields.
    
    Args:
        extracted_data: Data extracted from document (e.g., {"full_name": "John Doe", "address": "123 Main St"})
        form_fields: List of field names from the PDF form (e.g., ["first_name", "last_name", "street", "city"])
    
    Returns:
        {
            "mappings": [
                {
                    "type": "single",
                    "field": "complete_address",
                    "value": "123 Main St, Anytown",
                    "form_mapping": {
                        "type": "multiple",
                        "fields": [
                            {"field": "street", "value": "123 Main St"},
                            {"field": "city", "value": "Anytown"}
                        ]
                    }
                },
                ...
            ],
            "filled_fields": {"street": "123 Main St", "city": "Anytown", ...},
            "missing_fields": ["zip_code", "country"]
        }
    """
    try:
        client = get_qwen_client()
        
        prompt = f"""You are an intelligent form-filling assistant. Given extracted data from a document and a list of PDF form field names, create a smart mapping.

EXTRACTED DATA:
{json.dumps(extracted_data, indent=2)}

PDF FORM FIELDS:
{json.dumps(form_fields, indent=2)}

INSTRUCTIONS:
1. Map extracted data to form fields intelligently
2. If one extracted field maps to multiple form fields (e.g., "full_name" -> "first_name", "last_name"), split it
3. If multiple extracted fields combine into one form field (e.g., "street" + "city" -> "complete_address"), combine them
4. **IMPORTANT**: Handle numbered variants of fields (e.g., age, age_2, age_3). If you have data for "age", also fill "age_2", "age_3", etc. with the same value
5. **IMPORTANT**: For fields ending with _2, _3, etc., try to match them with the base field name (e.g., "firstname_2" should use data from "first_name" or "firstname")
6. Only mark a field as missing if there's truly no relevant data in the extracted data
7. Return a JSON object with three keys:
   - "mappings": array of mapping objects (see example below)
   - "filled_fields": flat dict of form_field -> value for all successfully mapped fields
   - "missing_fields": array of form field names that couldn't be filled from extracted data

MAPPING OBJECT STRUCTURE:
{{
  "type": "single" | "multiple",
  "field": "extracted_field_name",  // for single type
  "fields": [{{"field": "name", "value": "val"}}],  // for multiple type
  "value": "extracted_value",  // for single type
  "form_mapping": {{
    "type": "single" | "multiple",
    "field": "form_field_name",  // for single
    "fields": [{{"field": "form_field", "value": "val"}}]  // for multiple
  }}
}}

EXAMPLE OUTPUT:
{{
  "mappings": [
    {{
      "type": "single",
      "field": "full_name",
      "value": "John Doe",
      "form_mapping": {{
        "type": "multiple",
        "fields": [
          {{"field": "first_name", "value": "John"}},
          {{"field": "last_name", "value": "Doe"}},
          {{"field": "firstname_2", "value": "John"}},
          {{"field": "last_name_2", "value": "Doe"}}
        ]
      }}
    }},
    {{
      "type": "single",
      "field": "age",
      "value": "30",
      "form_mapping": {{
        "type": "multiple",
        "fields": [
          {{"field": "age", "value": "30"}},
          {{"field": "age_2", "value": "30"}}
        ]
      }}
    }},
    {{
      "type": "multiple",
      "fields": [
        {{"field": "street", "value": "123 Main St"}},
        {{"field": "city", "value": "Anytown"}}
      ],
      "form_mapping": {{
        "type": "single",
        "field": "complete_address",
        "value": "123 Main St, Anytown"
      }}
    }}
  ],
  "filled_fields": {{
    "first_name": "John",
    "last_name": "Doe",
    "firstname_2": "John",
    "last_name_2": "Doe",
    "age": "30",
    "age_2": "30",
    "complete_address": "123 Main St, Anytown"
  }},
  "missing_fields": ["zip_code", "country"]
}}

Return ONLY the JSON object, no explanations."""

        completion = client.chat.completions.create(
            model="qwen-plus",  # Using qwen-plus for reasoning
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that outputs valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
        )
        
        response_text = completion.choices[0].message.content
        
        # Parse JSON from response
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(1))
        else:
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: return basic mapping
                result = {
                    "mappings": [],
                    "filled_fields": {},
                    "missing_fields": form_fields,
                    "error": "Failed to parse AI response"
                }
        
        return result
        
    except Exception as e:
        return {
            "mappings": [],
            "filled_fields": {},
            "missing_fields": form_fields,
            "error": str(e)
        }
