from api.file_service.storage.api import Storage
from api.file_service.typings.typings import (FileCreateRequest,
                                              FileCreateResponse,
                                              FileUpdateRequest)
from typings import Optional


## These are responsible for create response objects whilst the inner layers can return reosurces e.g. FileServiceFile
class FileService():
    def __init__(self, config, storage: Optional[Storage] = None):
        self.storage = storage if storage else Storage(config)
        self.test = 'adsadasdasd'

    ## Post should just fil in db with all entries in request and hence download url will be empty.

    ## PUT/PATCH should check UpdateRequest object to see what fields are being updated. Should not use same request object as the POST request as then gets confusing as to which fields already exist vs which are ebing uploda


    '''This doesn't handle actually uploading the bytes'''
    def create_file(self, request: FileCreateRequest) -> FileCreateResponse:
           # 1. Parse the request object with the upload meta data
        if not isinstance(request.uuid, str):
            raise Exception('uuid argument must be a string')

        if len(request.uuid) == 0:
            raise Exception('uuid must not be empty string') ##update ot check its uuid4
        
        ## If meta data is valid then save this and create file entry

        ## If bytes field is valid then we can also save the bytes to s3 and get download url, and return this

        ## check if file uuid exists

        ##upload actual file if it exists
        download_url = self.storage.upload_file()

        ## save file along with meta and download url to our internal db
        file_id = self.storage.create_file()
      
        ## Build response

        response_body = FileCreateResponse().create_response()
        

        # 3. Take uuid and s3 download url and store in the resource mapping table

        # 4. Return the fileservice GET url which will be used to stream the video back to the user

    def update_file(self, request: FileUpdateRequest):
        ## Currenty we only support updating the bytes of a file (e.g. uploading a new file and linking it to an existing internal file object)

        download_url = self.storage.upload_file()

        self.storage.update_file()

