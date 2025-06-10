import logging
import string
import random

import pytest

from domain.commands.users import UserCredentialsStatus
from infrastructure.exception.users import UserNotFoundException


logger = logging.getLogger(__name__)


@pytest.mark.asyncio
class TestUnitOfWork:
    async def test_add_user(self, random_user_entity, sqlalchemy_user_uow):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.rollback()
            logger.info('User \'%s\' creation rolled back', random_user_entity.id)

            with pytest.raises(UserNotFoundException):
                await sqlalchemy_user_uow.users.get(random_user_entity.id)

            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' creation commited', random_user_entity.id)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)
            logger.info('User \'%s\' read from DB', result.id)
            assert result.id == random_user_entity.id


    async def test_remove_user(self, random_user_entity, sqlalchemy_user_uow):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' added to DB', random_user_entity.id)

            await sqlalchemy_user_uow.users.remove(random_user_entity.id)
            await sqlalchemy_user_uow.rollback()
            logger.info('User removal \'%s\' rolled back', random_user_entity.id)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)

            await sqlalchemy_user_uow.users.remove(random_user_entity.id)
            await sqlalchemy_user_uow.commit()
            logger.info('User removal \'%s\' commited', random_user_entity.id)
            with pytest.raises(UserNotFoundException):
                await sqlalchemy_user_uow.users.get(random_user_entity.id)


    async def test_update_status(self, random_user_entity, sqlalchemy_user_uow):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' added to DB', random_user_entity.id)

            new_status = UserCredentialsStatus.SUCCESS
            await sqlalchemy_user_uow.users.update_status(random_user_entity.id, new_status)
            await sqlalchemy_user_uow.rollback()
            logger.info('User status updating \'%s\' to \'%s\' rolled back', random_user_entity.id, new_status)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)
            assert result.credentials_status != new_status

            await sqlalchemy_user_uow.users.update_status(random_user_entity.id, new_status)
            await sqlalchemy_user_uow.commit()
            logger.info('User status updating \'%s\' to \'%s\' commited', random_user_entity.id, new_status)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)
            assert result.credentials_status == new_status


    async def test_update_photo(self, random_user_entity, sqlalchemy_user_uow):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' added to DB', random_user_entity.id)

            new_photo = 'new_photo.jpg'
            await sqlalchemy_user_uow.users.update_photo(random_user_entity.id, new_photo)
            await sqlalchemy_user_uow.rollback()
            logger.info('User photo updating \'%s\' to \'%s\' rolled back', random_user_entity.id, new_photo)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)
            assert result.photo != new_photo

            await sqlalchemy_user_uow.users.update_photo(random_user_entity.id, new_photo)
            await sqlalchemy_user_uow.commit()
            logger.info('User photo updating \'%s\' to \'%s\' commited', random_user_entity.id, new_photo)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)
            assert result.photo == new_photo


    async def test_update_email(self, random_user_entity, sqlalchemy_user_uow):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' added to DB', random_user_entity.id)

            new_email = f'{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(230))}@testmail.com'
            await sqlalchemy_user_uow.users.update_email(random_user_entity.id, new_email)
            await sqlalchemy_user_uow.rollback()
            logger.info('User email updating \'%s\' to \'%s\' rolled back', random_user_entity.id, new_email)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)
            assert result.email.as_generic() != new_email
            await sqlalchemy_user_uow.users.update_email(random_user_entity.id, new_email)
            await sqlalchemy_user_uow.commit()
            logger.info('User email updating \'%s\' to \'%s\' commited', random_user_entity.id, new_email)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)
            assert result.email.as_generic() == new_email


    async def test_update_phone_number(self, random_user_entity, sqlalchemy_user_uow):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' added to DB', random_user_entity.id)

            new_phone_number = f'+{''.join(random.choice(string.digits) for _ in range(14))}'
            await sqlalchemy_user_uow.users.update_phone_number(random_user_entity.id, new_phone_number)
            await sqlalchemy_user_uow.rollback()
            logger.info('User phone number updating \'%s\' to \'%s\' rolled back', random_user_entity.id, new_phone_number)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)
            assert result.phone_number.as_generic() != new_phone_number

            await sqlalchemy_user_uow.users.update_phone_number(random_user_entity.id, new_phone_number)
            await sqlalchemy_user_uow.commit()
            logger.info('User phone number updating \'%s\' to \'%s\' commited', random_user_entity.id, new_phone_number)
            result = await sqlalchemy_user_uow.users.get(random_user_entity.id)
            assert result.phone_number.as_generic() == new_phone_number
