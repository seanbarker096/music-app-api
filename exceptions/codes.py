from enum import Enum


class ErrorCodes(Enum):
    # 0 - 999 reserved for generic, non resource specific errors

    # Resource = File
    FILE_TOO_LARGE = 1000
    FILE_UUID_NOT_UNIQUE = 1001
