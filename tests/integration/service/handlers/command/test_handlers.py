import pytest

from domain.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
    UpdateUserCredentialsStatusCommand,
    UpdateUserPhotoCommand,
)
from domain.entities.users import UserWithCredentialsEntity, UserCredentialsStatus
from domain.events.users import UserCreatedEvent, UserDeletedEvent
from domain.value_objects.users import PasswordVO
from service.handlers.command.users import (
    CreateUserCommandHandler,
    DeleteUserCommandHandler,
    UpdateUserCredentialsStatusCommandHandler,
    UpdateUserPhotoCommandHandler,
)


@pytest.mark.asyncio
class TestCommandHandlers:
    async def test_create_user_command_handler(
        self, random_user_entity, sqlalchemy_user_uow
    ):
        command = CreateUserCommand(
            user_with_credentials=UserWithCredentialsEntity(
                user=random_user_entity,
                password=PasswordVO('VerySecretPa$$word1234'),
            )
        )
        handler = CreateUserCommandHandler(uow=sqlalchemy_user_uow)
        await handler(command=command)

        async with sqlalchemy_user_uow:
            user = await sqlalchemy_user_uow.users.get(user_id=random_user_entity.id)

        assert user is not None
        assert user.id == random_user_entity.id
        assert user.credentials_status == random_user_entity.credentials_status

        assert UserCreatedEvent in [event.__class__ for event in random_user_entity.events]
        assert len(random_user_entity.events) == 1
        assert random_user_entity.events[0].user_id == random_user_entity.id


    async def test_delete_user_command_handler(
        self, random_user_entity, sqlalchemy_user_uow, message_bus
    ):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()

        command = DeleteUserCommand(user_id=random_user_entity.id)
        handler = DeleteUserCommandHandler(uow=sqlalchemy_user_uow)
        await handler(command=command)

        loaded_users = sqlalchemy_user_uow.users.loaded_users
        assert len(loaded_users) == 1

        user = loaded_users.pop()
        assert user == random_user_entity

        assert UserDeletedEvent in [event.__class__ for event in user.events]
        assert len(user.events) == 1
        assert user.events[0].user_id == random_user_entity.id

        async with sqlalchemy_user_uow:
            user = await sqlalchemy_user_uow.users.get(user_id=random_user_entity.id)

        assert user is None


    async def test_update_user_credentials_status_command_handler(
        self, random_user_entity, sqlalchemy_user_uow, rabbitmq_consumer
    ):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()

        new_status = UserCredentialsStatus.SUCCESS

        command = UpdateUserCredentialsStatusCommand(
            user_id=random_user_entity.id,
            status=new_status
        )
        handler = UpdateUserCredentialsStatusCommandHandler(uow=sqlalchemy_user_uow)
        await handler(command=command)

        async with sqlalchemy_user_uow:
            user = await sqlalchemy_user_uow.users.get(user_id=random_user_entity.id)

        assert user is not None
        assert user.id == random_user_entity.id
        assert user.credentials_status == new_status != random_user_entity.credentials_status


    async def test_update_user_photo_command_handler(
        self, random_user_entity, sqlalchemy_user_uow, rabbitmq_consumer
    ):
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()
            user = await sqlalchemy_user_uow.users.get(user_id=random_user_entity.id)

        old_photo = user.photo
        new_photo = 'new_photo.png'

        command = UpdateUserPhotoCommand(
            user_id=random_user_entity.id,
            photo=new_photo,
        )
        handler = UpdateUserPhotoCommandHandler(uow=sqlalchemy_user_uow)
        await handler(command=command)

        async with sqlalchemy_user_uow:
            user = await sqlalchemy_user_uow.users.get(user_id=random_user_entity.id)

        assert user is not None
        assert user.id == random_user_entity.id
        assert user.photo == new_photo != old_photo
