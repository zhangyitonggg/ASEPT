import yaml
import pymysql
import hashlib
from fastapi import HTTPException, Depends, status

from backend.data.User import User, PermissionType
from backend.data.Announcement import Announcement

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
| uid      | uuid                 | NO   | MUL | NULL    |       |
| gid      | uuid                 | NO   | MUL | NULL    |       |
| is_admin | enum('True','False') | NO   |     | False   |       |
+----------+----------------------+------+-----+---------+-------+

UserGroups:
+-------------+----------------------+------+-----+---------+-------+
| Field       | Type                 | Null | Key | Default | Extra |
+-------------+----------------------+------+-----+---------+-------+
| gid         | uuid                 | NO   | PRI | NULL    |       |
| name        | varchar(255)         | NO   |     | NULL    |       |
| description | varchar(255)         | YES  |     | NULL    |       |
| owner       | uuid                 | NO   |     | NULL    |       |
| is_open     | enum('True','False') | NO   |     | False   |       |
| password    | varchar(255)         | YES  |     | NULL    |       |
+-------------+----------------------+------+-----+---------+-------+

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

Announcements:
+-----------+--------------+------+-----+---------------------+-------------------------------+
| Field     | Type         | Null | Key | Default             | Extra                         |
+-----------+--------------+------+-----+---------------------+-------------------------------+
| aid       | uuid         | NO   | PRI | NULL                |                               |
| title     | varchar(255) | NO   |     | NULL                |                               |
| content   | text         | NO   |     | NULL                |                               |
| update_at | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
| is_active | tinyint(1)   | NO   |     | 1                   |                               |
| author    | uuid         | NO   |     | NULL                |                               |
+-----------+--------------+------+-----+---------------------+-------------------------------+
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


def get_group(db, group_name: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroups WHERE name = %s", (group_name))
    return cursor.fetchone()


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


def get_user_by_uid(db, uid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE uid = %s", (uid))
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
    permissions = cursor.fetchone()
    db.close()
    if permissions:
        permissions = permissions[1::]
    else:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    return permissions


def get_admin_permissions(uid: str):
    db = new_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE uid = %s", (uid))
    user_status = cursor.fetchone()
    print(user_status[3] == 'True')
    if user_status[4] == b'\x01' or user_status[3] != 'True':
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    cursor.execute("SELECT * FROM Permissions WHERE uid = %s", (uid))
    permissions = cursor.fetchone()[1::]
    db.close()
    return permissions


def set_permission(db, target_user_name: str, perm: str):
    target_user = get_user(db, target_user_name)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User name not found.",
        )
    target_uid = target_user[1]
    if PermissionType.is_permission(perm) == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission not found.",
        )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Permissions WHERE uid = %s", (target_uid))
    perms = cursor.fetchone()
    old_perm = perms[PermissionType[perm].value + 1]
    cmd = f"UPDATE Permissions SET {perm.lower()} = %s WHERE uid = %s"
    cursor.execute(cmd, ('True' if old_perm == 'False' else 'False', target_uid))
    db.commit()


def join_group(db, group_name: str, uid: str, password: str | None = None):
    group = get_group(db, group_name)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    if group[5] != "NULL" and group[5] != password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password incorrect.",
        )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (group[0], uid))
    res = cursor.fetchone()
    if res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already in group.",
        )
    cursor.execute("INSERT INTO UserGroupMembers (gid, uid) VALUES (%s, %s)", (group[0], uid))
    db.commit()


def leave_group(db, group_name: str, name: str, acter: User):
    if name == acter.name:
        uid = acter.uid
    else:
        user_left = get_user(db, name)
        if not user_left:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found.",
            )
        uid = user_left[1]
    group = get_group(db, group_name)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    if group[3] == uid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner cannot leave group.",
        )
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (group[0], uid))
        db.commit()
    except Exception as e:
        print("Error leaving group: ", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error leaving group.",
        )


