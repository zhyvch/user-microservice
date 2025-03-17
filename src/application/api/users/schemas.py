from uuid import UUID
from pydantic import BaseModel, EmailStr, AwareDatetime, Field

class UserCreateSchema(BaseModel):
    password: str = Field(..., min_length=8)
    email: EmailStr
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None

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
    created_at: AwareDatetime
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
                'email': 'user@example.com',
                'phone_number': '+12345678901',
                'first_name': 'John',
                'last_name': 'Doe',
                'middle_name': None,
            }
        }


class UserUpdateSchema(BaseModel):
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None

    class Config:
        json_schema_extra = {
            'example': {
                'phone_number': '+12345678901',
                'first_name': 'John',
                'last_name': 'Doe',
            }
        }