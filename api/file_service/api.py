import io
from contextlib import contextmanager
from enum import Enum
from typing import Optional

from api.file_service.dao.api import FileServiceDAO
from api.file_service.storage.api import Storage
from api.file_service.typings.typings import (
    FileCreateRequest,
    FileCreateResult,
    FileGetFilter,
    FileGetResult,
    FileMetaCreateRequest,
    FileMetaUpdateRequest,
    FileUpdateRequest,
    FileUploadRequest,
)
from exceptions.db.exceptions import DBDuplicateKeyException
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import (
    FileTooLargeException,
    FileUUIDNotUniqueException,
)

# TODO: Update this


class AcceptedMimeTypes(Enum):
    APP_OCTET_STREAM = "application/octet-stream"
    MULTIPART = "multipart/form-data"


class FileWriter(object):
    file: io.BufferedWriter

    def __init__(self, filename):
        self.file_name = filename

    def __enter__(self):
        try:
            self.file = open(self.file_name, "wb")
            return self.file
        except IOError:
            raise Exception(f"Failed when opening file {self.file_name}")

    def __exit__(self, exception, exception_message, trace):
        self.file.close()
        if exception:
            raise exception(
                f"Failed when handling file {self.file_name} because: {exception_message}"
            )


## These are responsible for create response objects whilst the inner layers can return reosurces e.g. FileServiceFile
class FileService:
    MAX_FILE_SIZE = 1000000000000000

    def __init__(
        self,
        config,
        storage: Optional[Storage] = None,
        file_service_dao: Optional[FileServiceDAO] = None,
    ):
        self.storage = storage if storage else Storage(config)
        self.file_service_dao = file_service_dao if file_service_dao else FileServiceDAO(config)

    ## Post should just fil in db with all entries in request and hence download url will be empty.

    ## PUT/PATCH should check UpdateRequest object to see what fields are being updated. Should not use same request object as the POST request as then gets confusing as to which fields already exist vs which are ebing uploda

    # def save_file_meta_data():
    #     """Creates a file by storing is meta data in the database."""
    #     ...

    # def upload_file_bytes():
    #     """Once a file has been created, this function will upload the file bytes to the third party storage service provider."""

    #     ## Check file exists in db. If it does then upload bytes to s3 and get download url
    #     ...

    def create_file(self, request: FileCreateRequest) -> FileCreateResult:
        # Validate inputs
        if not isinstance(request.uuid, str) or len(request.uuid) == 0:
            raise InvalidArgumentException(
                message="Failed to upload file because uuid is not valid", source="uuid"
            )

        ## TODO: Check string is url safe. Check if uuid exists

        ## If meta data is valid then save this and create file entry
        ## TODO: SPLIT string by ; and check if any of the types match the accepted ones. This because of mime types like
        # accepted_mime_types = set(item.value for item in AcceptedMimeTypes)
        # if request.mime_type not in accepted_mime_types:
        #     raise ValueError(
        #         f"Failed to upload file. Invalid or unnaccepted MIME type of type {request.mime_type}"
        #     )

        if not isinstance(request.bytes, bytes):
            raise TypeError("Failed to upload file because bytes argument is not valid")

        if isinstance(request.file_size, int) and request.file_size > self.MAX_FILE_SIZE:
            raise InvalidArgumentException(
                f"Failed to upload file. File size exceeds maximum allowed value of {self.MAX_FILE_SIZE}"
            )

        ## store the file meta data in the db first. This means if our db is down we aren't storing files in s3 without having any info in our db. Also means if s3 is down we have some information in db to try again later with
        file_meta_create_request = FileMetaCreateRequest(
            uuid=request.uuid, mime_type=request.mime_type, file_name=request.file_name
        )

        try:
            file = self.file_service_dao.create_file_meta(file_meta_create_request)
        except DBDuplicateKeyException as e:
            if e.get_column() == "uuid":
                raise FileUUIDNotUniqueException(
                    message=f"Could not create file because file with uuid {request.uuid} already exists",
                    source=request.uuid,
                )
            else:
                raise e
        except:
            raise Exception(f"Failed to create file with uuid {request.uuid}")

        ## upload to cloud storage provider
        file_upload_request = FileUploadRequest(
            id=file.id,
            file_name=file.file_name,
            uuid=file.uuid,
            mime_type=file.mime_type,
            file_size=request.file_size,
            bytes=request.bytes,
        )

        ## Uploads file and returns a download url
        file = self.storage.upload_file(file_upload_request)

        # TODO: If file upload was successful then store the download_url in the DB
        file_with_url = self.file_service_dao.update_file(
            request=FileMetaUpdateRequest(id=file.id, url=file.url)
        )

        return FileCreateResult(file_with_url)

    def update_file(self, request: FileUpdateRequest):
        """Used to update file fields e.g. the bytes field when a user tries to upload the actual file after its meta data has been saved."""
        ...

    def get_file(self, filter: FileGetFilter) -> FileGetResult:
        # Check the file exists in the database. This is mostly the metadata

        file = self.file_service_dao.get_file_by_uuid(filter.uuid)

        bytes_object = self.storage.get_file(filter)
        ## seek required for some reason otherwise image not returned from api correctly
        bytes_object.seek(0)

        return FileGetResult(file_bytes=bytes_object, file=file)
