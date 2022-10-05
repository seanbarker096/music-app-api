# This module contains errors intended to be delivered to the user


from typing import Optional

from exceptions.codes import ErrorCodes


class ResponseBaseException(Exception):
    """For resource specific error classes to extend. This defines and sets some common properties and common methods to be used for other resource specific errors"""

    _http_code: int  # Should be set by the parent error class
    _name: str
    _code: int
    _detail: str  # Sent to front end but not shown to client
    _source: Optional[str] = None
    _message: str  # For debugging and logging purposes

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
    _message = "File uuid must be unique."

    def __init__(self, source: str):
        super().__init__(source)


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
