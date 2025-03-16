import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import UUID, DateTime, String, CheckConstraint, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

uuid_pk = Annotated[uuid.UUID, mapped_column(UUID, primary_key=True)]
timestamp = Annotated[datetime, mapped_column(DateTime(timezone=True))]


class Base(DeclarativeBase):
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[uuid_pk]
    created_at: Mapped[timestamp] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        Index('idx_users_email', 'email'),
        Index('idx_users_phone_number', 'phone_number'),
        Index('idx_users_name', 'first_name', 'last_name'),
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name="valid_email",
        ),
    )