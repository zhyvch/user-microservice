from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.users import UserEntity


@dataclass
class BaseUserRepository(ABC):
    loaded_users: set[UserEntity] = field(default_factory=set, kw_only=True)

    @abstractmethod
    async def get(self, user_id: UUID) -> UserEntity | None:
        pass

    @abstractmethod
    async def add(self, user: UserEntity) -> None:
        pass
