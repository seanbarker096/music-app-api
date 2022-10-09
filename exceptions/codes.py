from enum import Enum


class ErrorCodes(Enum):
    # 0 - 999 reserved for generic, non resource specific errors

    # Resource = File
    FILE_TOO_LARGE = 1000
    FILE_UUID_NOT_UNIQUE = 1001

    # File service errors which we throw instead of throwing a given storage implementations errors
    CREATE_FILE_DOWNLOAD_URL_FAILED = 1090