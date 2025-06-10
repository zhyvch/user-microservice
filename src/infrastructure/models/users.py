import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import UUID, DateTime, String, CheckConstraint, Index
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from domain.entities.users import UserCredentialsStatus
from infrastructure.storages.database import Base
from settings.config import settings


uuid_pk = Annotated[uuid.UUID, mapped_column(UUID, primary_key=True)]
timestamp = Annotated[datetime, mapped_column(DateTime(timezone=True))]


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[uuid_pk]
    created_at: Mapped[timestamp] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column(String(255), nullable=False, default=settings.USER_SERVICE_DEFAULT_USER_PHOTO)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(15), unique=True, nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    credentials_status: Mapped[UserCredentialsStatus] = mapped_column(
        SQLEnum(UserCredentialsStatus),
        nullable=False,
        default=UserCredentialsStatus.PENDING,
    )

    __table_args__ = (
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='valid_email',
        ),
        CheckConstraint(
            "(email IS NOT NULL) OR (phone_number IS NOT NULL)",
            name='credentials_required',
        ),
    )
