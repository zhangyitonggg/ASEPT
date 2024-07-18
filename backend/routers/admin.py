from fastapi import APIRouter, Depends, HTTPException, status, Header
import pymysql

from backend.utils import database, redis
from backend.data.User import Permissions, User, PermissionType
from backend.routers import security
import backend.conf as conf
from backend.data.Announcement import Announcement

router = APIRouter(
    prefix='/admin',
)


@router.post("/set_permission")
async def set_permission(
    target_user_name: str,
    permission: PermissionType,
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
    '''
    if user.permissions.get("IS_ADMIN") == False or \
        user.permissions.get("BLOCK_USER") == False or \
        user.permissions.get("REVIEW_TOPIC") == False or \
        user.permissions.get("MANAGE_PLATFORM") == False:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You have no full permissions."
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