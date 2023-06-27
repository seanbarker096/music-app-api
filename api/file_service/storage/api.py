from io import BytesIO
from typing import Optional

from api.file_service.storage.s3_storage_imp import S3StorageImp
from api.file_service.storage.storage_imp import StorageImp
from api.file_service.typings.typings import (
    FileDownloadURLGetRequest,
    FileServiceFile,
    FileUploadRequest,
)


class Storage:
    def __init__(self, config, storage_imp: Optional[StorageImp] = None):

        # determine storage impementation from environment vars
        self.config = config

        ## might need to use config parser syntax here
        if not storage_imp:

            implementation_type = self.config["config_file"]["file-service"].get(
                "storage-platform", "s3"
            )

            match implementation_type:
                case "s3":
                    self.storage_imp = S3StorageImp(config)
        else:
            self.storage_imp = storage_imp

    def upload_file(self, request: FileUploadRequest) -> FileServiceFile:
        """Upload file to third party storage service"""
        save_request = self.storage_imp.process_upload_request(request)

        ## method to save meta data to db
        self.storage_imp.save(save_request)

        url = self.get_file_url(request=FileDownloadURLGetRequest(file_identifier=request.uuid))

        ## We cache the aws presigned url so that every requuest for the file doesn't request a new presigned url
        return FileServiceFile(
            id=request.id,
            uuid=request.uuid,
            file_name=request.file_name,
            file_size=request.file_size,
            mime_type=request.mime_type,
            ## TODO: Consider whether we want to send back the bytes grabbed from s3 in case they are modified in some way
            url=url,
        )

    # TODO: Rename to create_file_url
    def get_file_url(self, request: FileDownloadURLGetRequest) -> str:
        return self.storage_imp.get_file_url(request)

    def get_file(self, uuid: str) -> BytesIO:
        bytes_object = self.storage_imp.get_item(uuid)
        return bytes_object
    
    def validate_file_url(self, url: str) -> bool:
        return self.storage_imp.validate_file_url(url)
