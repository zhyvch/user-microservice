from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID

from domain.commands.users import UserCredentialsStatus
from domain.entities.users import UserEntity


@dataclass
class BaseUserRepository(ABC):
    loaded_users: set[UserEntity] = field(default_factory=set, kw_only=True)

    @abstractmethod
    async def add(self, user: UserEntity) -> None:
        ...

    @abstractmethod
    async def get(self, user_id: UUID) -> UserEntity | None:
        ...

    @abstractmethod
    async def update_status(self, user_id: UUID, status: UserCredentialsStatus) -> None:
        ...

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        add = cls.add
        get = cls.get

        async def _add(self, user: UserEntity) -> None:
            await add(self, user)
            self.loaded_users.add(user)

        async def _get(self, user_id: UUID) -> UserEntity | None:
            user = await get(self, user_id)
            if user:
                self.loaded_users.add(user)
            return user

        cls.add = _add
        cls.get = _get

