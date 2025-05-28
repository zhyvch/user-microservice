from functools import lru_cache

from aiobotocore.session import AioSession, get_session
from punq import Container, Scope
from redis.asyncio import Redis, ConnectionPool
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.external_events.consumers.base import BaseConsumer
from application.external_events.consumers.rabbitmq import RabbitMQConsumer
from application.external_events.handlers.base import BaseExternalEventHandler
from application.external_events.handlers.users import UserCredentialsCreatedExternalEventHandler
from domain.commands.base import BaseCommand
from domain.commands.users import (
    CreateUserCommand,
    UpdateUserCredentialsStatusCommand,
    UpdateUserPhotoCommand,
    DeleteUserCommand,
)
from domain.events.base import BaseEvent
from domain.events.users import (
    UserCreatedEvent,
    UserRegistrationCompletedEvent,
    UserDeletedEvent
)
from infrastructure.storages.cache import redis_pool as default_redis_pool
from infrastructure.storages.database import session_factory as default_session_factory
from infrastructure.producers.base import BaseProducer
from infrastructure.producers.rabbitmq import RabbitMQProducer
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.repositories.users.postgresql import SQLAlchemyUserRepository
from infrastructure.storages.s3.aws import AWSS3Client
from infrastructure.storages.s3.base import BaseS3Client
from service.handlers.command.base import BaseCommandHandler
from service.handlers.command.users import (
    CreateUserCommandHandler,
    UpdateUserCredentialsStatusCommandHandler,
    UpdateUserPhotoCommandHandler,
    DeleteUserCommandHandler,
)
from service.handlers.event.base import BaseEventHandler
from service.handlers.event.users import (
    UserCreatedEventHandler,
    UserRegistrationCompletedEventHandler,
    UserDeletedEventHandler
)
from service.message_bus import MessageBus
from service.units_of_work.users.base import BaseUserUnitOfWork
from service.units_of_work.users.postgresql import SQLAlchemyUserUnitOfWork
from settings.config import Settings, settings


def get_commands_map(uow: BaseUserUnitOfWork) -> dict[type[BaseCommand], BaseCommandHandler]:
    create_user_handler = CreateUserCommandHandler(uow=uow)
    delete_user_handler = DeleteUserCommandHandler(uow=uow)
    update_user_creds_status_handler = UpdateUserCredentialsStatusCommandHandler(uow=uow)
    update_user_photo_handler = UpdateUserPhotoCommandHandler(uow=uow)

    commands_map = {
        CreateUserCommand: create_user_handler,
        DeleteUserCommand: delete_user_handler,
        UpdateUserCredentialsStatusCommand: update_user_creds_status_handler,
        UpdateUserPhotoCommand: update_user_photo_handler,
    }
    return commands_map

def get_events_map(producer: BaseProducer) -> dict[type[BaseEvent], list[BaseEventHandler]]:
    user_created_handler = UserCreatedEventHandler(
        producer=producer,
        topic='user.created',
    )
    user_deleted_handler = UserDeletedEventHandler(
        producer=producer,
        topic='user.deleted',
    )
    user_registration_handler = UserRegistrationCompletedEventHandler(
        producer=producer,
        topic='user.registration.completed',
    )

    events_map = {
        UserCreatedEvent: [user_created_handler],
        UserDeletedEvent: [user_deleted_handler],
        UserRegistrationCompletedEvent: [user_registration_handler],
    }
    return events_map

def get_external_events_map(bus: MessageBus) -> dict[str, BaseExternalEventHandler]:
    user_creds_created_handler = UserCredentialsCreatedExternalEventHandler(bus=bus)

    external_events_map = {
        'user.credentials.created': user_creds_created_handler,
    }
    return external_events_map


def _initialize_container() -> Container:
    container = Container()

    def initialize_s3_client(
        session: AioSession = None,
    ) -> BaseS3Client:
        if session is None:
            session = get_session()

        return AWSS3Client(
            secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL,
            bucket_name=settings.S3_BUCKET_NAME,
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_region_name=settings.AWS_S3_REGION_NAME,
            session=session,
        )


    def initialize_redis_client(
        redis_pool: ConnectionPool = None,
    ) -> Redis:
        if redis_pool is None:
            redis_pool = default_redis_pool

        return Redis(connection_pool=redis_pool)


    def initialize_user_sqlalchemy_repo(
        session_factory: async_sessionmaker = None,
    ) -> BaseUserRepository:
        if session_factory is None:
            session_factory = default_session_factory

        return SQLAlchemyUserRepository(session=session_factory())


    def initialize_user_sqlalchemy_uow(
        session_factory: async_sessionmaker = None,
    ) -> BaseUserUnitOfWork:
        if session_factory is None:
            session_factory = default_session_factory

        return SQLAlchemyUserUnitOfWork(session_factory=session_factory)


    def initialize_message_bus(
        uow: BaseUserUnitOfWork = None,
        producer: BaseProducer = None,
    ) -> MessageBus:
        if uow is None:
            uow = container.resolve(BaseUserUnitOfWork)

        if producer is None:
            producer = container.resolve(BaseProducer)

        bus = MessageBus(
            uow=uow,
            commands_map=get_commands_map(uow=uow),
            events_map=get_events_map(producer=producer),
        )
        return bus


    def initialize_producer() -> BaseProducer:
        return RabbitMQProducer(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            virtual_host=settings.RABBITMQ_VHOST,
            exchange_name=settings.NANOSERVICES_EXCH_NAME,
        )


    def initialize_consumer(
        bus: MessageBus = None,
    ) -> BaseConsumer:
        if bus is None:
            bus = container.resolve(MessageBus)

        return RabbitMQConsumer(
            external_events_map=get_external_events_map(bus),
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            virtual_host=settings.RABBITMQ_VHOST,
            queue_name=settings.USER_SERVICE_QUEUE_NAME,
            exchange_name=settings.NANOSERVICES_EXCH_NAME,
            consuming_topics=settings.USER_SERVICE_CONSUMING_TOPICS,
        )


    container.register(Settings, instance=settings, scope=Scope.singleton)
    container.register(BaseS3Client, factory=initialize_s3_client, scope=Scope.singleton)
    container.register(Redis, factory=initialize_redis_client, scope=Scope.singleton)
    container.register(BaseUserRepository, factory=initialize_user_sqlalchemy_repo)
    container.register(BaseUserUnitOfWork, factory=initialize_user_sqlalchemy_uow)
    container.register(MessageBus, factory=initialize_message_bus)
    container.register(BaseProducer, factory=initialize_producer, scope=Scope.singleton)
    container.register(BaseConsumer, factory=initialize_consumer, scope=Scope.singleton)

    return container


@lru_cache(1)
def initialize_container() -> Container:
    return _initialize_container()
