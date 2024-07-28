import json
import random
import yaml
import pymysql
import hashlib
from fastapi import HTTPException, status
import uuid
from fuzzywuzzy import process

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
        if user[2] == md5_passwd(password):
            return User(username, user[1], user[3], get_user_permissions(user[1]))
    return None


def add_user(db, username: str, password: str):
    if get_user(db, username):
        return False
    cursor = db.cursor()
    uid = str(uuid.uuid4())
    cursor.execute("INSERT INTO Users (name, uid, password) VALUES (%s, %s, %s)", (username, uid, password))
    cursor.execute("INSERT INTO Permissions (uid) VALUES (%s)", (uid))
    db.commit()
    join_group(db, "af8f07f4-2029-4d5a-a6f3-378f2f152126", uid)
    return True


def get_tag_by_tid(db, tid: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Tags WHERE tid = %s", (tid))
    return cursor.fetchone()


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
    if user_status[3] != 'True':
        raise HTTPException(
            status_code=401,
            detail="Permission denied. You are not an admin."
        )
    cursor.execute("SELECT * FROM Permissions WHERE uid = %s", (uid))
    permissions = cursor.fetchone()[1::]
    db.close()
    return permissions


def set_permission(db, target_user_name: str, perm: PermissionType, cancel: bool):
    target_user = get_user(db, target_user_name)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User name not found.",
        )
    target_uid = target_user[1]
    cursor = db.cursor()
    cmd = f"UPDATE Permissions SET {perm.name.lower()} = %s WHERE uid = %s"
    cursor.execute(cmd, (str(not cancel), target_uid))
    if perm.name == "IS_ADMIN":
        cursor.execute("UPDATE Users SET is_admin = %s WHERE uid = %s", (str(not cancel), target_uid))
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


def leave_group(db, gid: str, user: User):
    group = get_group_by_gid(db, gid)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found.",
        )
    if group[3] == user.uid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner cannot leave group.",
        )
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (group[0], user.uid))
        db.commit()
    except Exception as e:
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


def delete_group(db, gid: str, user: User):
    group = get_group_by_gid(db, gid)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    if group[3] != user.uid and user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission denied. You are not the owner of this group.",
        )
    cursor = db.cursor()
    cursor.execute("DELETE FROM UserGroups WHERE gid = %s", (gid))
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
            founder = get_user_by_uid(db, group[3])
            if founder:
                founder = founder[0]
            else:
                founder = "Unknown"
            res.append({
                "group_name": group[1],
                "founder": founder,
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


def modify_group(db, user: User, gid: str, group_name: str | None = None, password: str | None = None, description: str | None = None):
    group = get_group_by_gid(db, gid)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found.",
        )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (group[0], user.uid))
    relation = cursor.fetchone()
    if user.permissions.get("IS_ADMIN") == False:
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
    cursor.execute("UPDATE Announcements SET title = %s, content = %s, is_active = %s WHERE aid = %s", (announcement.title, announcement.content, 1 if announcement.is_active else 0 ,announcement.aid))
    db.commit()

