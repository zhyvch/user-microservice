from uuid import UUID

import pytest

from infrastructure.auth.tokens import verify_token, extract_user_id
from infrastructure.exception.users import JWTExpiredException, JWTWrongTypeException


class TestJWT:
    def test_verify_token(self, valid_jwt, expired_jwt, wrong_type_jwt):
        with pytest.raises(JWTExpiredException):
            verify_token(expired_jwt)

        with pytest.raises(JWTWrongTypeException):
            verify_token(wrong_type_jwt)

        payload = verify_token(valid_jwt)
        assert payload is not None

    def test_extract_user_id(self, valid_jwt):
        payload = verify_token(valid_jwt)
        user_id = extract_user_id(payload)
        assert user_id == UUID('df9b7aa6-b4e4-4a19-8c84-504e302eee98')
