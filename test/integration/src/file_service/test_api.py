import unittest
from configparser import ConfigParser
from unittest.mock import Mock

from api.file_service.api import FileService
from api.file_service.storage.api import Storage
from api.file_service.typings.typings import FileCreateRequest


class FileUploadIntegrationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.storage_imp_mock = Mock()

        self.config = {}

        config_parser = ConfigParser()
        self.config['config_file'] = config_parser.read_dict(
            dictionary={
                'file_service': {
                    'storage-platform': 's3'
                }
            }
        )


    def test_file_create_with_no_file(self):
        test_uuid = 'abcdefghikklmnop'
        mime_type = 'test_mime_type'

        request = FileCreateRequest(test_uuid, mime_type)

        
        storage = Storage(self.config, self.storage_imp_mock)
        
        
        file_service = FileService(self.config, storage)

        response = file_service.create_file(request)

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
