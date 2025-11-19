from pydantic import BaseModel
from datetime import datetime

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    verified: bool
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True
