from exceptions.exceptions import AppException


class DBDuplicateKeyException(AppException):
    def __init__(self, message):
        super().__init__(message)
