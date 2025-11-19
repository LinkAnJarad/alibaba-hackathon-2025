from pydantic import BaseModel

class UserOut(BaseModel):
    id: int | None = None
    email: str
    name: str
    verified: bool = False
