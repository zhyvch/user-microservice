import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import UUID, DateTime, String, CheckConstraint, Index
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from domain.commands.users import UserCredentialsStatus
from infrastructure.storages.database import Base

uuid_pk = Annotated[uuid.UUID, mapped_column(UUID, primary_key=True)]
timestamp = Annotated[datetime, mapped_column(DateTime(timezone=True))]



class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[uuid_pk]
    created_at: Mapped[timestamp] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    credentials_status: Mapped[UserCredentialsStatus] = mapped_column(
        SQLEnum(UserCredentialsStatus),
        nullable=False,
        default=UserCredentialsStatus.PENDING,
    )

    __table_args__ = (
        Index('idx_users_email', 'email'),
        Index('idx_users_phone_number', 'phone_number'),
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='valid_email',
        ),
    )