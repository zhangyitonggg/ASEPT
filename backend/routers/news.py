from fastapi import APIRouter, Depends, HTTPException, status, Header
import pymysql

from backend.utils import database, redis
from backend.data.User import Permissions, User
from backend.routers import security
from backend.data.Announcement import Announcement

router = APIRouter(
    prefix='/news',
)

@router.get("/get_announcements")
async def get_announcements(
    max_announcements: int = 3,
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    max_announcements: int 类型，最多获取的公告数量，默认为 3

    返回值：json 格式的公告列表。is_active 为表示公告是否有效。

    ```
    {
        "announcements": [
            {
                "title": "公告标题",
                "content": "公告内容",
                "update_at": "2021-01-01 00:00:00",
                "is_active": 1
                "author": "zyt"
            },
            {
                "title": "公告标题",
                "content": "公告内容",
                "update_at": "2021-01-01 00:00:00",
                "is_active": 1
                "author": "zyt"
            }
        ]
    }
    ```
    '''
    return database.get_announcements(db, max_announcements)