def get_all_users(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    res = []
    for user in users:
        res.append({
            "name": user[0],
            "uid": user[1],
            "is_admin": user[3],
            "blocked": get_user_permissions(user[1])[8],
        })
    return {"users": res}

def admin_get_all_problems(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems")
    problems = cursor.fetchall()
    res = []
    for problem in problems:
        res.append({
            "pid": problem[0],
            "title": problem[1],
            "content": problem[2],
            "type": problem[3],
            "author": problem[4],
            "update_time": problem[5],
            "choices": problem[6],
            "answers": problem[7],
            "is_public": problem[8],
        })
    return {"problems": res}

def get_all_groups(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroups")
    groups = cursor.fetchall()
    res = []
    for group in groups:
        res.append({
            "gid": group[0],
            "group_name": group[1],
            "description": group[2],
            "owner": get_user_by_uid(db, group[3])[0],
            "is_open": group[4],
            "password": group[5],
        })
    return {"groups": res}

def get_all_problem_groups(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemGroups")
    groups = cursor.fetchall()
    res = []
    for group in groups:
        res.append({
            "pgid": group[0],
            "name": group[1],
            "description": group[2],
            "owner": group[3],
        })
    return {"problem_groups": res}

def delete_admin(db, uid):
    cursor = db.cursor()
    cursor.execute("UPDATE Users SET is_admin = 'False' WHERE uid = %s", (uid))
    db.commit()

def get_all_admin(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE is_admin = 'True'")
    admins = cursor.fetchall()
    res = []
    for admin in admins:
        res.append({
            "name": admin[0],
            "uid": admin[1],
        })
    return {"admins": res}

def get_announcements(db, max_announcements: int, panel: int):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Announcements ORDER BY update_at DESC LIMIT %s", (max_announcements))
    announcements = cursor.fetchall()
    res = []
    for announcement in announcements:
        if announcement[4] | panel:
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

def modify_problem(db, pid: str, problem: Choice_Problem | Blank_Filling_Problem, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem_info = cursor.fetchone()
    if not problem_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    if problem_info[4] != user.uid and user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )
    cursor.execute("UPDATE Problems SET title = %s, content = %s, type = %s, choices = %s, answers = %s WHERE pid = %s",
                     (problem.title, problem.content, problem.type.name, None if isinstance(problem, Blank_Filling_Problem) else problem.choices, problem.answer, pid))
    db.commit()
    return pid

def create_problem_group(db, group_name: str, description: str, owner: User):
    cursor = db.cursor()
    cursor.execute("INSERT INTO ProblemGroups (pgid, name, description, owner) VALUES (UUID(), %s, %s, %s)", (group_name, description, owner.uid))
    db.commit()

def get_pgids_user_can_access(db, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM UserGroupMembers WHERE uid = %s", (user.uid))
    groups = cursor.fetchall()
    gids = [group[1] for group in groups]
    all_pgids = []
    for gid in gids:
        cursor.execute("SELECT * FROM ProblemGroupPerm WHERE gid = %s", (gid))
        pgids = cursor.fetchall()
        pgids = [pgid[0] for pgid in pgids]
        all_pgids.extend(pgids)

    cursor.execute("SELECT * FROM ProblemGroups WHERE owner = %s", (user.uid))
    groups = cursor.fetchall()
    pgids = [group[0] for group in groups]
    all_pgids.extend(pgids)
    return list(set(all_pgids))

def get_all_accessible_problems(db, user: User):
    cursor = db.cursor()
    all_pgids = get_pgids_user_can_access(db, user)
    cursor.execute("SELECT * FROM Problems WHERE author = %s", (user.uid))
    all_pids = cursor.fetchall()
    all_pids = [pid[0] for pid in all_pids]
    for pgid in all_pgids:
        cursor.execute("SELECT * FROM ProblemGroupMembers WHERE pgid = %s", (pgid))
        pids = cursor.fetchall()
        pids = [pid[1] for pid in pids]
        all_pids.extend(pids)
    all_pids = list(set(all_pids))
    problems_with_access = []
    for pid in all_pids:
        cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
        problem = cursor.fetchone()
        problems_with_access.append(problem)
    return problems_with_access

def get_problem_groups(db, user: User):
    '''
    获取用户有权限访问的题目组。
    
    返回格式：
    
    ```json
    {
        "problem_groups": [
            {
                "pgid": "1",
                "name": "Problem Group Name",
                "description": "Problem Group Description",
                "owner": "Creator Name",
            },
            {
                "pgid": "2",
                "name": "Problem Group Name",
                "description": "Problem Group Description",
                "owner": "Creator Name",
            }
        ]
    }
    ```
    '''
    all_pgids = get_pgids_user_can_access(db, user)
    cursor = db.cursor()
    res = []
    for pgid in all_pgids:
        cursor.execute("SELECT * FROM ProblemGroups WHERE pgid = %s", (pgid))
        group = cursor.fetchone()
        res.append({
            "pgid": group[0],
            "name": group[1],
            "description": group[2],
            "owner": group[3],
        })
    return {"problem_groups": res}
    
def get_problem_group_info(db, pgid: str, user: User):
    all_pgids = get_pgids_user_can_access(db, user)
    if pgid not in all_pgids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. You do not have access to this group."
        )
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
        "owner": group[3],
    }


def get_problem_group_problems(db, pgid: str, user: User):
    all_pgids = get_pgids_user_can_access(db, user)
    if pgid not in all_pgids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. You do not have access to this group."
        )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemGroupMembers WHERE pgid = %s", (pgid))
    problems = cursor.fetchall()
    res = []
    for problem in problems:
        cursor.execute("SELECT * FROM Problems WHERE pid = %s", (problem[1]))
        problem_info = cursor.fetchone()
        cursor.execute("SELECT * FROM ProblemTags WHERE pid = %s", (problem[0]))
        tags = cursor.fetchall()
        _tags_ = []
        for tag in tags:
            _tags_.append(get_tag_by_tid(db, tag[1])[1])
        res.append({
            "pid": problem_info[0],
            "title": problem_info[1],
            "content": problem_info[2],
            "type": problem_info[3],
            "author": problem_info[4],
            "update_time": problem_info[5],
            "choices": problem_info[6],
            "answers": problem_info[7],
            "is_public": problem_info[8],
            "tags": _tags_,
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
    if group[3] != owner.uid and owner.permissions.get("IS_ADMIN") == False:
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
    if group[3] != user.uid and user.permissions.get("IS_ADMIN") == False:
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
            detail="Problem Group not found."
        )
    cursor.execute("SELECT * FROM UserGroups WHERE gid = %s", (gid))
    user_group = cursor.fetchone()
    if not user_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User group not found."
        )
    cursor.execute("SELECT * FROM UserGroupMembers WHERE (gid, uid) = (%s, %s)", (gid, user.uid))
    if (not cursor.fetchone()) and user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission denied. User not in the user group."
        )
    cursor.execute("SELECT * FROM ProblemGroupPerm WHERE (pgid, gid) = (%s, %s)", (pgid, gid))
    if cursor.fetchone():
        return
    cursor.execute("INSERT INTO ProblemGroupPerm (pgid, gid) VALUES (%s, %s)", (pgid, gid))
    db.commit()


def add_tag_to_problem(db, pid: str, tag_name: str, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    if problem[4] != user.uid and user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )
    cursor.execute("SELECT * FROM Tags WHERE (tag_name) = (%s)", (tag_name))
    tag = cursor.fetchone()
    if not tag:
        tid = str(uuid.uuid4())
        cursor.execute("INSERT INTO Tags (tid, tag_name) VALUES (%s, %s)", (tid, tag_name))
        db.commit()
    else:
        tid = tag[0]
        cursor.execute("SELECT * FROM ProblemTags WHERE (pid, tid) = (%s, %s)", (pid, tid))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag already exists."
            )
    cursor.execute("INSERT INTO ProblemTags (pid, tid) VALUES (%s, %s)", (pid, tid))
    db.commit()


def remove_tag_from_problem(db, pid: str, tid: str, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    if problem[4] != user.uid and user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )
    cursor.execute("SELECT * FROM ProblemTags WHERE (pid, tid) = (%s, %s)", (pid, tid))
    tag = cursor.fetchone()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found in this problem."
        )
    cursor.execute("DELETE FROM ProblemTags WHERE (pid, tid) = (%s, %s)", (pid, tid))
    db.commit()


