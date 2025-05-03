import bcrypt

class PasswordUtils:
    @classmethod
    def hash_password(cls, password:str)->bytes:
        """
        Хеширует пароль
        
        :param password: Пароль
        :return: Хешированный пароль
        """
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode('utf-8')
        return bcrypt.hashpw(pwd_bytes, salt)
    
    @classmethod
    def validate_password(cls,
        password:str,
        hashed_password: bytes
    )->bool:
        """
        Сравнивает пароль
        
        :param password: Пароль
        :hashed_password: Захешированный пароль
        :return: Хешированный пароль
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    