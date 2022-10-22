import json

import flask
from api.file_service.typings.typings import (
    FileCreateAndUploadRequest,
    FileUpdateRequest,
    FileUploadRequest,
)

blueprint = flask.Blueprint("file_service", __name__)


@blueprint.route("/upload_file/", methods=["POST"])
def upload_file():
    """Upload the file meta data and return the file upload location."""

    form_data = flask.request.form
    file = flask.request.files["file"]
    mime_type = flask.request.headers.get("Content-Type")

    if not file:
        raise Exception("No file provided")

    byte_stream = file.read()

    # TODO: Validate the request
    request = FileCreateAndUploadRequest(
        uuid=form_data["uuid"], mime_type=mime_type, bytes=byte_stream, file_size=None
    )

    result = flask.current_app.conns.file_service.create_and_upload_file(request=request)

    response = {}
    response["file"] = vars(result.file)

    response = flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )

    return response


# @blueprint.route("/upload/<string:file_uuid>", methods=["PATCH"])
# def upload_file_bytes(file_uuid: str):
#     """Upload the file and create the download url."""
#     ## TODO: BUild the request using file_uuid and bytes we receive

#     mime_type = flask.request.headers.get("Content-Type")
#     file = flask.request.files["file"]

#     if not file:
#         raise Exception("No file provided")

#     byte_stream = file.read()

#     file_upload_request = FileUploadRequest(uuid=file_uuid, bytes=byte_stream, mime_type=mime_type)

#     upload_file_result = flask.current_app.conns.file_service.upload_file(
#         request=file_upload_request
#     )

#     return flask.current_app.response_class(
#         response=json.dumps(upload_file_result), status=200, mimetype="application/json"
#     )


@blueprint.route("/test/", methods=["POST"])
def test():
    print(f"request\n {flask.request.form}")
    print(f"files\n {flask.request.files['bytes'].read()}")
    response = flask.make_response({"test": 3333})
    return response
