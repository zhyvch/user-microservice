from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.users import UserEntity


class BaseUserRepositoryCacher(ABC):
    @abstractmethod
    async def get_from_cache(self, user_id: UUID) -> UserEntity | None:
        ...

    @abstractmethod
    async def add_to_cache(self, user: UserEntity) -> None:
        ...

    @abstractmethod
    async def remove_from_cache(self, user_id: UUID) -> None:
        ...

    def __call__(self, cls):
        get = cls.get
        update_status = cls.update_status

        async def _get(cls_self, user_id: UUID) -> UserEntity | None:
            user = await self.get_from_cache(user_id)
            if user:
                cls_self.loaded_users.add(user)
                return user

            user = await get(cls_self, user_id)
            if user:
                await self.add_to_cache(user)
            return user

        async def _update_status(cls_self, user_id: UUID, status: str) -> None:
            await update_status(cls_self, user_id, status)
            await self.remove_from_cache(user_id)

        cls.get = _get
        cls.update_status = _update_status
        return cls
