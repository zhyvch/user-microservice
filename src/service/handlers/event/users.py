from domain.events.users import UserCreatedEvent
from service.handlers.event.base import BaseEventHandler


class UserCreatedEventHandler(BaseEventHandler):
    async def __call__(self, event: UserCreatedEvent) -> None:
        await self.producer.publish(event, self.topic)
