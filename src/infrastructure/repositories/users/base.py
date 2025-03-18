from dataclasses import dataclass
from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.users import UserEntity


@dataclass
class BaseUserRepository(ABC):
    async def get(self, user_id: UUID) -> UserEntity | None:
        pass

    async def add(self, user: UserEntity) -> None:
        pass
