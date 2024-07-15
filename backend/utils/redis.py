import redis
import yaml
import jwt
import datetime

from backend import conf


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
        REDIS = redis.Redis(host=REDIS_ADDR, port=REDIS_PORT, password=REDIS_PASSWORD)
    except Exception as e:
        print("Error connecting to redis: ", e)


def create_token(data: dict, expire: int, key: str, algorithm: str):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expire)
    to_encode.update({"exp": expire, "iat": datetime.datetime.now(datetime.UTC)})
    token = jwt.encode(to_encode, key, algorithm=algorithm)
    return token


def get_user_permissions(db, user_id: int):
    cursor = db.cursor()
    cursor.execute("SELECT permission FROM Permissions WHERE uid=%s", (user_id,))
    permissions = cursor.fetchall()
    return [permission['permission'] for permission in permissions]


def cache_user_permissions(user_id: int, permissions: list):
    global REDIS
    REDIS.set(f"user_permissions:{user_id}", ','.join(permissions))


def get_user(token: str, user_name: str):
    payload = jwt.decode(token, conf.SECRET_KEY, algorithms=[conf.ALGORITHM], audience=user_name)
    username: str = payload.get("aud")
    if username is None:
        raise credentials_exception
    return username

def get_user_permissions_from_cache(user_id: int):
    global REDIS
    permissions = REDIS.get(f"user_permissions:{user_id}")
    if permissions:
        return permissions.decode('utf-8').split(',')
    return []

