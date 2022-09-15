from enum import Enum
from typing import Optional


class FileType(Enum):
    POST: str = ...


class FileUploadRequest(object):
    uuid: str = None
    file_type: FileType = None

    def __init__(self, uuid: str, file_type: FileType):
        ...


############## DB ##################
