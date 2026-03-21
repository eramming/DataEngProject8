from VenueIngester import VenueIngester
from typing import List
from Ingester import Ingester
import psycopg2


INIT_SQL_FILE = "sql/initialize.sql"

class IngestPipeline:

    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname="jhu",
            user="jhu",
            password="jhu123",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()
        self.ingesters: List[Ingester] = []
        self.ingesters.append(VenueIngester())


    def ingest_all(self) -> None:
        self.initialize()
        for ingester in self.ingesters:
            ingester.ingest()
        self.conn.close()

    def initialize(self) -> None:
        with open(INIT_SQL_FILE, "r") as f:
            sql: str = f.read()
            self.cur.execute(sql)
            self.conn.commit()
