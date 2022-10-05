import flask
from api.file_service.typings.typings import FileUpdateRequest, FileUploadRequest

blueprint = flask.Blueprint("file_service", __name__)


@blueprint.route("/upload/", methods=["POST"])
def upload():
    """Upload the file meta data and return the file upload location."""
    ## Receives the FileUploadRequest and we internall convert to MetaDataRequest due to our implementation of uploads
    json_data = flask.request.json
    uuid, mime_type, file_size = json_data.values()

    request = FileUploadRequest(uuid, mime_type, file_size)

    file_upload_response = flask.current_app.conns.file_service.upload_file(request)

    ## Build response from db entry
    file_upload_response.file = vars(file_upload_response.file)
    file_upload_response = vars(file_upload_response)

    response = flask.make_response(file_upload_response)

    ## Set Location header to be url to upload the file to
    response.location = f"https://domain/api/file_service/0.1/{uuid}"

    return flask.json.jsonify()


@blueprint.route("/upload/<string:file_uuid>", methods=["PATCH"])
def test():
    """Upload the file and create the download url."""
    ## uploads
    file_bytes = flask.data

    request = FileUpdateRequest(bytes=file_bytes)

    response = flask.current_app.conns.file_service.update_file()

    ##print(uploaded_file)
    ##file_object = uploaded_file.save()
