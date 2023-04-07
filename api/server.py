import os
import uuid
from configparser import ConfigParser

import flask
from flask_cors import CORS

from api.application import FlaskApp
from api.db.db import DBConnection
from api.debugger import initialize_flask_server_debugger_if_needed
from api.rest import (
    auth_api,
    features_api,
    file_service_api,
    performances_api,
    performer_api,
    posts_api,
    tags_api,
    users_api,
)
from api.utils.rest_utils import add_token_headers, after_request_setup

initialize_flask_server_debugger_if_needed()


config = ConfigParser(allow_no_value=True, interpolation=None)
config.optionxform = str

env = os.environ.get("ENVIRONMENT", "dev")
filename = os.path.join(flask.helpers.get_root_path(__name__), "config", f"{env}.cfg")

config.read(filename)

app = FlaskApp(config)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1000 * 1000  # TODO: Come up with sensible max file size
origin = config.get("cors", "origin")
CORS(app, origins=[origin])



app.register_blueprint(file_service_api.blueprint, url_prefix="/api/fileservice/0.1")
app.register_blueprint(posts_api.blueprint, url_prefix="/api/posts/0.1")
app.register_blueprint(auth_api.blueprint, url_prefix="/api/auth/0.1")
app.register_blueprint(users_api.blueprint, url_prefix="/api/users/0.1")
app.register_blueprint(performer_api.blueprint, url_prefix="/api/performers/0.1")
app.register_blueprint(features_api.blueprint, url_prefix="/api/features/0.1")
app.register_blueprint(tags_api.blueprint, url_prefix="/api/tags/0.1")
app.register_blueprint(performances_api.blueprint, url_prefix="/api/performances/0.1")


@app.before_request
def create_db_connection():
    flask.request.request_id = str(uuid.uuid4())
    DBConnection.instance(DBConnection, config=config)

@app.after_request
def after_request(response):
    print("RUNNING AFTER REQUEST")
    DBConnection.instance(DBConnection).close()
    return after_request_setup(response)


if __name__ == "__main__":
    app.run()
