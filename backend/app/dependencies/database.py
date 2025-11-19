from typing import AsyncGenerator
from ..core.db import SessionLocal

async def get_db() -> AsyncGenerator:
    """Dependency to provide database session."""
    async with SessionLocal() as session:
        yield session
