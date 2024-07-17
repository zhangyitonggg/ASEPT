from fastapi import APIRouter, Depends, HTTPException, status, Header
import pymysql

from backend.utils import database, redis
from backend.data.User import Permissions, User
from backend.routers import security
import backend.conf as conf
from backend.data.Announcement import Announcement

router = APIRouter(
    prefix='/admin',
)


@router.post("/set_permission")
async def set_permission(
    target_user_name: str,
    permission: str,
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    database.set_permission(db, target_user_name, permission)
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
    if user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    database.open_announcement(db, announcement, user)
    return {"status": "success"}