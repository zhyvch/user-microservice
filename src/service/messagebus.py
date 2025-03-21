from domain.events.base import BaseEvent
from domain.events.users import UserCreatedEvent


def send_user_created_event(event: UserCreatedEvent):
    ...


HANDLERS = {
    UserCreatedEvent: [send_user_created_event],
}


def handle(event: BaseEvent):
    for handler in HANDLERS[type(event)]:
        handler(event)