from Ingester import Ingester
import requests


class SrcAIngester(Ingester):

    def __init__(self):
        super().__init__()


    def ingest(self) -> None:
        self.helperA()
        self.helperB()
        raise NotImplementedError()
    
    def helperA(self) -> None:
        # response = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
        response = requests.get("https://api.sportmonks.com/v3/football/schedules/seasons/23690/teams/62?api_token={TOKEN}")
        data = response.json()
        print(f"Rangers 24/25 Szn Length: {len(data)}")
    
    def helperB(self) -> None:
        raise NotImplementedError()