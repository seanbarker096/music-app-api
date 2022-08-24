from flask import Flask, json

from debugger import initialize_flask_server_debugger_if_needed

initialize_flask_server_debugger_if_needed()

app = Flask(__name__)

@app.route("/api/")

def hello_world():
    response = {"message": "this has now changed asdfsdssafdasdffsdd"}
    return json.jsonify(response)

# Run the application
if __name__ == "__main__":
    app.run()
