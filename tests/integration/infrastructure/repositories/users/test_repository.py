import random
import string

import pytest
import logging

from domain.commands.users import UserCredentialsStatus
from infrastructure.exception.users import UserNotFoundException

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
class TestSQLAlchemyRepository:
    async def test_add_get_user(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        logger.info('User \'%s\' read from DB', result.id)
        assert result.id == random_user_entity.id
        assert result.email == random_user_entity.email
        assert result in sqlalchemy_user_repository.loaded_users


    async def test_remove_user(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        await sqlalchemy_user_repository.remove(random_user_entity.id)
        await sqlalchemy_user_repository.session.commit()
        logger.info('User \'%s\' removed from DB', random_user_entity.id)

        with pytest.raises(UserNotFoundException):
            await sqlalchemy_user_repository.get(random_user_entity.id)

        assert random_user_entity in sqlalchemy_user_repository.loaded_users


    async def test_update_status(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        new_status = UserCredentialsStatus.SUCCESS
        await sqlalchemy_user_repository.update_status(random_user_entity.id, new_status)
        logger.info('User \'%s\' status updated to %s', random_user_entity.id, new_status)

        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        assert result.credentials_status == new_status
        assert result in sqlalchemy_user_repository.loaded_users


    async def test_update_photo(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        new_photo = 'new_photo.jpg'
        await sqlalchemy_user_repository.update_photo(random_user_entity.id, new_photo)
        logger.info('User \'%s\' photo updated to %s', random_user_entity.id, new_photo)

        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        assert result is not None
        assert result.photo == new_photo
        assert result in sqlalchemy_user_repository.loaded_users


    async def test_update_email(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        new_email = f'{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(230))}@testmail.com'
        await sqlalchemy_user_repository.update_email(random_user_entity.id, new_email)
        logger.info('User \'%s\' email updated to %s', random_user_entity.id, new_email)
        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        assert result.email.as_generic() == new_email
        assert result in sqlalchemy_user_repository.loaded_users


    async def test_update_phone_number(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        new_phone_number = f'+{''.join(random.choice(string.digits) for _ in range(14))}'
        await sqlalchemy_user_repository.update_phone_number(random_user_entity.id, new_phone_number)
        logger.info('User \'%s\' phone number updated to %s', random_user_entity.id, new_phone_number)
        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        assert result.phone_number.as_generic() == new_phone_number
        assert result in sqlalchemy_user_repository.loaded_users
