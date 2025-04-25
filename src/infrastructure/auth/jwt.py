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
        if payload.get('type') != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token type. Expected \'access\'.',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired.',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from e
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials.',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from e


def extract_user_id(payload: Dict[str, Any]) -> UUID:
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token payload.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return UUID(user_id)
