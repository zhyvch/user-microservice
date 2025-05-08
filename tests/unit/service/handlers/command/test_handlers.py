import pytest

from domain.commands.users import CreateUserCommand, UpdateUserCredentialsStatusCommand, UpdateUserPhotoCommand
from domain.entities.users import UserWithCredentialsEntity, UserCredentialsStatus
from domain.value_objects.users import PasswordVO
from service.handlers.command.users import CreateUserCommandHandler, UpdateUserCredentialsStatusCommandHandler, \
    UpdateUserPhotoCommandHandler


@pytest.mark.asyncio
class TestCommandHandlers:
    async def test_create_user_command_handler(
            self, random_user_entity, fake_user_uow, fake_consumer
    ):
        command = CreateUserCommand(
            user_with_credentials=UserWithCredentialsEntity(
                user=random_user_entity,
                password=PasswordVO('VerySecretPa$$word1234'),
            )
        )
        async with fake_consumer:
            handler = CreateUserCommandHandler(uow=fake_user_uow)
            await handler(command=command)

        async with fake_user_uow:
            user = await fake_user_uow.users.get(user_id=random_user_entity.id)
            assert user is not None
            assert user.id == random_user_entity.id
            assert user.credentials_status == random_user_entity.credentials_status

        while not fake_consumer.broker.queue.empty():
            expected_produced_topics = ['user.created']
            item = await fake_consumer.broker.queue.get()
            assert item['topic'] in expected_produced_topics

    async def test_update_user_credentials_status_command_handler(
            self, random_user_entity, fake_user_uow
    ):
        async with fake_user_uow:
            await fake_user_uow.users.add(random_user_entity)
            await fake_user_uow.commit()

        new_status = UserCredentialsStatus.SUCCESS

        command = UpdateUserCredentialsStatusCommand(
            user_id=random_user_entity.id,
            status=new_status
        )
        handler = UpdateUserCredentialsStatusCommandHandler(uow=fake_user_uow)
        await handler(command=command)

        async with fake_user_uow:
            user = await fake_user_uow.users.get(user_id=random_user_entity.id)
            assert user is not None
            assert user.id == random_user_entity.id
            assert user.credentials_status == new_status

    async def test_update_user_photo_command_handler(
            self, random_user_entity, fake_user_uow
    ):
        async with fake_user_uow:
            await fake_user_uow.users.add(random_user_entity)
            await fake_user_uow.commit()
            user = await fake_user_uow.users.get(user_id=random_user_entity.id)
            old_photo = user.photo

        command = UpdateUserPhotoCommand(
            user_id=random_user_entity.id,
            photo='new_photo.png'
        )
        handler = UpdateUserPhotoCommandHandler(uow=fake_user_uow)
        await handler(command=command)

        async with fake_user_uow:
            user = await fake_user_uow.users.get(user_id=random_user_entity.id)
            assert user is not None
            assert user.id == random_user_entity.id
            assert user.photo != old_photo
