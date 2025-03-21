from dataclasses import dataclass
from uuid import UUID

from domain.events.base import BaseEvent


@dataclass
class UserCreatedEvent(BaseEvent):
    user_id: UUID


@dataclass
class UserDeletedEvent(BaseEvent):
    user_id: UUID
