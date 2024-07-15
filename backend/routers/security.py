from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import pymysql

from backend.utils import database, redis
from backend import conf

router = APIRouter(
    prefix='/security',
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")

@router.post("/token")
async def login(message: OAuth2PasswordRequestForm = Depends(), db: pymysql.connections.Connection = Depends(database.connect)):
    user = database.varify_user(db, message.username, message.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = redis.create_token(
        data = {"sub":message.scopes, "aud": message.username},
        expire = conf.EXPIRE_TIME_MINUTES,
        key = conf.SECRET_KEY,
        algorithm = conf.ALGORITHM
    )
    # uid = user["id"]
    # permissions = redis.get_user_permissions(db, uid)
    # redis.cache_user_permissions(uid, permissions)
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), user_name: str = Query(min_length=1, max_length=256)):
    user = redis.get_user(token, user_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user