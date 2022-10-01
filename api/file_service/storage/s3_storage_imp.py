from api.file_service.storage.storage_imp import StorageImp


class S3UploadRequest(object):
    def __init__(self, bytes: bytes):
        self.bytes = bytes


class S3StorageImp(StorageImp):
    def __init__(self):
        pass

    def save(self, request: S3UploadRequest):
        return None

    ## Shouldn't need to know about all the types of requests that could come in. Should just try to extract what it needs regardless of the object type. If it can't find it then get error. Hence we will validate the object carefully so strict types and request types as input args not required

    ## Ive basically implemented a bridge pattern here. Had possibilty of either creating a huge request object with optional fields for all possible requests for any given storage implementation, which allows us to define the type for the request object coming in here.
    # Alternatively i could accept a very generic reuqest object to account for the fact that the storage implementation requirements for the information they need to do an upload can vary massively. Then we indirectly enforce strictness and valid requests at the implementation level via run time validation
    def process_upload_request(self, request: object) -> S3UploadRequest:

        if not request.bytes or not isinstance(request.bytes, bytes):
            raise Exception("Failed to process upload request. Invalid value for parameter bytes")

        s3_upload_request = S3UploadRequest(request.bytes)
        s3_upload_request.bytes = request.bytes

        return s3_upload_request

        # s3 = boto3.resource('s3')


#     for bucket in s3.buckets.all():
#         print(bucket.name)

#     data = open('./assets/mic.png', 'rb')
#     s3.Bucket('seansgreattestbucket').put_object(Key='mic.png', Body=data)
