import os
from test.integration import IntegrationTestCase

from api.file_service.api import AcceptedMimeTypes
from api.file_service.storage.s3_storage_imp import S3GetRequest, S3StorageImp
from api.file_service.typings.typings import FileCreateRequest


class FileUploadIntegrationTestCase(IntegrationTestCase):
    def test_file_upload(self):
        s3_storage_imp = S3StorageImp(self.config)

        with open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "../test_files/test_s3_upload.mp4"
            ),
            "rb",
        ) as bytes:
            byte_stream = bytes.read()

            request = FileCreateRequest(
                uuid="atestfileuuid",
                bytes=byte_stream,
                mime_type=AcceptedMimeTypes.APP_OCTET_STREAM.value,
            )
            s3_upload_request = s3_storage_imp.process_upload_request(request)
            s3_storage_imp.save(s3_upload_request)

            # Now fetch object and assert on properties. The uuid was stored as the s3 key earlier
            get_request = S3GetRequest("atestfileuuid")

            file_bytes = s3_storage_imp.get_item(get_request)

        assert file_bytes.getvalue() == byte_stream
