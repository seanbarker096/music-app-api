from typing import Optional

from api.db.db import DB
from api.file_service.typings.typings import FileMetaCreateRequest, FileServiceFile


class FileServiceDAO:
    def __init__(self, config):
        ## Consider making this static, or maybe a flyweight or singleton
        self.db = DB(config)

    def create_file_meta(self, request: FileMetaCreateRequest) -> FileServiceFile:
        sql = """
        INSERT INTO files(uuid, file_size, mime_type, download_url) VALUES(%s, %s, %s, %s)
        """

        binds = (request.uuid, None, request.mime_type, None)

        insert_id = self.db.run_query(sql, binds)

        file = FileServiceFile(
            id=insert_id,
            uuid=request.uuid,
            mime_type=request.mime_type,
            download_url=None,
        )

        return file

    def update_file(self):
        ...
