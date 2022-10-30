import copy
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
        mime_type = "image/png"
        byte_message = bytes("message", "utf-8")

        request = FileCreateRequest(
            uuid=test_uuid, file_name="my-test-file.png", mime_type=mime_type, bytes=byte_message
        )

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
        mime_type = "image/png"
        byte_message = bytes("message", "utf-8")

        request = FileCreateRequest(
            test_uuid, "my-test-file.png", mime_type, file_size=100, bytes=byte_message
        )

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
        mime_type = "image/png"
        byte_message = bytes("message", "utf-8")

        request = FileCreateRequest(
            uuid=test_uuid_one,
            file_name="my-test-file.png",
            mime_type=mime_type,
            bytes=byte_message,
        )

        first_file = file_service.create_file(request).file

        test_uuid_two = test_uuid_one

        request_two = FileCreateRequest(
            uuid=test_uuid_two,
            file_name="my-second-test-file.png",
            mime_type=mime_type,
            bytes=byte_message,
        )

        with self.assertRaises(DBDuplicateKeyException) as e:
            file_service.create_file(request_two)

        self.assertEqual(
            e.exception.get_message(), "Duplicate entry 'testuuidone1234' for key 'files.uuid_idx'"
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
        ## Need to copy the bytes as they are mutated when we call read() below
        mock_storage_imp.get_item = Mock(return_value=copy.deepcopy(file_buffer))

        storage = Storage(self.config, mock_storage_imp)

        file_service = FileService(self.config, storage)

        ## Seed the db with a file.
        ## TODO: Create fixtures to avoid doing this directly in the test
        file_id = self.db.run_query(
            """
        INSERT INTO files(uuid, file_size, file_name, mime_type, download_url) VALUES(%s, %s, %s, %s, %s)
        """,
            (
                "abcdefghikklmnop",
                None,
                "my-test-file.png",
                "image/png",
                "https://storage-container-id.provider.domain.com/as?query-param-one=random-param",
            ),
        ).get_last_row_id()

        filter = FileGetFilter(uuid="abcdefghikklmnop")

        file_get_result = file_service.get_file(filter)
        file = file_get_result.file
        file_bytes = file_get_result.file_bytes

        mock_storage_imp.get_item.assert_called_once_with("abcdefghikklmnop")

        self.assertEqual(
            file_bytes.read(),
            file_buffer.read(),
            "Should return the correct file bytes",
        )

        self.assertEqual(file.uuid, "abcdefghikklmnop", "Should return the correct file uuid")
        self.assertEqual(file.mime_type, "image/png", "Should return the correct mime_type")
        self.assertEqual(
            file.download_url,
            "https://storage-container-id.provider.domain.com/as?query-param-one=random-param",
        )
        self.assertEqual(file.file_name, "my-test-file.png")

        self.assertEqual(file.id, file_id, "Should return the correct file id")
