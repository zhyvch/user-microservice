from typing import Dict, Any
from uuid import UUID

import jwt
from fastapi import HTTPException, status

from infrastructure.auth.security import get_public_key
from settings.config import settings

PUBLIC_KEY = get_public_key()


def verify_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            get_public_key(),
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )


def extract_user_id(payload: Dict[str, Any]) -> UUID:
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token payload',
        )
    return UUID(user_id)
