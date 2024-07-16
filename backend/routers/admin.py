from fastapi import APIRouter, Depends, HTTPException, status
import pymysql

from backend.utils import database
from backend.data.User import Permissions, User
from backend.routers import security

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