import requests
from typing import override
from Ingester import Ingester
import pandas as pd


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

        payload: pd.DataFrame = self.transform_data(response.json())

        
        print(payload.head())
        print(f"Rows: {len(payload)}")

      
        with self.conn.cursor() as cur:
            for _, row in payload.iterrows():
                cur.execute("""
                    INSERT INTO census (
                        city,
                        state_code,
                        population,
                        median_income,
                        education,
                        median_age,
                        unemployment
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (city, state_code) DO NOTHING;
                """, (
                    row["city"],
                    row["state_code"],
                    row["population"],
                    row["median_income"],
                    row["education"],
                    row["median_age"],
                    row["unemployment"]
                ))

        self.conn.commit()
        self.conn.close()

    def transform_data(self, data_json) -> pd.DataFrame:
        columns = data_json[0]
        data = data_json[1:]

        df = pd.DataFrame(data, columns=columns)

        split_cols = df["NAME"].str.split(",", n=1, expand=True)
        df["city"] = split_cols[0].str.strip()
        df["state_name"] = split_cols[1].str.strip() if split_cols.shape[1] > 1 else ""

        df.rename(columns={
            "state": "state_code",
            "place": "city_code",
            "B01001_001E": "population",
            "B19013_001E": "median_income",
            "B15003_022E": "education",
            "B01002_001E": "median_age",
            "B23025_005E": "unemployment"
        }, inplace=True)

        return df[[
            "city",
            "state_code",
            "population",
            "median_income",
            "education",
            "median_age",
            "unemployment"
        ]]


if __name__ == "__main__":
    CensusIngester().ingest()
