from fastapi import APIRouter, Depends, HTTPException, status
import pymysql

from backend.utils import database
from backend.data.User import Permissions, User
from backend.routers import security

router = APIRouter(
    prefix='/user_group',
)

@router.post("/join_group")
def join_group(
    gid: str,
    user_name: str | None = None,
    user: User = Depends(security.get_user),
    password: str | None = None,
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    NOTICE: params "user_name" is invalid. Maybe we will use it in the future.

    gid: str，要加入的用户组 id

    ~~user_name: str | None = None，要加入的用户名称~~ 没有用

    一定是当前登录的用户加入用户组

    password: str | None = None，用户组密码，如果用户组有密码的话

    **暂时不要使用这个接口，后端在调整**
    '''
    if user_name is None:
        user_name = user.name
    database.join_group(db, gid, user.uid, password)
    return {"status": "success"}


@router.post("/leave_group")
async def leave_group(
    gid: str,
    user_name: str | None = None,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    gid: str，要离开的用户组 id

    user_name: str | None = None，要离开的用户名称

    **先别用**
    '''
    database.leave_group(db, gid, user_name if user_name else user.name, user)
    return {"status": "success"}


@router.post("/create_group")
async def create_group(
    group_name: str,
    user: User = Depends(security.get_user),
    description: str | None = None,
    password: str | None = None,
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    group_name: str，用户组名称

    description: str | None = None，用户组描述，可以为空

    password: str | None = None，用户组密码，可以为空
    '''
    if password is not None and len(password) <= 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password too short")
    database.create_group(db, group_name, user.uid, description, password)
    return {"status": "success"}


@router.delete("/delete_group")
async def delete_group(
    group_name: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    删除用户组。
    
    group_name: str，用户组名称
    '''
    database.delete_group(db, group_name, user.uid)
    return {"status": "success"}


@router.get("/show_groups")
async def show_groups(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    返回当前用户所在的用户组。

    格式如下：

    ```
    {
        "groups": [
            {
                "group_name": "group1",
                "description": "description1",
                "owner": "owner1",
                "is_admin": true,
                "gid": "xxxx-xxxx-xxxx"
            },
            {
                "group_name": "group2",
                "description": "description2",
                "owner": "owner2",
                "is_admin": true,
                "gid": "xxxx-xxxx-xxxx"
            }
        ]
    }
    ```
    '''
    return database.show_groups(db, user.uid)


@router.get("/all_groups")
async def all_groups(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    返回所有用户组。

    格式如下：

    ```
    {
        "groups": [
            {
                "group_name": "group1",
                "description": "description1",
                "owner": "owner1",
                "is_admin": true,
                "gid": "xxxx-xxxx-xxxx"
            },
            {
                "group_name": "group2",
                "description": "description2",
                "owner": "owner2",
                "is_admin": true,
                "gid": "xxxx-xxxx-xxxx"
            }
        ]
    }
    ```
    '''
    return database.all_user_groups(db)

@router.post("/set_group_perm")
async def set_group_perm(
    group_name: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    设置用户组权限。
    
    group_name: str，用户组名称
    '''
    database.set_group_perm(db, group_name, user)
    return {"status": "success"}

@router.get("/find_open_groups")
async def find_open_groups(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    查找公开的用户组。
    
    返回格式如下：
    ```
    {
        "groups": [
            {
                "name": "group1",
                "description": "description1",
                "owner": "owner1"
            },
            {
                "name": "group2",
                "description": "description2",
                "owner": "owner2"
            }
        ]
    }
    '''
    return database.find_open_groups(db, user.uid)

@router.post("/set_group_password")
async def set_group_password(
    group_name: str,
    password: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    设置用户组密码。
    
    group_name: str，用户组名称
    
    password: str，用户组密码（至少 5 位），或者为空，表示取消密码
    '''
    if not password and len(password) <= 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password too short")
    database.set_group_password(db, group_name, password, user)
    return {"status": "success"}