import json
from turtle import down
from typing import Optional

import flask

from api.db.config import DBConfig
from api.db.db import DB
from api.file_service.typings.typings import FileCreateRequest, FileServiceFile


class FileServiceDAO():

    def __init__(self, config):
        ## Consider making this static, or maybe a flyweight or singleton
        self.db = DB(config)

    '''Download url is present if file was created in s3 before this'''
    ## TODO: Update return type
    def create_file(self, request: FileCreateRequest, download_url: Optional[str])->FileServiceFile:

        ## TODO: Handle case where download_url not being set (just uploading meta)
        sql  = """
        INSERT INTO files(uuid, file_size, mime_type, download_url) VALUES(%s, %s, %s, %s)
        """

        binds = (request.uuid, request.file_size, request.mime_type, download_url)

        insert_id = self.db.run_query(sql, binds)

        file = FileServiceFile(id=insert_id, uuid=request.uuid, mime_type=request.mime_type, file_size=request.file_size, download_url=download_url) 

        return file


    def update_file():
        ...