def get_all_problems(db, user: User):
    problems_with_access = get_all_accessible_problems(db, user)
    res = []
    for problem in problems_with_access:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM ProblemTags WHERE pid = %s", (problem[0]))
        tags = cursor.fetchall()
        _tags_ = []
        for tag in tags:
            _tags_.append(get_tag_by_tid(db, tag[1])[1])
        res.append({
            "pid": problem[0],
            "title": problem[1],
            "content": problem[2],
            "type": problem[3],
            "author": problem[4],
            "update_time": problem[5],
            "choices": problem[6],
            "answers": problem[7],
            "is_public": problem[8],
            "tags": _tags_,
        })
    return {"problems": res}

def get_problem_tags(db, pid: str, user: User):
    problems_with_access = get_all_accessible_problems(db, user)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    if problem not in problems_with_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )
    cursor.execute("SELECT * FROM ProblemTags WHERE pid = %s", (pid))
    tags = cursor.fetchall()
    tids = []
    for tag in tags:
        tids.append(tag[1])
    res = []
    for tid in tids:
        cursor.execute("SELECT * FROM Tags WHERE tid = %s", (tid))
        tag = cursor.fetchone()
        res.append({
            "tid": tag[0],
            "tag_name": tag[1],
        })
    return {"tags": res}

