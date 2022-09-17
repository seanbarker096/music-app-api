from urllib import request

from api_types.api_types import FileUploadRequest
from flask import Blueprint, current_app, json

blueprint =  Blueprint('file_service', __name__)


@blueprint.route('/upload')
def upload():
    request = FileUploadRequest(uuid='sdafasdfasdfaa', file_type='post')

    print(request.uuid)
    print(request.file_type)
    response = current_app.conns.file_service.upload(request)
    print(current_app.config)
    print(current_app.conns)
    return json.jsonify(response)
