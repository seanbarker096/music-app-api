from test.integration import IntegrationTestCase

from api.file_service.storage.s3_storage_imp import S3GetRequest, S3StorageImp
from api.file_service.typings.typings import FileCreateRequest


class FileUploadIntegrationTestCase(IntegrationTestCase):
    def test_file_upload(self):
        s3_storage_imp = S3StorageImp(self.config)

        with open("../test_files/test_s3_upload.mp4", "rb") as bytes:
            request = FileCreateRequest(uuid="atestfileuuid", bytes=bytes)
            s3_upload_request = s3_storage_imp.process_upload_request(request)
            s3_storage_imp.save(s3_upload_request)

        # Now fetch object and assert on properties. The uuid was stored as the s3 key earlier
        get_request = S3GetRequest("atestfileuuid")

        file_bytes = s3_storage_imp.get_item(get_request)

        # The representation of bytes objects uses the literal format (b'...')
        # TODO: Inspect the format outputted by both of these and check how to assert they are the same
        assert bytes.raw == file_bytes.getvalue()
