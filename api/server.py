import os
from configparser import ConfigParser

import flask
from flask_cors import CORS

from api.application import FlaskApp
from api.debugger import initialize_flask_server_debugger_if_needed
from api.rest import auth_api, file_service_api, posts_api

initialize_flask_server_debugger_if_needed()


config = ConfigParser(allow_no_value=True, interpolation=None)
config.optionxform = str

env = os.environ.get("ENVIRONMENT", "dev")
filename = os.path.join(flask.helpers.get_root_path(__name__), "config", f"{env}.cfg")

config.read(filename)

app = FlaskApp(config)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000
origin = config.get("cors", "origin")
CORS(app, origins=[origin])

app.register_blueprint(file_service_api.blueprint, url_prefix="/api/fileservice/0.1")
app.register_blueprint(posts_api.blueprint, url_prefix="/api/posts/0.1")
app.register_blueprint(auth_api.blueprint, url_prefix="/api/auth/0.1")


@app.after_request
def add_new_auth_token(response):
    """If a new auth token was generated during any given request (e.g. if it expired and refresh token used to generate new one), add it to the response header"""
    if flask.g.new_auth_token:
        response.headers["Authorization"] = f"Bearer {flask.g.new_auth_token}"


if __name__ == "__main__":
    app.run()
