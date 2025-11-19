# Simplified auth for prototyping (no JWT)
# For full auth flow, use query parameters or session management later

from fastapi import HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User
from ..services.auth_service import get_user_by_id
from .database import get_db


async def get_current_user_by_id(user_id: int = Query(...), db: AsyncSession = Depends(get_db)) -> User:
    """Get current user by ID (prototyping)."""
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
