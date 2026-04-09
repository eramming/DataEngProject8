import psycopg2
import time
from psycopg2.extras import RealDictCursor


class PostgresClient:
    def __init__(self):
        retries = 5
        for i in range(retries):
            try:
                self.conn = psycopg2.connect(
                    dbname="jhu",
                    user="jhu",
                    password="jhu123",
                    host="postgres",
                    port="5432"
             )
                print("Connected to Postgres!")
                break
            except psycopg2.OperationalError as e:
                print(f"Retry {i+1}/{retries}...")
                time.sleep(5)
        else:
            raise Exception("Could not connect to Postgres")

    def _fetch_all(self, query: str) -> list:
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            self.conn.rollback()
            print(f"Query failed: {e}")
            raise

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
    
    def get_game_view(self) -> list:
        query = """
        SELECT 
            g.game_id,
            g.game_date,

            wt.team_name AS winning_team,
            lt.team_name AS losing_team,

            wgt.score AS winning_score,
            lgt.score AS losing_score,

            v.stadium,
            v.capacity,
            g.attendance,
            c.median_income,
            c.median_age

        FROM mls_analysis.games g

        -- Winner
        JOIN mls_analysis.game_teams wgt
            ON g.game_id = wgt.game_id
            AND wgt.winner_flag = TRUE

        JOIN mls_analysis.teams wt
            ON wgt.team_id = wt.team_id

        -- Loser
        JOIN mls_analysis.game_teams lgt
            ON g.game_id = lgt.game_id
            AND lgt.winner_flag = FALSE

        JOIN mls_analysis.teams lt
            ON lgt.team_id = lt.team_id

        -- Other joins
        JOIN mls_analysis.venues v
            ON g.stadium = v.stadium

        JOIN mls_analysis.census c
            ON LOWER(v.city) = LOWER(c.city)
            AND v.state = c.state

        ORDER BY g.game_date DESC
        LIMIT 10;
        """
        return self._fetch_all(query)