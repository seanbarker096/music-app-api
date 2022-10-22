import json

import flask
from api.file_service.typings.typings import FileUpdateRequest, FileUploadRequest

blueprint = flask.Blueprint("file_service", __name__)


@blueprint.route("/upload_file_meta/", methods=["POST"])
def upload_file_meta():
    """Upload the file meta data and return the file upload location."""

    json_data = flask.request.json

    # TODO: Validate the request
    request = FileUploadRequest(
        uuid=json_data["uuid"], mime_type=json_data["mime_type"], file_size=None
    )

    file_upload_result = flask.current_app.conns.file_service.upload_file(request=request)

    response = {}
    response["file"] = vars(file_upload_result.file)

    response = flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )

    ## Set Location header to be url to upload the file to
    response.location = f"http://192.168.1.217:5000/api/fileservice/0.1/upload/{json_data['uuid']}"

    return response


@blueprint.route("/upload/<string:file_uuid>", methods=["PATCH"])
def upload_file_bytes(file_uuid: str):
    """Upload the file and create the download url."""
    ## TODO: BUild the request using file_uuid and bytes we receive

    mime_type = flask.request.headers.get("Content-Type")
    file = flask.request.files["file"]

    if not file:
        raise Exception("No file provided")

    byte_stream = file.read()

    file_upload_request = FileUploadRequest(uuid=file_uuid, bytes=byte_stream, mime_type=mime_type)

    flask.current_app.conns.file_service.upload_file(request=file_upload_request)


@blueprint.route("/test/", methods=["POST"])
def test():
    print(f"request\n {flask.request.form}")
    print(f"files\n {flask.request.files['bytes'].read()}")
    response = flask.make_response({"test": 3333})
    return response
