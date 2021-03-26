import os
from json import dumps
from flask import Flask
from werkzeug.exceptions import HTTPException
from flask_cors import CORS


def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": err.get_name(),
        "message": err.description,
    })
    response.content_type = 'application/json'
    return response

# the APP is written below cus it's hard to import the customized error into the
# server.py file

APP = Flask(__name__, static_folder='../static')
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)


# make the static files folder with init
if not os.path.isdir('static'):
    os.mkdir('static')

# http error
class ValueError(HTTPException):
    code = 400
    message = "Error"

    def get_name(self):
        return 'Value Error'

class AccessError(HTTPException):
    code = 400

    def get_name(self):
        return 'Access Error'
