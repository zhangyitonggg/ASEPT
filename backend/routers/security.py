from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import pymysql

from backend.utils import database, redis
from backend import conf
from backend.data.User import User

router = APIRouter(
    prefix='/security',
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")

@router.post("/token")
async def login(
    message: OAuth2PasswordRequestForm = Depends(),
    db: pymysql.connections.Connection = Depends(database.connect)
):
    user = database.varify_user(db, message.username, message.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = redis.create_token(
        data = {
            "sub": user.uid,
            "aud": message.username,
        },
        expire = conf.EXPIRE_TIME_MINUTES,
        key = conf.SECRET_KEY,
        algorithm = conf.ALGORITHM
    )
    redis.cache_user_permissions(user.uid, user.permissions)
    return {"access_token": token, "token_type": "bearer"}


async def get_user(
    token: str = Depends(oauth2_scheme),
    authorized_user_name: str = Query(min_length=1, max_length=256)
) -> User:
    user = redis.get_user(token, authorized_user_name)
    return user


async def get_admin(
    token: str = Depends(oauth2_scheme),
    authorized_user_name: str = Query(min_length=1, max_length=256)
) -> User:
    user = redis.get_admin(token, authorized_user_name)
    return user