from test.integration import IntegrationTestCase
from unittest.mock import Mock

from api.file_service.api import AcceptedMimeTypes, FileService, Storage
from api.file_service.typings.typings import FileCreateRequest
from exceptions.db.exceptions import DBDuplicateKeyException
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import FileUUIDNotUniqueException


class FileUploadIntegrationTestCase(IntegrationTestCase):
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

        storage = Storage(self.config, mock_storage_imp)

        file_service = FileService(config=self.config, storage=storage)

        test_uuid = "abcdefghikklmnop"
        mime_type = AcceptedMimeTypes.APP_OCTET_STREAM.value
        byte_message = bytes("message", "utf-8")

        request = FileCreateRequest(test_uuid, mime_type, file_size=111, bytes=byte_message)

        response = file_service.create_file(request)
        file_response = response.file

        mock_storage_imp.process_upload_request.assert_called_once()
        mock_storage_imp.save.assert_called_once_with(mock_storage_imp_save_request)

        assert file_response.uuid == test_uuid
        assert file_response.mime_type == mime_type
        assert file_response.download_url == "www.s3.com/download/some-random-location"
        assert file_response.file_size == 111

    def test_file_create_with_no_uuid(self):

        file_service = FileService(config=self.config)

        test_uuid = None
        mime_type = AcceptedMimeTypes.APP_OCTET_STREAM.value
        byte_message = bytes("message", "utf-8")

        request = FileCreateRequest(test_uuid, mime_type, file_size=100, bytes=byte_message)

        with self.assertRaises(InvalidArgumentException) as e:
            file_service.create_file(request)

        self.assertEqual(
            e.exception.get_message(), "Failed to create file because uuid is not valid"
        )

        self.assertEqual(e.exception.get_source(), "uuid")

    def test_file_create_with_duplicate_uuid(self):
        ## Create first file
        file_service = FileService(self.config)

        test_uuid_one = "testuuidone1234"
        mime_type = AcceptedMimeTypes.APP_OCTET_STREAM.value

        request = FileCreateRequest(test_uuid_one, mime_type)

        first_file = file_service.create_file(request).file

        test_uuid_two = test_uuid_one

        request_two = FileCreateRequest(test_uuid_two, mime_type)

        with self.assertRaises(DBDuplicateKeyException) as e:
            file_service.create_file(request_two)

        self.assertEqual(
            e.exception.get_message(), "Duplicate entry 'testuuidone1234' for key 'files.uuid_idx'"
        )

    def test_file_create_with_url_unsafe_uuid(self):
        """Tests file create with url unsafe uuid"""
        ...

    def test_file_create_with_invalid_mime_type(self):
        ...

    def test_file_create_exceeds_max_file_size(self):
        ...

    def test_file_update(self):
        ## Assert that download_url is set during update
        ...

    def test_file_update_from_non_owner(self):
        ...
