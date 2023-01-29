import io
import json
import os

import flask

import api
from api.file_service.typings.typings import FileCreateRequest, FileGetFilter
from api.utils.rest_utils import get_set_request_param

blueprint = flask.Blueprint("file_service", __name__)

auth = api.utils.rest_utils.auth

# TODO: Limit file extensions accepted (see https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/)
# TODO: use secure_filename function from flask. Rename to file_upload
@blueprint.route("/files/upload_file/", methods=["POST"])
@auth
def upload_file():
    """Upload the file meta data and return the file upload location. Accepts a multipart/form-data request"""
    print("test")
    form_data = flask.request.form
    file = flask.request.files["file"]
    print("file", file)

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


# TODO: Rename to file_get
@blueprint.route("/file_bytes/<string:file_uuid>/", methods=["GET"])
@auth
def get_file_bytes(file_uuid: str):
    """Get file from the file service"""
    get_filter = FileGetFilter(uuid=file_uuid)

    ## TODO: Adjust this conver the bytes into a file before returning. Use mime type to work out the extension
    get_result = flask.current_app.conns.file_service.get_file(filter=get_filter)

    return flask.current_app.response_class(
        response=get_result.file_bytes, status=200, mimetype=get_result.file.mime_type
    )


# TODO: Rename to file_get
@blueprint.route("/files/", methods=["GET"])
@auth
def get_files():
    """Get file from the file service"""

    file_uuids = get_set_request_param(parameter_name="uuids[]", type=str)

    file_ids = get_set_request_param(parameter_name="ids[]", type=int)

    if file_ids and len(file_ids) == 0:
        raise Exception("Invalid request. Must provide at least one file id")

    if file_uuids and len(file_uuids) == 0:
        raise Exception("Invalid request. Must provide at least one file uuid")

    if file_ids and file_uuids:
        raise Exception("Cannot query using both file_ids and uuids")

    if not file_ids and not file_uuids:
        raise Exception("Must provide either file_ids or file_uuids when getting a file")

    ## TODO: Make this backend work with multiple files when use case arises. For now we hack it
    ## as api was built for a single file initially

    get_filter = FileGetFilter(uuid=file_uuids[0]) if file_uuids else FileGetFilter(file_ids[0])

    ## TODO: Adjust this conver the bytes into a file before returning. Use mime type to work out the extension
    get_result = flask.current_app.conns.file_service.get_file(filter=get_filter)

    response = {}

    response["files"] = [vars(get_result.file)]

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/files/test/", methods=["GET"])
def test():

    return flask.current_app.response_class(response={test: "it worked!"}, status=200)
