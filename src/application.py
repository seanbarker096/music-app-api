import boto3
from flask import Flask, json

from debugger import initialize_flask_server_debugger_if_needed

initialize_flask_server_debugger_if_needed()

app = Flask(__name__)

@app.route("/api/")

def hello_world():
    response = {"message": "this has now changed erg"}
    return json.jsonify(response)

@app.route("/api/s3/")

def get_s3_file():
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)

    data = open('./assets/mic.png', 'rb')
    s3.Bucket('seansgreattestbucket').put_object(Key='mic.png', Body=data)

# Run the application
if __name__ == "__main__":
    app.run()
