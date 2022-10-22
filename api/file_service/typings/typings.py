from typing import Optional


class FileMeta(object):
    uuid: str = ...
    mime_type: str = ...
    file_size: Optional[int] = ...

    def __init__(self, uuid: str, mime_type: str, file_size: Optional[int] = None):
        self.uuid = uuid
        self.mime_type = mime_type
        self.file_size = file_size


class FileServiceFile(object):
    """Id of file stored in the file service db table"""

    id: int = ...
    uuid: str = ...
    mime_type: str = ...
    file_size: Optional[int] = None
    download_url: Optional[str] = None

    def __init__(
        self,
        id: str,
        uuid: str,
        mime_type: str,
        file_size: Optional[int] = None,
        download_url: Optional[str] = None,
    ):
        self.id: int = id
        self.uuid: str = uuid
        self.mime_type: str = mime_type
        self.file_size: Optional[int] = file_size
        self.download_url: Optional[str] = download_url


# Our storage service is built to integrate with any type of external service provider, so we can switch this out for a new Request object if a new provider is used and new fields are needed. The storage implementation validates the Request to ensure it has all the fields it needs. Validation shouldn't be done elsewhere to avoid coupling other Storage Service code to the specific service provider (e.g. S3)
class FileUploadRequest(object):
    id: int = ...
    uuid: str = ...
    mime_type: str = ...
    file_size: Optional[int] = None
    bytes: Optional[bytes] = None

    def __init__(
        self,
        id: int,
        uuid: str,
        mime_type: str,
        file_size: Optional[int] = None,
        bytes: Optional[bytes] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.mime_type = mime_type
        self.file_size = file_size
        self.bytes = bytes


class FileCreateAndUploadRequest(object):
    uuid: str = ...
    mime_type: str = ...
    bytes: bytes = ...
    file_size: Optional[int] = None

    def __init__(
        self,
        uuid: str,
        mime_type: str,
        bytes: bytes,
        file_size: Optional[int] = None,
    ) -> None:
        self.uuid = uuid
        self.mime_type = mime_type
        self.file_size = file_size
        self.bytes = bytes


class FileUploadResult(object):
    file: FileServiceFile

    def __init__(self, file: FileServiceFile) -> None:
        self.file = file


class FileUpdateRequest(object):
    bytes: str = ...

    def __init__(self, bytes: str) -> None:
        self.bytes = bytes


class FileDownloadURLGetRequest(object):
    file_identifier: str = ...

    def __init__(self, file_identifier: str):
        self.file_identifier = file_identifier


class FileGetRequest(object):
    ...


class FileGetResult(object):
    ...
