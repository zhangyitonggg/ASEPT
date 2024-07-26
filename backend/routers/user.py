from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
import pymysql

from backend.utils import database, redis
from backend.data.User import Permissions, User, PermissionType
from backend.routers import security
import backend.conf as conf
from backend.data.Announcement import Announcement

router = APIRouter(
    prefix='/user',
)

class ModifyUserInfo(BaseModel):
    originalPassword: str = Query(min_length=1, max_length=20)
    newPassword: str = Query(min_length=1, max_length=20)


@router.post("/modify")
async def set_permission(
    info: ModifyUserInfo,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    database.modify_user_info(db, user, info.originalPassword, info.newPassword)
    return {"status": "success"}


@router.get('/get_user_statistics')
async def get_user_statistics(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    获取用户题目统计信息。
    
    返回格式：
    
    ```
    {
        "choice_submit": 100,
        "choice_correct": 80,
        "blank_submit": 50,
        "blank_correct": 40,
    }
    ```
    '''
    return database.get_user_statistics(db, user)