from pwdlib import PasswordHash

pwh = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwh.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwh.verify(plain_password, password_hash)
