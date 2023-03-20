from enum import Enum


class ErrorCodes(Enum):
    # 0 - 999 reserved for generic, non resource specific errors
    INVALID_AUTH_TOKEN = 0

    # Resource = File
    FILE_TOO_LARGE = 1000
    FILE_UUID_NOT_UNIQUE = 1001
    FILE_NOT_FOUND = 1002

    # File service errors which we throw instead of throwing a given storage implementations errors
    CREATE_FILE_DOWNLOAD_URL_FAILED = 1090

    # Resource - User
    USER_ALREADY_EXISTS = 2000
    USER_NOT_FOUND = 2001

    # Resource = Performance
    PERFORMANCE_NOT_FOUND = 3000

    # Resource = Post
    POST_NOT_FOUND = 4000
