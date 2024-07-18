from fastapi import APIRouter, Depends, HTTPException, status, Header
import pymysql
import json

from backend.utils import database, redis
from backend.data.User import Permissions, User
from backend.routers import security
from backend.data.Problem import *

router = APIRouter(
    prefix='/problems',
)


@router.post('/upload_problem')
async def add_problem(
    problem: Choice_Problem | Blank_Filling_Problem,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    The choices should be like this:
    ```
    {
        "A": "Choice A",
        "B": "Choice B",
        "C": "Choice C",
        "D": "Choice D"
    }
    ```
    and the answer should be like this:
    ```
    {
        "A": "Choice A",
        "B": "Choice B"
    }
    ```
    for blank filling problem, the answer should be like this:
    ```
    {
        "1": "answer1",
        "2": [
            "answer2",
            "answer3"
        ]
    }
    ```
    '''
    if not user.permissions.get("UPLOAD_PROBLEM"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
    check_problem_format(problem)
    pid = database.add_problem(db, problem, user)
    return {'status': 'success', 'pid': pid}


@router.post('/add_problem_tag')
async def add_problem_tag(
    problem: Problem,
    tag: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    database.add_problem_tag(db, problem.pid, tag, user)
    return {'status': 'success'}


@router.get('/search_problem_by_tag')
async def search_problem_by_tag(
    tag: str,
    db: pymysql.connections.Connection = Depends(database.connect)
):
    return database.search_problem_by_tag(db, tag)


@router.get('/my_problems')
async def get_my_problems(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    获取当前用户上传的题目。

    返回格式：
    ```
    {
        "problems": [
            {
                "pid": 1,
                "title": "Problem Title",
                "content": "Problem Content",
                "type": 0,
                “author”: "Author Name",
                "upload_time": "2021-10-01 12:00:00",
                "choices": {
                    "A": "Choice A",
                    "B": "Choice B",
                    "C": "Choice C",
                    "D": "Choice D"
                },
                "answers": {
                    "A": "Choice A",
                    "B": "Choice B"
                },
                "is_public": 0
            },
            {
                "pid": 2,
                "title": "Problem Title",
                "content": "Problem Content",
                "type": 1,
                “author”: "Author Name",
                "upload_time": "2021-10-01 12:00:00",
                "choices": {
                    "A": "Choice A",
                    "B": "Choice B",
                    "C": "Choice C",
                    "D": "Choice D"
                },
                "answers": {
                    "B": "Choice B"
                },
                "is_published": 1
            },
            {
                "pid": 2,
                "title": "Problem Title",
                "content": "Problem Content",
                "type": 1,
                “author”: "Author Name",
                "upload_time": "2021-10-01 12:00:00",
                "choices": null,
                "answers": {
                    "B": "Choice B"
                },
                "is_published": 1
            }
        ]
    }
    '''
    return database.get_my_problems(db, user)


@router.get('/{problem_id}', response_model=Problem)
async def get_problem(
    problem_id: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    NOTICE: This function is not complete and will not work as expected.
            This function must be placed at the end of the file to avoid conflict with other routers.
    '''
    if database.problem_accessible(db, user, problem_id):
        return database.get_problem(db, problem_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')


def check_problem_format(problem: Choice_Problem | Blank_Filling_Problem):
    try:
        json.loads(problem.answer)
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid answer format')
    if isinstance(problem, Choice_Problem):
        try:
            json.loads(problem.choices)
        except json.JSONDecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid choices format')
        problem.type = ProblemType.CHOICE
    elif isinstance(problem, Blank_Filling_Problem):
        problem.type = ProblemType.BLANK_FILLING
        pass