import pytest

from domain.commands.users import (
    CreateUserCommand,
    UpdateUserCredentialsStatusCommand,
    UpdateUserPhotoCommand,
    DeleteUserCommand,
    UpdateUserEmailCommand,
    UpdateUserPhoneNumberCommand,
)
from domain.entities.users import UserWithCredentialsEntity, UserCredentialsStatus
from domain.events.users import UserCreatedEvent, UserDeletedEvent
from domain.value_objects.users import PasswordVO, EmailVO, PhoneNumberVO
from infrastructure.exception.users import UserNotFoundException
from service.handlers.command.users import (
    CreateUserCommandHandler,
    UpdateUserCredentialsStatusCommandHandler,
    UpdateUserPhotoCommandHandler,
    DeleteUserCommandHandler,
    UpdateUserEmailCommandHandler,
    UpdateUserPhoneNumberCommandHandler,
)


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

        assert UserCreatedEvent in [event.__class__ for event in random_user_entity.events]


    async def test_delete_user_command_handler(
        self, random_user_entity, fake_user_uow, fake_consumer
    ):
        async with fake_user_uow:
            await fake_user_uow.users.add(random_user_entity)
            await fake_user_uow.commit()

        command = DeleteUserCommand(user_id=random_user_entity.id)
        async with fake_consumer:
            handler = DeleteUserCommandHandler(uow=fake_user_uow)
            await handler(command=command)

        with pytest.raises(UserNotFoundException):
            async with fake_user_uow:
                user = await fake_user_uow.users.get(user_id=random_user_entity.id)

        assert UserDeletedEvent in [event.__class__ for event in random_user_entity.events]


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
        new_photo = 'new_photo.png'

        command = UpdateUserPhotoCommand(
            user_id=random_user_entity.id,
            photo=new_photo,
        )
        handler = UpdateUserPhotoCommandHandler(uow=fake_user_uow)
        await handler(command=command)

        async with fake_user_uow:
            user = await fake_user_uow.users.get(user_id=random_user_entity.id)

        assert user is not None
        assert user.id == random_user_entity.id
        assert user.photo == new_photo != old_photo


    async def test_update_user_email_command_handler(
        self, random_user_entity, fake_user_uow
    ):
        async with fake_user_uow:
            await fake_user_uow.users.add(random_user_entity)
            await fake_user_uow.commit()
            user = await fake_user_uow.users.get(user_id=random_user_entity.id)

        new_email = EmailVO('testmain@testmail.com')
        command = UpdateUserEmailCommand(
            user_id=random_user_entity.id,
            new_email=new_email,
        )
        handler = UpdateUserEmailCommandHandler(uow=fake_user_uow)
        await handler(command=command)
        async with fake_user_uow:
            user = await fake_user_uow.users.get(user_id=random_user_entity.id)
        assert user.id == random_user_entity.id
        assert user.email == new_email


    async def test_update_user_phone_number_command_handler(
        self, random_user_entity, fake_user_uow
    ):
        async with fake_user_uow:
            await fake_user_uow.users.add(random_user_entity)
            await fake_user_uow.commit()
            user = await fake_user_uow.users.get(user_id=random_user_entity.id)

        new_phone_number = PhoneNumberVO('+1234567890')
        command = UpdateUserPhoneNumberCommand(
            user_id=random_user_entity.id,
            new_phone_number=new_phone_number,
        )
        handler = UpdateUserPhoneNumberCommandHandler(uow=fake_user_uow)
        await handler(command=command)
        async with fake_user_uow:
            user = await fake_user_uow.users.get(user_id=random_user_entity.id)
        assert user is not None
        assert user.id == random_user_entity.id
        assert user.phone_number == new_phone_number
