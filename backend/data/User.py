class User:
    def __init__(self, name: str, uid: str, is_admin: bool, permissions: list):
        self.name = name
        self.uid = uid
        self.is_admin = is_admin
        self.permissions = Permissions(permissions)

from enum import Enum

class PermissionType(Enum):
    IS_ADMIN = 0
    BLOCK_USER = 1
    REVIEW_TOPIC = 2
    MANAGE_PLATFORM = 3
    UPLOAD_FILE = 4
    UPLOAD_PROBLEM = 5
    SHARE_PROBLEM = 6
    SEARCH_PROBLEM = 7
    BLOCKED = 8

    @staticmethod
    def is_permission(permission: str) -> bool:
        return permission in PermissionType.__members__

class Permissions:
    def __init__(self, permissions: list):
        self.permissions = []
        for i in range(0, len(PermissionType)):
            if permissions[i] == 'True':
                self.permissions.append(PermissionType(i).name)

    def get(self, permission: str) -> bool:
        return PermissionType[permission].name in self.permissions

    def to_list(self) -> list:
        res = []
        for i in range(0, len(PermissionType)):
            if PermissionType(i).name in self.permissions:
                res.append('True')
            else:
                res.append('False')
        return res