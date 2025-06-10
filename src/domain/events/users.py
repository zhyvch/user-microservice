from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.users import UserCredentialsStatus
from domain.events.base import BaseEvent
from domain.exceptions.users import InsufficientCredentialsInfoException


@dataclass
class UserCreatedEvent(BaseEvent):
    user_id: UUID
    password: str
    email: str | None
    phone_number: str | None

    def __post_init__(self):
        if not any([self.email, self.phone_number]):
            raise InsufficientCredentialsInfoException


@dataclass
class UserDeletedEvent(BaseEvent):
    user_id: UUID


@dataclass
class UserRegistrationCompletedEvent(BaseEvent):
    user_id: UUID
    photo: str
    created_at: datetime
    email: str | None
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    credentials_status: UserCredentialsStatus

    def __post_init__(self):
        if not any([self.email, self.phone_number]):
            raise InsufficientCredentialsInfoException
