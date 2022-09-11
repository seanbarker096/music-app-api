from cmath import exp


class FileServiceAPI():
    def __init__(self):
        return
        
    def upload(self, request):
        # 1. Parse the request object with the upload meta data
        if not isinstance(request.uuid, str):
            raise Exception('uuid argument must be a string')

        if len(request.uuid) == 0:
            raise Exception('uuid must not be empty string') ##update ot check its uuid4
        

        # 2. Extract uuid and upload to S3
        uuid4 = request.uuid

        # 3. Take uuid and s3 download url and store in the resource mapping table

        # 4. Return the fileservice GET url which will be used to stream the video back to the user
