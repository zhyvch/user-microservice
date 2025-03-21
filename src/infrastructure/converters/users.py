from domain.entities.users import UserEntity
from domain.value_objects.users import EmailVO, PhoneNumberVO, NameVO
from infrastructure.models.users import UserModel


def convert_user_entity_to_model(user: UserEntity) -> UserModel:
    return UserModel(
        id=user.id,
        email=user.email.as_generic(),
        phone_number=user.phone_number.as_generic() if user.phone_number else None,
        first_name=user.first_name.as_generic() if user.first_name else None,
        last_name=user.last_name.as_generic() if user.last_name else None,
        middle_name=user.middle_name.as_generic() if user.middle_name else None,
    )

def convert_user_model_to_entity(user: UserModel) -> UserEntity:
    return UserEntity(
        id=user.id,
        created_at=user.created_at,
        email=EmailVO(user.email),
        phone_number=PhoneNumberVO(user.phone_number) if user.phone_number else None,
        first_name=NameVO(user.first_name) if user.first_name else None,
        last_name=NameVO(user.last_name) if user.last_name else None,
        middle_name=NameVO(user.middle_name) if user.middle_name else None,
    )