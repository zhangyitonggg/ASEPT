from fastapi import APIRouter, Depends, HTTPException, status
import pymysql

from backend.utils import database
from backend.data.User import Permissions
from backend.routers import security

router = APIRouter(
    prefix='/admin',
)

@router.post("/set_permission")
async def set_permission(
    target_user_name: str,
    permission: str,
    permissions: Permissions = Depends(security.get_admin_permissions),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    if permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    database.set_permission(db, target_user_name, permission)
    return {"status": "success"}