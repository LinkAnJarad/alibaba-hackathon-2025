from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ...dependencies.auth import get_current_user
from ...core.security import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

@router.post("/login")
def login(payload: LoginRequest):
    # Stub: always returns a token
    token = create_access_token({"sub": payload.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(payload: RegisterRequest):
    # Stub: pretend user created
    return {"message": "registered", "email": payload.email}

@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return {"user": user}
