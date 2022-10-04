from io import BytesIO

import boto3
from exceptions.exceptions import InvalidArgumentException

from api.file_service.storage.storage_imp import StorageImp


class S3UploadRequest(object):
    def __init__(self, bytes: bytes, key: str):
        self.bytes = bytes
        self.key = key


class S3GetRequest(object):
    def __init__(self, key: str):
        self.key = key


class S3StorageImp(StorageImp):
    def __init__(self, config):
        self.bucket = config["config_file"]["s3"].get("file-service-bucket-arn")
        self.config = config
        self.connection = None

    def _get_s3_connection(self):
        config_file = self.config["config_file"]
        s3_access_key = config_file.get("aws", "aws_access_key_id")
        s3_secret_key = config_file.get("aws", "aws_secret_access_key")

        return boto3.Session(
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_key,
            aws_session_token=None,
        )

    def save(self, request: S3UploadRequest) -> any:
        # TODO: Also get the metadata saved using ExtraArgs param to _
        session = self._get_s3_connection()
        s3 = session.resource("s3")

        s3_object = s3.Bucket(self.bucket).put_object(Key=request.key, Body=request.bytes)

        return s3_object

    def get_item(self, request: S3GetRequest) -> BytesIO:
        session = self._get_s3_connection()
        s3 = session.resource("s3")

        bytes_obj = BytesIO()
        s3.Bucket(self.bucket).download_fileobj(Key=request.key, Fileobj=bytes_obj)

        return bytes_obj

    ## Shouldn't need to know about all the types of requests that could come in. Should just try to extract what it needs regardless of the object type. If it can't find it then get error. Hence we will validate the object carefully so strict types and request types as input args not required

    ## Ive basically implemented a bridge pattern here. Had possibilty of either creating a huge request object with optional fields for all possible requests for any given storage implementation, which allows us to define the type for the request object coming in here.
    # Alternatively i could accept a very generic reuqest object to account for the fact that the storage implementation requirements for the information they need to do an upload can vary massively. Then we indirectly enforce strictness and valid requests at the implementation level via run time validation
    def process_upload_request(self, request: object) -> S3UploadRequest:

        if not request.bytes or not isinstance(request.bytes, bytes):
            raise InvalidArgumentException(
                f"Failed to process upload request to S3. Invalid value {request.bytes} for parameter bytes",
                "request.bytes",
            )

        if not isinstance(request.uuid, str) or request.uuid == "":
            raise InvalidArgumentException(
                f"Failed to process upload request to S3. Invalid value {request.uuid} for parameter bytes",
                "request.uuid",
            )

        s3_upload_request = S3UploadRequest(bytes=request.bytes, key=request.uuid)

        return s3_upload_request
