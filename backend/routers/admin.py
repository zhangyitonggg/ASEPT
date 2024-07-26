from fastapi import APIRouter, Depends, HTTPException, status, Header
import pymysql
from pydantic import BaseModel

from backend.utils import database, redis
from backend.data.User import Permissions, User, PermissionType
from backend.routers import security
import backend.conf as conf
from backend.data.Announcement import Announcement

router = APIRouter(
    prefix='/admin',
)

class setPermissionReq(BaseModel):
    target_user_name: str
    permission: PermissionType
    cancel: bool


@router.post("/set_permission")
async def set_permission(
    requst: setPermissionReq,
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    给用户设置权限，只有**拥有全部权限的**管理员可以设置权限。

    target_user_name: str 类型，目标用户名。

    permission: PermissionType 类型，权限类型。前端用 0 - 7 表示权限，具体对应如下：

    1. 给予管理员权限
    2. 给予封禁用户权限
    3. 给予审核题目权限
    4. 给予管理平台权限
    5. 给予上传文件权限
    6. 给予上传题目权限
    7. 给予分享题目权限
    8. 搜索题目权限
    9. 封禁用户
    
    cancel: bool 类型，是否取消权限。
    '''
    if user.permissions.get("IS_ADMIN") == False or \
        user.permissions.get("BLOCK_USER") == False or \
        user.permissions.get("REVIEW_TOPIC") == False or \
        user.permissions.get("MANAGE_PLATFORM") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You have no full permissions."
        )
    database.set_permission(db, requst.target_user_name, requst.permission, requst.cancel)
    return {"status": "success"}


@router.post("/set_admin")
async def set_platform_super_admin(
    target_user_name: str,
    key: str | None = Header(charset="UTF-8", min_length=1, max_length=256, errors='strict'),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    NOTICE: THIS API WILL GIVE THE TARGET USER **ALL** PERMISSIONS.
    '''
    if key != conf.ADMIN_KEY:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. Invalid key."
        )
    redis.delete_user_permissions_from_cache(database.set_admin(db, target_user_name))
    return {"status": "success"}


@router.post("/open_announcement")
async def open_announcement(
    announcement: Announcement,
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    发布公告，只有管理员可以发布公告。

    在 body 中传入一个 json，格式如下：

    ```
    {
        "title": "公告标题",
        "content": "公告内容"
    }
    ```
    '''
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    database.open_announcement(db, announcement, user)
    return {"status": "success"}


@router.post("/modify_announcement")
async def modify_announcement(
    announcement: Announcement,
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    修改公告，只有管理员可以修改公告。

    在 body 中传入一个 json，格式如下：

    ```
    {
        "aid": "xxxx-xxxx",
        "title": "公告标题",
        "content": "公告内容",
        "is_active": 0
    }
    ```
    '''
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    database.modify_announcement(db, announcement, user)
    return {"status": "success"}


@router.get('/get_all_users')
async def get_all_users(
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    获取所有用户的信息，只有管理员可以获取。
    
    返回格式：
    
    ```
    {
        "users": [
            {
                "name": "用户名",
                "uid": "xxxx",(uuid)
                "is_admin": 'True'/'False',
                "blocked": 0/1,
            },
            ...
        ]
    }
    ```
    '''
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    return database.get_all_users(db)


@router.get('/get_all_problems')
async def get_all_problems(
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    获取所有题目的信息，只有管理员可以获取。
    
    返回格式：
    
    ```
    {
        "problems": [
            {
                "pid": 1,
                "title": "Problem Title",
                "content": "Problem Content",
                "type": 'choice',
                “author”: "xxx",(uuid)
                "update_time": "2021-10-01 12:00:00",
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
                "type": 'blank_filling',
                “author”: "xxx",(uuid)
                "update_time": "2021-10-01 12:00:00",
                "choices": null,
                "answers": {
                    "B": "Choice B"
                },
                "is_public": 1
            }
        ]
    }
    ```
    '''
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    return database.admin_get_all_problems(db)


@router.get('/get_all_groups')
async def get_all_groups(
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    获取所有用户组的信息，只有管理员可以获取。
    
    格式如下：

    ```
    {
        "groups": [
            {
                "gid": "xxx",(uuid)
                "name": "xxx",
                "description": "xxx",
                "owner": "xxx", (uuid)
                "is_open": 'True'/'False',
                "password": "xxx"
            },
            ...
        ]
    }
    ```
    '''
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    return database.get_all_groups(db)


@router.get('/get_all_problem_groups')
async def get_all_problem_groups(
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    获取所有题目与用户组的关联信息，只有管理员可以获取。
    
    返回格式：

    ```
    {
        "problem_groups": [
            {
                "pgid": "xxx",(uuid)
                "name": "xxx",
                "description": "xxx",
                "owner": "xxx" (uuid)
            },
            ...
        ]
    }
    ```
    '''
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    return database.get_all_problem_groups(db)


@router.post('/delete_admin')
async def delete_admin(
    uid: str,
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    删除管理员权限，只有管理员可以删除。
    '''
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    database.delete_admin(db, uid)
    return {"status": "success"}


@router.get('/get_all_admin')
async def get_all_admin(
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    获取所有管理员信息，只有管理员可以获取。
    
    返回格式：

    ```
    {
        "admins": [
            {
                "uid": "xxx",(uuid)
                "name": "xxx",
            },
            ...
        ]
    }
    ```
    '''
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    return database.get_all_admin(db)