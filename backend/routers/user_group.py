from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import pymysql

from backend.utils import database
from backend.data.User import Permissions, User
from backend.routers import security

class create_group_request(BaseModel):
    group_name: str
    description: str
    password: str


class group_infomation(BaseModel):
    gid: str
    password: str | None
    description: str | None
    group_name: str | None


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
    request: create_group_request,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    database.create_group(
        db,
        request.group_name,
        user.uid,
        None if request.description == "" else request.description,
        None if request.password == "" else request.password
    )
    return {"status": "success"}


@router.delete("/delete_group")
async def delete_group(
    group_name: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    DO NOT USE IT NOW
    '''
    database.delete_group(db, group_name, user.uid)
    return {"status": "success"}


@router.get("/show_unentered_groups")
async def show_groups(
    sub_name: str | None = None,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    返回当前用户**未**在的用户组。

    格式如下：

    ```
    {
        "groups": [
            {
                "group_name": "group1",
                "need_password": true,
                "gid": "xxxx-xxxx-xxxx",
                "description": "description1"
            }
        ]
    }
    ```
    '''
    return database.show_unentered_groups(db, user.uid, sub_name)


@router.get("/show_create_groups")
async def show_create_groups(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    返回当前用户创建的用户组。

    格式如下：

    ```
    {
        "groups": [
            {
                "group_name": "group1",
                "need_password":"boolen",
                "gid":"xxx",
                "description":"string"
            },
            {
                "group_name": "group2",
                "need_password":"boolen",
                "gid":"xxx",
                "description":"string"
            }
        ]
    }
    ```
    '''
    return database.show_created_groups(db, user.uid)


@router.get("/show_joined_groups")
async def show_joined_groups(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    返回当前用户加入的用户组。

    格式如下：

    ```
    {
        "groups": [
            {
                "group_name": "group1",
                "need_password":"boolen",
                "gid":"xxx",
                "description":"string"
            },
            {
                "group_name": "group2",
                "need_password":"boolen",
                "gid":"xxx",
                "description":"string"
            }
        ]
    }
    ```
    '''
    return database.show_joined_groups(db, user.uid)


@router.post("modify_group")
async def modify_group(
    group_info: group_infomation,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    * 修改群组的信息
    * 参数：**在body里**
        * 用户组的gid---gid
        * 密码---password，不修改是 null，取消密码是 ""
        * 描述---description,同密码
        * 群名---group_name,同密码
        * 返回：如果是群主或者admin的话返回ac，否则返回error
    '''
    database.modify_group(db, group_info, user.uid)
    return {"status": "success"}


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
    database.set_group_perm(db, group_name, user)
    return {"status": "success"}

@router.get("/find_open_groups")
async def find_open_groups(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    return database.find_open_groups(db, user.uid)

@router.post("/set_group_password")
async def set_group_password(
    group_name: str,
    password: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    if not password or len(password) <= 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password too short")
    database.set_group_password(db, group_name, password, user)
    return {"status": "success"}