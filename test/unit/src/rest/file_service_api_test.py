import json
from unittest.mock import Mock

from api.file_service.api import AcceptedMimeTypes
from api.file_service.typings.typings import FileServiceFile, FileUploadResult

from rest import FileServiceAPITestCase


class FileServiceApiTest(FileServiceAPITestCase):
    def test_upload(self):
        file_response = FileServiceFile(
            id=1, uuid="a-random-file-uuid", mime_type=AcceptedMimeTypes.APP_OCTET_STREAM.value
        )

        mock_file_service_response = FileUploadResult(file=file_response)

        self.app.conns.file_service = Mock()
        self.app.conns.file_service.upload_file = Mock(return_value=mock_file_service_response)

        response = self.test_client.post(
            "/upload/",
            json={
                "uuid": "a-random-file-uuid",
                "mime_type": AcceptedMimeTypes.APP_OCTET_STREAM.value,
            },
        )

        response_body = response.json
        ##print(response.mimetype)

        self.assertEqual(
            response_body["file"]["uuid"],
            "a-random-file-uuid",
            "Should return the correct file uuid",
        )
        self.assertEqual(
            response_body["file"]["mime_type"],
            AcceptedMimeTypes.APP_OCTET_STREAM.value,
            "Should return the correct mime type",
        )
        self.assertEqual(
            response.location,
            "https://domain/api/file_service/0.1/upload/a-random-file-uuid",
            "Should return the correct url to upload the actual file to",
        )
        self.assertEqual(response.status_code, 200)

    #  def test_upload(self):
    #     response = self.test_client.get("/api/fileservice/0.1/test/")
    #     print(response.get_json())
    #     self.assertTrue(response.get_json()["test"])
