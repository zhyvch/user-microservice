from dataclasses import dataclass
from uuid import UUID

from application.external_events.handlers.base import BaseExternalEventHandler
from domain.commands.users import UpdateUserCredentialsStatusCommand, UserCredentialsStatus


@dataclass
class UserCredentialsCreatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            UpdateUserCredentialsStatusCommand(
                user_id=UUID(body['user_id']),
                status=UserCredentialsStatus(body['status'])
            )
        )
