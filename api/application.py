# import boto3
from typing import Dict

from flask import Flask

from api.file_service.api import FileService


class Connections:
    def __init__(self, config):
        self.file_service = FileService(config)


class FlaskApp(Flask):
    config: Dict[str, any]
    conns: Connections

    def __init__(self, config, conns=None):
        super().__init__(__name__)

        self.config["config_file"] = config
        self.conns = conns if conns else Connections(self.config)
