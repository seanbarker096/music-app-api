import os
from configparser import ConfigParser

import flask

from api.application import FlaskApp
from api.debugger import initialize_flask_server_debugger_if_needed
from api.rest import file_service_api

initialize_flask_server_debugger_if_needed()


config = ConfigParser(allow_no_value=True, interpolation=None)
config.optionxform = str

env = os.environ.get("ENVIRONMENT", "dev")
filename = os.path.join(flask.helpers.get_root_path(__name__), "config", f'{env}.cfg')

## Get IPs from environment variables
db_host = os.environ.get("ENVIRONMENT", "CONTAINER_IP")

config.read(filename)
config['db']['host'] = db_host

app = FlaskApp(config)

app.register_blueprint(file_service_api.blueprint, url_prefix="/api/fileservice/0.1")

if __name__ == "__main__":
    app.run()
