from test.unit import TestCase
from unittest.mock import Mock

from api.file_service.storage.api import Storage


class FileUploadIntegrationTestCase(TestCase):
    def test_get_download_url(self):
        request = FileGetRequest()

        mock_storage_imp = Mock()
        mock_storage_imp.get_file_download_url = Mock(return_value="www.test.com/download/12345")
        mock_storage_imp.get_file_download_url.assert_called_once_with(GetDownloadUrlRequest)

        storage = Storage(config=self.config, storage_imp=mock_storage_imp)

        result = storage.get_file(request)

        assert request.download_url == "www.test.com/download/12345"

    def test_get_file(self):
        ...

    def test_upload_file(self):
        file_upload_request = FileUploadRequest()
        response = FileUploadResult()  # should contain download url

        mock_storage_imp = Mock()
        mock_storage_imp.save = Mock(return_value=response)

        mock_storage_imp.save.assert_called_once_with(file_upload_request)

        storage = Storage(config=self.config, storage_imp=mock_storage_imp)

        result = storage.upload_file(file_upload_request)

        assert result.download_url == "www.test.com/download/12345"
