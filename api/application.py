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


#     @app.route("/api/")
#     def hello_world():
#     response = {"message": "this has now changed erg"}
#     return json.jsonify(response)

# @app.route("/api/s3/")

# def get_s3_file():
#     s3 = boto3.resource('s3')
#     for bucket in s3.buckets.all():
#         print(bucket.name)

#     data = open('./assets/mic.png', 'rb')
#     s3.Bucket('seansgreattestbucket').put_object(Key='mic.png', Body=data)

# @app.route("/db/")
# def hit_db():
#     response = DB.hit_db()
#     return response