def search_problem_by_tag(db, tid, key, user: User):
    problems_with_access = get_all_accessible_problems(db, user)
    if tid:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM ProblemTags")
        problem_tags = cursor.fetchall()
        problem_tags = [problem for problem in problem_tags if tid in problem[1]]
        pids = [problem[0] for problem in problem_tags]
        problems = []
        for pid in pids:
            cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
            problem = cursor.fetchone()
            if problem in problems_with_access:
                problems.append(problem)
    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Problems")
        all_problems = cursor.fetchall()
        problems = []
        for problem in all_problems:
            if problem in problems_with_access:
                problems.append(problem)
    if key:
        problems = fuzzy_match(problems, key)
    res = []
    for problem in problems:
        res.append({
            "pid": problem[0],
            "title": problem[1],
            "content": problem[2],
            "type": problem[3],
            "author": problem[4],
            "update_time": problem[5],
            "choices": problem[6],
            "answers": problem[7],
            "is_public": problem[8],
        })
    return {"problems": res}


def get_all_tags(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Tags")
    tags = cursor.fetchall()
    res = []
    for tag in tags:
        res.append({
            "tid": tag[0],
            "tag_name": tag[1],
        })
    return {"tags": res}

def get_my_problems(db, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE author = %s", (user.uid))
    problems = cursor.fetchall()
    res = []
    for problem in problems:
        cursor.execute("SELECT * FROM ProblemTags WHERE pid = %s", (problem[0]))
        tags = cursor.fetchall()
        _tags_ = []
        for tag in tags:
            _tags_.append(get_tag_by_tid(db, tag[1])[1])
        if problem[3] == "choice":
            if len(json.loads(problem[7])) > 1:
                ptype = "MULTI_CHOICE"
            else:
                ptype = "SINGLE_CHOICE"
        else:
            ptype = "BLANK_FILLING"
        res.append({
            "pid": problem[0],
            "title": problem[1],
            "content": problem[2],
            "type": ptype,
            "author": problem[4],
            "update_time": problem[5],
            "choices": problem[6],
            "answers": problem[7],
            "is_public": problem[8],
            "tags": _tags_,
        })
    return {"problems": res}

def submit_problem(db, pid: str, answer: str, user: User):
    if len(answer) > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Answer too long"
        )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    problems_with_access = get_all_accessible_problems(db, user)
    if problem not in problems_with_access:
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

def get_user_statistics(db, user):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemSubmit WHERE uid = %s", (user.uid))
    submits = cursor.fetchall()
    def get_problem_type(pid):
        cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid,))
        return cursor.fetchone()[3]
    problem_pass_counts = {}
    choice_submit = 0
    choice_correct = 0
    blank_submit = 0
    blank_correct = 0
    last_submit_time = None
    for submit in submits:
        pid = submit[1]
        correct = submit[4]
        last_submit_time = submit[5]
        problem_type = get_problem_type(pid)
        if "choice" in problem_type:
            choice_submit += 1
            if correct:
                choice_correct += 1
        else:
            blank_submit += 1
            if correct:
                blank_correct += 1
        if correct and pid not in problem_pass_counts:
            problem_pass_counts[pid] = last_submit_time
    total_passes = len(problem_pass_counts)
    # # Calculate passes over regular intervals
    start_time = min(submits, key=lambda x: x[5])[5] if submits else None
    end_time = max(submits, key=lambda x: x[5])[5] if submits else None
    interval_count = {}
    label = {}
    if start_time and end_time:
        interval_duration = (end_time - start_time) / 7  # For example, 5 intervals
        for i in range(8):
            current_time = start_time + i * interval_duration
            label[i] = str(current_time).replace('T', ' ')
            interval_count[label[i]] = sum(1 for submit in submits if submit[4] and submit[5] <= current_time)

    return {
        "choice_submit": choice_submit,
        "choice_correct": choice_correct,
        "blank_submit": blank_submit,
        "blank_correct": blank_correct,
        "total_passes": total_passes,
        "last_submit_time": str(last_submit_time).replace('T', ' ') if last_submit_time else None,
        "labels": [label[i][0:19] for i in range(8)],
        "values": [interval_count[label[i]] for i in range(8)]
    }


