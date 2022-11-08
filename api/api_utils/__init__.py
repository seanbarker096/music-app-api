import argon2


def hash_password(password: str, salt: str):
    return argon2.argon2_hash(password, salt)
