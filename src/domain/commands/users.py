from dataclasses import dataclass

from domain.commands.base import BaseCommand
from domain.entities.users import UserWithCredentialsEntity


@dataclass
class UserCreateCommand(BaseCommand):
    user_with_credentials: UserWithCredentialsEntity
