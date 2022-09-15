import json
import os
from configparser import ConfigParser

import flask

from api.application import FlaskApp
from api.debugger import initialize_flask_server_debugger_if_needed

initialize_flask_server_debugger_if_needed()


config = ConfigParser(allow_no_value=True, interpolation=None)
config.optionxform = str

env = os.environ.get("ENVIRONMENT", "dev")
filename = os.path.join(flask.helpers.get_root_path(__name__), "config", f'{env}.cfg')

config.read(filename)

app = FlaskApp(config)

## TODO: Use blueprints

@app.route("/api/")
def hello_world():
    response = {"message": "this has now changed erg"}
    return json.jsonify(response)

if __name__ == "__main__":
    app.run()
