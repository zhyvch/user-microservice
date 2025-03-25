from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.commands.base import BaseCommand


@dataclass
class BaseCommandHandler(ABC):
    # message_broker: BaseMessageBroker
    # broker_topic: str | None = None

    @abstractmethod
    async def __call__(self, command: BaseCommand) -> None:
        ...
