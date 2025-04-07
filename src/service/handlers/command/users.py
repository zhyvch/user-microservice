from dataclasses import dataclass

from domain.commands.users import CreateUserCommand, UpdateUserCredentialsStatusCommand
from domain.events.users import UserCreatedEvent
from service.handlers.command.base import BaseCommandHandler
from service.units_of_work.users.base import BaseUserUnitOfWork


@dataclass
class CreateUserCommandHandler(BaseCommandHandler):
    uow: BaseUserUnitOfWork

    async def __call__(self, command: CreateUserCommand) -> None:
        async with self.uow:
            await self.uow.users.add(command.user_with_credentials.user)
            command.user_with_credentials.user.events.append(UserCreatedEvent(
                user_id=command.user_with_credentials.user.id,
                email=command.user_with_credentials.user.email.as_generic(),
                password=command.user_with_credentials.password.as_generic(),
            ))
            await self.uow.commit()


@dataclass
class UpdateUserCredentialsStatusCommandHandler(BaseCommandHandler):
    uow: BaseUserUnitOfWork

    async def __call__(self, command: UpdateUserCredentialsStatusCommand) -> None:
        async with self.uow:
            await self.uow.users.update_status(user_id=command.user_id, status=command.status)
            await self.uow.commit()