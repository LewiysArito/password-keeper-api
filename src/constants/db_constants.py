from src.super_enum import SuperEnum

class Roles(SuperEnum):
    ADMIN = 1
    SUPER_USER = 2
    CREATOR = 3
    EDITOR = 4
    VIEWER = 5
    BLOCKED = 6