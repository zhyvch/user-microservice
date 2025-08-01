from dataclasses import dataclass
from uuid import UUID

from application.external_events.handlers.base import BaseExternalEventHandler
from domain.commands.users import UpdateUserCredentialsStatusCommand, UpdateUserEmailCommand, \
    UpdateUserPhoneNumberCommand
from domain.entities.users import UserCredentialsStatus
from domain.value_objects.users import EmailVO, PhoneNumberVO
from service.handlers.event.users import UserRegistrationCompletedEvent


@dataclass
class UserCredentialsCreatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            UpdateUserCredentialsStatusCommand(
                user_id=UUID(body['user_id']),
                status=UserCredentialsStatus(body['status']),
            )
        )
        user = await self.bus.uow.users.get(UUID(body['user_id']))
        await self.bus.handle(
            UserRegistrationCompletedEvent(
                user_id=user.id,
                created_at=user.created_at,
                photo=user.photo,
                email=user.email.as_generic() if user.email else None,
                phone_number=user.phone_number.as_generic() if user.phone_number else None,
                first_name=user.first_name.as_generic() if user.first_name else None,
                last_name=user.last_name.as_generic() if user.last_name else None,
                middle_name=user.middle_name.as_generic() if user.middle_name else None,
                credentials_status=user.credentials_status,
            )
        )


@dataclass
class UserEmailUpdatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            UpdateUserEmailCommand(
                user_id=UUID(body['user_id']),
                new_email=EmailVO(body['new_email']),
            )
        )


@dataclass
class UserPhoneNumberUpdatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            UpdateUserPhoneNumberCommand(
                user_id=UUID(body['user_id']),
                new_phone_number=PhoneNumberVO(body['new_phone_number']),
            )
        )
