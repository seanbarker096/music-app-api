from api.file_service.storage.storage_imp import StorageImp


class S3StorageImp(StorageImp):
    def __init__(self):
        pass

    def save():
        ...
        #s3 = boto3.resource('s3')
#     for bucket in s3.buckets.all():
#         print(bucket.name)

#     data = open('./assets/mic.png', 'rb')
#     s3.Bucket('seansgreattestbucket').put_object(Key='mic.png', Body=data)
