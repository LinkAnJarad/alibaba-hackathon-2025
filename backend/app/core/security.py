from datetime import datetime, timedelta
from typing import Dict

from .config import settings

# NOTE: This is a stub. Replace with python-jose or PyJWT later.
def create_access_token(data: Dict, expires_minutes: int = 60) -> str:
    # Return a predictable mock token for MVP
    sub = data.get("sub", "user")
    return f"mock-token-for:{sub}"


def decode_token(token: str) -> Dict:
    if token.startswith("mock-token-for:"):
        sub = token.split("mock-token-for:", 1)[1]
        return {"sub": sub}
    return {}
