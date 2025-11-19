from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from ..models.user import User, UserRole
from ..core.security import get_password_hash, verify_password


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Retrieve a user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Retrieve a user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def register_user(
    db: AsyncSession, email: str, password: str, name: str
) -> User:
    """
    Register a new user.
    Returns the created user.
    Raises ValueError if email already exists.
    """
    # Check if user already exists
    existing_user = await get_user_by_email(db, email)
    if existing_user:
        raise ValueError("Email already registered")

    # Create new user
    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        name=name,
        password_hash=hashed_password,
        verified=False,
        role=UserRole.RESIDENT.value,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[User]:
    """
    Authenticate a user by email and password.
    Returns the user if credentials are valid, None otherwise.
    """
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def verify_user(db: AsyncSession, user_id: int) -> User:
    """
    Mark a user as verified (admin action after in-person verification).
    Returns the updated user.
    Raises ValueError if user not found.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    
    user.verified = True
    await db.commit()
    await db.refresh(user)
    return user


async def set_user_role(db: AsyncSession, user_id: int, role: UserRole) -> User:
    """
    Set a user's role (admin action).
    Returns the updated user.
    Raises ValueError if user not found.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    
    user.role = role.value
    await db.commit()
    await db.refresh(user)
    return user
