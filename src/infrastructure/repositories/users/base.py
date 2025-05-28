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
    async def add(self, user: UserEntity) -> None:
        ...

    @abstractmethod
    async def get(self, user_id: UUID) -> UserEntity | None:
        ...

    @abstractmethod
    async def remove(self, user_id: UUID) -> None:
        ...

    @abstractmethod
    async def update_status(self, user_id: UUID, status: UserCredentialsStatus) -> None:
        ...

    @abstractmethod
    async def update_photo(self, user_id: UUID, photo: str) -> None:
        ...

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        logger.debug('Initializing repository subclass: %s', cls.__name__)

        add = cls.add
        get = cls.get

        async def _add(self, user: UserEntity) -> None:
            logger.debug('Adding user \'%s\' to repo', user.id)
            await add(self, user)
            self.loaded_users.add(user)
            logger.debug('User \'%s\' added to loaded_users set', user.id)

        async def _get(self, user_id: UUID) -> UserEntity | None:
            logger.debug('Getting user \'%s\' from repo', user_id)
            user = await get(self, user_id)
            if user:
                logger.debug('User \'%s\' found, adding to loaded_users set', user_id)
                self.loaded_users.add(user)
            else:
                logger.debug('User \'%s\' not found in repo', user_id)
            return user

        cls.add = _add
        cls.get = _get
