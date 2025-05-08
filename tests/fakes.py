import asyncio
import logging
from dataclasses import field, dataclass
from uuid import UUID

from application.external_events.consumers.base import BaseConsumer
from domain.entities.users import UserEntity, UserCredentialsStatus
from domain.events.base import BaseEvent
from infrastructure.producers.base import BaseProducer
from infrastructure.repositories.users.base import BaseUserRepository
from service.units_of_work.users.base import BaseUserUnitOfWork


logger = logging.getLogger(__name__)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


@dataclass
class FakeUserRepository(BaseUserRepository):
    users_list: list[UserEntity] = field(default_factory=list)

    async def get(self, user_id: UUID) -> UserEntity | None:
        logger.info('Fetching user with ID: %s', user_id)
        for user in self.users_list:
            if user.id == user_id:
                logger.info('User found: %s', user_id)
                return user
        logger.info('User not found: %s', user_id)
        return None

    async def update_status(self, user_id: UUID, status: UserCredentialsStatus) -> None:
        logger.debug('Updating status for user %s to %s', user_id, status)
        for user in self.users_list:
            if user_id == user.id:
                user.credentials_status = status
                logger.debug('Status updated successfully for user %s', user_id)
                return None
        logger.warning('Failed to update status: user %s not found', user_id)
        return None

    async def update_photo(self, user_id: UUID, photo: str) -> None:
        logger.debug('Updating photo for user %s', user_id)
        for user in self.users_list:
            if user_id == user.id:
                user.photo = photo
                logger.debug('Photo updated successfully for user %s', user_id)
                return None
        logger.warning('Failed to update photo: user %s not found', user_id)
        return None

    async def add(self, user: UserEntity) -> None:
        logger.debug('Adding user with ID: %s', user.id)
        self.users_list.append(user)
        return None


class FakeUnitOfWork(BaseUserUnitOfWork):
    def __init__(self):
        logger.debug('Initializing FakeUnitOfWork')
        self.users = FakeUserRepository()
        self.committed = False

    async def commit(self):
        logger.debug('Committing FakeUnitOfWork')
        self.committed = True

    async def rollback(self):
        logger.debug('Rolling back FakeUnitOfWork')
        pass


@dataclass
class FakeBroker(metaclass=SingletonMeta):
    queue: asyncio.Queue = field(default_factory=asyncio.Queue)


class FakeProducer(BaseProducer):
    broker = FakeBroker()

    async def start(self):
        logger.debug('Starting FakeProducer')
        pass

    async def stop(self):
        logger.debug('Stopping FakeProducer')
        pass

    async def publish(self, event: BaseEvent, topic: str):
        logger.debug('Publishing event to topic: %s', topic)
        await self.broker.queue.put({'topic': topic, 'body': event.__dict__})


@dataclass
class FakeConsumer(BaseConsumer):
    broker: FakeBroker = field(default_factory=FakeBroker, kw_only=True)
    consuming_task: asyncio.Task | None = field(default=None, kw_only=True)
    topics_to_consume: list[str] = field(default_factory=list, kw_only=True)

    async def __aenter__(self):
        logger.debug('Entering FakeConsumer context')
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug('Exiting FakeConsumer context')
        await self.stop()

    async def start(self):
        logger.debug('Starting FakeConsumer')
        if not self.consuming_task:
            logger.debug('Creating new consuming task')
            self.consuming_task = asyncio.create_task(self.consume())

    async def stop(self):
        logger.debug('Stopping FakeConsumer')
        if self.consuming_task:
            logger.debug('Cancelling consuming task')
            self.consuming_task.cancel()
            self.consuming_task = None

    async def consume(self):
        logger.debug('FakeConsumer consuming messages')
        while not self.broker.queue.empty():
            message = await self.broker.queue.get()
            logger.info('Received message on topic: %s', message['topic'])
            if message['topic'] in self.topics_to_consume:
                logger.info('Processing message for topic: %s', message['topic'])
                await self.external_events_map[message['topic']](message['body'])
            else:
                await self.broker.queue.put(message)
                logger.debug('Ignoring message for topic: %s (not in subscribed topics)', message['topic'])
