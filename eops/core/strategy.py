# eops/core/strategy.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from .exchange import BaseExchange

class BaseStrategy(ABC):
    """
    Abstract Base Class for all strategy implementations.
    The user must implement a class that inherits from this one.
    """

    def __init__(self, context: Dict[str, Any], params: Dict[str, Any]):
        """
        Initialize the strategy.

        Args:
            context (Dict[str, Any]): A dictionary containing shared objects,
                                     like the exchange instance. e.g., {'exchange': ...}
            params (Dict[str, Any]): Strategy-specific parameters from the config file.
        """
        self.exchange: BaseExchange = context['exchange']
        self.params = params
        self.log = print # A simple logger, can be replaced later.

    @abstractmethod
    def next(self):
        """
        This is the main logic loop of the strategy.
        The engine will call this method on each "tick" or time interval.
        """
        pass