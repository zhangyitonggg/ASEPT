from pydantic import BaseModel
from enum import Enum

class ProblemType(Enum):
    CLASSIC = 0
    INTERACTIVE = 1
    OUTPUT_ONLY = 2
    SPECIAL_JUDGE = 3

class Problem(BaseModel):
    id: int
    name: str

    def __init(self, id: int, name: str):
        self.id = id
        self.name = name