def get_problem_recommend(db, user: User):
    problems = get_all_accessible_problems(db, user)
    cursor = db.cursor()
    res = []
    for problem in problems:
        cursor.execute("SELECT * FROM ProblemSubmit WHERE pid = %s", (problem[0]))
        submits = cursor.fetchall()
        correct = 0
        mysubmit = 0
        mycorrect = 0
        for submit in submits:
            if submit[4]:
                correct += 1
            if submit[2] == user.uid:
                mysubmit += 1
                if submit[4]:
                    mycorrect += 1
        res.append((problem[0], len(submits), correct, mysubmit, mycorrect))
    def get_correct_rate(submit, correct):
        if submit == 0:
            return 0
        return correct / submit
    my_res = [i for i in res if i[3] - i[4] > 0]
    res = [i for i in res if i[3] - i[4] == 0]
    my_res.sort(key=lambda x: get_correct_rate(x[3], x[4]))
    num1 = 7 if len(my_res) >= 10 else min(4, len(my_res))
    final_res, my_res = my_res[:num1], my_res[num1:]
    res = res + my_res
    num2 = min(10 - num1, len(res))
    final_res += random.sample(res, num2)
    ret = []
    for problem in final_res:
        cursor.execute("SELECT * FROM Problems WHERE pid = %s", (problem[0]))
        problem = cursor.fetchone()
        cursor.execute("SELECT * FROM ProblemTags WHERE pid = %s", (problem[0]))
        tags = cursor.fetchall()
        _tags_ = []
        for tag in tags:
            _tags_.append(get_tag_by_tid(db, tag[1])[1])
        ret.append({
            "pid": problem[0],
            "title": problem[1],
            "content": problem[2],
            "type": problem[3],
            "author": get_user_by_uid(db, problem[4])[0],
            "upload_time": problem[5],
            "choices": problem[6],
            "answers": problem[7],
            "is_public": problem[8],
            "tags": _tags_,
        })
    ret = random.sample(ret, min(7, len(ret)))
    return {"problems": ret}
    

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
    if problem == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    if problem[3] == "choice":
        if len(json.loads(problem[7])) > 1:
            ptype = "MULTI_CHOICE"
        else:
            ptype = "SINGLE_CHOICE"
    else:
        ptype = "BLANK_FILLING"
    return {
        "pid": problem[0],
        "title": problem[1],
        "content": problem[2],
        "type": ptype,
        "author": get_user_by_uid(db, problem[4])[0],
        "upload_time": problem[5],
        "choices": problem[6],
        "answers": problem[7],
        "is_public": problem[8],
    }


def set_problem_public_status(db, pid: str, is_public: bool, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if problem == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    if problem[4] != user.uid and user.permissions.get("IS_ADMIN") == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )
    cursor.execute("UPDATE Problems SET is_public = %s WHERE pid = %s", (1 if is_public else 0, pid))
    db.commit()


def get_user_problem_groups(db, user: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ProblemGroups WHERE owner = %s", (user.uid))
    groups = cursor.fetchall()
    res = []
    for group in groups:
        res.append({
            "pgid": group[0],
            "name": group[1],
            "description": group[2],
            "owner": group[3],
        })
    return {"problem_groups": res}


def get_problem_answer(db, pid):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Problems WHERE pid = %s", (pid))
    problem = cursor.fetchone()
    if problem == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found."
        )
    if problem[9]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Problem is in contest. Permission denied."
        )
    return problem[7]


def modify_user_info(db, user: User, original_password: str, new_password: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE uid = %s", (user.uid))
    user = cursor.fetchone()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    if user[2] != md5_passwd(original_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Original password incorrect."
        )
    cursor.execute("UPDATE Users SET password = %s WHERE uid = %s", (md5_passwd(new_password), user[1]))
    db.commit()


def get_current_time(db):
    cursor = db.cursor()
    cursor.execute("SELECT NOW()")
    time = cursor.fetchone()
    return time[0]


def fuzzy_match(problems, key, threshold=50):
    scores = []
    for problem in problems:
        title_score = process.extractOne(key, problem[1])[1]
        content_score = process.extractOne(key, problem[2])[1]
        overall_score = max(title_score, content_score)
        if overall_score >= threshold:
            scores.append((overall_score, problem))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [item[1] for item in scores]