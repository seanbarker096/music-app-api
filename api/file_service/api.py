from cmath import exp

from api_types.api_types import FileUploadRequest

from api.file_service.core.api import FileService


class FileServiceAPI():
    def __init__(self, config):
        self.file_service = FileService(self, config)
        
    def upload(self, request: FileUploadRequest):
        # 1. Parse the request object with the upload meta data
        if not isinstance(request.uuid, str):
            raise Exception('uuid argument must be a string')

        if len(request.uuid) == 0:
            raise Exception('uuid must not be empty string') ##update ot check its uuid4
        

        # 2. Extract uuid and upload to S3
        uuid4 = request.uuid

        

        # 3. Take uuid and s3 download url and store in the resource mapping table

        # 4. Return the fileservice GET url which will be used to stream the video back to the user

