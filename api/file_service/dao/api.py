from typing import Dict

import flask

from api.db.config import DBConfig
from api.db.db import DB
from api.file_service.typings.typings import FileCreateRequest, FileServiceFile


class FileServiceDAO():
    def __init__(self):
        pass
    
    def create_file(self, request: FileCreateRequest)->FileServiceFile:

        ## TODO: Handle case where download_url not being set (just uploading meta)
        sql  = "INSERT INTO files(uuid, file_size, mime_type, download_url) VALUES(%s, %d, %s, %d)"
        binds = (request.uuid, request.file_size, request.mime_type, request.download_url)

        file_id = flask.current_app.conns.db.run_query(sql, binds)

        file = FileServiceFile(id=file_id, uuid=request.uuid, mime_type=request.mime_type, file_size=request.file_size)

        return file


    def update_file():
        ...
