import flask
from api.file_service.typings.typings import (FileCreateRequest,
                                              FileUpdateRequest)

blueprint =  flask.Blueprint('file_service', __name__)

'''Upload the file meta data and return the file upload location.'''
@blueprint.route('/upload/', methods=['POST'])
def upload():
    ## Receives the FileUploadRequest and we internall convert to MetaDataRequest due to our implementation of uploads
    json_data = flask.request.json
    uuid, mime_type, file_size = json_data.values()

    request = FileCreateRequest(uuid, mime_type, file_size)

    response = flask.current_app.conns.file_service.create_file(request)
    ## Build response from db entry
    

    response = flask.make_response(response_body) 
    #Set headers
    response.location = f'https://domain/api/file_service/0.1/{uuid}'

   
    ## Set Location header to be url to upload the file to

    return flask.json.jsonify()


'''Upload the file and create the download url.'''
@blueprint.route('/upload/<string:file_uuid>', methods=['PATCH'])
def test():
    ## uploads
    file_bytes = flask.data

    request = FileUpdateRequest(bytes=file_bytes)

    response = flask.current_app.conns.file_service.update_file()



    ##print(uploaded_file)
    ##file_object = uploaded_file.save()
