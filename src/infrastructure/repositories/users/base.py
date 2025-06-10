import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.users import UserEntity, UserCredentialsStatus


logger = logging.getLogger(__name__)


@dataclass
class BaseUserRepository(ABC):
    loaded_users: set[UserEntity] = field(default_factory=set, kw_only=True)

    @abstractmethod
    async def add(
        self,
        user: UserEntity,
    ) -> None:
        ...

    @abstractmethod
    async def get(
        self,
        user_id: UUID,
    ) -> UserEntity:
        ...

    @abstractmethod
    async def update_status(
        self,
        user_id: UUID,
        status: UserCredentialsStatus,
    ) -> UserEntity:
        ...

    @abstractmethod
    async def update_photo(
        self,
        user_id: UUID,
        photo: str,
    ) -> UserEntity:
        ...

    @abstractmethod
    async def update_email(
        self,
        user_id: UUID,
        new_email: str,
    ) -> UserEntity:
        ...

    @abstractmethod
    async def update_phone_number(
        self,
        user_id: UUID,
        new_phone_number: str,
    ) -> UserEntity:
        ...

    @abstractmethod
    async def remove(
        self,
        user_id: UUID,
    ) -> UserEntity:
        ...

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        logger.debug('Initializing repository subclass: %s', cls.__name__)

        add = cls.add
        get = cls.get
        update_status = cls.update_status
        update_photo = cls.update_photo
        update_email = cls.update_email
        update_phone_number = cls.update_phone_number
        remove = cls.remove

        async def _add(
            self,
            user: UserEntity,
        ) -> None:
            logger.debug('Adding user \'%s\' to repo', user.id)
            await add(self, user)
            self.loaded_users.add(user)
            logger.debug('User \'%s\' added to loaded_users set', user.id)

        async def _get(
            self,
            user_id: UUID,
        ) -> UserEntity:
            logger.debug('Getting user \'%s\' from repo', user_id)
            user = await get(self, user_id)
            self.loaded_users.add(user)
            logger.debug('User \'%s\' added to loaded_users set', user.id)
            return user

        async def _update_status(
            self,
            user_id: UUID,
            status: UserCredentialsStatus,
        ) -> UserEntity:
            logger.debug('Updating status for user \'%s\' to %s', user_id, status)
            user = await update_status(self, user_id, status)
            self.loaded_users.add(user)
            logger.debug('User \'%s\' added to loaded_users set', user.id)
            return user

        async def _update_email(
            self,
            user_id: UUID,
            new_email: str,
        ) -> UserEntity:
            logger.debug('Updating email for user \'%s\' to %s', user_id, new_email)
            user = await update_email(self, user_id, new_email)
            self.loaded_users.add(user)
            logger.debug('User \'%s\' added to loaded_users set', user.id)
            return user

        async def _update_phone_number(
            self,
            user_id: UUID,
            new_phone_number: str,
        ) -> UserEntity:
            logger.debug('Updating phone number for user \'%s\' to %s', user_id, new_phone_number)
            user = await update_phone_number(self, user_id, new_phone_number)
            self.loaded_users.add(user)
            logger.debug('User \'%s\' added to loaded_users set', user.id)
            return user

        async def _update_photo(
            self,
            user_id: UUID,
            photo: str,
        ) -> UserEntity:
            logger.debug('Updating photo for user \'%s\' to %s', user_id, photo)
            user = await update_photo(self, user_id, photo)
            self.loaded_users.add(user)
            logger.debug('User \'%s\' added to loaded_users set', user.id)
            return user

        async def _remove(
            self,
            user_id: UUID,
        ) -> UserEntity:
            logger.debug('Removing user \'%s\' from repo', user_id)
            user = await remove(self, user_id)
            self.loaded_users.add(user)
            logger.debug('User \'%s\' added to loaded_users set', user.id)
            return user

        cls.add = _add
        cls.get = _get
        cls.update_status = _update_status
        cls.update_photo = _update_photo
        cls.update_email = _update_email
        cls.update_phone_number = _update_phone_number
        cls.remove = _remove
