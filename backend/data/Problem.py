from pydantic import BaseModel
from enum import Enum, auto
import datetime

class ProblemType(Enum):
    CHOICE = auto()
    BLANK_FILLING = auto()
    PROGRAM = auto()


class NewProblem(BaseModel):
    title: str
    type: ProblemType
    content: str


class Choice_Problem(NewProblem):
    choices: str
    answer: str


class Blank_Filling_Problem(NewProblem):
    answer: str


class Problem(BaseModel):
    title: str
    type: ProblemType
    content: str

    def __init__(self, pid: int, title: str, type: ProblemType, content: str, author: str, update_time: datetime):
        self.pid = pid
        self.title = title
        self.type = type
        self.content = content
        self.author = author
        self.update_time = update_time