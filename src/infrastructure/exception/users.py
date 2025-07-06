from dataclasses import dataclass
from uuid import UUID

from infrastructure.exception.base import InfrastructureException


@dataclass(frozen=True, eq=False)
class UserNotFoundException(InfrastructureException):
    user_id: UUID

    @property
    def message(self) -> str:
        return f'User with ID <{self.user_id}> not found.'


@dataclass(frozen=True, eq=False)
class JWTException(InfrastructureException):
    @property
    def message(self) -> str:
        return f'JWT is not valid.'


@dataclass(frozen=True, eq=False)
class JWTExpiredException(JWTException):
    @property
    def message(self) -> str:
        return f'Token has expired.'


@dataclass(frozen=True, eq=False)
class JWTCredentialsInvalidException(JWTException):
    @property
    def message(self) -> str:
        return f'JWT credentials are invalid.'


@dataclass(frozen=True, eq=False)
class JWTWrongTypeException(JWTException):
    expected_type: str
    actual_type: str

    @property
    def message(self) -> str:
        return f'JWT type mismatch. Expected <{self.expected_type}>, but got <{self.actual_type}>.'
