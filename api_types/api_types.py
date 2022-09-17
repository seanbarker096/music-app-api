from enum import Enum
from typing import Optional


class FileType(Enum):
    POST: str = ...


class FileUploadRequest(object):
    uuid: str = ...
    file_type: FileType = ...

    def __init__(self, uuid: str, file_type: FileType) -> None:
        self.uuid = uuid
        self.file_type = file_type


############## DB ##################
