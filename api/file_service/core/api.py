from api.file_service.storage.api import Storage


class FileService():
    def __init__(self, config):
        self.storage = Storage(self, config)


    def upload_to_storage(self):
        self.storage.save()
