from abc import ABC, abstractmethod
from dataclasses import dataclass

from infrastructure.repositories.users.base import BaseUserRepository
from service import messagebus


@dataclass
class BaseUserUnitOfWork(ABC):
    users: BaseUserRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    async def publish_events(self):
        for user in self.users.loaded_users:
            while user.events:
                event = user.events.pop(0)
                await messagebus.handle(event)

    async def _commit(self):
        await self.commit()
        await self.publish_events()


    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...