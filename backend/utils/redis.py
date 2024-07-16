import redis
import yaml
import jwt
import datetime
from fastapi import HTTPException

from backend import conf
from backend.data.User import Permissions
from backend.utils import database


REDIS_CONFIG_FILE = 'backend/redis.yml'
REDIS = None


def read_redis_config():
    global REDIS, REDIS_CONFIG_FILE
    with open(REDIS_CONFIG_FILE, 'r') as file:
        config = yaml.safe_load(file)
    try:
        db_env = config['environment']
        REDIS_ADDR = db_env['REDIS_ADDR']
        REDIS_PORT = db_env['REDIS_PORT']
        REDIS_PASSWORD = db_env['REDIS_PASSWORD']
    except Exception as e:
        print("Error reading database config: ", e)
        exit(1)
    try:
        REDIS = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, password=REDIS_PASSWORD)
    except Exception as e:
        print("Error connecting to redis: ", e)


def create_token(data: dict, expire: int, key: str, algorithm: str):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expire)
    to_encode.update({"exp": expire, "iat": datetime.datetime.now(datetime.UTC)})
    token = jwt.encode(to_encode, key, algorithm=algorithm)
    return token


def cache_user_permissions(uid: str, permissions: Permissions):
    global REDIS
    REDIS.set(
        f"user_permissions:{uid}",
        ','.join(permissions.to_list()),
        ex=conf.EXPIRE_TIME_MINUTES * 60,
        nx=True
    )


def get_user_permissions(token: str, user_name: str) -> Permissions:
    payload = jwt.decode(token, conf.SECRET_KEY, algorithms=[conf.ALGORITHM], audience=user_name)
    uid: str = payload.get("sub")
    return get_user_permissions_from_cache(uid)


def get_user_permissions_from_cache(uid: str):
    global REDIS
    permissions = REDIS.get(f"user_permissions:{uid}").decode()
    if permissions:
        return Permissions(uid, permissions.split(','))
    cache_user_permissions(uid, database.get_user_permissions(uid))
    permissions = REDIS.get(f"user_permissions:{uid}").decode()
    if permissions:
        return Permissions(uid, permissions.split(','))
    raise HTTPException(
        status_code=401,
        detail="Permission denied. We can't get your permissions as a user."
    )


def get_admin_permissions(token: str, user_name: str) -> Permissions:
    payload = jwt.decode(token, conf.SECRET_KEY, algorithms=[conf.ALGORITHM], audience=user_name)
    uid: str = payload.get("sub")
    return get_admin_permissions_from_cache(uid)


def get_admin_permissions_from_cache(uid: str):
    global REDIS
    permissions = REDIS.get(f"user_permissions:{uid}")
    if permissions:
        return Permissions(uid, permissions.decode().split(','))
    cache_user_permissions(uid, database.get_admin_permissions(uid))
    permissions = REDIS.get(f"user_permissions:{uid}")
    if permissions:
        return Permissions(uid, permissions.decode().split(','))
    raise HTTPException(
        status_code=401,
        detail="Permission denied. We can't get your permissions as an admin."
    )