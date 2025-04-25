from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from domain.entities.users import UserEntity, UserWithCredentialsEntity
from domain.value_objects.users import EmailVO, PhoneNumberVO, NameVO, PasswordVO


class UserCreateSchema(BaseModel):
    password: str
    email: str
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None

    def to_user_with_credentials_entity(self) -> UserWithCredentialsEntity:
        return UserWithCredentialsEntity(
            user=UserEntity(
                email=EmailVO(self.email),
                phone_number=PhoneNumberVO(self.phone_number) if self.phone_number else None,
                first_name=NameVO(self.first_name) if self.first_name else None,
                last_name=NameVO(self.last_name) if self.last_name else None,
                middle_name=NameVO(self.middle_name) if self.middle_name else None,
            ),
            password=PasswordVO(self.password),
        )

    class Config:
        json_schema_extra = {
            'example': {
                'password': '$ecurepaSS1234',
                'email': 'user@example.com',
                'phone_number': '+12345678901',
                'first_name': 'John',
                'last_name': 'Doe',
            }
        }


class UserDetailSchema(BaseModel):
    id: UUID
    created_at: datetime
    photo: str
    email: str
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    middle_name: str | None

    class Config:
        json_schema_extra = {
            'example': {
                'id': '123e4567-e89b-12d3-a456-426614174000',
                'created_at': '2023-01-01T12:00:00+00:00',
                'photo': 'https://example.com/photo.jpg',
                'email': 'user@example.com',
                'phone_number': '+12345678901',
                'first_name': 'John',
                'last_name': 'Doe',
                'middle_name': None,
            }
        }

    @staticmethod
    def from_user_entity(user: UserEntity):
        return UserDetailSchema(
            id=user.id,
            created_at=user.created_at,
            photo=user.photo,
            email=user.email.as_generic(),
            phone_number=user.phone_number.as_generic() if user.phone_number else None,
            first_name=user.first_name.as_generic() if user.first_name else None,
            last_name=user.last_name.as_generic() if user.last_name else None,
            middle_name=user.middle_name.as_generic() if user.middle_name else None,
        )