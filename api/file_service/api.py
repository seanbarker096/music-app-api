from enum import Enum
from typing import Optional

from api.file_service.dao.api import FileServiceDAO
from api.file_service.storage.api import Storage
from api.file_service.typings.typings import (FileCreateRequest,
                                              FileCreateResponse,
                                              FileUpdateRequest)

# TODO: Update this


class AcceptedMimeTypes(Enum):
    APP_OCTET_STREAM = 'application/octet-stream'

## These are responsible for create response objects whilst the inner layers can return reosurces e.g. FileServiceFile
class FileService():
    MAX_FILE_SIZE = 1000000000000000

    def __init__(self, config, storage: Optional[Storage] = None, file_service_dao: Optional[FileServiceDAO] = None):
        self.storage = storage if storage else Storage(config)
        self.file_service_dao = file_service_dao if file_service_dao else FileServiceDAO()

    ## Post should just fil in db with all entries in request and hence download url will be empty.

    ## PUT/PATCH should check UpdateRequest object to see what fields are being updated. Should not use same request object as the POST request as then gets confusing as to which fields already exist vs which are ebing uploda


    '''This doesn't handle actually uploading the bytes'''
    def create_file(self, request: FileCreateRequest) -> FileCreateResponse:
        if not isinstance(request.uuid, str) or len(request.uuid) == 0:
            raise Exception('Failed to create file for file because uuid is not valid')
        
        ## TODO: Check string is url safe
        
        ## If meta data is valid then save this and create file entry
        accepted_mime_types = set(item.value for item in AcceptedMimeTypes)
        print(accepted_mime_types)
        print(request.mime_type)
        if request.mime_type not in accepted_mime_types:
            raise Exception(f'Failed to create file. Invalid or unnaccepted MIME type of type {request.mime_type}')

        download_url = None

        if request.bytes:
            if not isinstance(request.bytes, bytes):
                raise Exception('Failed to create file because bytes is not valid')
            
            download_url = self.storage.upload_file(request)    

        if isinstance(request.file_size, int) and request.file_size > self.MAX_FILE_SIZE:
            raise Exception(f'Failed to create file. File size exceeds maximum allowed value of {self.MAX_FILE_SIZE}')

        ## TODO: check if file uuid exists
        ## if self.file_service_dao.get_file_by_uuid(request.uuid):
            #raise Exception(f'Failed to create file with uuid {uuid} because it already exists')


        file = self.file_service_dao.create_file(FileCreateRequest, download_url=download_url)
        

        return FileCreateResponse(file)

    def update_file(self, request: FileUpdateRequest):
        ## Currenty we only support updating the bytes of a file (e.g. uploading a new file and linking it to an existing internal file object)

        download_url = self.storage.upload_file()

        self.storage.update_file()

