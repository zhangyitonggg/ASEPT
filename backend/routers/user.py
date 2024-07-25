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