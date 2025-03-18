from domain.entities.users import UserEntity
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
