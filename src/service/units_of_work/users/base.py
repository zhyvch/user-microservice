from abc import ABC, abstractmethod

from infrastructure.repositories.users.base import BaseUserRepository


class BaseUserUnitOfWork(ABC):
    users: BaseUserRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...