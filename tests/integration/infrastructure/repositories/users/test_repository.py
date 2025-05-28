import pytest
import logging

from domain.commands.users import UserCredentialsStatus

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
class TestSQLAlchemyRepository:
    async def test_add_get_user(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        logger.info('User \'%s\' read from DB', result.id)
        assert result is not None
        assert result.id == random_user_entity.id
        assert result.email == random_user_entity.email
        assert result in sqlalchemy_user_repository.loaded_users


    async def test_remove_user(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        await sqlalchemy_user_repository.remove(random_user_entity.id)
        logger.info('User \'%s\' removed from DB', random_user_entity.id)
        await sqlalchemy_user_repository.session.commit()

        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        assert result is None
        assert random_user_entity in sqlalchemy_user_repository.loaded_users


    async def test_update_status(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        new_status = UserCredentialsStatus.SUCCESS
        await sqlalchemy_user_repository.update_status(random_user_entity.id, new_status)
        logger.info('User \'%s\' status updated to %s', random_user_entity.id, new_status)

        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        assert result is not None
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
