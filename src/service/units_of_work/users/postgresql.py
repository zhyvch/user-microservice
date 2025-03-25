from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.database import session_factory
from infrastructure.repositories.users.postgresql import SQLAlchemyUserRepository
from service.units_of_work.users.base import BaseUserUnitOfWork


class SQLAlchemyUserUnitOfWork(BaseUserUnitOfWork):
    section_factory: async_sessionmaker = session_factory

    async def __aenter__(self):
        self.session = self.section_factory()
        self.users = SQLAlchemyUserRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()



