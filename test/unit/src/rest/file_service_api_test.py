import copy
import io
import os
from test.test_utils import set_up_patches
from unittest.mock import Mock

from rest.base import APITestCase

from api.file_service.api import AcceptedMimeTypes
from api.file_service.typings.typings import (
    FileCreateResult,
    FileGetResult,
    FileServiceFile,
)

## Setup patches before the test case is initialised, which results in the blueprint file being called and defines functions before they can be patched
set_up_patches()

from api.rest import file_service_api


class FileServiceAPITestCase(APITestCase):
    BLUEPRINT = file_service_api.blueprint

    def setUp(self):
        super().setUp()


class FileServiceApiTest(FileServiceAPITestCase):

    test_files = os.path.dirname(os.path.realpath(__file__)) + "/../../../test_files"

    def test_upload_file(self):
        file_response = FileServiceFile(
            id=1,
            uuid="a-random-file-uuid",
            file_name="my-test-file.txt",
            mime_type=AcceptedMimeTypes.APP_OCTET_STREAM.value,
        )

        expected_response = FileCreateResult(file=file_response)

        self.app.conns.file_service = Mock()
        self.app.conns.file_service.create_file = Mock(return_value=expected_response)

        data = {
            "uuid": "a-random-file-uuid",
            "mime_type": AcceptedMimeTypes.APP_OCTET_STREAM.value,
            "file_name": "my-test-file.txt",
            "file": open(self.test_files + "/nav-bar.png", "rb"),
        }

        response = self.test_client.post("/files/upload_file/", data=data)

        ## To do: create some sort of json -> dict encoder to avoid ahving to do this everytime
        expected_json_response = {}
        expected_json_response["file"] = vars(expected_response.file)

        response_body = response.json

        self.assertEqual(
            response_body,
            expected_json_response,
            "Should return the correct response",
        )

        self.assertEqual(response.status_code, 200)

    def test_file_get(self):

        expected_file_service_file = FileServiceFile(
            id=1,
            uuid="12345abc",
            file_name="my-test-file.png",
            mime_type="image/png",
            file_size=None,
            url="https://storage-container-id.provider.domain.com/as?query-param-one=random-param",
        )

        bytes = io.BytesIO(b"some intial bytes")
        expected_file_get_response = FileGetResult(
            file=expected_file_service_file, file_bytes=copy.copy(bytes)
        )

        self.app.conns.file_service = Mock()
        self.app.conns.file_service.get_file = Mock(return_value=expected_file_get_response)

        response = self.test_client.get("/files/12345abc/")

        bytes_response = response.data

        self.assertEqual(bytes.read(), bytes_response, "Should return the correct file byte stream")
