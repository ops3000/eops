# eops/core/handler/decider.py
from abc import ABC, abstractmethod
from typing import Set, TYPE_CHECKING

from ..event import Event, EventType

if TYPE_CHECKING:
    from ..strategy import BaseStrategy

class BaseDecider(ABC):
    """
    Abstract Base Class for deciders.
    Deciders consume events and may produce new events (like ORDER)
    onto their strategy's event bus.
    """
    def __init__(self, strategy: 'BaseStrategy'):
        self.strategy = strategy
        self.log = self.strategy.log
        self.event_bus = self.strategy.event_bus

    @property
    @abstractmethod
    def subscribed_events(self) -> Set[EventType]:
        """Returns the set of EventTypes this decider is interested in."""
        pass

    @abstractmethod
    def process(self, event: Event):
        """The core logic to process an event and make a decision."""
        pass