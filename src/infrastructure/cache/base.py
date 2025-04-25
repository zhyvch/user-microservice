import logging
from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.users import UserEntity

logger = logging.getLogger(__name__)


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
        update_photo = cls.update_photo

        async def _get(cls_self, user_id: UUID) -> UserEntity | None:
            logger.debug('Attempting to get user %s from cache', user_id)
            user = await self.get_from_cache(user_id)
            if user:
                logger.debug('User \'%s\' are loaded in cache continue without repo hit', user_id)
                cls_self.loaded_users.add(user)
                return user

            logger.debug('User \'%s\' are not loaded in cache continue with repo hit', user_id)
            user = await get(cls_self, user_id)
            if user:
                logger.debug('Adding user \'%s\' to cache', user_id)
                try:
                    await self.add_to_cache(user)
                    logger.debug('User \'%s\' successfully added to cache', user_id)
                except Exception as e:
                    logger.exception('Failed to add user \'%s\' to cache: %s', user_id, str(e))
            return user

        async def _update_status(cls_self, user_id: UUID, status: str) -> None:
            logger.debug('Updating status for user \'%s\' to \'%s\'', user_id, status)
            await update_status(cls_self, user_id, status)

            logger.debug('Removing user \'%s\' from cache after status update', user_id)
            try:
                await self.remove_from_cache(user_id)
                logger.debug('User \'%s\' successfully removed from cache', user_id)
            except Exception as e:
                logger.critical('Failed to remove user \'%s\' from cache: %s', user_id, str(e), exc_info=True)

        async def _update_photo(cls_self, user_id: UUID, photo: str) -> None:
            logger.debug('Updating photo for user \'%s\' to \'%s\'', user_id, photo)
            await update_photo(cls_self, user_id, photo)

            logger.debug('Removing user \'%s\' from cache after photo update', user_id)
            try:
                await self.remove_from_cache(user_id)
                logger.debug('User \'%s\' successfully removed from cache', user_id)
            except Exception as e:
                logger.critical('Failed to remove user \'%s\' from cache: %s', user_id, str(e), exc_info=True)

        cls.get = _get
        cls.update_status = _update_status
        cls.update_photo = _update_photo
        return cls