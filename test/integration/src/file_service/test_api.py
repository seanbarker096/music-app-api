from types.types import *

from api.file_service.api import FileServiceAPI


class FileUploadAPIIntegrationTestCase:


    def __init__(self):
        return

    def testFileUploadToS3Success():

        test_uuid = 'abcdefghikklmnop'
        fileUploadRequest = FileUploadRequest(test_uuid, FileType.POST)

        fileServiceAPI = FileServiceAPI()

        downloadUrl = fileServiceAPI.upload(fileUploadRequest)
        # Should create entry in db for uuid and the specific product
        ## TODO - Use the same db class we will use in the DAO to grab the data

        # Should return file service download url to client
        ## assert s3ImpMock.upload called with test_uuid
        assert downloadUrl == f'api/v0.1/fileservice/download/{test_uuid}'
