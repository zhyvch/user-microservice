from dataclasses import dataclass
from uuid import UUID

from infrastructure.exception.base import InfrastructureException


@dataclass(frozen=True, eq=False)
class UserNotFoundException(InfrastructureException):
    user_id: UUID

    @property
    def message(self) -> str:
        return f'User with ID <{self.user_id}> not found.'
