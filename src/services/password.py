from pwdlib import PasswordHash


class PasswordHandler:
    """Сервис для работы с хешированными паролями"""

    password_hash: PasswordHash = PasswordHash.recommended()

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return cls.password_hash.verify(plain_password, hashed_password)

    @classmethod
    def get_hashed_password(cls, password) -> str:
        return cls.password_hash.hash(password)
