import json

import flask

import api
from api.file_service.typings.typings import FileCreateRequest, FilesGetFilter
from api.utils.rest_utils import (
    class_to_dict,
    error_handler,
    process_api_set_request_param,
)
from exceptions.response.exceptions import FileTooLargeException

blueprint = flask.Blueprint("file_service", __name__)

auth = api.utils.rest_utils.auth

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# TODO: Limit file extensions accepted (see https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/)
# TODO: use secure_filename function from flask. Rename to file_upload
@blueprint.route("/files/upload_file/", methods=["POST"])
@auth
@error_handler
def upload_file():
    """Upload the file meta data and return the file upload location. Accepts a multipart/form-data request"""

    form_data = flask.request.form
    file = flask.request.files.get("file")

    if not file:
        raise Exception("No file provided")

    # todo: This should be in the file service. Read in chunks in case of large files, so we don't have to load the entire file into memory. Instead each chunk will be freed up from memory after it is processed, meaning he memory is available for garbage collection sooner
    chunk_size = 4096 
    byte_stream = bytearray()

    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break

        # Check the file size
        
        byte_stream.extend(chunk)

        if len(byte_stream) > MAX_FILE_SIZE:
            raise FileTooLargeException("File size exceeds the maximum allowed size")
        

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
    get_filter = FilesGetFilter(uuids=[file_uuid])

    ## TODO: Adjust this conver the bytes into a file before returning. Use mime type to work out the extension
    get_result = flask.current_app.conns.file_service.get_files(filter=get_filter, with_bytes=True)

    file = get_result.files[0]

    return flask.current_app.response_class(
        response=file.bytes, status=200, mimetype=file.mime_type
    )


# TODO: Rename to file_get
@blueprint.route("/files/", methods=["GET"])
@auth
def get_files():
    """Get file from the file service"""

    file_uuids = process_api_set_request_param(parameter_name="uuids[]", type=str)

    file_ids = process_api_set_request_param(parameter_name="ids[]", type=int)

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

    get_filter = FilesGetFilter(uuids=file_uuids) if file_uuids else FilesGetFilter(file_ids)

    ## TODO: Adjust this conver the bytes into a file before returning. Use mime type to work out the extension
    files = flask.current_app.conns.file_service.get_files(filter=get_filter).files

    file_dicts = [class_to_dict(file) for file in files]

    response = {}

    response["files"] = file_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


# @blueprint.route("/files/test/", methods=["GET"])
# def test():

#     return flask.current_app.response_class(response={test: "it worked!"}, status=200)


@blueprint.route("/files/test/", methods=["POST"])
def test():
    print(flask.request.json)
    return flask.current_app.response_class(response={test: "it worked!"}, status=200)
