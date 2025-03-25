import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.users import UserEntity

#
# @dataclass
# class BaseUserRepository(ABC):
#     @abstractmethod
#     async def get(self, user_id: UUID) -> UserEntity | None:
#         pass
#
#     @abstractmethod
#     async def add(self, user: UserEntity) -> None:
#         pass
#


@dataclass
class BaseUserRepository(ABC):
    loaded_users: set[UserEntity] = field(default_factory=set, kw_only=True)

    @abstractmethod
    async def add(self, user: UserEntity) -> None:
        pass

    @abstractmethod
    async def get(self, user_id: UUID) -> UserEntity | None:
        pass

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

