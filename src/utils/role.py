from src.constants.db_constants import Roles 

def validate_role(role_id: int) -> None:
    if role_id not in Roles.values():
        raise ValueError(f"Некорректный идентификатор роли: {role_id}")

def is_admin_access(role_id: int)->bool:
    """
    Проверка, что роль группы пользователя является админской
    
    :param: role - идентификатор роли
    :return: Возвращает True, если роль - администратор
    """
    validate_role(role_id)
    return Roles.ADMIN.value == role_id

def is_superuser_access(role_id: int):
    """
    Проверка, что роль группы пользователя является суперпользовательской или более высокой в правах 
    
    :param: role - идентификатор роли
    :return: Возвращает True, если роль не ниже суперпользователя 
    """
    validate_role(role_id)
    return Roles.SUPER_USER.value <= role_id

def is_creator_access(role_id: int):
    """
    Проверка, что роль группы пользователя является ни ниже уровня создателя
    
    :param: role - идентификатор роли
    :return: Возвращает True, если роль не ниже создателя 
    """
    if role_id not in Roles.values():
        raise ValueError(f"Некорректный идентификатор роли: {role_id}")
    return Roles.CREATOR.value <= role_id

def is_editor_access(role_id: int):
    """
    Проверка, что роль группы пользователя является ни ниже уровня редактора
    
    :param: role - идентификатор роли
    :return: Возвращает True, если роль не ниже редактор 
    """
    if role_id not in Roles.values():
        raise ValueError(f"Некорректный идентификатор роли: {role_id}")
    return Roles.EDITOR.value <= role_id

def is_viewer_access(role_id: int):
    """
    Проверка, что роль группы пользователя является смотрителем
    
    :param: role - идентификатор роли
    :return: Возвращает True, если роль не ниже уровня смотрителя
    """
    if role_id not in Roles.values():
        raise ValueError(f"Некорректный идентификатор роли: {role_id}")
    return Roles.VIEWER.value <= role_id

def is_blocked_access(role_id: int):
    """
    Проверка, что доступ у пользователя к группе был заблокирован 
    
    :param: role - идентификатор роли
    :return: Возвращает принадлежность к роли 
    """
    if role_id not in Roles.values():
        raise ValueError(f"Некорректный идентификатор роли: {role_id}")
    return Roles.BLOCKED.value == role_id
