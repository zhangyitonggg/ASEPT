from fastapi import APIRouter, Query, Depends, HTTPException, status
import pymysql

from backend.utils import database

router = APIRouter(
    prefix='/create_user',
)

@router.post("/")
async def create_user(
    username: str = Query(min_length=1, max_length=256),
    password: str = Query(min_length=1, max_length=256),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    if database.add_user(db, username, database.md5_passwd(password)):
        return {"username": username}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user name already used",
        )