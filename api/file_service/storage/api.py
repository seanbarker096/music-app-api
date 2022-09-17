from api.file_service.storage.s3_storage_imp import S3StorageImp
from api.file_service.storage.storage_imp import StorageImp


class Storage():
    def __init__(self, config):

        # determine storage impementation from environment vars
        self.config = config

        ## might need to use config parser syntax here
        implementation_type = self.config['config_file']['file-service'].get('storage-platform', 's3')

        match implementation_type:
            case 's3':
                self.storage_imp = S3StorageImp()

    def save(self):
        self.storage_imp.save()
    