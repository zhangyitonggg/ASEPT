from pydantic import BaseModel
from enum import Enum, auto
import datetime

class ProblemType(Enum):
    SINGLE_CHOICE = auto()
    MULTI_CHOICE = auto()
    BLANK_FILLING = auto()
    PROGRAM = auto()


class NewProblem(BaseModel):
    title: str
    type: ProblemType
    content: str


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