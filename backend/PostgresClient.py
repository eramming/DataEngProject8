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

    def _fetch_all(self, query: str) -> list:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

    def get_venues(self) -> list:
        return self._fetch_all("SELECT * FROM mls_analysis.venues")

    def get_census(self) -> list:
        return self._fetch_all("SELECT * FROM mls_analysis.census LIMIT 100")

    def get_seasons(self) -> list:
        return self._fetch_all("SELECT * FROM mls_analysis.seasons")

    def get_teams(self) -> list:
        return self._fetch_all("SELECT * FROM mls_analysis.teams")

    def get_games(self) -> list:
        return self._fetch_all("SELECT * FROM mls_analysis.games")

    def get_game_teams(self) -> list:
        return self._fetch_all("SELECT * FROM mls_analysis.game_teams")