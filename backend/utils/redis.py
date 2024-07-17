import redis
import yaml
import jwt
import datetime
from fastapi import HTTPException

from backend import conf
from backend.data.User import Permissions, User
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


def delete_user_permissions_from_cache(uid: str):
    global REDIS
    REDIS.delete(f"user_permissions:{uid}")


def flush_all_cache():
    global REDIS
    REDIS.flushall()


def get_user(token: str, user_name: str) -> User:
    try:
        payload = jwt.decode(token, conf.SECRET_KEY, algorithms=[conf.ALGORITHM], audience=user_name)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired. Please login again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token. Please login again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Unknow error. Please login again."
        )
    try:
        uid: str = payload.get("sub")
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. We can't get your permissions as a user."
        )
    return User(user_name, uid, False, get_permission_from_cache(uid).to_list())


def get_permission_from_cache(uid: str) -> Permissions:
    global REDIS
    permissions = REDIS.get(f"user_permissions:{uid}")
    if permissions:
        return Permissions(permissions.decode().split(','))
    cache_user_permissions(uid, Permissions(database.get_user_permissions(uid)))
    permissions = REDIS.get(f"user_permissions:{uid}")
    if permissions:
        return Permissions(permissions.decode().split(','))
    raise HTTPException(
        status_code=401,
        detail="Permission denied. We can't get your permissions as a user."
    )


def get_admin(token: str, user_name: str) -> User:
    try:
        payload = jwt.decode(token, conf.SECRET_KEY, algorithms=[conf.ALGORITHM], audience=user_name)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired. Please login again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token. Please login again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Unknow error. Please login again."
        )
    try:
        uid: str = payload.get("sub")
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. We can't get your permissions as a user."
        )
    return User(user_name, uid, True, get_admin_permissions_from_cache(uid).to_list())


def get_admin_permissions_from_cache(uid: str) -> Permissions:
    global REDIS
    permissions = REDIS.get(f"user_permissions:{uid}")
    if permissions:
        return Permissions(permissions.decode().split(','))
    cache_user_permissions(uid, Permissions(database.get_admin_permissions(uid)))
    permissions = REDIS.get(f"user_permissions:{uid}")
    if permissions:
        return Permissions(permissions.decode().split(','))
    raise HTTPException(
        status_code=401,
        detail="Permission denied. We can't get your permissions as an admin."
    )