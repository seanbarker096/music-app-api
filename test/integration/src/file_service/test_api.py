from test.integration import IntegrationTestAPI
from unittest.mock import Mock

from api.file_service.api import AcceptedMimeTypes, FileService, Storage
from api.file_service.typings.typings import FileCreateRequest


class FileUploadIntegrationTestCase(IntegrationTestAPI):
    def test_file_create_with_meta_data(self):
        """Asserts that can succesfully upload file meta data, and no calls are made to try to store the file bytes given they do not exist."""

        file_service = FileService(self.config)

        test_uuid = "abcdefghikklmnop"
        mime_type = AcceptedMimeTypes.APP_OCTET_STREAM.value

        request = FileCreateRequest(test_uuid, mime_type)

        response = file_service.create_file(request)
        file_response = response.file

        ## Assert meta data has been added to db correctly
        assert file_response.uuid == test_uuid
        assert file_response.mime_type == mime_type
        assert file_response.download_url is None
        assert file_response.file_size is None

    def test_file_create_with_file_data(self):
        mock_storage_imp = Mock()
        mock_storage_imp_save_request = Mock()  ## This method usually returns some sort of object
        mock_storage_imp.save = Mock(return_value="www.s3.com/download/some-random-location")
        mock_storage_imp.process_upload_request = Mock(return_value=mock_storage_imp_save_request)

        storage = Storage(mock_storage_imp)

        file_service = FileService(config=self.config, storage=storage)

        test_uuid = None
        mime_type = AcceptedMimeTypes.APP_OCTET_STREAM.value
        byte_message = bytes("message", "utf-8")

        request = FileCreateRequest(test_uuid, mime_type, file_size=2342342, bytes=byte_message)

        response = file_service.create_file(request)
        file_response = response.file

        mock_storage_imp.process_upload_request.assert_called_once()
        mock_storage_imp.save.assert_called_once_with(mock_storage_imp_save_request)

        assert file_response.uuid == test_uuid
        assert file_response.mime_type == mime_type
        assert file_response.download_url == "www.s3.com/download/some-random-location"
        assert file_response.file_size == 2342342

        ## Assert storage imp not called and error thrown
        ## self.storage_imp_mock.save.assert_not_called()

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
    #     ## assert up to s3 mock calling the actual sdk function. Assert s3ImpMocksadsadasdsadasdsad upload called  with test_uuid. Once succesful we should then upload to our db and assert this has worked

    #      ## This should only be returned if whole process, including adding to our db table, was successful
    #     assert fileServiceUploadResponse.download_url == f'api/v0.1/fileservice/download/{test_uuid}'

    # def test_file_update():
    #     ## Assert that download_url is set during update
    #     ...

    # def test_file_update_from_non_owner():
    #     ...
