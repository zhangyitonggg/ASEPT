import json
from pathlib import Path

import backend.utils.database as database
import backend.utils.redis as redis

CONF_FILE = "backend/conf.json"
UPLOAD_DIRECTORY = "uploads"
SECRET_KEY = ""
ALGORITHM = ""
EXPIRE_TIME_MINUTES = 998244353
MAX_FILE_SIZE = 5 * 1024 * 1024
ADMIN_KEY = "_"

def init():
    global UPLOAD_DIRECTORY, SECRET_KEY, ALGORITHM, EXPIRE_TIME_MINUTES, MAX_FILE_SIZE, ADMIN_KEY
    database.read_db_config()
    redis.read_redis_config()
    with open(CONF_FILE, "r") as f:
        conf = json.load(f)
    UPLOAD_DIRECTORY = Path(conf["UPLOAD_DIRECTORY"])
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    SECRET_KEY = conf["SECRET_KEY"]
    ALGORITHM = conf["ALGORITHM"]
    EXPIRE_TIME_MINUTES = conf["EXPIRE_TIME_MINUTES"]
    ADMIN_KEY = conf["ADMIN_KEY"]