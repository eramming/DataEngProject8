import psycopg2
from psycopg2.extras import RealDictCursor


class PostgresClient:

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="jhu",
            user="jhu",
            password="jhu123",
            host="postgres",
            port="5432"
        )

    def get_venues(self) -> list:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM mls_analysis.venues")
            data = cur.fetchall()
        return data

    def get_census(self) -> list:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM mls_analysis.census LIMIT 100")
            data = cur.fetchall()
        return data