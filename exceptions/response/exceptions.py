# This module contains errors intended to be delivered to the user


from typing import Optional

from exceptions.codes import ErrorCodes


class ResponseBaseException(Exception):
    """For resource specific error classes to extend. This defines and sets some common properties and common methods to be used for other resource specific errors"""

    _http_code: int  # Should be set by the parent error class
    _name: str
    _code: int
    _detail: str  # Sent to front end but not shown to client. Set these in the Exception itself
    _source: Optional[str] = None
    _message: str  # For debugging and logging purposes. This message is passed in when creating the exception

    def __init__(self, message=None, source=None):
        """We set some common properties here to avoid repeatedly doing this in child classes"""
        self._message = message
        self._source = source

    def get_detail(self):
        return self._detail

    def get_message(self):
        return self._message

    def get_http_code(self):
        return self._http_code

    def get_code(self):
        return self._code

    def get_name(self):
        return self._name

    def get_source(self):
        return self._source


class FileTooLargeException(ResponseBaseException):
    _http_code = 400
    _name = "FILE_TOO_LARGE"
    _code = ErrorCodes.FILE_TOO_LARGE.value
    _message = "File is too large."

    def __init__(self, source: str):
        super().__init__(source)


class FileUUIDNotUniqueException(ResponseBaseException):
    _http_code = 400
    _name = "FILE_UUID_NOT_UNIQUE"
    _code = ErrorCodes.FILE_UUID_NOT_UNIQUE.value
    _detail = "File uuid must be unique."

    def __init__(self, source: str, message: str):
        super().__init__(message, source)


class FileNotFoundException(ResponseBaseException):
    _http_code = 404
    _name = "FILE_NOT_FOUND"
    _code = ErrorCodes.FILE_NOT_FOUND
    _message = "File was not found"

    def __init__(self, source: str, message: Optional[str] = None):
        ## Allow overwriting of default message
        if message:
            self._message = message

        super().__init__(message=self._message, source=source)


class BadRequestException(ResponseBaseException):
    ...


class CreateFileDownloadURLFailedException(ResponseBaseException):
    # We are creating this error purely to avoid throwing an S3 error. Otherwise we wouldn't
    # usually create errors for a specific action. Instead we would throw an error indicating
    # why the action failed
    _http_code = 500
    _name = "CREATE_FILE_DOWNLOAD_URL_FAILED"
    _code = ErrorCodes.CREATE_FILE_DOWNLOAD_URL_FAILED.value
    _detail = "Failed to create file download url."

    def __init__(self, message: str):
        super().__init__(message)


class UserAlreadyExistsException(ResponseBaseException):
    _http_code = 400
    _name = "USER_ALREADY_EXISTS"
    _code = ErrorCodes.USER_ALREADY_EXISTS.value
    _detail = "Failed to create user as they already exist."

    def __init__(self, message: str):
        super().__init__(message=message)


class UserNotFoundException(ResponseBaseException):
    _http_code = 404
    _name = "USER_NOT_FOUND"
    _code = ErrorCodes.USER_NOT_FOUND.value
    _detail = "Failed to find user"

    def __init__(self, message: str):
        super().__init__(message=message)


class InvalidAuthTokenException(ResponseBaseException):
    _http_code = 401
    _name = "INVALID_AUTH_TOKEN"
    _code = ErrorCodes.INVALID_AUTH_TOKEN.value
    _detail = "Invalid authentication token"

    def __init__(self, message: str):
        super().__init__(message=message)


class PerformanceNotFoundException(ResponseBaseException):
    _http_code = 404
    _name = "PERFORMANCE_NOT_FOUND"
    _code = ErrorCodes.PERFORMANCE_NOT_FOUND.value
    _detail = "Failed to find performance"

    def __init__(self, message: str):
        super().__init__(message=message)
