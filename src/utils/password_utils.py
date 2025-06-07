import bcrypt

class PasswordUtils:
    @classmethod
    def hash_password(cls, password:str)->str:
        """
        Хеширует пароль
        
        :param password: Пароль
        :return: Хешированный пароль
        """
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt).decode()
    
    @classmethod
    def validate_password(cls,
        password:str,
        hashed_password: str
    )->bool:
        """
        Сравнивает пароль
        
        :param password: Пароль
        :hashed_password: Захешированный пароль
        :return: Хешированный пароль
        """
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    