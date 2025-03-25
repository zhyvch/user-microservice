from domain.commands.base import BaseCommand
from service.handlers.command.base import BaseCommandHandler


class UserCreateCommandHandler(BaseCommandHandler):
    async def __call__(self, command: BaseCommand) -> None:
        ...
