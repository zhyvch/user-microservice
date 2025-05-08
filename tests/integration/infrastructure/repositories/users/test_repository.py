import pytest
import logging

from domain.commands.users import UserCredentialsStatus

logger = logging.getLogger(__name__)

# TODO: Add remove from repo functionality tests

@pytest.mark.asyncio
class TestSQLAlchemyRepository:
    async def test_add_get_user(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        await sqlalchemy_user_repository.session.commit()
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        logger.info('User \'%s\' read from DB', result.id)
        assert result is not None
        assert result.id == random_user_entity.id
        assert result.email == random_user_entity.email

    async def test_update_status(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        await sqlalchemy_user_repository.session.commit()
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        new_status = UserCredentialsStatus.SUCCESS
        await sqlalchemy_user_repository.update_status(random_user_entity.id, new_status)
        await sqlalchemy_user_repository.session.commit()
        logger.info('User \'%s\' status updated to %s', random_user_entity.id, new_status)

        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        assert result is not None
        assert result.credentials_status == new_status

    async def test_update_photo(self, random_user_entity, sqlalchemy_user_repository):
        await sqlalchemy_user_repository.add(random_user_entity)
        await sqlalchemy_user_repository.session.commit()
        logger.info('User \'%s\' added to DB', random_user_entity.id)

        new_photo = 'new_photo.jpg'
        await sqlalchemy_user_repository.update_photo(random_user_entity.id, new_photo)
        await sqlalchemy_user_repository.session.commit()
        logger.info('User \'%s\' photo updated to %s', random_user_entity.id, new_photo)

        result = await sqlalchemy_user_repository.get(random_user_entity.id)
        assert result is not None
        assert result.photo == new_photo
