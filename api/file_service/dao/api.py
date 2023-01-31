from typing import Dict, List, Optional

from api.db.db import DB
from api.db.utils.db_util import (
    assert_row_key_exists,
    build_update_set_string,
    build_where_query_string,
)
from api.file_service.typings.typings import (
    FileMetaCreateRequest,
    FileMetaUpdateRequest,
    FileServiceFile,
    FilesGetFilter,
)
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import FileNotFoundException


class FileDBAlias:
    FILE_ID = "file_id"
    FILE_UUID = "file_uuid"
    FILE_FILE_SIZE = "file_file_size"
    FILE_FILE_NAME = "file_file_name"
    FILE_MIME_TYPE = "file_mime_type"
    FILE_URL = "file_url"


class FileServiceDAO:
    FILE_SELECTS = [
        "id as " + FileDBAlias.FILE_ID,
        "uuid as " + FileDBAlias.FILE_UUID,
        "file_size as " + FileDBAlias.FILE_FILE_SIZE,
        "file_name as " + FileDBAlias.FILE_FILE_NAME,
        "mime_type as " + FileDBAlias.FILE_MIME_TYPE,
        "url as " + FileDBAlias.FILE_URL,
    ]

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
            file = self.files_get(filter=FilesGetFilter(ids=[request.id]))[0]

            if not file:
                raise Exception()
        except:
            raise FileNotFoundException(
                source="",
                message=f"Failed to update file with id {request.id} because the file could not be found",
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

    def files_get(self, filter: FilesGetFilter) -> List[FileServiceFile]:
        selects = f"""
            SELECT {', '.join(self.FILE_SELECTS)} 
            FROM files
        """

        wheres = []
        binds = []

        if filter.ids:
            wheres.append("id in %s")
            binds.append(filter.ids)

        if filter.uuids:
            wheres.append("uuid in %s")
            binds.append(filter.uuids)

        if not filter.uuids and not filter.ids:
            raise InvalidArgumentException(
                "Must provide at least one filter field when getting files", source="filter"
            )

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        rows = self.db.run_query(sql, binds).get_rows()

        files = []
        for row in rows:
            file = self._build_file_from_db_row(row)
            files.append(file)

        return files

    # def get_files_by_id(self, id: int) -> FileServiceFile:
    #     sql = """
    #     SELECT id, uuid, file_size, file_name, mime_type, url
    #     FROM files
    #     WHERE id = %s
    #     """

    #     binds = (id,)

    #     result = self.db.run_query(sql, binds).get_rows()

    #     if len(result) > 1:
    #         raise Exception(f"More than one file returned for file id {id}")

    #     if len(result) == 0:
    #         raise FileNotFoundException(source=id, message=f"Could not find file with id {id}")

    #     row = result[0]

    #     ## TODO: Maybe add a builder class to convert row to class
    #     file = FileServiceFile(
    #         id=row["id"],
    #         uuid=row["uuid"],
    #         file_name=row["file_name"],
    #         mime_type=row["mime_type"],
    #         file_size=row["file_size"],
    #         url=row["url"],
    #     )

    #     return file

    def _build_file_from_db_row(self, db_row: Dict[str, any]) -> FileServiceFile:
        assert_row_key_exists(db_row, FileDBAlias.FILE_ID)
        file_id = int(db_row[FileDBAlias.FILE_ID])

        assert_row_key_exists(db_row, FileDBAlias.FILE_UUID)
        file_uuid = db_row[FileDBAlias.FILE_UUID]

        assert_row_key_exists(db_row, FileDBAlias.FILE_FILE_SIZE)
        file_size = (
            int(db_row[FileDBAlias.FILE_FILE_SIZE]) if db_row[FileDBAlias.FILE_FILE_SIZE] else None
        )

        assert_row_key_exists(db_row, FileDBAlias.FILE_FILE_NAME)
        file_name = db_row[FileDBAlias.FILE_FILE_NAME]

        assert_row_key_exists(db_row, FileDBAlias.FILE_MIME_TYPE)
        mime_type = db_row[FileDBAlias.FILE_MIME_TYPE]

        assert_row_key_exists(db_row, FileDBAlias.FILE_URL)
        file_url = db_row[FileDBAlias.FILE_URL] if db_row[FileDBAlias.FILE_URL] else None

        return FileServiceFile(
            id=file_id,
            uuid=file_uuid,
            file_name=file_name,
            file_size=file_size,
            mime_type=mime_type,
            url=file_url,
        )
