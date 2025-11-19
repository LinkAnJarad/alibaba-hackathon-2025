from pydantic import BaseModel

class SubmissionOut(BaseModel):
    id: int | None = None
    form_type: str
    status: str
    document_url: str
    extracted_data: str | None = None
