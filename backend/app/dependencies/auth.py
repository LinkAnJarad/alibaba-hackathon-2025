from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import decode_token
from ..services.auth_service import get_user_by_id
from ..models.user import User
from .database import get_db


async def get_current_user(
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Dependency to get the current authenticated user from JWT token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            raise ValueError("Invalid scheme")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = await get_user_by_id(db, user_id_int)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


async def get_current_verified_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to ensure current user is verified."""
    if not current_user.verified:
        raise HTTPException(
            status_code=403,
            detail="User not verified. Please visit barangay hall for verification.",
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to ensure current user is an admin."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
