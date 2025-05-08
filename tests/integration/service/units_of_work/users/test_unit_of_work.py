import logging

import pytest

from domain.commands.users import UserCredentialsStatus


logger = logging.getLogger(__name__)

# TODO: Add rollback functionality tests, add remove from repo functionality tests

@pytest.mark.asyncio
class TestUnitOfWork:
    async def test_add_user(self, random_user_entity, sqlalchemy_user_uow):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users_list.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' added to DB', random_user_entity.id)

            result = await sqlalchemy_user_uow.users_list.get(random_user_entity.id)
            logger.info('User \'%s\' read from DB', result.id)
            assert result is not None
            assert result.id == random_user_entity.id


    async def test_update_status(self, random_user_entity, sqlalchemy_user_uow):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users_list.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' added to DB', random_user_entity.id)

            new_status = UserCredentialsStatus.SUCCESS
            await sqlalchemy_user_uow.users_list.update_status(random_user_entity.id, new_status)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' status updated to %s', random_user_entity.id, new_status)

            result = await sqlalchemy_user_uow.users_list.get(random_user_entity.id)
            assert result is not None
            assert result.credentials_status == new_status


    async def test_update_photo(self, random_user_entity, sqlalchemy_user_uow):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users_list.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' added to DB', random_user_entity.id)

            new_photo = 'new_photo.jpg'
            await sqlalchemy_user_uow.users_list.update_photo(random_user_entity.id, new_photo)
            await sqlalchemy_user_uow.commit()
            logger.info('User \'%s\' photo updated to %s', random_user_entity.id, new_photo)

            result = await sqlalchemy_user_uow.users_list.get(random_user_entity.id)
            assert result is not None
            assert result.photo == new_photo


