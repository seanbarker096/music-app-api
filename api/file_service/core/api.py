import json

from api.file_service.storage.api import Storage


class FileService():
    def __init__(self, config):
        self.storage = Storage(config)
        self.test = 'adsadasdasd'


    def upload_to_storage(self, file_uuid: str ):
        # self.storage.save()
        return {'file_uuid': file_uuid}
