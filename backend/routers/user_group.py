from fastapi import APIRouter, Depends, HTTPException, status
import pymysql

from backend.utils import database
from backend.data.User import Permissions, User
from backend.routers import security

router = APIRouter(
    prefix='/user_group',
)

@router.post("/join_group")
def join_group(
    group_name: str,
    user_name: str | None = None,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    '''
    NOTICE: params "user_name" is invalid. Maybe we will use it in the future.
    '''
    if user_name is None:
        user_name = user.name
    database.join_group(db, group_name, user.uid)
    return {"status": "success"}


@router.post("/leave_group")
async def leave_group(
    group_name: str,
    user_name: str | None = None,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    database.leave_group(db, group_name, user_name if user_name else user.name, user)
    return {"status": "success"}


@router.post("/create_group")
async def create_group(
    group_name: str,
    user: User = Depends(security.get_user),
    description: str | None = None,
    db: pymysql.connections.Connection = Depends(database.connect)
):
    database.create_group(db, group_name, user.uid, description)
    return {"status": "success"}


@router.post("/delete_group")
async def delete_group(
    group_name: str,
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    database.delete_group(db, group_name)
    return {"status": "success"}


@router.get("/show_groups")
async def show_groups(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    return database.show_groups(db, user.uid)


@router.get("/all_groups")
async def all_groups(
    user: User = Depends(security.get_user),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    return database.all_user_groups(db)