def create_group(
    db, 
    group_name: str, 
    uid: str,
    discription: str | None = None, 
    password: str | None = None
):
    group = get_group(db, group_name)
    if group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group already exists.",
        )
    cursor = db.cursor()
    cursor.execute("INSERT INTO UserGroups (gid, name, description, owner, is_open, password) VALUES (UUID(), %s, %s, %s, 'False', %s)", (group_name, discription, uid, password if password else "NULL"))
    db.commit()
    cursor.execute("SELECT * FROM UserGroups WHERE name = %s", (group_name))
    group = cursor.fetchone()
    cursor.execute("INSERT INTO UserGroupMembers (gid, uid, is_admin) VALUES (%s, %s, 'True')", (group[0], uid))
    db.commit()


def delete_group(db, group_name: str, uid: str):
    group = get_group(db, group_name)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    if group[3] != uid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission denied. You are not the owner of this group.",
        )
    cursor = db.cursor()
    cursor.execute("DELETE FROM UserGroups WHERE name = %s", (group_name))
    cursor.execute("DELETE FROM UserGroupMembers WHERE gid = %s", (group[0]))
    db.commit()


def set_group_password(db, group_name: str, uid: str, password: str):
    group = get_group(db, group_name)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    if group[3] != uid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission denied. You are not the owner of this group.",
        )
    cursor = db.cursor()
    cursor.execute("UPDATE UserGroups SET password = %s WHERE name = %s", (password, group_name))
    db.commit()


def set_group_perm(db, group_name: str, user: User):
    group = get_group(db, group_name)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    gid = group[0]
    owner = group[3]
    if owner != user.uid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission denied. You are not the owner of this group.",
        )
    cursor = db.cursor()
    cur_state = group[4]
    cursor.execute("UPDATE UserGroups SET is_open = %s WHERE gid = %s", ('True' if cur_state == 'False' else 'False', gid))
    db.commit()


def find_open_groups(db, uid: str):
    # find groups with is_open = True and uid is not in the group
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroups WHERE is_open = 'True'")
    groups = cursor.fetchall()
    res = []
    for group in groups:
        cursor.execute("SELECT * FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (group[0], uid))
        if not cursor.fetchone():
            res.append({
                "name": group[1],
                "description": group[2] if group[2] else "This group has no description.",
                "owner": get_user_by_uid(db, group[3])[0],
            })
    return {"groups": res}


def show_groups(db, uid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroupMembers WHERE uid = %s", (uid))
    groups = cursor.fetchall()
    res = []
    for group in groups:
        cursor.execute("SELECT * FROM UserGroups WHERE gid = %s", (group[1]))
        group_info = cursor.fetchone()
        owner_uid = group_info[3]
        user = get_user_by_uid(db, owner_uid)
        user_name = "ThisAccountHasBeenDeleted" if not user else user[0]
        res.append({
            "name": group_info[1],
            "description": group_info[2] if group_info[2] else "This group has no description.",
            "owner": user_name,
            "is_admin": group[2]
        })
    return {"groups": res}


def set_admin(db, user_name):
    user = get_user(db, user_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found.",
        )
    cursor = db.cursor()
    cursor.execute("UPDATE Users SET is_admin = 'True' WHERE uid = %s", (user[1]))
    db.commit()
    cursor.execute("UPDATE Permissions SET is_admin = 'True', block_user = 'True', review_topic = 'True', manage_platform = 'True' WHERE uid = %s", (user[1]))
    db.commit()
    return user[1]


def open_announcement(db, announcement:Announcement, user: User):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Announcements (aid, title, content, author) VALUES (UUID(), %s, %s, %s)", (announcement.title, announcement.content, user.uid))
    db.commit()


def get_announcements(db, max_announcements: int):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Announcements ORDER BY update_at DESC LIMIT %s", (max_announcements))
    announcements = cursor.fetchall()
    res = []
    for announcement in announcements:
        res.append({
            "title": announcement[1],
            "content": announcement[2],
            "update_at": announcement[3],
            "is_active": announcement[4],
            "author": get_user_by_uid(db, announcement[5])[0],
        })
    return {"announcements": res}


def all_user_groups(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroups")
    groups = cursor.fetchall()
    res = []
    for group in groups:
        res.append({
            "name": group[1],
            "description": group[2] if group[2] else "This group has no description.",
            "owner": get_user_by_uid(db, group[3])[0],
        })
    return {"groups": res}