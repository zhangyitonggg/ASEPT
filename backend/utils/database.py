import yaml
import pymysql
import hashlib
from fastapi import HTTPException, Depends, status

from backend.data.User import User, PermissionType

MYSQL_CONFIG_FILE = 'backend/db.yml'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = ''
MYSQL_USER = ''
MYSQL_ADDR = ''
MYSQL_PORT = ''

'''
Permissions:
+-----------------+----------------------+------+-----+---------+-------+
| Field           | Type                 | Null | Key | Default | Extra |
+-----------------+----------------------+------+-----+---------+-------+
| uid             | uuid                 | NO   | PRI | NULL    |       |
| is_admin        | enum('True','False') | NO   | MUL | False   |       |
| block_user      | enum('True','False') | NO   |     | False   |       |
| review_topic    | enum('True','False') | NO   |     | False   |       |
| manage_platform | enum('True','False') | NO   |     | False   |       |
| upload_file     | enum('True','False') | NO   |     | True    |       |
| upload_problem  | enum('True','False') | NO   |     | True    |       |
| share_problem   | enum('True','False') | NO   |     | True    |       |
| search_problem  | enum('True','False') | NO   |     | True    |       |
+-----------------+----------------------+------+-----+---------+-------+

UserGroupMembers:
+----------+----------------------+------+-----+---------+-------+
| Field    | Type                 | Null | Key | Default | Extra |
+----------+----------------------+------+-----+---------+-------+
| rid      | uuid                 | NO   | PRI | NULL    |       |
| uid      | uuid                 | NO   | MUL | NULL    |       |
| gid      | uuid                 | NO   | MUL | NULL    |       |
| is_admin | enum('True','False') | NO   |     | False   |       |
+----------+----------------------+------+-----+---------+-------+

UserGroups:
+-------------+--------------+------+-----+---------+-------+
| Field       | Type         | Null | Key | Default | Extra |
+-------------+--------------+------+-----+---------+-------+
| gid         | uuid         | NO   | PRI | NULL    |       |
| name        | varchar(255) | NO   |     | NULL    |       |
| description | varchar(255) | YES  |     | NULL    |       |
| owner       | uuid         | NO   |     | NULL    |       |
+-------------+--------------+------+-----+---------+-------+

Users:
+----------+----------------------+------+-----+---------+-------+
| Field    | Type                 | Null | Key | Default | Extra |
+----------+----------------------+------+-----+---------+-------+
| name     | varchar(255)         | NO   | PRI | NULL    |       |
| uid      | uuid                 | NO   | MUL | NULL    |       |
| password | varchar(255)         | NO   |     | NULL    |       |
| is_admin | enum('True','False') | NO   | MUL | False   |       |
| blocked  | bit(1)               | NO   |     | b'0'    |       |
+----------+----------------------+------+-----+---------+-------+
'''


def read_db_config():
    global MYSQL_CONFIG_FILE, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_USER, MYSQL_ADDR, MYSQL_PORT
    with open(MYSQL_CONFIG_FILE, 'r') as file:
        config = yaml.safe_load(file)
    try:
        db_env = config['environment']
        MYSQL_PASSWORD = db_env['MYSQL_PASSWORD']
        MYSQL_DATABASE = db_env['MYSQL_DATABASE']
        MYSQL_USER = db_env['MYSQL_USER']
        MYSQL_ADDR = db_env['MYSQL_ADDR']
        MYSQL_PORT = db_env['MYSQL_PORT']
    except Exception as e:
        print("Error reading database config: ", e)
        exit(1)


def connect():
    try:
        db = pymysql.connect(
            host=MYSQL_ADDR,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=int(MYSQL_PORT)
        )
        yield db
    finally:
        db.close()


def new_db():
    return pymysql.connect(
        host=MYSQL_ADDR,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=int(MYSQL_PORT)
    )


