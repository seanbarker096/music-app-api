from test.unit import TestCase
from unittest.mock import Mock

from api.file_service.api import AcceptedMimeTypes
from api.file_service.storage.api import Storage
from api.file_service.storage.s3_storage_imp import S3UploadRequest
from api.file_service.typings.typings import (
    FileDownloadURLGetRequest,
    FileServiceFile,
    FileUploadRequest,
    FileUploadResult,
)


class StorageUnitTestCase(TestCase):
    def test_get_download_url(self):
        request = FileDownloadURLGetRequest(file_identifier="myfile123")

        mock_storage_imp = Mock()
        mock_storage_imp.get_file_download_url = Mock(return_value="www.test.com/download/12345")

        storage = Storage(self.config, mock_storage_imp)

        result = storage.get_file_download_url(request)

        mock_storage_imp.get_file_download_url.assert_called_once_with(request)
        assert result == "www.test.com/download/12345"

    def test_upload_file(self):
        file_upload_request = FileUploadRequest(
            id=1234,
            uuid="fileuuid",
            bytes=b"makesomebytesbaby",
            mime_type=AcceptedMimeTypes.APP_OCTET_STREAM.value,
            file_size=222,
        )

        mock_storage_imp = Mock()

        mock_storage_imp.save = Mock()
        storage_imp_save_request = S3UploadRequest(bytes=b"makesomebytesbaby", key="fileuuid")

        mock_storage_imp.process_upload_request = Mock(return_value=storage_imp_save_request)

        mock_storage_imp.get_file_download_url = Mock(return_value="www.test.com/download/12345")

        storage = Storage(config=self.config, storage_imp=mock_storage_imp)

        result = storage.upload_file(file_upload_request)

        mock_storage_imp.save.assert_called_once_with(storage_imp_save_request)

        self.assertEqual(result.download_url, "www.test.com/download/12345")
        self.assertEqual(result.file_size, 222)
        self.assertEqual(result.mime_type, AcceptedMimeTypes.APP_OCTET_STREAM.value)
        self.assertEqual(result.id, 1234)

    def test_get_file(self):
        ...
