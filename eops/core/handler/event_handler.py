# eops/core/handler/event_handler.py
from abc import ABC, abstractmethod
from typing import Set, TYPE_CHECKING

from ..event import Event, EventType

if TYPE_CHECKING:
    from ..strategy import BaseStrategy

class BaseEventHandler(ABC):
    """
    Abstract Base Class for event handlers.
    Event handlers consume events from their strategy's event bus.
    """
    def __init__(self, strategy: 'BaseStrategy'):
        self.strategy = strategy
        self.log = self.strategy.log
        self.event_bus = self.strategy.event_bus

    @property
    @abstractmethod
    def subscribed_events(self) -> Set[EventType]:
        """Returns the set of EventTypes this handler is interested in."""
        pass

    @abstractmethod
    def process(self, event: Event):
        """The core logic to process a subscribed event."""
        pass