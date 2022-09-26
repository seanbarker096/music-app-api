import unittest
from configparser import ConfigParser
from test import IntegrationTestAPI
from unittest.mock import Mock

from api.file_service.api import AcceptedMimeTypes, FileService
from api.file_service.storage.api import Storage
from api.file_service.typings.typings import FileCreateRequest


class FileUploadIntegrationTestCase(IntegrationTestAPI):

    def test_file_create_with_no_file(self):
        test_uuid = 'abcdefghikklmnop'
        mime_type = AcceptedMimeTypes.APP_OCTET_STREAM.value

        request = FileCreateRequest(test_uuid, mime_type)

        response = self.app.conns.file_service.create_file(request)
    

        ## Assert meta data has been added to db correctly
        assert test_uuid == response.uuid
        assert mime_type == response.mime_type
        
        ## Assert storage imp not called
        self.storage_imp_mock.save.assert_not_called()

        ## Assert that download_url is empty
        assert response.download_url == None

    
    # ''' Tests file create with url unsafe uuid'''
    # def test_file_create_with_invalid_uuid():
    #     ...

    # def test_file_create_with_duplicate_uuid():
    #     ...
    
    # def test_file_create_with_invalid_mime_type():
    #     ...

    # def test_file_create_above_size_limit():
    #     ...

    # def test_file_create_with_file():
    #     ## assert that file created as above
    #     ## assert download url returned
    #     ## assert up to s3 mock calling the actual sdk function. Assert s3ImpMock.upload called with test_uuid. Once succesful we should then upload to our db and assert this has worked

    #      ## This should only be returned if whole process, including adding to our db table, was successful
    #     assert fileServiceUploadResponse.download_url == f'api/v0.1/fileservice/download/{test_uuid}'

    # def test_file_update():
    #     ## Assert that download_url is set during update
    #     ...

    # def test_file_update_from_non_owner():
    #     ...
