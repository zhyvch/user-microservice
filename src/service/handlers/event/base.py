from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class BaseEventHandler(ABC):
    # message_broker: BaseMessageBroker
    # broker_topic: str | None = None

    @abstractmethod
    async def __call__(self, event: BaseEvent) -> None:
        ...
