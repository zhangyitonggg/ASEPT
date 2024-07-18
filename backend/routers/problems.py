from fastapi import APIRouter, Depends, HTTPException, status, Header
import pymysql

from backend.utils import database, redis
from backend.data.User import Permissions, User
from backend.routers import security
from backend.data.Problem import Problem, NewProblem

router = APIRouter(
    prefix='/problems',
)


@router.post('/upload_problem')
async def add_problem(
    problem: NewProblem,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    if not user.permissions.get("UPLOAD_PROBLEM"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
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