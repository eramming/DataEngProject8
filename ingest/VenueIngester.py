import requests
from typing import override
from Ingester import Ingester
import io
import pandas as pd
from psycopg2.extras import RealDictCursor


VENUES_CREATE: str = "sql/venues_create.sql"
VENUES_INSERT: str = "sql/venues_insert.sql"

class VenueIngester(Ingester):

    def __init__(self):
        super().__init__()
        self.url: str = "https://cdn.jsdelivr.net/gh/gavinr/usa-soccer@master/mls.csv"


    @override
    def ingest(self) -> None:
        response = requests.get(self.url)
        payload: pd.DataFrame = self.transform_data(response.content.decode("utf-8"))
        self.load_into_pg(payload)
        self.conn.close()
        

    def transform_data(self, data_str: str) -> pd.DataFrame:
        df: pd.DataFrame = pd.read_csv(io.StringIO(data_str))
        print(df.head())
        df = df.drop(columns=["joined", "head_coach", "url", 
                         "wikipedia_url", "logo_url"])
        df = df.rename({
            "latitude": "lat", 
            "longitude": "lon",
            "stadium_capacity": "capacity"
            })
        return df

    
    def load_into_pg(self, payload: pd.DataFrame) -> None:
        with open(VENUES_CREATE, 'r') as f:
            sql: str = f.read()
            self.cur.execute(sql)
        buffer = io.StringIO()
        payload.to_csv(buffer, index=False, header=True)
        buffer.seek(0)
        with open(VENUES_INSERT, 'r') as f:
            self.cur.copy_expert(f.read(), buffer)
        self.conn.commit()
    

if __name__ == "__main__":
    ing = VenueIngester()
    ing.ingest()
    with ing.conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM mls_analysis.venues")
        data = cur.fetchall()
        print(data)