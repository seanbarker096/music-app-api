import datetime
import secrets
import time

from argon2 import PasswordHasher
from argon2 import exceptions as ArgonExceptions

ph = PasswordHasher(time_cost=12, memory_cost=16384)


def generate_salt():
    return secrets.token_hex(8)


def hash_password(password: str):
    ## TODO: work out whats best

    return ph.hash(password)


def verify_hash(hash: str, password: str):
    try:
        return ph.verify(hash, password)
    except ArgonExceptions.VerifyMismatchError:
        raise Exception(
            "Failed to verify hash and password because password does not match the hash"
        )


## TODO: Complete this
def validate_password(password: str):
    return True


def date_time_to_unix_time(datetime: datetime.datetime):
    return time.mktime(datetime.timetuple())
