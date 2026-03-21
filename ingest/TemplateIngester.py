from Ingester import Ingester
from typing import override

class SrcAIngester(Ingester):

    def __init__(self):
        super().__init__()


    @override
    def ingest(self) -> None:
        self.helperA()
        self.helperB()
        raise NotImplementedError()
    
    def helperA(self) -> None:
        raise NotImplementedError()
    
    def helperB(self) -> None:
        raise NotImplementedError()