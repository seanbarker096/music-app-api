# import boto3
from typing import Dict

from flask import Flask

from api.authentication_service.api import JWTTokenAuthService
from api.db.db import DBConnection
from api.file_service.api import FileService
from api.midlayer.api import Midlayer


class Connections:
    def __init__(self, config):
        self.file_service = FileService(config)
        self.midlayer = Midlayer(config)
        self.auth_service = JWTTokenAuthService(config)


class FlaskApp(Flask):
    config: Dict[str, any]
    conns: Connections

    def __init__(self, config, conns=None):
        super().__init__(__name__)

        self.config["config_file"] = config
        self.conns = conns if conns else Connections(self.config)
