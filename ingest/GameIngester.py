from pathlib import Path
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import override
from Ingester import Ingester
import io


BASE_DIR = Path(__file__).resolve().parent
GAMES_CREATE = BASE_DIR / "sql" / "games_create.sql"
GAMES_INSERT = BASE_DIR / "sql" / "games_insert.sql"

class GameIngester(Ingester):

    def __init__(self):
        super().__init__()
        self.start = datetime(2026, 2, 1).date()
        self.end = datetime.now().date()

    @override
    def ingest(self) -> None:
        raw_games = self.extract()
        payload = self.transform(raw_games)
        self.load_into_pg(payload)


    # -----------------------------
    # 1. Extract
    # -----------------------------
    def extract(self):
        all_games = []
        current = self.start

        while current <= self.end:
            date_str = current.strftime("%Y%m%d")
            url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard?dates={date_str}"
            
            response = requests.get(url)
            data = response.json()
            all_games.extend(data.get("events", []))

            current += timedelta(days=1)

        print(f"Total games pulled: {len(all_games)}")
        return all_games

    # -----------------------------
    # 2. Transform
    # -----------------------------
    def transform(self, games) -> dict:
        games_rows = []
        game_teams_rows = []
        teams_rows = []
        seasons_rows = []

        seen_teams = set()
        seen_seasons = set()

        for g in games:
            comp = g["competitions"][0]

            home = [t for t in comp["competitors"] if t["homeAway"] == "home"][0]
            away = [t for t in comp["competitors"] if t["homeAway"] == "away"][0]

            game_id = int(g["id"])
            season_id = int(g["season"]["year"])
            season_type = g["season"]["slug"]

            game_date = g["date"][:10]

            stadium_name = comp.get("venue", {}).get("fullName")
            attendance = comp.get("attendance")

            # ---- Games ----
            games_rows.append({
                "game_id": game_id,
                "stadium": stadium_name,
                "season_id": season_id,
                "game_date": game_date,
                "attendance": attendance
            })

            # ---- Seasons ----
            if season_id not in seen_seasons:
                seasons_rows.append({
                    "season_id": season_id,
                    "year": season_id,
                    "season_type": season_type
                })
                seen_seasons.add(season_id)

            # ---- Teams + Game_Teams ----
            for team, side in [(home, "home"), (away, "away")]:
                team_id = int(team["team"]["id"])
                team_name = team["team"]["displayName"]
                score = int(team["score"])

                if team_id not in seen_teams:
                    teams_rows.append({
                        "team_id": team_id,
                        "team_name": team_name,
                        "stadium": stadium_name
                    })
                    seen_teams.add(team_id)

                game_teams_rows.append({
                    "game_id": game_id,
                    "team_id": team_id,
                    "home_away": side,
                    "score": score
                })

            # winner flag
            home_score = int(home["score"])
            away_score = int(away["score"])

            for row in game_teams_rows[-2:]:
                if home_score == away_score:
                    row["winner_flag"] = False
                elif row["home_away"] == "home":
                    row["winner_flag"] = home_score > away_score
                else:
                    row["winner_flag"] = away_score > home_score
        
        return {
            "games": pd.DataFrame(games_rows),
            "teams": pd.DataFrame(teams_rows),
            "game_teams": pd.DataFrame(game_teams_rows),
            "seasons": pd.DataFrame(seasons_rows)
        }

    # -----------------------------
    # 3. Load
    # -----------------------------
    def load_into_pg(self, payload: dict) -> None:
        with open(GAMES_CREATE, "r") as f:
            self.cur.execute(f.read())

        for table_name, df in payload.items():
            buffer = io.StringIO()
            df.to_csv(buffer, index=False, header=True)
            buffer.seek(0)

            with open(GAMES_INSERT, "r") as f:
                sql = f.read().replace("{{TABLE}}", table_name)
                self.cur.copy_expert(sql, buffer)

        self.conn.commit()
