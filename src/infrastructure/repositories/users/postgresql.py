import logging
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.users import UserEntity, UserCredentialsStatus
from infrastructure.cache import cache_repository
from infrastructure.converters.users import convert_user_entity_to_model, convert_user_model_to_entity
from infrastructure.exception.users import UserNotFoundException
from infrastructure.models.users import UserModel
from infrastructure.repositories.users.base import BaseUserRepository


logger = logging.getLogger(__name__)


# @cache_repository
@dataclass
class SQLAlchemyUserRepository(BaseUserRepository):
    session: AsyncSession

    async def add(self, user: UserEntity) -> None:
        logger.debug('Adding user \'%s\' to DB', user.id)
        try:
            user_model = convert_user_entity_to_model(user)
            self.session.add(user_model)
            logger.info('User \'%s\' added to DB session', user.id)
        except Exception as e:
            logger.exception('Error adding user \'%s\' to DB: %s', user.id, str(e))
            raise


    async def get(
        self,
        user_id: UUID,
    ) -> UserEntity:
        logger.debug('Getting user \'%s\' from DB', user_id)
        try:
            user = await self.session.get(UserModel, user_id)

            if not user:
                logger.debug('User \'%s\' not found in DB', user_id)
                raise UserNotFoundException(user_id=user_id)

            logger.debug('User \'%s\' found in DB', user_id)
            user_entity = convert_user_model_to_entity(user)
            return user_entity
        except Exception as e:
            logger.exception('Error retrieving user %s from DB: %s', user_id, str(e))
            raise


    async def update_status(
        self,
        user_id: UUID,
        status: UserCredentialsStatus,
    ) -> UserEntity:
        logger.debug('Updating status for user \'%s\' to %s', user_id, status)
        try:
            user = await self.session.get(UserModel, user_id)
            if not user:
                logger.debug('User \'%s\' not found in DB for status update', user_id)
                raise UserNotFoundException(user_id=user_id)

            user.credentials_status = status
            logger.debug('Status for user \'%s\' updated to %s', user_id, status)
            return convert_user_model_to_entity(user)
        except Exception as e:
            logger.exception('Error updating status for user \'%s\': %s', user_id, str(e))
            raise


    async def update_photo(
        self,
        user_id: UUID,
        photo: str,
    ) -> UserEntity:
        logger.debug('Updating photo for user \'%s\' to %s', user_id, photo)
        try:
            user = await self.session.get(UserModel, user_id)

            if not user:
                logger.debug('User \'%s\' not found in DB for status update', user_id)
                raise UserNotFoundException(user_id=user_id)

            user.photo = photo
            logger.debug('Photo for user \'%s\' updated to %s', user_id, photo)
            return convert_user_model_to_entity(user)
        except Exception as e:
            logger.exception('Error updating photo for user \'%s\': %s', user_id, str(e))
            raise


    async def update_email(
        self,
        user_id: UUID,
        new_email: str,
    ) -> UserEntity:
        logger.debug('Updating email for user \'%s\' to %s', user_id, new_email)
        try:
            user = await self.session.get(UserModel, user_id)

            if not user:
                logger.debug('User \'%s\' not found in DB for email update', user_id)
                raise UserNotFoundException(user_id=user_id)

            user.email = new_email
            logger.debug('Email for user \'%s\' updated to %s', user_id, new_email)
            return convert_user_model_to_entity(user)
        except Exception as e:
            logger.exception('Error updating email for user \'%s\': %s', user_id, str(e))
            raise


    async def update_phone_number(
        self,
        user_id: UUID,
        new_phone_number: str,
    ) -> UserEntity:
        logger.debug('Updating phone number for user \'%s\' to %s', user_id, new_phone_number)
        try:
            user = await self.session.get(UserModel, user_id)

            if not user:
                logger.debug('User \'%s\' not found in DB for phone number update', user_id)
                raise UserNotFoundException(user_id=user_id)

            user.phone_number = new_phone_number
            logger.debug('Phone number for user \'%s\' updated to %s', user_id, new_phone_number)
            return convert_user_model_to_entity(user)
        except Exception as e:
            logger.exception('Error updating phone number for user \'%s\': %s', user_id, str(e))
            raise


    async def remove(
        self,
        user_id: UUID,
    ) -> UserEntity:
        logger.debug('Removing user \'%s\' from DB', user_id)
        try:
            user = await self.session.get(UserModel, user_id)

            if not user:
                logger.debug('User \'%s\' not found in DB for status update', user_id)
                raise UserNotFoundException(user_id=user_id)

            await self.session.delete(user)
            logger.info('User \'%s\' removed from DB session', user_id)
            return convert_user_model_to_entity(user)
        except Exception as e:
            logger.exception('Error removing user \'%s\' from DB: %s', user_id, str(e))
            raise
