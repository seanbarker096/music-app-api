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
    meta: FileMeta = ...
    download_url: Optional[str] = ...

    def __init__(self, id: str, meta: FileMeta, download_url: Optional[str] = None):
        self.id = id
        self.meta = meta
        self.download_url = download_url


class FileCreateRequest(object):
    uuid: str = ...
    mime_type: str = ...
    file_size: Optional[int] = ...
    download_url: Optional[str] = ...
    bytes: Optional[bytes] = ...
    
    def __init__(self, uuid: str,mime_type: str, file_size: Optional[int] = None, download_url: Optional[str] = ..., bytes: Optional[bytes] = None) -> None:
        self.uuid = uuid
        self.mime_type = mime_type
        self.file_size = file_size
        self.download_url = download_url
        self.bytes = bytes

class FileCreateResponse(object):
    uuid: str = ...
    '''The id of the file entry created in the database, which the file will later be stored in'''
    file_id: int = ...
    mime_type: str = ...
    file_size: Optional[int] = ...
    download_url: Optional[str]
    
    def __init__(self, uuid: str, file_id: int, mime_type: str, file_size: Optional[int], download_url: Optional[str]) -> None:
        self.uuid = uuid
        self.file_id = file_id
        self.mime_type = mime_type
        self.file_size = file_size
        self.download_url = download_url

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

