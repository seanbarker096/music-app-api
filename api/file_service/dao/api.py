from typing import Optional

from api.db.db import DB
from api.db.utils.db_util import build_update_set_string
from api.file_service.typings.typings import (
    FileMetaCreateRequest,
    FileMetaUpdateRequest,
    FileServiceFile,
)
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import FileNotFoundException


class FileServiceDAO:
    def __init__(self, config):
        ## Consider making this static, or maybe a flyweight or singleton
        self.db = DB(config)

    def create_file_meta(self, request: FileMetaCreateRequest) -> FileServiceFile:
        sql = """
        INSERT INTO files(uuid, file_size, file_name, mime_type, url) VALUES(%s, %s, %s, %s, %s)
        """

        binds = (request.uuid, None, request.file_name, request.mime_type, None)

        insert_id = self.db.run_query(sql, binds).get_last_row_id()

        file = FileServiceFile(
            id=insert_id,
            uuid=request.uuid,
            file_name=request.file_name,
            mime_type=request.mime_type,
            url=None,
        )

        return file

    def update_file(self, request: FileMetaUpdateRequest) -> FileServiceFile:
        if not request.id:
            raise InvalidArgumentException(
                message="Must provide file id to update file meta",
                source="request.id",
            )

        try:
            file = self.get_file_by_id(request.id)
        except:
            raise Exception(
                "Failed to update file with id {request.id} because the file could not be found"
            )

        updates = []
        binds = []

        if request.url is not None and file.url != request.url:
            updates.append(
                "url = %s",
            )
            binds.append(request.url)
            file.url = request.url

        if len(updates) == 0:
            raise Exception(
                "Failed to update file because no fields provided to update in the file update request, or no fields in request have changed from original files fields"
            )

        set_string = build_update_set_string(updates)

        sql = f"""
            UPDATE files {set_string} WHERE id = {request.id}
        """

        db_result = self.db.run_query(sql, binds)

        if db_result.affected_rows() == 0:
            raise Exception("Failed to update any files for the provided request parameters")

        return file

    def get_file_by_uuid(self, uuid: str) -> FileServiceFile:
        sql = """
        SELECT id, uuid, file_size, file_name, mime_type, url 
        FROM files 
        WHERE uuid = %s
        """

        binds = uuid

        result = self.db.run_query(sql, binds).get_rows()

        if len(result) > 1:
            raise Exception(f"More than one file returned for uuid {uuid}")

        if len(result) == 0:
            raise FileNotFoundException(
                source=uuid, message=f"Could not find file with uuid {uuid}"
            )

        row = result[0]

        ## TODO: Maybe add a builder class to convert row to class
        file = FileServiceFile(
            id=row["id"],
            uuid=row["uuid"],
            file_name=row["file_name"],
            mime_type=row["mime_type"],
            file_size=row["file_size"],
            url=row["url"],
        )

        return file

    def get_file_by_id(self, id: int) -> FileServiceFile:
        sql = """
        SELECT id, uuid, file_size, file_name, mime_type, url 
        FROM files 
        WHERE id = %s
        """

        binds = (id,)

        result = self.db.run_query(sql, binds).get_rows()

        if len(result) > 1:
            raise Exception(f"More than one file returned for file id {id}")

        if len(result) == 0:
            raise FileNotFoundException(source=id, message=f"Could not find file with id {id}")

        row = result[0]

        ## TODO: Maybe add a builder class to convert row to class
        file = FileServiceFile(
            id=row["id"],
            uuid=row["uuid"],
            file_name=row["file_name"],
            mime_type=row["mime_type"],
            file_size=row["file_size"],
            url=row["url"],
        )

        return file

    def files_get(self):
        ...
