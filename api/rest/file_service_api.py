import io
import json
import os

import flask
from api.file_service.typings.typings import FileCreateRequest, FileGetFilter

blueprint = flask.Blueprint("file_service", __name__)

# TODO: Limit file extensions accepted (see https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/)
# TODO: use secure_filename function from flask
@blueprint.route("/files/upload_file/", methods=["POST"])
def upload_file():
    """Upload the file meta data and return the file upload location. Accepts a multipart/form-data request"""
    print("test")
    form_data = flask.request.form
    file = flask.request.files["file"]

    if not file:
        raise Exception("No file provided")

    byte_stream = file.read()

    # TODO: Validate the request
    request = FileCreateRequest(
        uuid=form_data["uuid"],
        file_name=form_data["file_name"],
        mime_type=form_data["mime_type"],
        bytes=byte_stream,
    )

    result = flask.current_app.conns.file_service.create_file(request=request)

    response = {}
    response["file"] = vars(result.file)

    response = flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )

    return response


@blueprint.route("/files/<string:file_uuid>/", methods=["GET"])
def get_file(file_uuid: str):
    """Get file from the file service"""
    get_filter = FileGetFilter(uuid=file_uuid)

    ## TODO: Adjust this conver the bytes into a file before returning. Use mime type to work out the extension
    get_result = flask.current_app.conns.file_service.get_file(filter=get_filter)

    return flask.current_app.response_class(
        response=get_result.file_bytes, status=200, mimetype=get_result.file.mime_type
    )


@blueprint.route("/files/test/", methods=["GET"])
def test():

    with open(
        os.path.dirname(os.path.realpath(__file__)) + "/../../test/test_files/nav-bar.png", "rb"
    ) as f:
        bytes = io.BytesIO(f.read())

    print(bytes)

    return flask.send_file(bytes, mimetype="image/png")
