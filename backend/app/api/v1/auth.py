from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from ...dependencies.database import get_db
from ...services.auth_service import register_user, authenticate_user, verify_user
from ...schemas.user import UserOut
from ...models.user import User

router = APIRouter()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class MessageResponse(BaseModel):
    message: str


class VerifyUserRequest(BaseModel):
    user_id: int


@router.post("/register", response_model=MessageResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    Register a new user account.
    User will need to visit barangay hall for in-person verification.
    """
    try:
        user = await register_user(
            db=db, email=payload.email, password=payload.password, name=payload.name
        )
        return MessageResponse(
            message=f"Registration successful. User ID: {user.id}. Please visit the barangay hall for verification."
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=UserOut)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return user object.
    For prototyping only (no JWT tokens).
    """
    user = await authenticate_user(db=db, email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return user


@router.get("/me", response_model=UserOut)
async def me(user_id: int = Query(..., description="User ID"), db: AsyncSession = Depends(get_db)):
    """
    Get user information by ID.
    For prototyping: pass user_id as query parameter.
    """
    from ...services.auth_service import get_user_by_id
    
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/verify", response_model=UserOut)
async def verify_user_endpoint(
    payload: VerifyUserRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Admin endpoint: Verify a user after in-person identity check.
    For prototyping: simplified (no role check).
    """
    try:
        user = await verify_user(db=db, user_id=payload.user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
