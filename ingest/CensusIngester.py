import requests
import pandas as pd
from typing import override
from Ingester import Ingester
import io

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CENSUS_CREATE = BASE_DIR / "sql" / "census_create.sql"
CENSUS_INSERT = BASE_DIR / "sql" / "census_insert.sql"


class CensusIngester(Ingester):

    def __init__(self):
        super().__init__()
        self.url = (
            "https://api.census.gov/data/2024/acs/acs5?"
            "get=NAME,B01001_001E,B19013_001E,B15003_022E,B01002_001E,B23025_005E"
            "&for=place:*&in=state:*"
        )

    @override
    def ingest(self) -> None:
        raw_data = self.extract()
        payload = self.transform(raw_data)
        self.load_into_pg(payload)
        self.conn.close()

    # -----------------------------
    # 1. Extract
    # -----------------------------
    def extract(self):
        response = requests.get(self.url)
        response.raise_for_status()
        data = response.json()
        print(f"Total census rows pulled: {len(data) - 1}")
        return data

    # -----------------------------
    # 2. Transform
    # -----------------------------
    def transform(self, data_json) -> pd.DataFrame:
        columns = data_json[0]
        data = data_json[1:]

        df = pd.DataFrame(data, columns=columns)

        df.rename(columns={
            "B01001_001E": "population",
            "B19013_001E": "median_income",
            "B15003_022E": "education",
            "B01002_001E": "age",
            "B23025_005E": "unemployment"
        }, inplace=True)

        split_cols = df["NAME"].str.split(",", n=1, expand=True)
        df["city"] = split_cols[0].str.strip()
        df["state"] = split_cols[1].str.strip()

        # clean city names a bit for better consistency
        df["city"] = df["city"].str.replace(
            r"\s+(city|town|village|borough|CDP|municipality)$",
            "",
            regex=True
        )
        df["city"] = df["city"].str.replace(
            r"\s+(metro township|unified government)$",
            "",
            regex=True
        )

        numeric_cols = ["population", "median_income", "education", "age", "unemployment"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["city", "state"])
        df = df.drop_duplicates(subset=["city", "state"])

        df = df[[
            "city",
            "state",
            "population",
            "median_income",
            "education",
            "age",
            "unemployment"
        ]]

        print(df.head())
        print(f"Cleaned census rows: {len(df)}")

        return df

    # -----------------------------
    # 3. Load
    # -----------------------------
    def load_into_pg(self, payload: pd.DataFrame) -> None:
        with open(CENSUS_CREATE, "r") as f:
            self.cur.execute(f.read())

        buffer = io.StringIO()
        payload.to_csv(buffer, index=False, header=True)
        buffer.seek(0)

        with open(CENSUS_INSERT, "r") as f:
            self.cur.copy_expert(f.read(), buffer)

        self.conn.commit()

if __name__ == "__main__":
    ing = CensusIngester()
    ing.ingest()
