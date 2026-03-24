from abc import ABC, abstractmethod
import psycopg2


class Ingester(ABC):

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="jhu",
            user="jhu",
            password="jhu123",
            host="postgres",
            port="5432"
        )
        self.cur = self.conn.cursor()

    @abstractmethod
    def ingest(self) -> None:
        """Abstract method that must be implemented by subclasses."""
        pass