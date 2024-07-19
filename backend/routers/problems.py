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

'''
- 上传题目（pdf，文字）   题目创建时只有自己有访问权限，将其加入题目组后其他人才可能有访问权限
- 添加tag，*删除tag*
- 根据tag搜索题目，搜索范围为 自己有权限能看到的题目（自己创建的+分享的）
- 题目组创建，加入题目，*从题目组中删除题目*，分享给用户组
- tag & 题目组 & 题目名称
- 题目信息（总提交次数，总通过次数，错误答案）
- 个性化题目推荐
- 题目敏感词
'''

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


@router.post('/create_problem_group')
async def create_problem_group(
    name: str,
    description: str = '',
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    创建题目组。
    
    name: str，题目组名称
    
    description: str = ''，题目组描述，可选
    '''
    database.create_problem_group(db, name, description, user)
    return {'status': 'success'}


@router.post('/change_problem_group_info')
async def change_problem_group_info(
    pgid: str,
    name: str,
    description: str = '',
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    修改题目组信息。
    
    pgid: str，题目组 id
    
    name: str，题目组名称
    
    description: str = ''，题目组描述，可选
    '''
    database.change_problem_group_info(db, pgid, name, description, user)
    return {'status': 'success'}


@router.post('/add_problem_to_group')
async def add_problem_to_group(
    pid: str,
    pgid: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    将题目加入题目组。
    
    pid: str，题目 id
    
    pgid: str，题目组 id
    '''
    database.add_problem_to_group(db, pid, pgid, user)
    return {'status': 'success'}


@router.post('/share_problem_group_to_user_group')
async def share_problem_group_to_user_group(
    pgid: str,
    gid: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    将题目组分享给用户组。
    
    当且仅当用户是题目组创建者 且 用户在用户组中才能分享
    
    pgid: str，题目组 id
    
    gid: str，用户组 id
    '''
    database.share_problem_group_to_user_group(db, pgid, gid, user)
    return {'status': 'success'}


@router.post('/add_problem_tag')
async def add_problem_tag(
    pid: str,
    tag: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    为题目添加标签。
    
    pid: str，题目 id
    
    tag: str，标签名称
    '''
    database.add_problem_tag(db, pid, tag, user)
    return {'status': 'success'}


@router.get('/search_problem_by_tag')
async def search_problem_by_tag(
    tag: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    根据标签搜索题目。
    
    tag: str，标签名称
    
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
            }
        ]
    }   
    '''
    return database.search_problem_by_tag(db, tag, user)


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