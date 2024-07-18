from pydantic import BaseModel
from enum import Enum, auto

class ProblemType(Enum):
    CHOICE = "CHOICE"
    BLANK_FILLING = "BLANK_FILLING"
    PROGRAM = "PROGRAM"


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
    pid: str
    title: str
    content: str
    type: ProblemType
    author: str
    update_time: str
    is_published: bool
    choices: str | None = None
    answers: str | None = None