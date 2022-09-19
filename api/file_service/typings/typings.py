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
    file_size: Optional[int] = ...
    download_url: Optional[str] = ...

    def __init__(self, id: str, uuid: str, mime_type: str, file_size: Optional[int] = None, download_url: Optional[str] = None):
        self.id = id
        self.uuid: str = uuid
        self.mime_type: str = mime_type
        self.file_size: Optional[int] = file_size
        self.download_url = Optional[str] = download_url


class FileCreateRequest(object):
    uuid: str = ...
    mime_type: str = ...
    file_size: Optional[int] = ...
    bytes: Optional[bytes] = ...
    
    def __init__(self, uuid: str,mime_type: str, file_size: Optional[int] = None, bytes: Optional[bytes] = None) -> None:
        self.uuid = uuid
        self.mime_type = mime_type
        self.file_size = file_size
        self.bytes = bytes

class FileCreateResponse(object):
    file = FileServiceFile
    
    def __init__(self, file: FileServiceFile) -> None:
        self.file = file

    def create_response(self) -> dict[str, str | int]:
        return {
            'uuid': self.uuid,
            'download_url': self.download_url,
            'mime_type': self.mime_type,
            'file_size': self.file_size,
            'file_id': self.file_id
        }


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

