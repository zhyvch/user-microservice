from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.value_objects.users import EmailVO, PhoneNumberVO, NameVO, PasswordVO


@dataclass(eq=False)
class UserEntity(BaseEntity):
    photo: str = field(default='', kw_only=True)
    email: EmailVO
    phone_number: PhoneNumberVO | None
    first_name: NameVO | None
    last_name: NameVO | None
    middle_name: NameVO | None


@dataclass
class UserWithCredentialsEntity:
    user: UserEntity
    password: PasswordVO
