from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from domain.commands.base import BaseCommand
from domain.entities.users import UserWithCredentialsEntity


class UserCredentialsStatus(Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'


@dataclass
class CreateUserCommand(BaseCommand):
    user_with_credentials: UserWithCredentialsEntity


@dataclass
class UpdateUserCredentialsStatusCommand(BaseCommand):
    user_id: UUID
    status: UserCredentialsStatus
