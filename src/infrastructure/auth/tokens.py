from typing import Dict, Any
from uuid import UUID

import jwt

from infrastructure.auth.security import get_public_key
from infrastructure.exception.users import JWTExpiredException, JWTCredentialsInvalidException, JWTWrongTypeException, \
    JWTException
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
            raise JWTWrongTypeException(expected_type='access', actual_type=payload.get('type'))
        return payload
    except jwt.ExpiredSignatureError as e:
        raise JWTExpiredException from e
    except jwt.PyJWTError as e:
        raise JWTCredentialsInvalidException from e


def extract_user_id(payload: Dict[str, Any]) -> UUID:
    user_id = payload.get('sub')
    if not user_id:
        raise JWTException
    return UUID(user_id)
