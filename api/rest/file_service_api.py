import json

import flask
from api.file_service.typings.typings import FileUpdateRequest, FileUploadRequest

blueprint = flask.Blueprint("file_service", __name__)


@blueprint.route("/upload/", methods=["POST"])
def upload():
    """Upload the file meta data and return the file upload location."""
    json_data = flask.request.json

    request = FileUploadRequest(
        uuid=json_data["uuid"], mime_type=json_data["mime_type"], file_size=None
    )

    file_upload_result = flask.current_app.conns.file_service.upload_file(request)

    file_upload_result.file = vars(file_upload_result.file)
    file_upload_result = vars(file_upload_result)

    response = flask.current_app.response_class(
        response=json.dumps(file_upload_result), status=200, mimetype="application/json"
    )

    ## Set Location header to be url to upload the file to
    response.location = f"https://domain/api/file_service/0.1/upload/{json_data['uuid']}"

    return response


# @blueprint.route("/upload/<string:file_uuid>", methods=["PATCH"])
# def test():
#     """Upload the file and create the download url."""
#     ## uploads
#     # file_bytes = flask.data

#     # request = FileUpdateRequest(bytes=file_bytes)

#     # response = flask.current_app.conns.file_service.update_file()

#     print("running test route")

#     return True

#     ##print(uploaded_file)
#     ##file_object = uploaded_file.save()


@blueprint.route("/test/", methods=["GET"])
def test():
    response = flask.make_response({"test": True})
    return response
