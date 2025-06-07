from src.super_enum import SuperEnum

class Roles(SuperEnum):
    ADMIN = 6
    SUPER_USER = 5
    CREATOR = 4
    EDITOR = 3
    VIEWER = 2
    BLOCKED = 1