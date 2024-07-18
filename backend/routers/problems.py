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
    if not user.permissions.get("UPLOAD_PROBLEM"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
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
    pid = database.add_problem(db, problem, user)
    return {'status': 'success', 'pid': pid}

@router.get('/my_problems')
async def get_my_problems(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    return database.get_my_problems(db, user)


@router.get('/{problem_id}', response_model=Problem)
async def get_problem(
    problem_id: str,
    user: User = Depends(security.get_user)
):
    '''
    NOTICE: This function is not complete and will not work as expected.
            This function must be placed at the end of the file to avoid conflict with other routers.
    '''
    if not user.has_permission(Permissions.VIEW_PROBLEM):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
    return {"status": "success"}