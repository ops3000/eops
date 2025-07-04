# eops/core/handler/executor.py
from abc import ABC, abstractmethod
from typing import Set, TYPE_CHECKING

from ..event import Event, EventType

if TYPE_CHECKING:
    from ..strategy import BaseStrategy

class BaseExecutor(ABC):
    """
    Abstract Base Class for executors.
    Executors consume events (typically ORDER) and interact with the
    trading venue, potentially producing new events (like FILL).
    """
    def __init__(self, strategy: 'BaseStrategy'):
        self.strategy = strategy
        self.log = self.strategy.log
        self.event_bus = self.strategy.event_bus

    @property
    @abstractmethod
    def subscribed_events(self) -> Set[EventType]:
        """Returns the set of EventTypes this executor is interested in."""
        pass

    @abstractmethod
    def process(self, event: Event):
        """The core logic to execute an order event."""
        pass