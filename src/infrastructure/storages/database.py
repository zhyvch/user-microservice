from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from settings.config import settings

engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=settings.USER_SERVICE_DEBUG,
    pool_size=5,
    max_overflow=10,
)

session_factory = async_sessionmaker(bind=engine)

class Base(DeclarativeBase):
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.__dict__}>'
