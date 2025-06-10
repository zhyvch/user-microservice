import logging
from dataclasses import dataclass

from domain.commands.users import (
    CreateUserCommand,
    UpdateUserCredentialsStatusCommand,
    UpdateUserPhotoCommand,
    DeleteUserCommand, UpdateUserEmailCommand, UpdateUserPhoneNumberCommand,
)
from domain.events.users import UserCreatedEvent, UserDeletedEvent
from service.handlers.command.base import BaseCommandHandler
from service.units_of_work.users.base import BaseUserUnitOfWork


logger = logging.getLogger(__name__)


@dataclass
class CreateUserCommandHandler(BaseCommandHandler):
    uow: BaseUserUnitOfWork

    async def __call__(self, command: CreateUserCommand) -> None:
        logger.info('Creating new user with ID: \'%s\'', command.user_with_credentials.user.id)
        async with self.uow:
            try:
                await self.uow.users.add(command.user_with_credentials.user)
                await self.uow.commit()
                produced_events = [
                    UserCreatedEvent(
                        user_id=command.user_with_credentials.user.id,
                        email=command.user_with_credentials.user.email.as_generic() if command.user_with_credentials.user.email else None,
                        phone_number=command.user_with_credentials.user.phone_number.as_generic() if command.user_with_credentials.user.phone_number else None,
                        password=command.user_with_credentials.password.as_generic(),
                    ),
                ]
                command.user_with_credentials.user.events.extend(produced_events)
                logger.info('User created successfully with ID: \'%s\'', command.user_with_credentials.user.id)
            except Exception as e:
                logger.exception('Failed to create user: %s', str(e))
                raise


@dataclass
class DeleteUserCommandHandler(BaseCommandHandler):
    uow: BaseUserUnitOfWork

    async def __call__(self, command: DeleteUserCommand) -> None:
        logger.info('Deleting user with ID: \'%s\'', command.user_id)
        async with self.uow:
            try:
                user = await self.uow.users.remove(user_id=command.user_id)
                await self.uow.commit()
                produced_events = [
                    UserDeletedEvent(user_id=command.user_id),
                ]
                user.events.extend(produced_events)
                logger.info('User deleted successfully with ID: \'%s\'', command.user_id)
            except Exception as e:
                logger.exception('Failed to delete user: %s', str(e))
                raise


@dataclass
class UpdateUserCredentialsStatusCommandHandler(BaseCommandHandler):
    uow: BaseUserUnitOfWork

    async def __call__(self, command: UpdateUserCredentialsStatusCommand) -> None:
        logger.info('Updating credentials status for user ID: \'%s\' to %s', command.user_id, command.status)
        async with self.uow:
            try:
                await self.uow.users.update_status(user_id=command.user_id, status=command.status)
                await self.uow.commit()
                logger.info('Credentials status updated successfully for user ID: \'%s\' ', command.user_id)
            except Exception as e:
                logger.exception('Failed to update credentials status: %s', str(e))
                raise


@dataclass
class UpdateUserPhotoCommandHandler(BaseCommandHandler):
    uow: BaseUserUnitOfWork

    async def __call__(self, command: UpdateUserPhotoCommand) -> None:
        logger.info('Updating user photo for user ID: \'%s\' to %s', command.user_id, command.photo)
        async with self.uow:
            try:
                await self.uow.users.update_photo(user_id=command.user_id, photo=command.photo)
                await self.uow.commit()
                logger.info('Photo updated successfully for user ID: \'%s\'', command.user_id)
            except Exception as e:
                logger.exception('Failed to update photo: %s', str(e))
                raise


@dataclass
class UpdateUserEmailCommandHandler(BaseCommandHandler):
    uow: BaseUserUnitOfWork

    async def __call__(self, command: UpdateUserEmailCommand) -> None:
        logger.info('Updating email for user ID: \'%s\' to %s', command.user_id, command.new_email.as_generic())
        async with self.uow:
            try:
                await self.uow.users.update_email(user_id=command.user_id, new_email=command.new_email.as_generic())
                await self.uow.commit()
                logger.info('Email updated successfully for user ID: \'%s\'', command.user_id)
            except Exception as e:
                logger.exception('Failed to update email: %s', str(e))
                raise


@dataclass
class UpdateUserPhoneNumberCommandHandler(BaseCommandHandler):
    uow: BaseUserUnitOfWork

    async def __call__(self, command: UpdateUserPhoneNumberCommand) -> None:
        logger.info('Updating phone number for user ID: \'%s\' to %s', command.user_id, command.new_phone_number.as_generic())
        async with self.uow:
            try:
                await self.uow.users.update_phone_number(user_id=command.user_id, new_phone_number=command.new_phone_number.as_generic())
                await self.uow.commit()
                logger.info('Phone number updated successfully for user ID: \'%s\'', command.user_id)
            except Exception as e:
                logger.exception('Failed to update phone number: %s', str(e))
                raise
