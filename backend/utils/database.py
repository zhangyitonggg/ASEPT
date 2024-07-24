import json
import random
import yaml
import pymysql
import hashlib
from fastapi import HTTPException, status
import uuid

from backend.data.User import User, PermissionType
from backend.data.Announcement import Announcement
from backend.data.Problem import *

MYSQL_CONFIG_FILE = 'backend/db.yml'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = ''
MYSQL_USER = ''
MYSQL_ADDR = ''
MYSQL_PORT = ''

'''
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT,
    COLUMN_KEY
FROM
    information_schema.COLUMNS
WHERE
    TABLE_SCHEMA = 'test'; -- 替换为你的数据库名

+-------------------------+-----------------+-----------+-------------+---------------------+------------+
| TABLE_NAME              | COLUMN_NAME     | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT      | COLUMN_KEY |
+-------------------------+-----------------+-----------+-------------+---------------------+------------+
| Users                   | name            | varchar   | NO          | NULL                | PRI        |
| Users                   | uid             | uuid      | NO          | NULL                | PRI        |
| Users                   | password        | varchar   | NO          | NULL                |            |
| Users                   | is_admin        | enum      | NO          | 'False'             | MUL        |
| Users                   | blocked         | bit       | NO          | b'0'                |            |
| Permissions             | uid             | uuid      | NO          | NULL                | PRI        |
| Permissions             | is_admin        | enum      | NO          | 'False'             | MUL        |
| Permissions             | block_user      | enum      | NO          | 'False'             |            |
| Permissions             | review_topic    | enum      | NO          | 'False'             |            |
| Permissions             | manage_platform | enum      | NO          | 'False'             |            |
| Permissions             | upload_file     | enum      | NO          | 'True'              |            |
| Permissions             | upload_problem  | enum      | NO          | 'True'              |            |
| Permissions             | share_problem   | enum      | NO          | 'True'              |            |
| Permissions             | search_problem  | enum      | NO          | 'True'              |            |
| ProblemGroupPerm        | pgid            | uuid      | NO          | NULL                | PRI        |
| ProblemGroupPerm        | gid             | uuid      | NO          | NULL                | PRI        |
| ProblemTags             | pid             | uuid      | NO          | NULL                | MUL        |
| ProblemTags             | tag             | varchar   | NO          | NULL                |            |
| ProblemSubmit           | sid             | uuid      | NO          | uuid()              | PRI        |
| ProblemSubmit           | pid             | uuid      | NO          | NULL                | MUL        |
| ProblemSubmit           | uid             | uuid      | NO          | NULL                | MUL        |
| ProblemSubmit           | answer          | text      | NO          | NULL                |            |
| ProblemSubmit           | is_correct      | tinyint   | NO          | 0                   |            |
| Announcements           | aid             | uuid      | NO          | NULL                | PRI        |
| Announcements           | title           | varchar   | NO          | NULL                |            |
| Announcements           | content         | text      | NO          | NULL                |            |
| Announcements           | update_at       | timestamp | NO          | current_timestamp() |            |
| Announcements           | is_active       | tinyint   | NO          | 1                   |            |
| Announcements           | author          | uuid      | NO          | NULL                |            |
| ProblemGroupMembers     | pgid            | uuid      | NO          | NULL                | PRI        |
| ProblemGroupMembers     | pid             | uuid      | NO          | NULL                | PRI        |
| ProblemGroups           | pgid            | uuid      | NO          | NULL                | PRI        |
| ProblemGroups           | name            | varchar   | NO          | NULL                |            |
| ProblemGroups           | description     | text      | YES         | NULL                |            |
| ProblemGroups           | owner           | uuid      | NO          | NULL                | MUL        |
| UserGroups              | gid             | uuid      | NO          | NULL                | PRI        |
| UserGroups              | name            | varchar   | NO          | NULL                | MUL        |
| UserGroups              | description     | varchar   | YES         | NULL                |            |
| UserGroups              | owner           | uuid      | NO          | NULL                |            |
| UserGroups              | is_open         | enum      | NO          | 'False'             |            |
| UserGroups              | password        | varchar   | YES         | NULL                |            |
| Problems                | pid             | uuid      | NO          | NULL                | PRI        |
| Problems                | title           | varchar   | NO          | NULL                |            |
| Problems                | content         | longtext  | NO          | NULL                |            |
| Problems                | type            | enum      | NO          | NULL                |            |
| Problems                | author          | uuid      | NO          | NULL                |            |
| Problems                | update_time     | timestamp | NO          | current_timestamp() |            |
| Problems                | choices         | longtext  | YES         | NULL                |            |
| Problems                | answers         | longtext  | YES         | NULL                |            |
| Problems                | is_public       | tinyint   | YES         | 0                   |            |
| UserGroupMembers        | uid             | uuid      | NO          | NULL                | MUL        |
| UserGroupMembers        | gid             | uuid      | NO          | NULL                | MUL        |
| UserGroupMembers        | is_admin        | enum      | NO          | 'False'             |            |
+-------------------------+-----------------+-----------+-------------+---------------------+------------+
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


def get_group_by_gid(db, gid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroups WHERE gid = %s", (gid))
    return cursor.fetchone()


def uid_in_group(db, uid: str, gid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroupMembers WHERE (uid, gid) = (%s, %s)", (uid, gid))
    return cursor.fetchone() != None


def get_problem_by_pid(db, pid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
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
    join_group(db, "af8f07f4-2029-4d5a-a6f3-378f2f152126", uid)
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


def set_permission(db, target_user_name: str, perm: PermissionType):
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


def join_group(db, gid: str, uid: str, password: str | None = None):
    group = get_group_by_gid(db, gid)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    if group[5] != None and group[5] != md5_passwd(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password incorrect.",
        )
    if uid_in_group(db, uid, group[0]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already in group.",
        )
    cursor = db.cursor()
    cursor.execute("INSERT INTO UserGroupMembers (gid, uid) VALUES (%s, %s)", (gid, uid))
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
    description: str | None = None,
    password: str | None = None
):
    gid = str(uuid.uuid4())
    cursor = db.cursor()
    cursor.execute("INSERT INTO UserGroups (gid, name, description, owner, is_open, password) VALUES (%s, %s, %s, %s, 'False', %s)",
                   (gid, group_name, description if description else None, uid, md5_passwd(password) if password else None))
    cursor.execute("INSERT INTO UserGroupMembers (gid, uid, is_admin) VALUES (%s, %s, 'True')", (gid, uid))
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
    if not password:
        password = "NULL"
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


def show_unentered_groups(db, uid: str, search_key: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroups WHERE owner != %s", (uid))
    groups = cursor.fetchall()
    res = []
    for group in groups:
        cursor.execute("SELECT * FROM UserGroupMembers WHERE gid = %s AND uid = %s", (group[0], uid))
        if cursor.fetchone() == None:
            res.append({
                "group_name": group[1],
                "founder": get_user_by_uid(db, group[3])[0],
                "need_password": group[5] != None,
                "gid": group[0],
                "description": group[2] if group[2] else "This group has no description."
            })
    return {"groups": res}


def show_created_groups(db, uid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroups WHERE owner = %s", (uid))
    groups = cursor.fetchall()
    res = []
    for group in groups:
        res.append({
            "group_name": group[1],
            "need_password": group[5] != None,
            "gid": group[0],
            "description": group[2] if group[2] else "This group has no description."
        })
    return {"groups": res}


def show_joined_groups(db, uid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroupMembers WHERE uid = %s", (uid))
    groups = cursor.fetchall()
    res = []
    for group in groups:
        group_info = get_group_by_gid(db, group[1])
        res.append({
            "group_name": group_info[1],
            "need_password": group_info[5] != None,
            "founder": get_user_by_uid(db, group_info[3])[0],
            "gid": group_info[0],
            "description": group_info[2] if group_info[2] else "This group has no description."
        })
    return {"groups": res}


def modify_group(db, uid: str, gid: str, group_name: str | None = None, password: str | None = None, description: str | None = None):
    group = get_group_by_gid(db, gid)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (group[0], uid))
    relation = cursor.fetchone()
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission denied. You are not in this group.",
        )
    if relation[2] != 'True':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission denied. You are not the admin of this group.",
        )
    if group_name != None:
        cursor.execute("UPDATE UserGroups SET name = %s WHERE gid = %s", (group_name, gid))
    if description != None:
        if description == "":
            cursor.execute("UPDATE UserGroups SET description = NULL WHERE gid = %s", (gid))
        else:
            cursor.execute("UPDATE UserGroups SET description = %s WHERE gid = %s", (description, gid))
    if password != None:
        print("password: ", password)
        if password == "":
            cursor.execute("UPDATE UserGroups SET password = NULL WHERE gid = %s", (gid))
        else:
            cursor.execute("UPDATE UserGroups SET password = %s WHERE gid = %s", (md5_passwd(password), gid))
    db.commit()


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


def modify_announcement(db, announcement:Announcement, user: User):
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE Announcements SET title = %s, content = %s, is_active = %s WHERE aid = %s", (announcement.title, announcement.content, 1 if announcement.is_active else 0 ,announcement.aid))
        db.commit()
    except Exception as e:
        print("Error modifying announcement: ", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error modifying announcement. Maybe the announcement does not exist.",
        )


def get_announcements(db, max_announcements: int):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Announcements ORDER BY update_at DESC LIMIT %s", (max_announcements))
    announcements = cursor.fetchall()
    res = []
    for announcement in announcements:
        res.append({
            "aid": announcement[0],
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


################################################
#                   Problems                   #
################################################


def add_problem(db, problem: Choice_Problem | Blank_Filling_Problem, user: User):
    pid = str(uuid.uuid4())
    cursor = db.cursor()
    cursor.execute("INSERT INTO Problems (pid, title, content, type, author, choices, answers) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (pid, problem.title, problem.content, problem.type.name, user.uid, None if isinstance(problem, Blank_Filling_Problem) else problem.choices, problem.answer))
    db.commit()
    return pid


def create_problem_group(db, group_name: str, description: str, owner: User):
    cursor = db.cursor()
    cursor.execute("INSERT INTO ProblemGroups (pgid, name, description, owner) VALUES (UUID(), %s, %s, %s)", (group_name, description, owner.uid))
    db.commit()
    
    
def get_problem_group_info(db, pgid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemGroups WHERE pgid = %s", (pgid))
    group = cursor.fetchone()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found."
        )
    return {
        "pgid": group[0],
        "name": group[1],
        "description": group[2],
        "owner": get_user_by_uid(db, group[3])[0],
    }


def get_problem_group_problems(db, pgid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemGroupMembers WHERE pgid = %s", (pgid))
    problems = cursor.fetchall()
    res = []
    for problem in problems:
        cursor.execute("SELECT * FROM Problems WHERE pid = %s", (problem[1]))
        problem_info = cursor.fetchone()
        res.append({
            "pid": problem_info[0],
            "title": problem_info[1],
            "content": problem_info[2],
            "type": problem_info[3],
            "author": get_user_by_uid(db, problem_info[4])[0],
            "update_time": problem_info[5],
            "choices": problem_info[6],
            "answers": problem_info[7],
            "is_public": problem_info[8],
        })
    return {"problems": res}


def change_problem_group_info(db, pgid: str, group_name: str, description: str, owner: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemGroups WHERE pgid = %s", (pgid))
    group = cursor.fetchone()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found."
        )
    if group[3] != owner.uid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. You are not the owner of this group."
        )
    cursor.execute("UPDATE ProblemGroups SET name = %s, description = %s WHERE pgid = %s", (group_name, description, pgid))
    db.commit()


def add_problem_to_group(db, pid: str, pgid: str, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemGroups WHERE pgid = %s", (pgid))
    group = cursor.fetchone()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found."
        )
    if group[3] != user.uid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. You are not the owner of this group."
        )
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    cursor.execute("SELECT * FROM ProblemGroupMembers WHERE (pgid, pid) = (%s, %s)", (pgid, pid))
    if cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Problem already in the group."
        )
    cursor.execute("INSERT INTO ProblemGroupMembers (pgid, pid) VALUES (%s, %s)", (pgid, pid))
    db.commit()


def share_problem_group_to_user_group(db, pgid: str, gid: str, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemGroups WHERE pgid = %s", (pgid))
    group = cursor.fetchone()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found."
        )
    if group[3] != user.uid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. You are not the owner of this group."
        )
    cursor.execute("SELECT * FROM UserGroups WHERE gid = %s", (gid))
    user_group = cursor.fetchone()
    if not user_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User group not found."
        )
    cursor.execute("SELECT * FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (gid, user.uid))
    if not cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission denied. User not in the group."
        )
    cursor.execute("SELECT * FROM ProblemGroupAccessibleGroups WHERE (pgid, gid) = (%s, %s)", (pgid, gid))
    if cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User group already has access to the problem group."
        )
    cursor.execute("INSERT INTO ProblemGroupAccessibleGroups (pgid, gid) VALUES (%s, %s)", (pgid, gid))
    db.commit()


def add_problem_tag(db, pid: str, tag: str, user: User):
    # check if user is the author of the problem
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    if problem[4] != user.uid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )
    # check if problem already has the tag
    cursor.execute("SELECT * FROM ProblemTags WHERE (pid, tag) = (%s, %s)", (pid, tag))
    if cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already exists."
        )
    cursor.execute("INSERT INTO ProblemTags (pid, tag) VALUES (%s, %s)", (pid, tag))
    db.commit()

def get_all_accessible_problems(db, user: User):
    # get problems that user has access to
    # get the problems owned by the user
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE author = %s", (user.uid))
    all_pids = cursor.fetchall()
    all_pids = [pid[0] for pid in all_pids]
    # get all the groups that the user is in
    cursor.execute("SELECT * FROM UserGroupMembers WHERE uid = %s", (user.uid))
    groups = cursor.fetchall()
    # for each group, get problems the group has access to
    # get all the pgids
    all_pgids = []
    for group in groups:
        cursor.execute("SELECT * FROM ProblemGroupPerm WHERE gid = %s", (group[1]))
        pgids = cursor.fetchall()
        all_pgids.extend(pgids)
    all_pgids = list(set(all_pgids))
    # get all the pids
    for pgid in all_pgids:
        cursor.execute("SELECT * FROM ProblemGroupMembers WHERE pgid = %s", (pgid))
        pids = cursor.fetchall()
        all_pids.extend(pids)
    all_pids = list(set(all_pids))
    # get all the problems that the user has access to
    problems_with_access = []
    for pid in all_pids:
        cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
        problem = cursor.fetchone()
        problems_with_access.append(problem)
    return problems_with_access
    

def search_problem_by_tag(db, tag: str, user: User):
    problems_with_access = get_all_accessible_problems(db, user)
    # get problems whose tag contains the input tag
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemTags")
    problems = cursor.fetchall()
    problems = [problem for problem in problems if tag in problem[1]]
    # union the two lists
    final_problems = list(set(problems) & set(problems_with_access))
    # return the final list
    res = []
    for problem in final_problems:
        res.append({
            "pid": problem[0],
            "title": problem[1],
            "content": problem[2],
            "type": problem[3],
            "author": get_user_by_uid(db, problem[4])[0],
            "update_time": problem[5],
            "choices": problem[6],
            "answers": problem[7],
            "is_public": problem[8],
        })
    return {"problems": res}

def get_my_problems(db, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE author = %s", (user.uid))
    problems = cursor.fetchall()
    res = []
    for problem in problems:
        res.append(Problem(
            pid=problem[0],
            title=problem[1],
            content=problem[2],
            type=ProblemType[problem[3].upper()],
            author=problem[4],
            update_time=str(problem[5]),
            choices=problem[6],
            answers=problem[7],
            is_public=bool(problem[8])
        ))
    return {"problems": res}

def submit_problem(db, pid: str, answer: str, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    cursor.execute("SELECT * FROM ProblemGroupMembers WHERE pid = %s", (pid))
    pgroups = cursor.fetchall()
    groups_with_access = []
    for pgroup in pgroups:
        cursor.execute("SELECT * FROM ProblemGroupPerm WHERE pgid = %s", (pgroup[1]))
        groups_with_access.append(cursor.fetchall())
    groups_with_access = set([group[1] for group in groups_with_access])
    cursor.execute("SELECT * FROM UserGroupMembers WHERE uid = %s", (user.uid))
    groups_user_in = cursor.fetchall()
    groups_user_in = set([group[1] for group in groups_user_in])
    if not groups_user_in & groups_with_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )
    def judge_problem(type: str, answer: str, user_answer: str):
        ans = json.loads(answer)
        usr = json.loads(user_answer)
        return ans == usr
    is_correct = judge_problem(problem[3], problem[7], answer)
    cursor.execute("INSERT INTO ProblemSubmit (sid, pid, uid, answer, is_correct) VALUES (UUID(), %s, %s, %s, %s)", (pid, user.uid, answer, is_correct))
    db.commit()
    return is_correct

def get_user_statistics(db, user: User):
    '''
    获取用户题目统计信息。
    
    返回格式：
    
    ```
    {
        "choice_submit": 100,
        "choice_correct": 80,
        "blank_submit": 50,
        "blank_correct": 40,
    }
    ```
    '''
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemSubmit WHERE uid = %s", (user.uid))
    submits = cursor.fetchall()
    def get_problem_type(pid):
        cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
        problem = cursor.fetchone()
        return problem[3]
    choice_submit = 0
    choice_correct = 0
    blank_submit = 0
    blank_correct = 0
    for submit in submits:
        if get_problem_type(submit[2]) == "CHOICE":
            choice_submit += 1
            if submit[5]:
                choice_correct += 1
        else:
            blank_submit += 1
            if submit[5]:
                blank_correct += 1
    return {
        "choice_submit": choice_submit,
        "choice_correct": choice_correct,
        "blank_submit": blank_submit,
        "blank_correct": blank_correct,
    }
    

def get_problem_recommend(db, user: User):
    '''
    获取题目推荐。
    
    返回格式：
    
    ```
    {
        "problems": [
            {
                "pid": 1,
                "title": "Problem Title",
                "content": "Problem Content",
                "type": 0,
                “author”: "Author Name",
                "upload_time": "2021-10-01 12:00:00",
                "choices": {
                    "A": "Choice A",
                    "B": "Choice B",
                    "C": "Choice C",
                    "D": "Choice D"
                },
                "answers": {
                    "A": "Choice A",
                    "B": "Choice B"
                },
                "is_public": 0
            },
            {
                "pid": 2,
                "title": "Problem Title",
                "content": "Problem Content",
                "type": 1,
                “author”: "Author Name",
                "upload_time": "2021-10-01 12:00:00",
                "choices": {
                    "A": "Choice A",
                    "B": "Choice B",
                    "C": "Choice C",
                    "D": "Choice D"
                },
                "answers": {
                    "B": "Choice B"
                },
                "is_public": 1
            }
        ]
    }
    '''
    # take 20 problem with max wrong rate and choose rondom 10 problem within them
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems")
    problems = cursor.fetchall()
    res = []
    for problem in problems:
        cursor.execute("SELECT * FROM ProblemSubmit WHERE pid = %s", (problem[0]))
        submits = cursor.fetchall()
        correct = 0
        for submit in submits:
            if submit[5]:
                correct += 1
        res.append((problem[0], correct / len(submits)))
    res = sorted(res, key=lambda x: x[1])
    res = res[:20]
    res = random.sample(res, 10)
    res = res[:10]
    final_res = []
    for problem in res:
        cursor.execute("SELECT * FROM Problems WHERE pid = %s", (problem[0]))
        problem = cursor.fetchone()
        final_res.append({
            "pid": problem[0],
            "title": problem[1],
            "content": problem[2],
            "type": problem[3],
            "author": get_user_by_uid(db, problem[4])[0],
            "upload_time": problem[5],
            "choices": problem[6],
            "answers": problem[7],
            "is_public": problem[8],
        })
    return {"problems": final_res}
    

def problem_accessible(db, user: User, pid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if problem == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    if user.permissions.get("REVIEW_TOPIC"):
        return True
    if problem[4] == user.uid:
        return True
    if problem[8] == 0:
        return False
    cursor.execute("SELECT * FROM ProblemAccessibleGroups WHERE pid = %s", (pid))
    groups = cursor.fetchall()
    for group in groups:
        gid = group[1]
        if uid_in_group(db, user.uid, gid):
            return True
    return False


def get_problem(db, pid: str, user: User):
    '''
    根据pid获取题目信息。
    
    返回格式：
    
    ```
    {
        "pid": 1,
        "title": "Problem Title",
        "content": "Problem Content",
        "type": 0,
        “author”: "Author Name",
        "upload_time": "2021-10-01 12:00:00",
        "choices": {
            "A": "Choice A",
            "B": "Choice B",
            "C": "Choice C",
            "D": "Choice D"
        },
        "answers": {
            "A": "Choice A",
            "B": "Choice B"
        },
        "is_public": 0
    }
    '''
    # check user's permission and then return problem or raise error
    problems_with_access = get_all_accessible_problems(db, user)
    problems_with_access = [problem[0] for problem in problems_with_access]
    if pid not in problems_with_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    return {
        "pid": problem[0],
        "title": problem[1],
        "content": problem[2],
        "type": problem[3],
        "author": get_user_by_uid(db, problem[4])[0],
        "upload_time": problem[5],
        "choices": problem[6],
        "answers": problem[7],
        "is_public": problem[8],
    }
    
    # cursor = db.cursor()
    # cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    # problem = cursor.fetchone()
    # if problem == None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Problem not found."
    #     )
    # problem = Problem(
    #     pid=problem[0],
    #     title=problem[1],
    #     content=problem[2],
    #     type=ProblemType[problem[3].upper()],
    #     author=problem[4],
    #     update_time=str(problem[5]),
    #     choices=problem[6],
    #     answers=problem[7],
    #     is_public=bool(problem[8])
    # )
    # return problem