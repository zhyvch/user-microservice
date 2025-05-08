import logging
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.users import UserEntity, UserCredentialsStatus
from infrastructure.cache import cache_repository
from infrastructure.converters.users import convert_user_entity_to_model, convert_user_model_to_entity
from infrastructure.models.users import UserModel
from infrastructure.repositories.users.base import BaseUserRepository

logger = logging.getLogger(__name__)


@cache_repository
@dataclass
class SQLAlchemyUserRepository(BaseUserRepository):
    session: AsyncSession

    async def get(self, user_id: UUID) -> UserEntity | None:
        logger.debug('Getting user \'%s\' from DB', user_id)
        try:
            user = await self.session.get(UserModel, user_id)
            if user:
                logger.debug('User \'%s\' found in DB', user_id)
                user_entity = convert_user_model_to_entity(user)
                return user_entity
            logger.debug('User \'%s\' not found in DB', user_id)
            return None
        except Exception as e:
            logger.exception('Error retrieving user %s from DB: %s', user_id, str(e))
            raise

    async def add(self, user: UserEntity) -> None:
        logger.debug('Adding user \'%s\' to DB', user.id)
        try:
            user_model = convert_user_entity_to_model(user)
            self.session.add(user_model)
            logger.info('User \'%s\' added to DB session', user.id)
        except Exception as e:
            logger.exception('Error adding user \'%s\' to DB: %s', user.id, str(e))
            raise

    async def update_status(self, user_id: UUID, status: UserCredentialsStatus) -> None:
        logger.debug('Updating status for user \'%s\' to %s', user_id, status)
        try:
            user = await self.session.get(UserModel, user_id)
            if user:
                user.credentials_status = status
                logger.debug('Status for user \'%s\' updated to %s', user_id, status)
            else:
                logger.warning('Attempted to update status for non-existent user \'%s\'', user_id)
        except Exception as e:
            logger.exception('Error updating status for user \'%s\': %s', user_id, str(e))
            raise

    async def update_photo(self, user_id: UUID, photo: str) -> None:
        logger.debug('Updating photo for user \'%s\' to %s', user_id, photo)
        try:
            user = await self.session.get(UserModel, user_id)
            if user:
                user.photo = photo
                logger.debug('Photo for user \'%s\' updated to %s', user_id, photo)
            else:
                logger.warning('Attempted to update photo for non-existent user \'%s\'', user_id)
        except Exception as e:
            logger.exception('Error updating photo for user \'%s\': %s', user_id, str(e))
            raise
