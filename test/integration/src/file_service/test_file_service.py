import io
from test.integration import IntegrationTestCase
from unittest.mock import Mock

from api.file_service.api import AcceptedMimeTypes, FileService, Storage
from api.file_service.typings.typings import FileCreateRequest, FileGetFilter
from exceptions.db.exceptions import DBDuplicateKeyException
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import FileUUIDNotUniqueException


class FileUploadIntegrationTestCase(IntegrationTestCase):
    def test_file_create(self):
        """Asserts that can succesfully upload file meta data, and no calls are made to try to store the file bytes given they do not exist."""
        mock_storage_imp = Mock()
        mock_storage_imp.save = Mock()
        mock_storage_imp_save_request = Mock()  ## This method usually returns some sort of object
        mock_storage_imp.process_upload_request = Mock(return_value=mock_storage_imp_save_request)
        mock_storage_imp.get_file_download_url = Mock(
            return_value="www.file-store.com/download/some-random-location"
        )

        storage = Storage(self.config, mock_storage_imp)

        file_service = FileService(config=self.config, storage=storage)

        test_uuid = "abcdefghikklmnop"
        mime_type = AcceptedMimeTypes.APP_OCTET_STREAM.value
        byte_message = bytes("message", "utf-8")

        request = FileCreateRequest(uuid=test_uuid, mime_type=mime_type, bytes=byte_message)

        response = file_service.create_file(request)
        file_response = response.file

        mock_storage_imp.process_upload_request.assert_called_once()
        mock_storage_imp.save.assert_called_once()

        ## Assert meta data has been added to db correctly
        self.assertTrue(isinstance(file_response.id, int))
        assert file_response.uuid == test_uuid
        assert file_response.mime_type == mime_type
        assert file_response.download_url == "www.file-store.com/download/some-random-location"
        assert file_response.file_size is None

        ## TODO: Improve test by actually querying the db for the file and ensuring its been stored there correctly

    def test_file_upload_with_no_uuid(self):

        file_service = FileService(config=self.config)

        test_uuid = None
        mime_type = AcceptedMimeTypes.APP_OCTET_STREAM.value
        byte_message = bytes("message", "utf-8")

        request = FileCreateRequest(test_uuid, mime_type, file_size=100, bytes=byte_message)

        with self.assertRaises(InvalidArgumentException) as e:
            file_service.create_file(request)

        self.assertEqual(
            e.exception.get_message(), "Failed to upload file because uuid is not valid"
        )

        self.assertEqual(e.exception.get_source(), "uuid")

    def test_file_upload_with_duplicate_uuid(self):
        ## Create first file
        file_service = FileService(self.config)

        test_uuid_one = "testuuidone1234"
        mime_type = AcceptedMimeTypes.APP_OCTET_STREAM.value
        byte_message = bytes("message", "utf-8")

        request = FileCreateRequest(uuid=test_uuid_one, mime_type=mime_type, bytes=byte_message)

        first_file = file_service.create_file(request).file

        test_uuid_two = test_uuid_one

        request_two = FileCreateRequest(uuid=test_uuid_two, mime_type=mime_type, bytes=byte_message)

        with self.assertRaises(DBDuplicateKeyException) as e:
            file_service.create_file(request_two)

        self.assertEqual(
            e.exception.get_message(), "Duplicate entry 'testuuidone1234' for key 'files.uuid_id'"
        )

    def test_file_upload_with_url_unsafe_uuid(self):
        """Tests file create with url unsafe uuid"""
        ...

    def test_file_upload_with_invalid_mime_type(self):
        ...

    def test_file_upload_exceeds_max_file_size(self):
        ...

    def test_file_update(self):
        ## Assert that download_url is set during update
        ...

    def test_file_update_from_non_owner(self):
        ...

    def test_file_get(self):

        file_buffer = io.BytesIO(b"some initial binary data")

        mock_storage_imp = Mock()
        mock_storage_imp.get_file = Mock(return_value=file_buffer)

        storage = Storage(self.config, mock_storage_imp)

        file_service = FileService(self.config, storage)

        ## Seed the db with a file.
        ## TODO: Create fixtures to avoid doing this directly in the test
        file_id = self.db.run_query(
            """
        INSERT INTO files(uuid, file_size, mime_type, download_url) VALUES(%s, %s, %s, %s)
        """,
            (
                "abcdefghikklmnop",
                None,
                "image/png",
                "https://storage-container-id.provider.domain.com/as?query-param-one=random-param",
            ),
        ).get_last_row_id()

        filter = FileGetFilter(uuid="abcdefghikklmnop")

        file_get_result = file_service.get_file(filter)
        file = file_get_result.file

        self.assertEquals(
            file_get_result.bytes, file_buffer.read(), "Should return the correct file bytes"
        )
        self.assertEquals(file.uuid, "abcdefghikklmnop", "Should return the correct file uuid")
        self.assertEquals(
            file.download_url,
            "https://storage-container-id.provider.domain.com/as?query-param-one=random-param",
        )
        self.assertEquals(file.mime_type, "image/png", "Should return the correct mime_type")
        self.assertEquals(file.id, file_id, "Should return the correct file id")
