import os
from test.integration import IntegrationTestCase

from api.file_service.api import AcceptedMimeTypes
from api.file_service.storage.s3_storage_imp import S3GetRequest, S3StorageImp
from api.file_service.typings.typings import (
    FileDownloadURLGetRequest,
    FileUploadRequest,
)


class FileUploadIntegrationTestCase(IntegrationTestCase):
    def tearDown(self):
        ## Clear aws
        return super().tearDown()

    def test_save(self):
        s3_storage_imp = S3StorageImp(self.config)

        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../../test_files/test_s3_upload.mp4",
            ),
            "rb",
        ) as bytes:
            byte_stream = bytes.read()

            request = FileUploadRequest(
                id=1234,
                file_name="my-test-file.mp4",
                mime_type="mp4",
                uuid="atestfileuuid",
                bytes=byte_stream,
            )
            s3_upload_request = s3_storage_imp.process_upload_request(request)
            s3_storage_imp.save(s3_upload_request)

        # Now fetch object and assert on properties. The uuid was stored as the s3 key earlier
        file_bytes = s3_storage_imp.get_item(lookup_key="atestfileuuid")

        assert file_bytes.getvalue() == byte_stream

    def test_get_download_url(self):
        s3_storage_imp = S3StorageImp(self.config)

        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../../test_files/test_s3_upload.mp4",
            ),
            "rb",
        ) as bytes:
            byte_stream = bytes.read()

            request = FileUploadRequest(
                id=1234,
                file_name="my-test-file.mp4",
                uuid="atestfileuuid",
                mime_type="mp4",
                bytes=byte_stream,
            )
            s3_upload_request = s3_storage_imp.process_upload_request(request)
            s3_storage_imp.save(s3_upload_request)

        # Now fetch the download url
        request = FileDownloadURLGetRequest(file_identifier="atestfileuuid")

        download_url = s3_storage_imp.get_file_url(request)

        self.assertTrue(isinstance(download_url, str))
        self.assertTrue(len(download_url) > 0)
        self.assertTrue(".s3.amazonaws.com/atestfileuuid?" in download_url)