def get_user(db, username: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE name = %s", (username))
    return cursor.fetchone()


def varify_user(db, username: str, password: str) -> User:
    user = get_user(db, username)
    if user:
        if user[2] == md5_passwd(password) and user[4] == b'\x00':
            return User(username, user[1], user[3], get_user_permissions(user[1]))
    return None


def add_user(db, username: str, password: str):
    if get_user(db, username):
        return False
    cursor = db.cursor()
    cursor.execute("INSERT INTO Users (name, uid, password) VALUES (%s, UUID(), %s)", (username, password))
    db.commit()
    cursor.execute("SELECT uid FROM Users WHERE name = %s", (username))
    uid = cursor.fetchone()[0]
    cursor.execute("INSERT INTO Permissions (uid) VALUES (%s)", (uid))
    db.commit()
    return True


def md5_passwd(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def get_user_permissions(uid: str):
    db = new_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Permissions WHERE uid = %s", (uid))
    permissions = cursor.fetchone()[1::]
    db.close()
    return permissions


def get_admin_permissions(uid: str):
    db = new_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE uid = %s", (uid))
    user_status = cursor.fetchone()
    print(str(user_status[3] == True))
    if user_status[4] == b'\x01' or user_status[3] != True:
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    cursor.execute("SELECT * FROM Permissions WHERE uid = %s", (uid))
    permissions = cursor.fetchone()[1::]
    db.close()
    return permissions


def set_permission(db, target_user_name: str, permission: str):
    target_user = get_user(db, target_user_name)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User name not found.",
        )
    if PermissionType.is_permission(permission) == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission not found.",
        )
    cursor = db.cursor()
    cursor.execute("UPDATE Permissions SET %s = NOT %s WHERE uid = %s", (permission, permission, target_user[1]))
    db.commit()


def join_group(db, group_name: str, uid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroups WHERE name = %s", (group_name))
    group = cursor.fetchone()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    cursor.execute("SELECT * FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (group[0], uid))
    res = cursor.fetchone()
    if res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already in group.",
        )
    cursor.execute("INSERT INTO UserGroupMembers (rid, gid, uid, is_admin) VALUES (UUID(), %s, %s, 'False')", (group[0], uid))
    db.commit()


def leave_group(db, group_name: str, name: str):
    cursor = db.cursor()
    # get uid of name
    cursor.execute("SELECT * FROM Users WHERE name = %s", (name))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found.",
        )
    uid = user[1]
    # get target group
    cursor.execute("SELECT * FROM UserGroups WHERE name = %s", (group_name))
    group = cursor.fetchone()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    # check if user is in group
    cursor.execute("SELECT * FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (group[0], uid))
    res = cursor.fetchone()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not in group.",
        )
    cursor.execute("DELETE FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (group[0], uid))
    db.commit()


def create_group(db, group_name: str, uid: str, discription: str | None = None):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroups WHERE name = %s", (group_name))
    group = cursor.fetchone()
    if group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group already exists.",
        )
    cursor.execute("INSERT INTO UserGroups (gid, name, description, owner) VALUES (UUID(), %s, %s, %s)", (group_name, discription, uid))
    db.commit()
    cursor.execute("SELECT * FROM UserGroups WHERE name = %s", (group_name))
    group = cursor.fetchone()
    cursor.execute("INSERT INTO UserGroupMembers (rid, gid, uid, is_admin) VALUES (UUID(), %s, %s, 'True')", (group[0], uid))
    db.commit()


def show_groups(db, uid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroupMembers WHERE uid = %s", (uid))
    groups = cursor.fetchall()
    print("groups: ", groups)
    res = []
    for group in groups:
        cursor.execute("SELECT * FROM UserGroups WHERE gid = %s", (group[2]))
        group_info = cursor.fetchone()
        res.append({
            "name": group_info[1],
            "description": group_info[2],
            "owner": group_info[3],
            "is_admin": group[3]
        })
    return res