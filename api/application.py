# import boto3
from flask import Flask, json

from api.file_service.api import FileServiceAPI


class FlaskApp(Flask):
    def __init__(self, config):
        super().__init__(__name__)

        self.config['config_file'] = config
        print(self.config['config_file'])

        self.conns = Connections(self.config)

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


class Connections():
    def __init__(self, config):
        self.file_service = FileServiceAPI(config)
