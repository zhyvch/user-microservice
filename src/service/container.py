from functools import lru_cache

from punq import Container, Scope

from domain.commands.users import UserCreateCommand
from domain.events.users import UserCreatedEvent
from service.handlers.command.users import UserCreateCommandHandler
from service.handlers.event.users import UserCreatedEventHandler
from service.message_bus import MessageBus
from service.units_of_work.users.base import BaseUserUnitOfWork
from service.units_of_work.users.postgresql import SQLAlchemyUserUnitOfWork
from settings.config import Settings


@lru_cache(1)
def initialize_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    def initialize_users_sqlalchemy_uow() -> BaseUserUnitOfWork:
        return SQLAlchemyUserUnitOfWork()

    container.register(BaseUserUnitOfWork, factory=initialize_users_sqlalchemy_uow)

    def initialize_message_bus() -> MessageBus:
        create_user_handler = UserCreateCommandHandler(

        )

        user_created_handler = UserCreatedEventHandler(

        )

        commands_map = {
            UserCreateCommand: create_user_handler,
        }
        events_map = {
            UserCreatedEvent: [user_created_handler],
        }

        bus = MessageBus(
            uow=container.resolve(BaseUserUnitOfWork),
            commands_map=commands_map,
            events_map=events_map,
        )

        return bus

    container.register(MessageBus, factory=initialize_message_bus, scope=Scope.singleton)


    return container
