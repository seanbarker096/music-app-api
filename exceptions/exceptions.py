"""For more generic error types"""


class AppException(Exception):
    """Parent Exception class which other non-client exceptions should wrap around. Defines some methods used by all exception classes."""

    _message: str

    def __init__(self, message: str):
        self._message = message
        super().__init__(message)

    def get_message(self):
        return self._message


class InvalidArgumentException(AppException):
    _message: str
    # Argument which is the source of the error
    _source: str

    def __init__(self, message: str, source: str):
        self._message = message
        self._source = source
        super().__init__(message)

    def get_source(self):
        return self._source


class AppSearchServiceException(AppException):
    _message: str

    def __init__(self, message: str):
        self._message = message
        super().__init__(message)
