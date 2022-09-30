from enum import Enum
from turtle import down
from typing import Optional


class FileMeta(object):
    uuid: str = ...
    mime_type: str = ...
    file_size: Optional[int] = ...
    
    def __init__(self, uuid: str,mime_type: str, file_size: Optional[int] = None):
        self.uuid = uuid
        self.mime_type = mime_type
        self.file_size = file_size



class FileServiceFile(object):
    '''Id of file stored in the file service db table'''
    id:  int = ...
    uuid: str = ...
    mime_type: str = ...
    file_size: Optional[int] = None
    download_url: Optional[str] = None

    def __init__(self, id: str, uuid: str, mime_type: str, file_size: Optional[int] = None, download_url: Optional[str] = None):
        self.id = id
        self.uuid: str = uuid
        self.mime_type: str = mime_type
        self.file_size: Optional[int] = file_size
        self.download_url = Optional[str] = download_url


class FileCreateRequest(object):
    uuid: str = ...
    mime_type: str = ...
    file_size: Optional[int] = None
    bytes: Optional[bytes] = None
    
    def __init__(self, uuid: str,mime_type: str, file_size: Optional[int] = None, bytes: Optional[bytes] = None) -> None:
        self.uuid = uuid
        self.mime_type = mime_type
        self.file_size = file_size
        self.bytes = bytes

class FileCreateResponse(object):
    file: FileServiceFile
    
    def __init__(self, file: FileServiceFile) -> None:
        self.file = file


class FileUpdateRequest(object):
    bytes: str = ...

    def __init__(self,  bytes: str) -> None:
        self.bytes = bytes


class FileUploadResponse(object):
    uuid: str = ...
    download_url: str = ...

    def __init__(self, uuid: str, download_url: str) -> None:
        self.uuid = uuid
        self.download_url = download_url

