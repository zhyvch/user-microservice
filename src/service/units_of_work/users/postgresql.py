import logging
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.storages.database import session_factory
from infrastructure.repositories.users.postgresql import SQLAlchemyUserRepository
from service.exceptions.users import TransactionException
from service.units_of_work.users.base import BaseUserUnitOfWork

logger = logging.getLogger(__name__)


class SQLAlchemyUserUnitOfWork(BaseUserUnitOfWork):
    session_factory: async_sessionmaker = session_factory

    async def __aenter__(self):
        logger.debug('Opening database session')
        self.session = self.session_factory()
        self.users = SQLAlchemyUserRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug('Closing database session')
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()
        if exc_type:
            logger.warning('Session closed with exception: %s', exc_val)

    async def commit(self):
        logger.debug('Committing transaction')
        try:
            await self.session.commit()
            logger.debug('Transaction committed successfully')
        except Exception as e:
            logger.exception('Transaction commit failed: %s', str(e))
            await self.rollback()
            raise TransactionException() from e

    async def rollback(self):
        logger.debug('Rolling back transaction')
        try:
            await self.session.rollback()
            logger.debug('Transaction rolled back successfully')
        except Exception as e:
            logger.exception('Transaction rollback failed: %s', str(e))
            raise
