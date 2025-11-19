from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from ...dependencies.auth import get_current_user, get_current_admin_user
from ...dependencies.database import get_db
from ...core.security import create_access_token
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


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


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
            message=f"Registration successful. Please visit the barangay hall for verification. User ID: {user.id}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return JWT access token.
    """
    user = await authenticate_user(db=db, email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create JWT token with user ID as subject
    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    return current_user


@router.post("/verify", response_model=UserOut)
async def verify_user_endpoint(
    payload: VerifyUserRequest,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user),
):
    """
    Admin endpoint: Verify a user after in-person identity check.
    Requires admin role.
    """
    try:
        user = await verify_user(db=db, user_id=payload.user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
