from abc import ABC, abstractmethod


class Ingester(ABC):

    @abstractmethod
    def ingest(self) -> None:
        """Abstract method that must be implemented by subclasses."""
        pass