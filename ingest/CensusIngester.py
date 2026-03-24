import requests
from typing import override
from Ingester import Ingester
import io
import pandas as pd
from psycopg2.extras import RealDictCursor


CENSUS_CREATE: str = "sql/census_create.sql"
CENSUS_INSERT: str = "sql/census_insert.sql"


class CensusIngester(Ingester):

    def __init__(self):
        super().__init__()
        self.url: str = (
            "https://api.census.gov/data/2024/acs/acs5?"
            "get=NAME,B01001_001E,B19013_001E,B15003_022E,B01002_001E,B23025_005E"
            "&for=place:*&in=state:*"
        )

    @override
    def ingest(self) -> None:
        response = requests.get(self.url)
        response.raise_for_status()

        payload: pd.DataFrame = self.transform_data(response.json())

        print(payload.head())
        print(f"Rows: {len(payload)}")

        mask = payload["city"].str.contains("Kansas", case=False, na=False)
        print(f"\nExample of cleaned census rows:\n{payload.loc[mask].head()}")

        self.load_into_pg(payload)
        self.conn.close()

    def transform_data(self, data_json) -> pd.DataFrame:
        columns = data_json[0]
        data = data_json[1:]

        df = pd.DataFrame(data, columns=columns)

        df.rename(columns={
            "state": "state_code",
            "place": "city_code",
            "B01001_001E": "population",
            "B19013_001E": "median_income",
            "B15003_022E": "education",
            "B01002_001E": "median_age",
            "B23025_005E": "unemployment"
        }, inplace=True)

        split_cols = df["NAME"].str.split(",", n=1, expand=True)
        df["city"] = split_cols[0].str.strip()
        df["state"] = split_cols[1].str.strip()

        # remove place qualifiers so future joins on city/state work better
        df["city"] = df["city"].str.replace(r"\s+(city|town|village|borough|CDP|municipality)$", "", regex=True)
        df["city"] = df["city"].str.replace(r"\s+(metro township|unified government)$", "", regex=True)

        numeric_cols = [
            "population",
            "median_income",
            "education",
            "median_age",
            "unemployment"
        ]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["city", "state", "state_code"])
        df = df.drop_duplicates(subset=["city", "state_code"])

        return df[[
            "city",
            "state",
            "state_code",
            "population",
            "median_income",
            "education",
            "median_age",
            "unemployment"
        ]]

    def load_into_pg(self, payload: pd.DataFrame) -> None:
        with open(CENSUS_CREATE, "r") as f:
            sql: str = f.read()
            self.cur.execute(sql)

        buffer = io.StringIO()
        payload.to_csv(buffer, index=False, header=True)
        buffer.seek(0)

        with open(CENSUS_INSERT, "r") as f:
            self.cur.copy_expert(f.read(), buffer)

        self.conn.commit()


if __name__ == "__main__":
    ing = CensusIngester()
    ing.ingest()
    with ing.conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM mls_analysis.census LIMIT 10")
        data = cur.fetchall()
        print(data)