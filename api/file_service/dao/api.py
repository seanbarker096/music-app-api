from typing import Optional

from api.db.db import DB
from api.file_service.typings.typings import FileMetaCreateRequest, FileServiceFile


class FileServiceDAO:
    def __init__(self, config):
        ## Consider making this static, or maybe a flyweight or singleton
        self.db = DB(config)

    def create_file_meta(self, request: FileMetaCreateRequest) -> FileServiceFile:
        sql = """
        INSERT INTO files(uuid, file_size, file_name, mime_type, uri) VALUES(%s, %s, %s, %s, %s)
        """

        binds = (request.uuid, None, request.file_name, request.mime_type, None)

        insert_id = self.db.run_query(sql, binds).get_last_row_id()

        file = FileServiceFile(
            id=insert_id,
            uuid=request.uuid,
            file_name=request.file_name,
            mime_type=request.mime_type,
            uri=None,
        )

        return file

    def update_file(self):
        ...

    def get_file_by_uuid(self, uuid: str) -> FileServiceFile:
        sql = """
        SELECT id, uuid, file_size, file_name, mime_type, uri 
        FROM files 
        WHERE uuid = %s
        """

        binds = uuid

        result = self.db.run_query(sql, binds).get_rows()

        if len(result) > 1:
            raise Exception("More than one file returned")

        row = result[0]

        ## TODO: Maybe add a builder class to convert row to class
        file = FileServiceFile(
            id=row["id"],
            uuid=row["uuid"],
            file_name=row["file_name"],
            mime_type=row["mime_type"],
            file_size=row["file_size"],
            uri=row["uri"],
        )

        return file

    def files_get(self):
        ...
