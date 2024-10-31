from passlib.context import CryptContext


passwd_context = CryptContext(schemes=["bcrypt"])



def generate_passwd_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_passwd(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)