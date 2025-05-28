import logging
from dataclasses import dataclass

from domain.events.users import UserCreatedEvent, UserRegistrationCompletedEvent, UserDeletedEvent
from service.handlers.event.base import BaseEventHandler


logger = logging.getLogger(__name__)


@dataclass
class UserCreatedEventHandler(BaseEventHandler):
    async def __call__(self, event: UserCreatedEvent) -> None:
        logger.info('Publishing user created event for user ID: %s', event.user_id)
        try:
            await self.producer.publish(event, self.topic)
            logger.info('Successfully published user created event to topic: %s', self.topic)
        except Exception as e:
            logger.exception('Failed to publish user created event: %s', str(e))
            raise


@dataclass
class UserDeletedEventHandler(BaseEventHandler):
    async def __call__(self, event: UserDeletedEvent) -> None:
        logger.info('Publishing user deleted event for user ID: %s', event.user_id)
        try:
            await self.producer.publish(event, self.topic)
            logger.info('Successfully published user deleted event to topic: %s', self.topic)
        except Exception as e:
            logger.exception('Failed to publish user deleted event: %s', str(e))
            raise


@dataclass
class UserRegistrationCompletedEventHandler(BaseEventHandler):
    async def __call__(self, event: UserRegistrationCompletedEvent) -> None:
        logger.info('Publishing registration completed event for user ID: %s', event.user_id)
        try:
            await self.producer.publish(event, self.topic)
            logger.info('Successfully published registration completed event to topic: %s', self.topic)
        except Exception as e:
            logger.exception('Failed to publish registration completed event: %s', str(e))
            raise
