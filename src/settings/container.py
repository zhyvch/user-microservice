from functools import lru_cache

from punq import Container, Scope
from redis.asyncio import Redis

from application.external_events.consumers.base import BaseConsumer
from application.external_events.consumers.rabbitmq import RabbitMQConsumer
from application.external_events.handlers.base import BaseExternalEventHandler
from application.external_events.handlers.users import UserCredentialsCreatedExternalEventHandler
from domain.commands.base import BaseCommand
from domain.commands.users import CreateUserCommand, UpdateUserCredentialsStatusCommand, UpdateUserPhotoCommand
from domain.events.base import BaseEvent
from domain.events.users import UserCreatedEvent, UserRegistrationCompletedEvent
from infrastructure.storages.cache import get_redis_client
from infrastructure.storages.database import session_factory
from infrastructure.producers.base import BaseProducer
from infrastructure.producers.rabbitmq import RabbitMQProducer
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.repositories.users.postgresql import SQLAlchemyUserRepository
from infrastructure.storages.s3.clients.aws import AWSS3Client
from infrastructure.storages.s3.clients.base import BaseS3Client
from service.handlers.command.base import BaseCommandHandler
from service.handlers.command.users import CreateUserCommandHandler, UpdateUserCredentialsStatusCommandHandler, \
    UpdateUserPhotoCommandHandler
from service.handlers.event.base import BaseEventHandler
from service.handlers.event.users import UserCreatedEventHandler, UserRegistrationCompletedEventHandler
from service.message_bus import MessageBus
from service.units_of_work.users.base import BaseUserUnitOfWork
from service.units_of_work.users.postgresql import SQLAlchemyUserUnitOfWork
from settings.config import Settings, settings


@lru_cache(1)
def initialize_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    def get_commands_map(uow: BaseUserUnitOfWork) -> dict[type[BaseCommand], BaseCommandHandler]:
        create_user_handler = CreateUserCommandHandler(uow=uow)
        update_user_creds_status_handler = UpdateUserCredentialsStatusCommandHandler(uow=uow)
        update_user_photo_handler = UpdateUserPhotoCommandHandler(uow=uow)

        commands_map = {
            CreateUserCommand: create_user_handler,
            UpdateUserCredentialsStatusCommand: update_user_creds_status_handler,
            UpdateUserPhotoCommand: update_user_photo_handler,
        }
        return commands_map

    def get_events_map(producer: BaseProducer) -> dict[type[BaseEvent], list[BaseEventHandler]]:
        user_created_handler = UserCreatedEventHandler(
            producer=producer,
            topic='user.created',
        )
        user_registration_handler = UserRegistrationCompletedEventHandler(
            producer=producer,
            topic='user.registration.completed',
        )

        events_map = {
            UserCreatedEvent: [user_created_handler],
            UserRegistrationCompletedEvent: [user_registration_handler],
        }
        return events_map

    def get_external_events_map(bus: MessageBus) -> dict[str, BaseExternalEventHandler]:
        user_creds_created_handler = UserCredentialsCreatedExternalEventHandler(bus=bus)

        external_events_map = {
            'user.credentials.created': user_creds_created_handler,
        }
        return external_events_map

    def initialize_s3_client() -> BaseS3Client:
        return AWSS3Client()

    def initialize_redis_client() -> Redis:
        return get_redis_client()

    def initialize_user_sqlalchemy_repo() -> BaseUserRepository:
        return SQLAlchemyUserRepository(session_factory())

    def initialize_user_sqlalchemy_uow() -> BaseUserUnitOfWork:
        return SQLAlchemyUserUnitOfWork()

    def initialize_message_bus() -> MessageBus:
        uow = container.resolve(BaseUserUnitOfWork)
        producer = container.resolve(BaseProducer)

        bus = MessageBus(
            uow=uow,
            commands_map=get_commands_map(uow=uow),
            events_map=get_events_map(producer=producer),
        )
        return bus

    def initialize_consumer() -> BaseConsumer:
        bus = container.resolve(MessageBus)
        return RabbitMQConsumer(external_events_map=get_external_events_map(bus))

    def initialize_producer() -> BaseProducer:
        return RabbitMQProducer()

    container.register(Settings, instance=settings, scope=Scope.singleton)
    container.register(BaseS3Client, factory=initialize_s3_client, scope=Scope.singleton)
    container.register(Redis, factory=initialize_redis_client, scope=Scope.singleton)
    container.register(BaseUserRepository, factory=initialize_user_sqlalchemy_repo)
    container.register(BaseUserUnitOfWork, factory=initialize_user_sqlalchemy_uow)
    container.register(MessageBus, factory=initialize_message_bus)
    container.register(BaseConsumer, factory=initialize_consumer, scope=Scope.singleton)
    container.register(BaseProducer, factory=initialize_producer, scope=Scope.singleton)

    return container
