from fastapi import APIRouter, Depends, HTTPException, status, Header
import pymysql
from pydantic import BaseModel

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
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    max_announcements: int 类型，最多获取的公告数量，默认为 3

    返回值：json 格式的公告列表。is_active 为表示公告是否有效。

    ```
    {
        "announcements": [
            {
                "aid": xxxx-xxxx,
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
    return database.get_announcements(db, max_announcements, False)


@router.get("/get_all_announcements")
async def get_announcements(
    max_announcements: int = 3,
    user: User = Depends(security.get_admin),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    max_announcements: int 类型，最多获取的公告数量，默认为 3

    返回值：json 格式的公告列表。is_active 为表示公告是否有效。

    ```
    {
        "announcements": [
            {
                "aid": xxxx-xxxx,
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
    return database.get_announcements(db, max_announcements, True)


@router.get("/current_time")
async def get_current_time(db: pymysql.connections.Connection = Depends(database.connect)):
    '''
    返回当前时间，格式为 "2021-01-01 00:00:00"
    '''
    return {
        "current_time": str(database.get_current_time(db)).replace('T', ' ')
    }


class Feedback(BaseModel):
    name: str
    email: str
    advice: str | None = None
    complaint: str | None = None


@router.post("/receive_feedback")
async def receive_feedback(
    feedback: Feedback,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    database.receive_feedback(db, user, feedback)
    return { "status": "success" }