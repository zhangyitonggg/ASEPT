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
    return database.get_announcements(db, max_announcements)